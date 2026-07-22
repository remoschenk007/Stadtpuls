#!/usr/bin/env python3
# ============================================================
#  STADTPULS · Adress-Nachtrag fuer BESTEHENDE Events
#
#  Fuer alte Events, die VOR dem Adress-Fix (import_eventfrog.py,
#  SP_LOC_FIX v1) eingefuegt wurden und keine Adresse haben:
#   1) Adresse via Eventfrog-Location-API nachladen -> Datenbank-Zeile
#      wird per UPSERT (Treffer ueber ef_id) aktualisiert.
#   2) Wenn das Event bei Eventfrog gar nicht mehr auffindbar ist
#      (abgesagt/entfernt) ODER auch die Location-API keine Adresse
#      liefert: Zeile wird GELOESCHT.
#      Grund: Google & Nutzer moegen Event-Seiten ohne Adresse nicht -
#      lieber sauber weg als kaputt/leer online.
#
#  Vergangene Events werden ignoriert (die entfernt eh der naechste
#  Lauf von import_eventfrog.py per cleanup_old()).
#
#  BRAUCHT: SUPABASE_KEY (service_role) zum Schreiben (Update + Delete).
#           Ohne den Key bricht das Skript sofort ab (macht sonst nichts).
#
#  AUFRUFE:
#   SUPABASE_KEY=<service_role> python3 backfill_adressen.py --dry   # nur zeigen, nichts schreiben
#   SUPABASE_KEY=<service_role> python3 backfill_adressen.py         # wirklich schreiben/loeschen
# ============================================================
import urllib.request, urllib.parse, urllib.error, json, os, sys, time
from datetime import datetime

SU = 'https://pnynkzrqnfoshojqfqxn.supabase.co'
SK = os.environ.get('SUPABASE_KEY')
DRY = '--dry' in sys.argv

if not SK:
    print('\n⚠ ABBRUCH: Kein SUPABASE_KEY (service_role) gesetzt.')
    print('  Ohne diesen Key kann nicht geschrieben/geloescht werden -> es passiert sicherheitshalber gar nichts.')
    print('  Aufruf so: SUPABASE_KEY=<dein-service-role-key> python3 backfill_adressen.py --dry\n')
    sys.exit(1)

EF_KEY = '11D282C1-D0CF-4A4E-9060-DF6B5FC4FE4C'
EF_URL = 'https://api.eventfrog.net/public/v1/events'
EF_LOC_URL = 'https://api.eventfrog.net/public/v1/locations'
EF_TABLE = 'eventfrog_events'
PER_PAGE = 100
MAX_PAGES = 60
LOC_CHUNK = 50
DEL_CHUNK = 100

PLZ_KREIS = {'8001':1,'8002':2,'8038':2,'8003':3,'8036':3,'8055':3,'8004':4,'8005':5,'8064':5,'8006':6,'8057':6,'8032':7,'8044':7,'8053':7,'8008':8,'8034':8,'8047':9,'8048':9,'8037':10,'8049':10,'8046':11,'8050':11,'8051':11,'8052':12}
HEUTE = datetime.now().strftime('%Y-%m-%d')


def ef_get(url, tries=5):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + EF_KEY, 'Accept': 'application/json'})
    wait = 3
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < tries:
                print(f'  ⏳ 429 — warte {wait}s und versuche nochmal ({attempt}/{tries}) …')
                time.sleep(wait)
                wait = min(wait * 2, 30)
                continue
            raise


def ef_fetch_all_events():
    """Holt ALLE aktuellen Events frisch von Eventfrog -> Mapping ef_id -> locationIds."""
    out = {}
    for page in range(1, MAX_PAGES + 1):
        zip_params = '&'.join('zip=' + p for p in PLZ_KREIS.keys())
        url = f'{EF_URL}?{zip_params}&page={page}&perPage={PER_PAGE}'
        try:
            d = ef_get(url)
        except Exception as e:
            print(f'  Seite {page}: FEHLER {e} — stop')
            break
        items = d.get('events', [])
        if not items:
            break
        for it in items:
            eid = str(it.get('id') or '')
            if eid:
                out[eid] = it.get('locationIds') or []
        total = d.get('totalNumberOfResources', 0)
        print(f'\r  Eventfrog frisch geladen: {len(out)}' + (f' / {total}' if total else ''), end='')
        if total and len(out) >= total:
            break
        time.sleep(0.4)
    print()
    return out


def ef_fetch_locations(ids):
    ids = sorted({str(i) for i in ids if i})
    out = {}
    for i in range(0, len(ids), LOC_CHUNK):
        chunk = ids[i:i + LOC_CHUNK]
        params = '&'.join('id=' + urllib.parse.quote(x) for x in chunk)
        url = f'{EF_LOC_URL}?{params}'
        try:
            d = ef_get(url)
            for loc in d.get('locations', []):
                lid = str(loc.get('id') or '')
                if lid:
                    out[lid] = loc
        except Exception as e:
            print(f'  ⚠ Location-Batch {i}-{i+LOC_CHUNK} fehlgeschlagen: {e}')
        time.sleep(0.6)
    return out


def db_get(url):
    req = urllib.request.Request(url, headers={'apikey': SK, 'Authorization': 'Bearer ' + SK})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def fetch_events_ohne_adresse():
    """Alle bestehenden, noch kommenden Events ohne Adresse."""
    url = (f'{SU}/rest/v1/{EF_TABLE}'
           f'?select=id,ef_id,titel,datum_start'
           f'&or=(adresse.is.null,adresse.eq.)'
           f'&datum_start=gte.{HEUTE}'
           f'&limit=100000')
    return db_get(url)


def upsert_adressen(rows):
    """Update per UPSERT (Treffer ueber ef_id) - setzt nur die mitgeschickten Spalten."""
    if not rows or DRY:
        return len(rows) if DRY else 0
    written = 0
    for i in range(0, len(rows), 200):
        batch = rows[i:i + 200]
        body = json.dumps(batch).encode('utf-8')
        req = urllib.request.Request(f'{SU}/rest/v1/{EF_TABLE}?on_conflict=ef_id', data=body,
            headers={'apikey': SK, 'Authorization': 'Bearer ' + SK, 'Content-Type': 'application/json',
                     'Prefer': 'resolution=merge-duplicates,return=minimal'}, method='POST')
        try:
            urllib.request.urlopen(req, timeout=20)
            written += len(batch)
        except urllib.error.HTTPError as e:
            print(f'  HTTP {e.code} beim Update: {e.read().decode()[:200]}')
        except Exception as e:
            print(f'  FEHLER beim Update: {e}')
    return written


def delete_efids(ef_ids):
    if not ef_ids or DRY:
        return len(ef_ids) if DRY else 0
    deleted = 0
    ef_ids = list(ef_ids)
    for i in range(0, len(ef_ids), DEL_CHUNK):
        chunk = ef_ids[i:i + DEL_CHUNK]
        ids_param = ','.join(urllib.parse.quote(x) for x in chunk)
        url = f'{SU}/rest/v1/{EF_TABLE}?ef_id=in.({ids_param})'
        req = urllib.request.Request(url, headers={'apikey': SK, 'Authorization': 'Bearer ' + SK, 'Prefer': 'return=minimal'}, method='DELETE')
        try:
            urllib.request.urlopen(req, timeout=20)
            deleted += len(chunk)
        except urllib.error.HTTPError as e:
            print(f'  HTTP {e.code} beim Loeschen: {e.read().decode()[:200]}')
        except Exception as e:
            print(f'  FEHLER beim Loeschen: {e}')
    return deleted


def main():
    mode = '🟡 DRY-RUN' if DRY else '🟢 WRITE'
    print(f'\n ADRESS-NACHTRAG (bestehende Events) — {mode} — ab {HEUTE}\n')

    ohne = fetch_events_ohne_adresse()
    print(f'  Events ohne Adresse (kommend): {len(ohne)}')
    if not ohne:
        print('\nFERTIG — nichts zu tun.\n')
        return

    print('\n→ Aktuelle Events frisch von Eventfrog laden (fuer Location-Zuordnung) …')
    fresh = ef_fetch_all_events()

    # locationIds sammeln, die wir fuer die betroffenen Events brauchen
    needed_loc_ids = set()
    for row in ohne:
        loc_ids = fresh.get(row['ef_id'])
        if loc_ids:
            needed_loc_ids.add(str(loc_ids[0]))
    print(f'\n  benoetigte Location-IDs: {len(needed_loc_ids)}')
    loc_lookup = ef_fetch_locations(needed_loc_ids)
    print(f'  Locations aufgelöst: {len(loc_lookup)} / {len(needed_loc_ids)}')

    updates = []
    delete_nicht_mehr_da = []
    delete_keine_adresse = []

    for row in ohne:
        eid = row['ef_id']
        loc_ids = fresh.get(eid)
        if loc_ids is None:
            # Event bei Eventfrog nicht mehr auffindbar -> abgesagt/entfernt
            delete_nicht_mehr_da.append(eid)
            continue
        loc = loc_lookup.get(str(loc_ids[0])) if loc_ids else None
        adresse = (loc or {}).get('addressLine') or ''
        if not adresse:
            delete_keine_adresse.append(eid)
            continue
        loc_title = (loc or {}).get('title') or {}
        venue_name = loc_title.get('de') or loc_title.get('en') or loc_title.get('fr') or ''
        plz = str((loc or {}).get('zip') or '').strip()
        kreis = PLZ_KREIS.get(plz)
        updates.append({
            'ef_id': eid,
            'venue_name': venue_name,
            'adresse': adresse,
            'plz': plz or None,
            'kreis': kreis,
        })

    print(f'\n  → Adresse gefunden, wird aktualisiert: {len(updates)}')
    print(f'  → bei Eventfrog nicht mehr da, wird gelöscht: {len(delete_nicht_mehr_da)}')
    print(f'  → auch bei Eventfrog keine Adresse, wird gelöscht: {len(delete_keine_adresse)}')

    if updates:
        print(f'  Beispiel Update: {updates[0]}')

    n_updated = upsert_adressen(updates)
    n_deleted = delete_efids(delete_nicht_mehr_da + delete_keine_adresse)

    if DRY:
        print(f'\nFERTIG (DRY, nichts geschrieben) — würde aktualisieren: {len(updates)} · würde löschen: {len(delete_nicht_mehr_da) + len(delete_keine_adresse)}\n')
    else:
        print(f'\nFERTIG — aktualisiert: {n_updated} · gelöscht: {n_deleted}\n')


if __name__ == '__main__':
    main()
