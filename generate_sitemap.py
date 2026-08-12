#!/usr/bin/env python3
# STADTPULS · generate_sitemap.py — dynamische Sitemap für ALLE Profile.
# Holt Lokale + Events aus Supabase und schreibt:
#   sitemap-pages.xml (statische Seiten) · sitemap-locations.xml · sitemap-events.xml
#   sitemap.xml (Index auf die drei)
# Nur Python-Standardbibliothek. Lokal ausführen, committen — später in die tägliche GitHub Action.
import json, urllib.request, datetime, sys

SU = "https://pnynkzrqnfoshojqfqxn.supabase.co"
SK = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ"
BASE = "https://depuls.ch/"
TODAY = datetime.date.today().isoformat()

def fetch(path):
    req = urllib.request.Request(SU + path, headers={"apikey": SK, "Authorization": "Bearer " + SK})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def urlset(urls):
    out = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for loc, lastmod in urls:
        out += f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>\n"
    return out + "</urlset>\n"

# 1) Statische Seiten  (news.html + immobilien.html sind noindex-Weiterleitungen -> NICHT in die Sitemap!)
PAGES = ['','gastro.html','nachtleben.html','events.html','shopping.html','kultur.html','dating.html',
 'feedback.html','kontakt.html','platzierung.html','impressum.html','datenschutz.html',
 'quartiere.html','musik.html','jobs.html','wohnungstausch/','mobilitaet.html','community.html','gps.html','partners.html','marktplatz.html']
import glob as _g
PAGES += sorted(p.replace('index.html','') for p in _g.glob('*/kreis-*/index.html'))  # nur real existierende Kreis-Seiten
open('sitemap-pages.xml','w',encoding='utf-8').write(urlset([(BASE+p, TODAY) for p in PAGES]))
print(f"sitemap-pages.xml: {len(PAGES)} URLs")

# 2) Alle aktiven Lokale (Profil-URL je Kategorie)
# SP_PRETTY_LOC v1 -- gastro/shopping/nachtleben/kultur nutzen die huebschen URLs
# aus location-links.json (von generate_location_pages.py im selben Lauf zuvor
# geschrieben).
import json as _json2
try:
    _LOC_LINKS = _json2.load(open('location-links.json', encoding='utf-8'))
except FileNotFoundError:
    print("WARNUNG: location-links.json fehlt -- generate_location_pages.py zuerst laufen lassen.")
    _LOC_LINKS = {}

PROFIL = {'gastro':'gastro-profil.html?id={id}','shopping':'shopping-profil.html?id={id}',
          'nachtleben':'nachtleben-profil.html?slug={slug}','kultur':'kultur-profil.html?id={id}'}
locs = fetch("/rest/v1/locations?select=id,slug,kategorie,aktiv&aktiv=eq.true&order=id.asc&limit=3000")
lurls = []
for l in locs:
    if l.get('kategorie') in ('gastro', 'shopping', 'nachtleben', 'kultur') and l['id'] in _LOC_LINKS:
        lurls.append((BASE.rstrip('/') + _LOC_LINKS[l['id']], TODAY))
        continue
    tpl = PROFIL.get(l.get('kategorie'))
    if not tpl: continue
    lurls.append((BASE + tpl.format(id=l['id'], slug=l.get('slug') or l['id']), TODAY))
open('sitemap-locations.xml','w',encoding='utf-8').write(urlset(lurls))
print(f"sitemap-locations.xml: {len(lurls)} URLs")

# 3) Kommende Events -- SP_PRETTY v1: liest die huebschen URLs, die
#    generate_event_pages.py im selben Lauf zuvor geschrieben hat
#    (event-links.json). Reihenfolge im nightly Job: erst
#    generate_event_pages.py, DANN dieses Skript.
import json as _json
try:
    _links = _json.load(open('event-links.json', encoding='utf-8'))
    _seen = set()
    eurls = []
    for _url in _links.values():
        if _url in _seen: continue
        _seen.add(_url)
        eurls.append((BASE.rstrip('/') + _url, TODAY))
except FileNotFoundError:
    print("WARNUNG: event-links.json fehlt -- generate_event_pages.py zuerst laufen lassen. Sitemap-Events bleibt leer.")
    eurls = []
open('sitemap-events.xml','w',encoding='utf-8').write(urlset(eurls))
print(f"sitemap-events.xml: {len(eurls)} URLs")

# 3b) Kreis-News & Storys -- Dateisystem-Scan (robust, kei Supabase noetig):
#     News-Hub /news/ + 12 Kreis-Hubs /kreis-N/news/ + alle Story-Detailseite.
NEWS = ['news/']
NEWS += sorted(p.replace('index.html','') for p in _g.glob('kreis-*/news/index.html'))    # 12 Kreis-Hubs
NEWS += sorted(p.replace('index.html','') for p in _g.glob('kreis-*/news/*/index.html'))   # Story-Detailseite
open('sitemap-news.xml','w',encoding='utf-8').write(urlset([(BASE+p, TODAY) for p in NEWS]))
print(f"sitemap-news.xml: {len(NEWS)} URLs")

# 4) Sitemap-Index
idx = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for f in ['sitemap-pages.xml','sitemap-locations.xml','sitemap-events.xml','sitemap-news.xml']:
    idx += f"  <sitemap><loc>{BASE}{f}</loc><lastmod>{TODAY}</lastmod></sitemap>\n"
idx += "</sitemapindex>\n"
open('sitemap.xml','w',encoding='utf-8').write(idx)
print(f"sitemap.xml: Index auf 4 Sitemaps · Total {len(PAGES)+len(lurls)+len(eurls)+len(NEWS)} URLs")
