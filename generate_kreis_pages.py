#!/usr/bin/env python3
# STADTPULS · generate_kreis_pages.py — 12 statische SEO-Landingpages: /gastro/kreis-N/
# Zieht die Top-Lokale je Kreis aus Supabase und rendert sie STATISCH (crawlbarer Content).
# Nur Standardbibliothek. Nach dem Lauf: generate_sitemap.py erneut ausführen.
import json, urllib.request, urllib.parse, os, datetime, html

SU = "https://pnynkzrqnfoshojqfqxn.supabase.co"
SK = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ"
D = "https://depuls.ch"
esc = html.escape

KREIS = {
 1:('Altstadt & City','Zwüsched Limmat, Bahnhofstrass und Niederdorf — Klassiker, Gourmet und Tradition sit Generatione.'),
 2:('Enge & Wollishofen','Am See entlang: Sommer-Terrasse, feini Quartier-Beize und Ruhe nach em Feierabig.'),
 3:('Wiedikon','Idaplatz-Flair und multikulturell — vo de Trend-Beiz bis zum ehrliche Quartier-Lokal.'),
 4:('Langstrass','S pulsierende Herz: rau, laut, legendär — vo de Kult-Beiz bis zum Late-Night-Spot.'),
 5:('Industriequartier','Vom Viadukt bis zur Hardbrugg — Industrie-Chic, Streetfood und Szene-Lokale.'),
 6:('Unterstrass & Oberstrass','Zwüsched Uni und Irchel — studentisch, gmüetlich, mit versteckte Perle.'),
 7:('Hottingen & Fluntern','Am Zürihorn-Hang: ruhig, grün und mit Ussicht — Quartier-Gastro mit Klasse.'),
 8:('Seefeld','Riesbach und Seefeld — Brunch-Meile, See-Nöchi und mediterrans Flair.'),
 9:('Altstetten & Albisrieden','Im Weste am Wachse — neui Lokale, ehrlichi Priise, echts Quartierläbe.'),
 10:('Höngg & Wipkingen','Am Limmat-Ufer: Röschtibach-Charme, Quartier-Beize und Wümmet-Tradition.'),
 11:('Oerlikon & Affoltern','De Norde läbt — vom Markt am Marktplatz bis zur Asia-Perle bim Bahnhof.'),
 12:('Schwamendingen','Understatement pur — wer suecht, findt hier di ehrlichste Quartier-Küche.'),
}

KATEGORIEN = {
 'gastro':     dict(pfad='gastro',     h1='ESSE IM',   wort='Restaurants, Cafés und Bars', titel='Restaurants', profil=lambda l: _LOC_LINKS.get(l['id']) or f"/gastro-profil.html?id={l['id']}",
                    faqv='isst me', faqv_de='isst man'),
 'nachtleben': dict(pfad='nachtleben', h1='USGAH IM',  wort='Clubs, Bars und Late-Night-Spots', titel='Nachtleben', profil=lambda l: _LOC_LINKS.get(l['id']) or f"/nachtleben-profil.html?slug={l.get('slug') or l['id']}",
                    faqv='gaht me us', faqv_de='geht man aus'),
 'shopping':   dict(pfad='shopping',   h1='SHOPPE IM', wort='Läden, Boutiquen und Brockis', titel='Shopping', profil=lambda l: _LOC_LINKS.get(l['id']) or f"/shopping-profil.html?id={l['id']}",
                    faqv='shoppt me', faqv_de='kauft man ein'),
 'kultur':     dict(pfad='kultur',     h1='ERLÄBE IM', wort='Museen, Galerie, Theater und Konzert', titel='Kultur', profil=lambda l: _LOC_LINKS.get(l['id']) or f"/kultur-profil.html?id={l['id']}",
                    faqv='findt me Kultur', faqv_de='findet man Kultur'),
}
MIN_LOKALE = 3  # unter 3 Lokal: kei Siite (Thin-Content-Schutz)

# SP_PRETTY_LOC v1 -- huebsche Location-URLs, von generate_location_pages.py geschrieben
try:
    _LOC_LINKS = json.load(open('location-links.json', encoding='utf-8'))
except FileNotFoundError:
    _LOC_LINKS = {}

def fetch(path):
    req = urllib.request.Request(SU + path, headers={"apikey": SK, "Authorization": "Bearer " + SK})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

TPL = """<!DOCTYPE html>
<html lang="gsw">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Restaurants Kreis {N} Zürich — {QNAME} | Stadtpuls</title>
<meta name="description" content="Die besten Restaurants, Cafés und Bars im Zürcher Kreis {N} ({QNAME_DE}): handkuratiert, mit Live-Öffnungsstatus und echten Bewertungen — ohne bezahlte Rankings.">
<link rel="canonical" href="{D}/gastro/kreis-{N}/">
<meta property="og:title" content="Restaurants Kreis {N} Zürich — {QNAME}">
<meta property="og:description" content="Die besten Lokale im Kreis {N}: handkuratiert auf Stadtpuls, mit Live-Status und echten Bewertungen.">
<meta property="og:url" content="{D}/gastro/kreis-{N}/">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_CH">
<meta property="og:site_name" content="Stadtpuls">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:image" content="{D}/og-image.png">
<meta name="twitter:image" content="{D}/og-image.png">
<script type="application/ld+json">{LD}</script>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@1,900&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#04040a;color:#e8e4d9;font-family:'DM Mono',monospace;min-height:100vh}}
a{{color:inherit}}
header{{padding:18px 22px;border-bottom:1px solid #14141f;display:flex;align-items:center;justify-content:space-between}}
.hleft{{display:flex;align-items:center;gap:9px;text-decoration:none}}
.ldot{{width:9px;height:9px;background:#ff2d00;border-radius:50%}}
.brand{{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:18px;letter-spacing:1px}}
main{{max-width:880px;margin:0 auto;padding:56px 22px}}
.eye{{font-size:9px;letter-spacing:3px;color:#ff2d00;text-transform:uppercase;margin-bottom:16px}}
h1{{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:clamp(44px,9vw,84px);line-height:.92;text-transform:uppercase}}
h1 span{{color:#ff2d00}}
.intro{{margin-top:20px;font-size:12px;line-height:1.9;color:#8a8778;max-width:560px}}
.cta{{display:inline-block;margin-top:26px;font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:15px;letter-spacing:1.5px;padding:13px 24px;background:#ff2d00;color:#04040a;text-decoration:none;text-transform:uppercase}}
.cta:hover{{background:#e8e4d9}}
h2{{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:24px;letter-spacing:1px;text-transform:uppercase;margin:52px 0 14px;color:#c8ff00}}
.loc{{display:flex;justify-content:space-between;align-items:baseline;gap:14px;padding:13px 0;border-bottom:1px solid rgba(232,228,217,.06);text-decoration:none}}
.loc b{{font-size:12px;letter-spacing:.5px}}
.loc:hover b{{color:#ff2d00}}
.loc .sub{{font-size:9px;color:#8a8778;letter-spacing:1px;text-transform:uppercase}}
.loc .r{{font-size:10px;color:#c8ff00;white-space:nowrap}}
details{{border:1px solid #14141f;margin-bottom:8px}}
summary{{cursor:pointer;padding:14px 16px;font-size:11px;color:#e8e4d9;list-style:none;display:flex;justify-content:space-between;gap:10px}}
summary::after{{content:'+';color:#ff2d00}}
details[open] summary::after{{content:'–'}}
details div{{padding:0 16px 14px;font-size:10.5px;line-height:1.8;color:#8a8778}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin-top:14px}}
.grid a{{border:1px solid #14141f;padding:10px;text-align:center;font-size:10px;letter-spacing:1px;text-decoration:none}}
.grid a:hover{{border-color:#ff2d00;color:#ff2d00}}
footer{{padding:18px 22px;border-top:1px solid #14141f;font-size:8px;letter-spacing:2px;color:#3a3a48;text-transform:uppercase}}
</style>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R1B1HL5W61"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-R1B1HL5W61');
</script>
</head>
<body>
<!-- SP_KREIS v1 -->
<header>
  <a class="hleft" href="/index.html"><div class="ldot"></div><div class="brand">STADTPULS</div></a>
  <a href="/gastro.html" style="font-size:9px;letter-spacing:2px;text-decoration:none;color:#8a8778">ALLI LOKAL →</a>
</header>
<main>
  <div class="eye">Gastro · Kreis {N} · {QNAME}</div>
  <h1>ESSE IM <span>KREIS {N}</span></h1>
  <p class="intro">{INTRO} Alli Lokal handkuratiert, mit Live-Öffnigsstatus und echte Bewertige — kei bezahlti Rankings ohni Kennzeichnig.</p>
  <a class="cta" href="/gastro.html?kreis={N}">Live-Liste Kreis {N} →</a>
  <h2>Top-Lokal im Kreis {N}</h2>
{LOCS}
  <h2>Frage &amp; Antworte</h2>
{FAQ}
  <h2>Anderi Kreis</h2>
  <div class="grid">
{GRID}
  </div>
</main>
<footer>STADTPULS — De Puls vo Züri · Handgmacht, kei Algorithmus-Bullshit</footer>
</body>
</html>
"""

TODAY = datetime.date.today().isoformat()
total = 0
qde_map = {1:'Altstadt und City',2:'Enge und Wollishofen',3:'Wiedikon',4:'Langstrasse',5:'Industriequartier',6:'Unterstrass und Oberstrass',7:'Hottingen und Fluntern',8:'Seefeld',9:'Altstetten und Albisrieden',10:'Höngg und Wipkingen',11:'Oerlikon und Affoltern',12:'Schwamendingen'}
for kat, K in KATEGORIEN.items():
  for n, (qname, intro) in KREIS.items():
    locs = fetch(f"/rest/v1/locations?select=id,slug,name,subkategorie,rating,rating_count&kategorie=eq.{kat}&aktiv=eq.true&kreis=eq.{n}&order=rating.desc.nullslast,rating_count.desc.nullslast&limit=10")
    if len(locs) < MIN_LOKALE:
        print(f"SKIP {kat}/kreis-{n}: nur {len(locs)} Lokal (< {MIN_LOKALE})")
        continue
    rows, items = [], []
    for i, l in enumerate(locs):
        name = esc(l.get('name') or '')
        sub = esc(l.get('subkategorie') or 'Lokal')
        r = l.get('rating')
        rtxt = f"★ {r:.1f}" if r else "—"
        href = K['profil'](l)
        rows.append(f'  <a class="loc" href="{href}"><span><b>{name}</b><br><span class="sub">{sub}</span></span><span class="r">{rtxt}</span></a>')
        items.append({"@type":"ListItem","position":i+1,"name":l.get('name') or '',"url":D+href})
    qde = qde_map[n]
    faq_pairs = [
      (f"Wo {K['faqv']} am beste im Kreis {n}?", f"Di Top-Adresse vom Kreis {n} stönd grad obe uf dere Siite — sortiert nach echte Bewertige. Für alli mit Filter: d Live-Liste.",
       f"Wo {K['faqv_de']} am besten in Zürich Kreis {n}?", f"Die Top-Adressen im Kreis {n} ({qde}) sind auf dieser Seite nach echten Bewertungen sortiert. Die vollständige, filterbare Liste gibt es auf depuls.ch/{K['pfad']}.html."),
      (f"Was hät im Kreis {n} jetzt offe?", "D Live-Liste zeigt de OFFE-Status in Echtzeit — berechnet uf Züri-Zit.",
       f"Was hat im Kreis {n} jetzt geöffnet?", "Die Live-Liste auf Stadtpuls zeigt den Öffnungsstatus in Echtzeit, berechnet auf Zürcher Zeit.")]
    faq_html = '\n'.join(f'  <details><summary>{esc(q)}</summary><div>{esc(a)}</div></details>' for q,a,_,_ in faq_pairs)
    ld = [
      {"@context":"https://schema.org","@type":"CollectionPage","name":f"{K['titel']} Kreis {n} Zürich","url":f"{D}/{K['pfad']}/kreis-{n}/","inLanguage":"de-CH",
       "mainEntity":{"@type":"ItemList","itemListElement":items}},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":qd,"acceptedAnswer":{"@type":"Answer","text":ad}} for _,_,qd,ad in faq_pairs]},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Stadtpuls","item":D+"/"},
        {"@type":"ListItem","position":2,"name":K['titel'],"item":f"{D}/{K['pfad']}.html"},
        {"@type":"ListItem","position":3,"name":f"Kreis {n}","item":f"{D}/{K['pfad']}/kreis-{n}/"}]},
    ]
    grid = '\n'.join(f'    <a href="/{K["pfad"]}/kreis-{k}/">KREIS {k}</a>' for k in KREIS if k != n)
    out = TPL.format(N=n, QNAME=esc(qname), QNAME_DE=esc(qde), INTRO=esc(intro), D=D,
                     LD=json.dumps(ld, ensure_ascii=False), LOCS='\n'.join(rows),
                     FAQ=faq_html, GRID=grid)
    out = out.replace('ESSE IM <span>', K['h1'] + ' <span>')
    out = out.replace('Restaurants Kreis', f"{K['titel']} Kreis").replace('Restaurants, Cafés und Bars', K['wort'])
    out = out.replace('/gastro.html?kreis=', f"/{K['pfad']}.html?kreis=").replace('href="/gastro.html"', f'href="/{K["pfad"]}.html"')
    out = out.replace('/gastro/kreis-', f"/{K['pfad']}/kreis-")
    out = out.replace('Gastro · Kreis', f"{K['titel']} · Kreis")
    os.makedirs(f"{K['pfad']}/kreis-{n}", exist_ok=True)
    open(f"{K['pfad']}/kreis-{n}/index.html", 'w', encoding='utf-8').write(out)
    total += 1
    print(f"OK {K['pfad']}/kreis-{n}/index.html — {len(locs)} Lokal")
import json as _j
_links={k:[] for k in KATEGORIEN}
import glob as _g2
for p in _g2.glob('*/kreis-*/index.html'):
    kat,kr=p.split('/')[0], int(p.split('kreis-')[1].split('/')[0])
    if kat in _links: _links[kat].append(kr)
for k in _links: _links[k].sort()
open('kreis-links.js','w',encoding='utf-8').write('window.SP_KREIS_LINKS='+_j.dumps(_links)+';')
print('OK kreis-links.js:', {k:len(v) for k,v in _links.items()})
print(f"FERTIG: {total} Kreis-Seiten (gastro+nachtleben+shopping+kultur). Jetzt generate_sitemap.py erneut ausführen!")
