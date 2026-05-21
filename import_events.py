#!/usr/bin/env python3
"""
STADTPULS — Events Import Script
Läuft direkt vom Mac — kein CORS, kein Browser
"""

import urllib.request
import urllib.parse
import json
import re
from datetime import datetime, timedelta

SU = 'https://pnynkzrqnfoshojqfqxn.supabase.co'
SK = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ'
ZT  = 'https://www.zuerich.com/en/api/v2/data'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

VON = datetime.now().strftime('%Y-%m-%d')
BIS = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')

PLZ_KREIS = {
    '8001':1,'8002':2,'8038':2,'8003':3,'8036':3,'8055':3,'8004':4,
    '8005':5,'8064':5,'8006':6,'8057':6,'8032':7,'8044':7,'8053':7,
    '8008':8,'8034':8,'8047':9,'8048':9,'8037':10,'8049':10,
    '8046':11,'8050':11,'8051':11,'8052':12
}

KATEGORIEN = [
    (96,  'kultur',    'kultur'),
    (133, 'kultur',    'film'),
    (134, 'kultur',    'musik'),
    (175, 'kultur',    'oper'),
    (176, 'kultur',    'theater'),
    (178, 'kultur',    'galerie'),
    (162, 'nachtleben','club'),
    (1414,'nachtleben','techno'),
    (1432,'nachtleben','jazz'),
    (1417,'nachtleben','hiphop'),
    (163, 'nachtleben','livemusic'),
    (1435,'nachtleben','party'),
    (132, 'shopping',  'markt'),
    (97,  'sport',     'sport'),
]

def slugify(s):
    s = s.lower()
    for a, b in [('ä','ae'),('ö','oe'),('ü','ue'),('ß','ss')]:
        s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')[:80]

def zt_fetch(zt_id):
    url = f'{ZT}?id={zt_id}&limit=500&dateFrom={VON}&dateTo={BIS}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            return data if isinstance(data, list) else data.get('data', [])
    except Exception as e:
        print(f'  ❌ Fetch Fehler: {e}')
        return []

def sb_check_exists(quelle_id):
    url = f'{SU}/rest/v1/events?quelle_id=eq.{urllib.parse.quote(str(quelle_id))}&select=id&limit=1'
    req = urllib.request.Request(url, headers={'apikey': SK, 'Authorization': f'Bearer {SK}'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return len(data) > 0
    except:
        return False

def sb_insert(ev):
    url = f'{SU}/rest/v1/events'
    body = json.dumps(ev).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        'apikey': SK,
        'Authorization': f'Bearer {SK}',
        'Content-Type': 'application/json',
        'Prefer': 'resolution=ignore-duplicates'
    }, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status in [200, 201]
    except Exception as e:
        print(f'  ❌ Insert Fehler: {e}')
        return False

def map_event(item, kat, subkat, zt_id):
    name = (item.get('name') or {}).get('de') or (item.get('name') or {}).get('en') or ''
    if not name:
        return None
    addr = item.get('address') or item.get('location') or {}
    plz  = str(addr.get('postalCode', '')).strip()
    kreis = PLZ_KREIS.get(plz)
    df = item.get('dateFrom') or item.get('startDate')
    dt = item.get('dateTo') or item.get('endDate') or df
    if not df:
        return None
    try:
        if datetime.strptime(df[:10], '%Y-%m-%d') < datetime.now():
            return None
    except:
        pass
    is_popup = False
    try:
        d1 = datetime.strptime(df[:10], '%Y-%m-%d')
        d2 = datetime.strptime(dt[:10], '%Y-%m-%d')
        is_popup = (d2 - d1).days < 7
    except:
        pass
    geo  = item.get('geoCoordinates') or {}
    img  = item.get('image') or {}
    desc = (item.get('description') or {}).get('de') or ''
    return {
        'titel': name,
        'slug': slugify(name) + '-' + str(item.get('identifier', ''))[:6],
        'kategorie': kat,
        'zt_kategorie_id': zt_id,
        'zt_subkategorie_id': zt_id,
        'venue_name': addr.get('name', ''),
        'adresse': addr.get('streetAddress', ''),
        'plz': plz,
        'kreis': kreis,
        'lat': geo.get('latitude'),
        'lng': geo.get('longitude'),
        'datum_start': df[:10] if df else None,
        'datum_ende': dt[:10] if dt else df[:10] if df else None,
        'uhrzeit_start': item.get('timeFrom'),
        'uhrzeit_ende': item.get('timeTo'),
        'ganztaegig': not bool(item.get('timeFrom')),
        'beschreibung': desc,
        'beschreibung_kurz': desc[:200] if desc else '',
        'bild_url': img.get('url'),
        'ticket_url': item.get('ticketUrl') or item.get('bookingUrl'),
        'eintritt_typ': 'kostenpflichtig' if item.get('price') else 'kostenlos',
        'preis_von': item.get('priceFrom'),
        'preis_bis': item.get('priceTo'),
        'popup': is_popup,
        'veranstalter': (item.get('organizer') or {}).get('name'),
        'quelle': 'zuerich_tourismus',
        'quelle_id': str(item.get('identifier', '')),
        'aktiv': True,
        'featured': False,
        'abgesagt': False,
        'seo_title': f'{name} — Event Zürich | Stadtpuls'
    }

def main():
    print(f'\n🔴 STADTPULS EVENTS IMPORT')
    print(f'   Zeitraum: {VON} → {BIS}')
    print(f'   Kategorien: {len(KATEGORIEN)}\n')
    total_ok = 0
    total_sk = 0
    total_er = 0
    total_popup = 0
    for zt_id, kat, subkat in KATEGORIEN:
        print(f'\n→ {kat}/{subkat} (id={zt_id})')
        items = zt_fetch(zt_id)
        print(f'  {len(items)} Events von ZT API')
        for item in items:
            ev = map_event(item, kat, subkat, zt_id)
            if not ev:
                total_sk += 1
                continue
            qid = ev['quelle_id']
            if sb_check_exists(qid):
                total_sk += 1
                continue
            ok = sb_insert(ev)
            if ok:
                total_ok += 1
                popup_str = ' 🎪 POP-UP' if ev['popup'] else ''
                print(f'  ✅ {ev["titel"][:50]} ({ev["datum_start"]}){popup_str}')
                if ev['popup']:
                    total_popup += 1
            else:
                total_er += 1
                print(f'  ❌ FEHLER: {ev["titel"][:50]}')
    print(f'\n{"="*50}')
    print(f'✅ FERTIG — Importiert: {total_ok} | Skip: {total_sk} | Fehler: {total_er} | Pop-Ups: {total_popup}')
    print(f'{"="*50}\n')

if __name__ == '__main__':
    main()
