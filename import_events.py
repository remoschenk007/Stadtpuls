#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime, timedelta

SU='https://pnynkzrqnfoshojqfqxn.supabase.co'
SK='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ'
ZT='https://www.zuerich.com/en/api/v2/data'
HEADERS={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36','Accept':'application/json'}
VON=datetime.now().strftime('%Y-%m-%d')
BIS=(datetime.now()+timedelta(days=60)).strftime('%Y-%m-%d')
PLZ_KREIS={'8001':1,'8002':2,'8038':2,'8003':3,'8036':3,'8055':3,'8004':4,'8005':5,'8064':5,'8006':6,'8057':6,'8032':7,'8044':7,'8053':7,'8008':8,'8034':8,'8047':9,'8048':9,'8037':10,'8049':10,'8046':11,'8050':11,'8051':11,'8052':12}
KATEGORIEN=[(96,'kultur','kultur'),(133,'kultur','film'),(134,'kultur','musik'),(175,'kultur','oper'),(176,'kultur','theater'),(178,'kultur','galerie'),(162,'nachtleben','club'),(1414,'nachtleben','techno'),(1432,'nachtleben','jazz'),(1417,'nachtleben','hiphop'),(163,'nachtleben','livemusic'),(1435,'nachtleben','party'),(132,'shopping','markt'),(97,'sport','sport')]

def slugify(s):
    s=s.lower()
    for a,b in [('ä','ae'),('ö','oe'),('ü','ue'),('ß','ss')]:s=s.replace(a,b)
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')[:80]

def zt_fetch(zt_id):
    url=f'{ZT}?id={zt_id}&limit=500&dateFrom={VON}&dateTo={BIS}'
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=15) as r:
            d=json.loads(r.read())
            return d if isinstance(d,list) else d.get('data',[])
    except Exception as e:
        print(f'  FETCH FEHLER: {e}')
        return []

def sb_insert(ev):
    body=json.dumps(ev).encode('utf-8')
    req=urllib.request.Request(f'{SU}/rest/v1/events',data=body,headers={'apikey':SK,'Authorization':f'Bearer {SK}','Content-Type':'application/json','Prefer':'resolution=ignore-duplicates,return=minimal'},method='POST')
    try:
        urllib.request.urlopen(req,timeout=10)
        return True
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}: {e.read().decode()[:120]}')
        return False
    except Exception as e:
        print(f'  FEHLER: {e}')
        return False

def map_ev(item,kat,zt_id):
    name=((item.get('name')or{}).get('de')or(item.get('name')or{}).get('en')or'').strip()
    if not name:return None
    addr=item.get('address')or item.get('location')or{}
    plz=str(addr.get('postalCode','')).strip()
    df=item.get('dateFrom')or item.get('startDate')
    dt=item.get('dateTo')or item.get('endDate')or df
    if not df:return None
    is_popup=False
    try:
        is_popup=(datetime.strptime(dt[:10],'%Y-%m-%d')-datetime.strptime(df[:10],'%Y-%m-%d')).days<7
    except:pass
    geo=item.get('geoCoordinates')or{}
    img=item.get('image')or{}
    desc=((item.get('description')or{}).get('de')or'')
    return{'titel':name,'slug':slugify(name)+'-'+str(item.get('identifier',''))[:6],'kategorie':kat,'zt_kategorie_id':zt_id,'zt_subkategorie_id':zt_id,'venue_name':addr.get('name',''),'adresse':addr.get('streetAddress',''),'plz':plz,'kreis':PLZ_KREIS.get(plz),'lat':geo.get('latitude'),'lng':geo.get('longitude'),'datum_start':df[:10],'datum_ende':dt[:10],'uhrzeit_start':item.get('timeFrom'),'uhrzeit_ende':item.get('timeTo'),'ganztaegig':not bool(item.get('timeFrom')),'beschreibung':desc,'beschreibung_kurz':desc[:200],'bild_url':img.get('url'),'ticket_url':item.get('ticketUrl')or item.get('bookingUrl'),'eintritt_typ':'kostenpflichtig' if item.get('price') else 'kostenlos','preis_von':item.get('priceFrom'),'preis_bis':item.get('priceTo'),'popup':is_popup,'veranstalter':(item.get('organizer')or{}).get('name'),'quelle':'zuerich_tourismus','quelle_id':str(item.get('identifier','')),'aktiv':True,'featured':False,'abgesagt':False,'seo_title':f'{name} — Event Zürich | Stadtpuls'}

ok=sk=er=popup=0
print(f'\n EVENTS IMPORT v2 — {VON} bis {BIS}\n')
for zt_id,kat,subkat in KATEGORIEN:
    print(f'\n-> {kat}/{subkat} (id={zt_id})')
    items=zt_fetch(zt_id)
    print(f'  {len(items)} Events')
    for item in items:
        ev=map_ev(item,kat,zt_id)
        if not ev:sk+=1;continue
        if sb_insert(ev):
            ok+=1
            if ev['popup']:popup+=1
            print(f'  OK: {ev["titel"][:45]} ({ev["datum_start"]})')
        else:er+=1
print(f'\nFERTIG — OK:{ok} SKIP:{sk} ERR:{er} POPUP:{popup}\n')
