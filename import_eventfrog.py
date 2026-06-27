#!/usr/bin/env python3
# ============================================================
#  STADTPULS · Eventfrog-Sync   (Eventfrog API → Supabase `eventfrog_events`)
#
#  Ersetzt den kaputten Browser-/corsproxy-Weg aus import.html.
#  Lokal (oder in der GitHub Action) gibt es kein CORS → direkter,
#  zuverlässiger API-Call mit deinem Eventfrog-Key.
#
#  ZIELE:
#   • NEUE rein, ALTE raus  (vergangene Events werden entfernt;
#     vergangene werden gar nicht erst importiert)
#   • FEATURED (bezahlte Platzierung) bleibt unangetastet
#     → bestehende Events werden nie überschrieben (nur neue eingefügt)
#   • POPUPS zeitlich begrenzt (popup=True bei Dauer < 3 Tagen)
#
#  AUFRUFE:
#   python3 import_eventfrog.py --dry     # holt + zeigt, schreibt NICHTS
#   python3 import_eventfrog.py           # schreibt neue Events
#   SUPABASE_KEY=<service_role> python3 import_eventfrog.py   # + löscht alte
#
#  ENV:
#   SUPABASE_KEY  → service_role-Key nötig zum Löschen alter Events
#                   (Supabase → Settings → API). Ohne ihn läuft nur Insert.
# ============================================================
import urllib.request, urllib.parse, json, re, os, sys
from datetime import datetime

SU = 'https://pnynkzrqnfoshojqfqxn.supabase.co'
SK_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ'
SK = os.environ.get('SUPABASE_KEY') or SK_ANON
HAS_SERVICE_KEY = bool(os.environ.get('SUPABASE_KEY'))
DRY = '--dry' in sys.argv

EF_KEY = '11D282C1-D0CF-4A4E-9060-DF6B5FC4FE4C'
EF_URL = 'https://api.eventfrog.net/public/v1/events'
EF_TABLE = 'eventfrog_events'
PER_PAGE = 100
MAX_PAGES = 40

PLZ_KREIS = {'8001':1,'8002':2,'8038':2,'8003':3,'8036':3,'8055':3,'8004':4,'8005':5,'8064':5,'8006':6,'8057':6,'8032':7,'8044':7,'8053':7,'8008':8,'8034':8,'8047':9,'8048':9,'8037':10,'8049':10,'8046':11,'8050':11,'8051':11,'8052':12}
HEUTE = datetime.now().strftime('%Y-%m-%d')


def slugify(s):
    s = s.lower()
    for a, b in [('ä','ae'),('ö','oe'),('ü','ue'),('ß','ss')]:
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:80]


def ef_fetch_page(page):
    zip_params = '&'.join('zip=' + p for p in PLZ_KREIS.keys())
    url = f'{EF_URL}?{zip_params}&page={page}&perPage={PER_PAGE}'
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + EF_KEY, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read())
    return d.get('events', []), d.get('totalNumberOfResources', 0)


def map_item(item):
    title = item.get('title') or {}
    name = title.get('de') or title.get('en') or title.get('fr') or ''
    if not name:
        return None
    if item.get('cancelled'):
        return None
    alias = item.get('locationAlias') or {}
    plz = str(alias.get('zip') or '').strip()
    kreis = PLZ_KREIS.get(plz)
    begin = item.get('begin') or ''
    end = item.get('end') or begin
    datum_start = begin[:10] if begin else None
    datum_ende = end[:10] if end else datum_start
    if not datum_start:
        return None
    if datum_start < HEUTE:        # vergangene gar nicht erst importieren
        return None
    is_popup = False
    if datum_start and datum_ende:
        try:
            diff = (datetime.strptime(datum_ende, '%Y-%m-%d') - datetime.strptime(datum_start, '%Y-%m-%d')).days
            is_popup = diff < 3
        except Exception:
            pass
    rubric = item.get('rubricId') or 0
    kategorie, subkategorie = 'event', 'allgemein'
    if rubric in (1, 2, 3):
        kategorie, subkategorie = 'nachtleben', 'party'
    elif rubric in (4, 5):
        kategorie, subkategorie = 'kultur', 'konzert'
    elif rubric in (6, 7):
        kategorie, subkategorie = 'sport', 'sport'
    emblem = item.get('emblemToShow') or {}
    return {
        'ef_id': str(item.get('id') or ''),
        'titel': name,
        'slug': slugify(name) + '-' + str(item.get('id') or '')[:8],
        'kategorie': kategorie, 'subkategorie': subkategorie,
        'kreis': kreis,
        'venue_name': alias.get('name') or '',
        'adresse': alias.get('street') or '',
        'plz': plz or None,
        'datum_start': datum_start, 'datum_ende': datum_ende,
        'uhrzeit_start': begin[11:16] if len(begin) > 10 else None,
        'uhrzeit_ende': end[11:16] if len(end) > 10 else None,
        'beschreibung': ((item.get('shortDescription') or {}).get('de') or (item.get('shortDescription') or {}).get('en') or ''),
        'bild_url': emblem.get('url'),                 # nur die URL (für <img>), nicht das ganze Objekt
        'ticket_url': item.get('url'),
        'eintritt_typ': 'kostenlos' if item.get('freeOfCharge') else 'kostenpflichtig',
        'popup': is_popup,
        'aktiv': True, 'featured': False,
        'seo_title': name + ' — Event Zürich | Stadtpuls'
    }


def existing_efids():
    """Schon vorhandene ef_ids holen → nur wirklich neue einfügen (Featured bleibt unangetastet)."""
    try:
        url = f'{SU}/rest/v1/{EF_TABLE}?select=ef_id&limit=100000'
        req = urllib.request.Request(url, headers={'apikey': SK, 'Authorization': 'Bearer ' + SK})
        with urllib.request.urlopen(req, timeout=20) as r:
            return {row['ef_id'] for row in json.loads(r.read()) if row.get('ef_id')}
    except Exception as e:
        print(f'  ⚠ konnte bestehende ef_ids nicht laden: {e}')
        return set()


def insert_batch(rows):
    if not rows or DRY:
        return len(rows) if DRY else 0
    body = json.dumps(rows).encode('utf-8')
    req = urllib.request.Request(f'{SU}/rest/v1/{EF_TABLE}?on_conflict=ef_id', data=body,
        headers={'apikey': SK, 'Authorization': 'Bearer ' + SK, 'Content-Type': 'application/json',
                 'Prefer': 'resolution=ignore-duplicates,return=minimal'}, method='POST')
    try:
        urllib.request.urlopen(req, timeout=20)
        return len(rows)
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}: {e.read().decode()[:160]}')
        return 0
    except Exception as e:
        print(f'  FEHLER: {e}')
        return 0


def cleanup_old():
    print(f'\n→ Cleanup: vergangene Events (datum_ende < {HEUTE}) entfernen …')
    if DRY:
        print('  [DRY-RUN] würde löschen, macht aber nichts')
        return
    if not HAS_SERVICE_KEY:
        print('  ⚠ übersprungen — kein service_role-Key (SUPABASE_KEY) gesetzt. Inserts liefen trotzdem.')
        return
    url = f'{SU}/rest/v1/{EF_TABLE}?datum_ende=lt.{HEUTE}'
    req = urllib.request.Request(url, headers={'apikey': SK, 'Authorization': 'Bearer ' + SK, 'Prefer': 'return=minimal'}, method='DELETE')
    try:
        urllib.request.urlopen(req, timeout=20)
        print('  ✓ alte Events entfernt')
    except Exception as e:
        print(f'  FEHLER beim Löschen: {e}')


def main():
    mode = '🟡 DRY-RUN' if DRY else ('🟢 WRITE (+ Cleanup)' if HAS_SERVICE_KEY else '🟢 WRITE (nur Insert)')
    print(f'\n EVENTFROG SYNC — {mode} — ab {HEUTE}\n')

    have = existing_efids()
    print(f'  bereits in DB: {len(have)} Events')

    raw = []
    total = None
    for page in range(1, MAX_PAGES + 1):
        try:
            items, total = ef_fetch_page(page)
        except Exception as e:
            print(f'  Seite {page}: FEHLER {e} — stop')
            break
        if not items:
            break
        raw.extend(items)
        print(f'\r  geladen: {len(raw)}' + (f' / {total}' if total else ''), end='')
        if total and len(raw) >= total:
            break
    print()

    mapped = [m for m in (map_item(it) for it in raw) if m]
    # nur neue (ef_id noch nicht in DB) + Duplikate innerhalb des Laufs raus
    seen, neu = set(), []
    for r in mapped:
        if r['ef_id'] in have or r['ef_id'] in seen:
            continue
        seen.add(r['ef_id'])
        neu.append(r)

    popup = sum(1 for r in neu if r['popup'])
    print(f'  geholt: {len(raw)} · gültig (kommend): {len(mapped)} · davon NEU: {len(neu)} · Popups: {popup}')
    if neu:
        print(f'  Beispiel neu: {neu[0]["titel"][:50]} ({neu[0]["datum_start"]})')

    written = 0
    for i in range(0, len(neu), 200):
        written += insert_batch(neu[i:i + 200])

    cleanup_old()
    print(f'\nFERTIG — NEU geschrieben: {written if not DRY else str(len(neu)) + " (DRY, nichts geschrieben)"}')
    print()


if __name__ == '__main__':
    main()
