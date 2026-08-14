#!/usr/bin/env python3
# Diagnose: zeigt, wie die Oeffnungszeiten in Supabase wirklich heissen & aussehen.
# Laeuft im Repo-Root (liest SU/SK aus generate_location_pages.py). Nichts wird geaendert.
import urllib.request, json, re

src = open('generate_location_pages.py', encoding='utf-8').read()
SU = re.search(r'^SU\s*=\s*"([^"]+)"', src, re.M).group(1)
SK = re.search(r'^SK\s*=\s*"([^"]+)"', src, re.M).group(1)

def fetch(path):
    req = urllib.request.Request(SU + path, headers={"apikey": SK, "Authorization": "Bearer " + SK})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

rows = fetch("/rest/v1/locations?select=*&kategorie=eq.gastro&aktiv=eq.true&limit=8")
if not rows:
    print("Keine Zeilen erhalten."); raise SystemExit

hours_keys = [k for k in rows[0].keys() if re.search(r'offn|zeit|hour|open', k, re.I)]
print("HOURS-VERDAECHTIGE SPALTEN:", hours_keys)
print("ALLE SPALTEN:", sorted(rows[0].keys()))
print("=" * 60)
for r in rows:
    print("NAME:", r.get('name'))
    for k in (hours_keys or ['oeffnungszeiten']):
        v = r.get(k)
        print(f"  {k} = {repr(v)[:240]}   (type {type(v).__name__})")
    print("-" * 40)
