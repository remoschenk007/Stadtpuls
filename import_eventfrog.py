#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

EF_KEY = '11D282C1-D0CF-4A4E-9060-DF6B5FC4FE4C'
EF_URL = 'https://api.eventfrog.net/public/v1/events'
SU = 'https://pnynkzrqnfoshojqfqxn.supabase.co'
SK = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ'

PLZ_KREIS = {
    '8001':1,'8002':2,'8038':2,'8003':3,'8036':3,'8055':3,'8004':4,
    '8005':5,'8064':5,'8006':6,'8057':6,'8032':7,'8044':7,'8053':7,
    '8008':8,'8034':8,'8047':9,'8048':9,'8037':10,'8049':10,
    '8046':11,'8050':11,'8051':11,'8052':12
}

# Wieviele Seiten importieren? (je 100 Events)
# 1 = ~100 Events (Test)
# 10 = ~1000 Events
# 25 = ~2500 Events (alle)
MAX_PAGES = 25

def slugify(s):
    s = (s or '').lower()
    for a, b in [('ä','ae'),('ö','oe'),('ü','ue'),('ß','ss')]:
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:80]

def fetch_page(page):
    plz_params = '&'.join(['zip=' + p for p in PLZ_KREIS.keys()])
    url = f'{EF_URL}?{plz_params}&page={page}&perPage=100'
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {EF_KEY}',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f'  FETCH FEHLER Seite {page}: {e}')
        return None

def map_item(item):
    title = item.get('title') or {}
    name = title.get('de') or title.get('en') or title.get('fr') or ''
    name = name.strip()
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

    today = datetime.now().strftime('%Y-%m-%d')
    if datum_start < today:
        return None

    is_popup = False
    if datum_start and datum_ende:
        try:
            diff = (datetime.strptime(datum_ende, '%Y-%m-%d') - datetime.strptime(datum_start, '%Y-%m-%d')).days
            is_popup = diff < 3
        except:
            pass

    # Kategorie ableiten
    kategorie = 'event'
    subkategorie = 'allgemein'
    rubric_id = item.get('rubricId') or 0

    short_desc = item.get('shortDescription') or {}
    beschreibung = short_desc.get('de') or short_desc.get('en') or ''

    return {
        'ef_id': str(item.get('id') or ''),
        'titel': name,
        'slug': slugify(name) + '-' + str(item.get('id') or '')[:8],
        'kategorie': kategorie,
        'subkategorie': subkategorie,
        'kreis': kreis,
        'venue_name': alias.get('name') or '',
        'adresse': alias.get('street') or '',
        'plz': plz or None,
        'datum_start': datum_start,
        'datum_ende': datum_ende,
        'uhrzeit_start': begin[11:16] if len(begin) > 10 else None,
        'uhrzeit_ende': end[11:16] if len(end) > 10 else None,
        'beschreibung': beschreibung,
        'bild_url': item.get('emblemToShow') or None,
        'ticket_url': item.get('url') or None,
        'eintritt_typ': 'kostenlos' if item.get('freeOfCharge') else 'kostenpflichtig',
        'popup': is_popup,
        'aktiv': True,
        'featured': False,
        'seo_title': f'{name} — Event Zürich | Stadtpuls'
    }

def sb_insert(ev):
    body = json.dumps(ev).encode('utf-8')
    req = urllib.request.Request(
        f'{SU}/rest/v1/eventfrog_events',
        data=body,
        headers={
            'apikey': SK,
            'Authorization': f'Bearer {SK}',
            'Content-Type': 'application/json',
            'Prefer': 'resolution=ignore-duplicates,return=minimal'
        },
        method='POST'
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:150]
        print(f'  HTTP {e.code}: {body}')
        return False
    except Exception as e:
        print(f'  FEHLER: {e}')
        return False

# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════
ok = sk = er = popups = 0
today = datetime.now().strftime('%Y-%m-%d')
print(f'\n🐸 EVENTFROG IMPORT — Zürich alle Kreise — {today}')
print(f'   Max Seiten: {MAX_PAGES} (~{MAX_PAGES*100} Events)\n')

for page in range(1, MAX_PAGES + 1):
    print(f'\n→ Seite {page}/{MAX_PAGES}...')
    data = fetch_page(page)

    if not data:
        er += 1
        continue

    events = data.get('events') or []
    total = data.get('totalNumberOfResources') or 0

    if page == 1:
        print(f'  Total verfügbar: {total} Events')

    if not events:
        print(f'  Keine Events auf Seite {page} — fertig.')
        break

    print(f'  {len(events)} Events auf dieser Seite')

    for item in events:
        ev = map_item(item)
        if not ev:
            sk += 1
            continue

        if sb_insert(ev):
            ok += 1
            if ev['popup']:
                popups += 1
            kreis_str = f' K{ev["kreis"]}' if ev['kreis'] else ''
            popup_str = ' 🎪' if ev['popup'] else ''
            print(f'  OK: {ev["titel"][:45]} ({ev["datum_start"]}){kreis_str}{popup_str}')
        else:
            er += 1

print(f'\n✅ FERTIG — OK:{ok} SKIP:{sk} ERR:{er} POPUP:{popups}\n')
