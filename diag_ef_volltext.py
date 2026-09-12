#!/usr/bin/env python3
# Findet heraus, WO bei Eventfrog der volle Text steckt und ob wir ihn abgreifen.
# Liest nur, aendert nichts. Im Repo-Root laufen lassen.
import urllib.request, json, re, time

src = open('import_eventfrog.py', encoding='utf-8').read()
EF_KEY = re.search(r"EF_KEY\s*=\s*'([^']+)'", src).group(1)
EF_URL = re.search(r"EF_URL\s*=\s*'([^']+)'", src).group(1)
zips = list(dict.fromkeys(re.findall(r"'(80\d\d)'", src)))
zp = '&'.join('zip=' + z for z in zips)

def ef_get(url):
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'Authorization':'Bearer '+EF_KEY,'Accept':'application/json'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            print(f"  (retry {attempt+1}: {e})"); time.sleep(3)
    return {}

events = []
for page in (1, 2, 3):
    events += ef_get(f"{EF_URL}?{zp}&page={page}&perPage=100").get('events', [])
    time.sleep(1)
print("Events geladen:", len(events))
if not events:
    raise SystemExit

def L(e, path):
    v = e
    for k in path.split('.'):
        v = (v or {}).get(k) if isinstance(v, dict) else None
    return len(v) if isinstance(v, str) else 0

print("\n=== ALLE Top-Level-Felder ===")
print(sorted(events[0].keys()))

print("\n=== Feld-Laengen pro Event (Title | shortDescription | descriptionAsHTML) ===")
for e in events[:30]:
    t = ((e.get('title') or {}).get('de') or '')[:34]
    print(f"  {t:36} short={L(e,'shortDescription.de'):5}  html={L(e,'descriptionAsHTML.de'):6}")

# B.ARBIE (oder erstes Event mit sehr kurzem html aber vorhandenem short) VOLL dumpen
tgt = next((e for e in events if 'ARBIE' in ((e.get('title') or {}).get('de') or '').upper()), None)
if not tgt:
    tgt = next((e for e in events if L(e,'descriptionAsHTML.de') < 50 and L(e,'shortDescription.de') > 0), events[0])
print(f"\n{'='*64}\n=== VOLLDUMP (ungekuerzt): {(tgt.get('title') or {}).get('de')} ===")
print(json.dumps(tgt, ensure_ascii=False, indent=2))
