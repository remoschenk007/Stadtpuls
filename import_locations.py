#!/usr/bin/env python3
# ============================================================
#  STADTPULS · Locations-Sync   (Zürich-Tourismus-API → Supabase `locations`)
#
#  Frischt Orte auf: Gastro, Nachtleben, Shopping (+ Kultur, Sport, Wellness).
#  Lokal/Action — kein CORS, kein allorigins-Proxy (anders als import.html).
#
#  • Fügt nur WIRKLICH NEUE Orte ein (Dedup über zt_api_id UND slug)
#  • FEATURED bleibt unangetastet (bestehende werden nie überschrieben)
#  • Kein 409-Spam
#
#  AUFRUFE:
#   python3 import_locations.py --dry     # holt + zeigt, schreibt NICHTS
#   python3 import_locations.py           # schreibt neue Orte
#
#  ENV: SUPABASE_KEY (optional service_role; anon reicht zum Einfügen)
# ============================================================
import urllib.request, urllib.parse, json, re, os, sys
from datetime import datetime

SU = 'https://pnynkzrqnfoshojqfqxn.supabase.co'
SK_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ'
SK = os.environ.get('SUPABASE_KEY') or SK_ANON
DRY = '--dry' in sys.argv

ZT = 'https://www.zuerich.com/en/api/v2/data'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'application/json'}

# ZT-Kategorie-ID → (kategorie, subkategorie-Default)
CATS = [
    (101, 'gastro', 'restaurant'),
    (102, 'gastro', 'cafe'),
    (103, 'nachtleben', 'bar'),
    (162, 'nachtleben', 'club'),
    (95, 'shopping', 'shopping'),
    (96, 'kultur', 'kultur'),
    (97, 'sport', 'sport'),
    (98, 'wellness', 'wellness'),
]

PLZ_KREIS = {'8001':1,'8002':2,'8038':2,'8003':3,'8036':3,'8055':3,'8004':4,'8005':5,'8064':5,'8006':6,'8057':6,'8032':7,'8044':7,'8053':7,'8008':8,'8034':8,'8047':9,'8048':9,'8037':10,'8049':10,'8046':11,'8050':11,'8051':11,'8052':12}


def slugify(s):
    s = s.lower()
    for a, b in [('ä','ae'),('ö','oe'),('ü','ue'),('ß','ss')]:
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:80]


def zt_fetch(zt_id):
    url = f'{ZT}?id={zt_id}&limit=500'
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=20) as r:
            d = json.loads(r.read())
            return d if isinstance(d, list) else d.get('data', [])
    except Exception as e:
        print(f'  FETCH FEHLER (id={zt_id}): {e}')
        return []


def map_row(item, kategorie, subkat, kat_id):
    a = item.get('address') or {}
    g = item.get('geoCoordinates') or {}
    plz = str(a.get('postalCode') or '').strip()
    kreis = PLZ_KREIS.get(plz)
    if not kreis:            # nur Zürcher PLZ → echte Stadt-Locations
        return None
    name = ((item.get('name') or {}).get('de') or (item.get('name') or {}).get('en') or '').strip()
    if not name:
        return None
    img = item.get('image') or {}
    photos = [p.get('url') for p in (item.get('photo') or []) if p.get('url')]
    desc = (item.get('description') or {}).get('de') or (item.get('description') or {}).get('en')
    desc_kurz = (item.get('disambiguatingDescription') or {}).get('de') or (item.get('textTeaser') or {}).get('de')
    oeff = item.get('openingHours') or []
    return {
        'name': name, 'slug': slugify(name), 'kategorie': kategorie, 'subkategorie': subkat,
        'zt_kategorie_id': kat_id, 'zt_subkategorie_id': kat_id, 'zt_api_id': item.get('identifier'),
        'adresse': a.get('streetAddress'), 'plz': plz or None, 'kreis': kreis, 'stadt': 'Zürich', 'land': 'CH',
        'lat': g.get('latitude'), 'lng': g.get('longitude'),
        'beschreibung': desc, 'beschreibung_kurz': desc_kurz,
        'bild_url': img.get('url'), 'bild_urls': photos or None,
        'telefon': item.get('telephone') or a.get('telephone'),
        'website': item.get('url') or a.get('url'), 'email': a.get('email'),
        'oeffnungszeiten': oeff or None,
        'zurichcard': item.get('zurichcard') or False,
        'place_indoor': 'Indoors' in (item.get('place') or []),
        'place_outdoor': 'Outdoors' in (item.get('place') or []),
        'seo_title': f'{name} — {subkat} Zürich Kreis {kreis} | Stadtpuls',
        'seo_description': desc_kurz or (desc[:160] if desc else None),
        'schema_type': item.get('@type') or 'LocalBusiness',
        'quelle': 'zuerich.com', 'aktiv': True, 'featured': False,
    }


def existing():
    """Bestehende zt_api_id + slug holen → nur wirklich Neue einfügen, kein 409-Spam."""
    try:
        url = f'{SU}/rest/v1/locations?select=zt_api_id,slug&limit=100000'
        req = urllib.request.Request(url, headers={'apikey': SK, 'Authorization': 'Bearer ' + SK})
        with urllib.request.urlopen(req, timeout=20) as r:
            rows = json.loads(r.read())
        return ({r['zt_api_id'] for r in rows if r.get('zt_api_id')},
                {r['slug'] for r in rows if r.get('slug')})
    except Exception as e:
        print(f'  ⚠ konnte bestehende Locations nicht laden: {e}')
        return set(), set()


def insert_batch(rows):
    if not rows or DRY:
        return len(rows) if DRY else 0
    body = json.dumps(rows).encode('utf-8')
    req = urllib.request.Request(f'{SU}/rest/v1/locations', data=body,
        headers={'apikey': SK, 'Authorization': 'Bearer ' + SK, 'Content-Type': 'application/json',
                 'Prefer': 'resolution=ignore-duplicates,return=minimal'}, method='POST')
    try:
        urllib.request.urlopen(req, timeout=25)
        return len(rows)
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}: {e.read().decode()[:160]}')
        return 0
    except Exception as e:
        print(f'  FEHLER: {e}')
        return 0


def main():
    mode = '🟡 DRY-RUN' if DRY else '🟢 WRITE'
    print(f'\n LOCATIONS SYNC — {mode}\n')
    have_api, have_slug = existing()
    print(f'  bereits in DB: {len(have_api)} Locations\n')

    neu, seen_api, seen_slug = [], set(), set()
    stats = {}
    for kat_id, kategorie, subkat in CATS:
        items = zt_fetch(kat_id)
        gemappt = 0
        for it in items:
            row = map_row(it, kategorie, subkat, kat_id)
            if not row:
                continue
            api, slug = row['zt_api_id'], row['slug']
            if (api and api in have_api) or slug in have_slug or api in seen_api or slug in seen_slug:
                continue
            if api:
                seen_api.add(api)
            seen_slug.add(slug)
            neu.append(row)
            gemappt += 1
        stats[f'{kategorie}/{subkat} (id={kat_id})'] = (len(items), gemappt)
        print(f'  {kategorie}/{subkat:11} (id={kat_id}): {len(items):4} geholt · {gemappt:3} neu')

    print(f'\n  → insgesamt NEU: {len(neu)}')
    if neu:
        print(f'  Beispiel: {neu[0]["name"]} · Kreis {neu[0]["kreis"]} · {neu[0]["kategorie"]}')

    written = 0
    for i in range(0, len(neu), 200):
        written += insert_batch(neu[i:i + 200])

    print(f'\nFERTIG — NEU: {written if not DRY else str(len(neu)) + " (DRY, nichts geschrieben)"}')
    print()


if __name__ == '__main__':
    main()
