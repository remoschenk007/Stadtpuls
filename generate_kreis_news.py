#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STADTPULS · Generator für die 12 Kreis-News-Hubs
Baut statische, einzeln indexierbari Syte: /kreis-1/news/ ... /kreis-12/news/
Jedi Syte: eigene Title/H1/Canonical, Quartier-Intro, FAQ + FAQPage-Schema,
BreadcrumbList, plus die aktuelle LIVE-Storys us Supabase FIX iigbacke (SEO),
und interni Verlinkig zu de andere Kreis.

Uusfüehre im Repo-Root:   python3 generate_kreis_news.py
Danach:                   git add kreis-* && git commit -m "Kreis-News-Hubs" && git push

Kei externi Library nötig (nur Python-Standardbibliothek).
"""

import os, json, html, re, urllib.request, urllib.error

# ── Supabase (öffentliche anon-Key, wie im Rest vom Code) ──────────────────
SB_URL = "https://pnynkzrqnfoshojqfqxn.supabase.co"
SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ"
SITE = "https://depuls.ch"

# ── Kreis-Date (Name, Farb, Title, Meta, Intro, FAQ) ──────────────────────
KREISE = {
 1:{"name":"Altstadt","c":"#ff2d00","meta":"News & Storys aus dem Kreis 1 Zürich – Altstadt, Niederdorf, Bahnhofstrasse & Lindenhof. Neueröffnungen, Quartier-Gschichte, Insider-Tipps.",
    "intro":"De Kreis 1 isch s Herz vo Züri – zwüsche Bahnhofstrasse, Lindenhof, Niederdorf und em See. Do schlaht de Puls vo de Stadt: Boutiquen, Kaffis, Altstadtgassen und s meischte Gwusel. Es Quartier zwüsche Business am Tag und Usgang am Abig, wo Tradition und Trend uf enge Rüüm ufenandertreffed.",
    "faq":[("Was ist neu im Kreis 1 Zürich?","Im Kreis 1 (Altstadt/City) dreiht sich viel um Gastro, Retail und Kultur rund um Bahnhofstrasse und Niederdorf. Aktuelle Neueröffnungen und Quartier-News meldet die Community laufend."),("Wo geht man im Kreis 1 aus?","Das Niederdorf und die Gassen der Altstadt sind das klassische Ausgangsgebiet – Bars, Beizen und Clubs auf engem Raum."),("Was macht den Kreis 1 besonders?","Er ist das historische und wirtschaftliche Zentrum Zürichs: Lindenhof, Grossmünster, Bahnhofstrasse und Limmatquai.")]},
 2:{"name":"Enge","c":"#00f5ff","meta":"News & Storys aus dem Kreis 2 Zürich – Enge, Wollishofen & Leimbach. Seenähe, Rieterpark, Quartierleben. Neueröffnungen und Insider-Tipps.",
    "intro":"De Kreis 2 ligt am linke Seeufer – vo de noble Enge über Wollishofen bis Leimbach. Rieterpark und Museum Rietberg, s Seebad Enge, ruhigi Wohnstrasse und trotzdem nöch am Zentrum. Es Quartier für Lüt, wo Grüen, See und Ruhe wänd, ohni uf d Stadt z verzichte.",
    "faq":[("Was ist neu im Kreis 2 Zürich?","Im Kreis 2 (Enge/Wollishofen/Leimbach) geht es viel um Quartierleben, Gastro und Seenähe."),("Was kann man im Kreis 2 unternehmen?","Rieterpark und Museum Rietberg, die Seepromenade, das Seebad Enge – Kultur und Erholung am Wasser."),("Ist der Kreis 2 ein gutes Wohnquartier?","Ja – die Enge gilt als eines der begehrtesten Wohnviertel Zürichs: seenah, grün und zentral.")]},
 3:{"name":"Wiedike","c":"#9333ea","meta":"News & Storys aus dem Kreis 3 Zürich – Wiedikon, Sihlfeld & Idaplatz. Quartierleben, Gastro, Neueröffnungen. Hyperlokal und ehrlich.",
    "intro":"De Kreis 3 – Wiedike, am Fuess vom Üetliberg – isch s Quartier mit Charakter: multikulti, bodeständig und im Ufwind. Rund um de Idaplatz, s Sihlfeld und s Lochergut gits chlini Beizli, Kaffis und Läde, wo mer no s Quartier gspürt. Weniger Schickimicki, meh echts Läbe – bsundrig bi Studente und Junge beliebt.",
    "faq":[("Was ist neu im Kreis 3 Zürich?","Wiedikon (Kreis 3) rund um Idaplatz und Sihlfeld ist ein Quartier im Aufwind – neue Cafés, Läden und Gastro entstehen laufend."),("Wo ist es am Idaplatz schön?","Der Idaplatz gilt als eine der gemütlichsten Ecken Zürichs – kleine Cafés, Beizli und Quartierflair."),("Was macht Wiedikon aus?","Wiedikon ist bodenständig, multikulturell und lebendig – zwischen Tradition und junger Kreativszene.")]},
 4:{"name":"Langstrass","c":"#ec4899","meta":"News & Storys aus dem Kreis 4 Zürich – Langstrasse & Aussersihl. Nachtleben, Neueröffnungen, Quartier-Gschichte. Der Puls des Ausgangsviertels.",
    "intro":"De Kreis 4 – Aussersihl mit em Werd, de Langstrass und em Hard – isch s pulsierendschte Quartier vo Züri. D Langstrass schloft nie: vo de Bahnhof-Unterführig bis zum Helvetiaplatz läbt d Stadt rund um d Uhr. Über hundert Nationalitäte, Bars, Beizli us aller Wält, Clubs und chlini Läde uf de bekannteschte Meile vo de Schwiiz. Rund um Helvetiaplatz, Bäckeranlage, Stauffacher und d Europaallee mischt sich rau und herzlich, alt und nöi.",
    "faq":[("Was ist neu im Kreis 4 Zürich?","Im Kreis 4 (Langstrasse/Aussersihl) tut sich ständig etwas – neue Bars, Restaurants und Läden. Die Community meldet Neueröffnungen laufend."),("Wo geht man im Kreis 4 aus?","Der Kreis 4 rund um die Langstrasse ist das Nachtleben-Zentrum Zürichs: Bars, Clubs und Beizen dicht an dicht."),("Wie ist das Quartier Kreis 4?","Lebendig, multikulturell (über 100 Nationalitäten) und dicht bebaut – tagsüber Quartierleben, nachts das grosse Ausgangsviertel.")]},
 5:{"name":"Industrie","c":"#c8ff00","meta":"News & Storys aus dem Kreis 5 Zürich – Industriequartier & Zürich-West. Prime Tower, Frau Gerolds Garten, Kultur & Gastro. Das hippste Viertel.",
    "intro":"De Kreis 5 – s Industriequartier, au „Züri-West\" gnennt – isch vom Fabrik-Viertel zum hippste Quartier vo de Stadt worde. Rund um d Hardbrugg staht de Prime Tower, dernäbed Frau Gerolds Garte, s Löwenbräu-Kunstareal, de Schiffbau und de Freitag-Tower. Industriecharme trifft uf Design, Kunst, Foodmärt und Clubs – kreativ, urban, immer en Schritt vorus.",
    "faq":[("Was ist neu im Kreis 5 Zürich?","Zürich-West (Kreis 5) ist eines der dynamischsten Quartiere – rund um Prime Tower, Frau Gerolds Garten und das Löwenbräu-Areal entsteht laufend Neues."),("Was kann man im Kreis 5 machen?","Kunst im Löwenbräu-Areal, Ausgang an der Hardbrücke, Foodmärkte und Rooftop-Bars – Zürich-West ist Kultur und Nightlife zugleich."),("Warum ist Zürich-West so beliebt?","Das ehemalige Industriequartier wurde zum Kreativ- und Ausgangsviertel: Backstein-Charme, Design, Kunst und Gastro auf engem Raum.")]},
 6:{"name":"Unterstrass","c":"#ff2d00","meta":"News & Storys aus dem Kreis 6 Zürich – Unterstrass & Oberstrass. Uni-Nähe, Familienquartier, Rigiblick. Neueröffnungen und Quartier-Tipps.",
    "intro":"De Kreis 6 – Unter- und Oberstrass – ligt am Hang zwüsche Zentrum und Züribärg. Nöch bi Uni und ETH, und trotzdem grüen und ruhig: es beliebts Quartier für Familie und Studente. Vom Rigiblick mit Sicht über d Stadt bis zu de Quartierstrasse mit Bäckerei, Kaffi und Buchlade.",
    "faq":[("Was ist neu im Kreis 6 Zürich?","Im Kreis 6 (Unterstrass/Oberstrass) dreht sich vieles um Quartierleben, Gastro und die Uni-Nähe."),("Ist der Kreis 6 ein gutes Wohnquartier?","Ja – Unter- und Oberstrass sind beliebt bei Familien und Studierenden: grün, ruhig, zentral, nahe an Uni und ETH."),("Was kann man im Kreis 6 unternehmen?","Aussicht vom Rigiblick, gemütliche Quartiercafés und die Nähe zu Uni/ETH prägen den Kreis 6.")]},
 7:{"name":"Fluntere","c":"#00f5ff","meta":"News & Storys aus dem Kreis 7 Zürich – Fluntern, Hottingen, Hirslanden & Witikon. Zürichberg, Zoo, Aussicht. Quartier-News und Tipps.",
    "intro":"De Kreis 7 ligt am Züribärg – s grüenschte und eis vo de nobelste Quartier vo Züri. Fluntere, Hottinge, Hirslande und Witike: Villenquartier, Wald, Aussicht über See und Stadt. Do sind de Zoo, de Dolder und ruhigi Wohnlage – für Lüt, wo Natur, Ruhe und Weitsicht schätzed.",
    "faq":[("Was ist neu im Kreis 7 Zürich?","Im Kreis 7 (Zürichberg) geht es um Quartierleben, Gastro und die grüne, ruhige Wohnlage."),("Was kann man im Kreis 7 machen?","Der Zoo Zürich, Spaziergänge im Zürichbergwald, Aussicht vom Dolder – Natur und Panorama pur."),("Warum gilt der Kreis 7 als nobel?","Der Zürichberg ist eines der teuersten und grünsten Wohngebiete Zürichs: Villen, Wald und Weitblick.")]},
 8:{"name":"Seefeld","c":"#9333ea","meta":"News & Storys aus dem Kreis 8 Zürich – Seefeld & Riesbach. Zürichhorn, Chinagarten, Seepromenade, Boutiquen. Quartier-News und Insider-Tipps.",
    "intro":"De Kreis 8 – s Seefeld – isch Züris chic-entspannti Seesite. Rund um d Seefeldstrass reihed sich Boutiquen, Kaffis und Restaurants, dernäbed s Zürihorn mit Chinagarte, Blatterwiese und Seebad. Do trifft Lifestyle uf Wasser: joggen am See, Kaffi mit Sicht, Apéro bi Sunneuntergang.",
    "faq":[("Was ist neu im Kreis 8 Zürich?","Im Seefeld (Kreis 8) dreht sich vieles um Gastro, Boutiquen und das Leben am See."),("Was kann man im Kreis 8 unternehmen?","Zürichhorn mit Chinagarten, Seepromenade, Seebad Utoquai und die Boutiquen der Seefeldstrasse."),("Ist das Seefeld ein teures Quartier?","Ja – das Seefeld gilt als eines der begehrtesten und lebendigsten Seeviertel Zürichs.")]},
 9:{"name":"Altstette","c":"#ec4899","meta":"News & Storys aus dem Kreis 9 Zürich – Altstetten & Albisrieden. Grösster Kreis, Quartier im Wandel, Neueröffnungen. Hyperlokal aus dem Westen.",
    "intro":"De Kreis 9 – Altstette und Albisriede – isch de bevölkerungsriichscht Kreis vo Züri und im grosse Wandel. Im Weschte glägä, mischt sich do alts Dorfquartier mit nöie Überbauige, Gwerbe und Familie. Rund um de Lindeplatz und d Bahnhöf entstaht laufend Nöis: Wohne, Läden, Gastro. Es Quartier, wo Züri wachst.",
    "faq":[("Was ist neu im Kreis 9 Zürich?","Der Kreis 9 (Altstetten/Albisrieden) ist ein Quartier im starken Wandel – neue Überbauungen, Gewerbe und Gastro entstehen laufend."),("Was macht den Kreis 9 aus?","Altstetten und Albisrieden bilden den grössten Kreis Zürichs – altes Dorfquartier und moderne Stadtentwicklung im Westen."),("Ist der Kreis 9 ein gutes Wohnquartier?","Der Kreis 9 ist bezahlbarer als die Innenstadt, gut angebunden und im Aufwind.")]},
 10:{"name":"Höngg","c":"#c8ff00","meta":"News & Storys aus dem Kreis 10 Zürich – Höngg & Wipkingen. Limmat, Röschibachplatz, Quartierleben. Neueröffnungen und Insider-Tipps.",
    "intro":"De Kreis 10 – Höngg und Wipkinge – ligt am Hang über de Limmat, ruhig und grüen. Wipkinge mit em läbendige Röschibachplatz isch es junges, gmütlichs Quartier, Höngg meh dörflich mit Reblage und Wiitsicht. Do läbt mer nöch am Wasser und trotzdem uf em Land-Gfühl.",
    "faq":[("Was ist neu im Kreis 10 Zürich?","Im Kreis 10 (Höngg/Wipkingen) dreht sich vieles um Quartierleben, Gastro und das Leben an der Limmat."),("Wo ist es in Wipkingen schön?","Der Röschibachplatz ist das lebendige Herz von Wipkingen – Cafés, Beizli und Quartierflair."),("Was macht Höngg aus?","Höngg ist eher dörflich, mit Rebbergen, Aussicht und ruhigem Wohncharakter – trotzdem nah an der Stadt.")]},
 11:{"name":"Oerlike","c":"#ff2d00","meta":"News & Storys aus dem Kreis 11 Zürich – Oerlikon, Seebach & Affoltern. MFO-Park, Hallenstadion, Quartier im Boom. Neueröffnungen und Tipps.",
    "intro":"De Kreis 11 – Affoltere, Oerlike und Seebach – isch de Norde vo Züri und eis vo de am schnellschte wachsende Gebiet. Oerlike isch es eiges chlises Zentrum: Bahnhof, MFO-Park, Hallestadion, Messe und immer meh Gastro. Rund ume entstönd nöi Quartier, Büros und Wohnige – dynamisch, jung und im Cho.",
    "faq":[("Was ist neu im Kreis 11 Zürich?","Der Kreis 11 (Oerlikon/Seebach/Affoltern) boomt – rund um Bahnhof Oerlikon, MFO-Park und die Messe entstehen laufend neue Läden und Gastro."),("Was kann man in Oerlikon machen?","MFO-Park, Hallenstadion, Messe Zürich und ein wachsendes Gastro-Angebot machen Oerlikon zum lebendigen Zentrum von Zürich-Nord."),("Ist der Kreis 11 ein gutes Wohnquartier?","Ja – Zürich-Nord ist gut angebunden, bezahlbarer als das Zentrum und stark im Aufwind.")]},
 12:{"name":"Schwamendinge","c":"#00f5ff","meta":"News & Storys aus dem Kreis 12 Zürich – Schwamendingen. Gartenstadt, Quartierleben, viel Grün. Neueröffnungen und hyperlokale Tipps.",
    "intro":"De Kreis 12 – Schwamendinge – isch d „Gartestadt\" vo Züri: viel Grüen, Genossenschaftssiedlige und en starke Quartier-Zämehalt. Im Nordoschte glägä, günstiger als s Zentrum und mit em Tram schnell aagbunde. Es Quartier im Wandel, wo grad viel Nöis entstaht und trotzdem sini bodeständigi, familiäri Seele bhaltet.",
    "faq":[("Was ist neu im Kreis 12 Zürich?","In Schwamendingen (Kreis 12) tut sich einiges – neue Überbauungen, Gastro und Quartierprojekte."),("Was macht Schwamendingen aus?","Schwamendingen ist als „Gartenstadt\" bekannt: viel Grün, Genossenschaftssiedlungen und ein starkes Quartierleben im Nordosten."),("Ist der Kreis 12 ein gutes Wohnquartier?","Ja – Schwamendingen ist bezahlbar, grün, familienfreundlich und mit dem Tram gut angebunden.")]},
}

def slugify(s):
    s=(s or "").lower()
    for a,b in [("ä","ae"),("ö","oe"),("ü","ue"),("ß","ss")]: s=s.replace(a,b)
    out=[]
    for ch in s:
        if ch.isalnum(): out.append(ch)
        elif ch in " -_": out.append("-")
    r="".join(out)
    while "--" in r: r=r.replace("--","-")
    return r.strip("-")

def fetch_stories(kreis):
    url=f"{SB_URL}/rest/v1/news_stories?select=*&status=eq.live&kreis=eq.{kreis}&order=created_at.desc&limit=100"
    req=urllib.request.Request(url, headers={"apikey":SB_KEY,"Authorization":"Bearer "+SB_KEY})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print(f"   ! Kreis {kreis}: kei Live-Date ({e}) — Syte wird ohni Storys gnereiert.")
        return []

def esc(s): return html.escape(str(s or ""), quote=True)

# URLs im (scho escapte!) Fliesstext automatisch klickbar mache.
# WICHTIG: immer NACH esc() ufrüefe, susch würded &amp; etc. doppelt escaped.
_URL_RE = re.compile(r'https?://[^\s<>()]+')
def linkify(escaped_text):
    def _repl(m):
        url = m.group(0)
        trail = ""
        # Satzzeichen am Schluss ghööred nöd i de Link (Slash / bliibt = Clean-URL)
        while url and url[-1] in ".,!?":
            trail = url[-1] + trail
            url = url[:-1]
        if not url:
            return m.group(0)
        internal = "depuls.ch" in url
        attrs = "" if internal else ' target="_blank" rel="noopener nofollow"'
        return f'<a href="{url}"{attrs}>{url}</a>{trail}'
    return _URL_RE.sub(_repl, escaped_text)

# ── SEO / GEO-Helfer ───────────────────────────────────────────────
# Zwischentitel-Erkennig: churzi Zile wo mit eme Emoji aafanged (z.B.
# "💧 1. Wasser…", "🚨 Was mache…") werded als <h2> grendert → bessri
# Struktur für Google & KI-Suche. Bulletpoints (*, -) und Zitat (>) nöd.
def _is_heading(line):
    s = (line or "").strip()
    if not s or s[0] in "*->•·":
        return False
    return ord(s[0]) >= 0x2600 and len(s) <= 80

def render_body(inhalt, teaser=""):
    parts = []
    for raw in (inhalt or "").split(chr(10)):
        line = raw.strip()
        if not line:
            continue
        tag = "h2" if _is_heading(line) else "p"
        parts.append(f"<{tag}>{linkify(esc(line))}</{tag}>")
    return "".join(parts) or f"<p>{linkify(esc(teaser))}</p>"

def keywords_for(k, kat):
    name = KREISE[k]["name"]
    kws = [f"Kreis {k} Zürich", f"News Kreis {k}", name, "Zürich",
           kat, "Quartier News", "Stadtpuls", "Züri"]
    seen, out = set(), []
    for w in kws:
        w = (w or "").strip()
        if w and w.lower() not in seen:
            seen.add(w.lower()); out.append(w)
    return ", ".join(out)

def faq_block_html(k):
    name = KREISE[k]["name"]
    items = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary>'
        f'<div class="faq-a">{esc(a)}</div></details>'
        for q, a in KREISE[k]["faq"])
    return (f'<section class="art-faq"><h2>Häufigi Frooge · Kreis {k} {esc(name)}</h2>'
            f'{items}</section>') if items else ""

def story_card(k, o):
    titel=o.get("titel") or o.get("title") or "Ohni Titel"
    teaser=o.get("teaser") or o.get("inhalt") or ""
    kat=o.get("kategorie") or "Quartier"
    autor=o.get("autor") or "@stadtpuls"
    slug=o.get("slug") or slugify(titel)
    surl=f"/kreis-{k}/news/{slug}"
    alt=f"{titel} / Stadtpuls Kreis {k} Zürich"
    img=o.get("bild_url") or ""
    imgtag=f'<img class="cimg" src="{esc(img)}" alt="{esc(alt)}" loading="lazy">' if img else ""
    return f'''<a class="card" href="{esc(surl)}" style="text-decoration:none;color:inherit">{imgtag}
      <div class="toprow"><span class="ktag">Kreis {k}</span><span class="cat">{esc(kat)}</span></div>
      <h3>{esc(titel)}</h3><p>{esc(teaser)}</p>
      <div class="foot"><span>{esc(autor)}</span><span class="readmore">Läse →</span></div></a>'''

def faq_schema(faq):
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}, ensure_ascii=False)

def breadcrumb_schema(k):
    return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Stadtpuls","item":SITE},
        {"@type":"ListItem","position":2,"name":"News","item":SITE+"/news"},
        {"@type":"ListItem","position":3,"name":f"News Kreis {k} Zürich","item":f"{SITE}/kreis-{k}/news/"}]}, ensure_ascii=False)

TEMPLATE = open(os.path.join(os.path.dirname(__file__),"_kreis_news_template.html"),encoding="utf-8").read() \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"_kreis_news_template.html")) else None

def page(k, stories):
    d=KREISE[k]; name=d["name"]; col=d["c"]
    cards="\n".join(story_card(k,o) for o in stories) if stories else \
        f'<div class="empty"><div class="disp">SEI DE ERSCHT</div><p>No kei Story im Kreis {k} ({esc(name)}). Schrib du die erschti — sie chunnt sofort dur d KI-Prüfig live.</p><a class="wb" href="/login.html">Story schriebe →</a></div>'
    faq_html="\n".join(f'<details class="faq-item"><summary>{esc(q)}</summary><div class="faq-a">{esc(a)}</div></details>' for q,a in d["faq"])
    # Nachbar-Kreis-Links (interni Link-Pyramide)
    others="".join(f'<a class="kchip" href="/kreis-{n}/news/">Kreis {n} · {esc(KREISE[n]["name"])}</a>' for n in KREISE if n!=k)
    title=f"News Kreis {k} Zürich – {name} | Stadtpuls"
    tokens={
      "__K__":str(k),"__NAME__":esc(name),"__COL__":col,"__TITLE__":esc(title),
      "__META__":esc(d["meta"]),"__CANON__":f"{SITE}/kreis-{k}/news/","__INTRO__":esc(d["intro"]),
      "__CARDS__":cards,"__FAQ__":faq_html,"__OTHERS__":others,
      "__SCHEMA_FAQ__":faq_schema(d["faq"]),"__SCHEMA_BC__":breadcrumb_schema(k),
    }
    out=PAGE_HTML
    for t,v in tokens.items(): out=out.replace(t,v)
    return out

PAGE_HTML = r"""<!DOCTYPE html>
<html lang="de-CH">
<head>
<base href="/">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__META__">
<link rel="canonical" href="__CANON__">
<meta property="og:type" content="website"><meta property="og:title" content="News Kreis __K__ Zürich – __NAME__">
<meta property="og:description" content="__META__"><meta property="og:url" content="__CANON__"><meta property="og:locale" content="de_CH">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">__SCHEMA_BC__</script>
<script type="application/ld+json">__SCHEMA_FAQ__</script>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,900;1,900&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#04040a;--rot:#ff2d00;--volt:#c8ff00;--cream:#e8e4d9;--kc:__COL__}
body{background:var(--bg);color:var(--cream);font-family:'DM Mono',monospace;padding-top:47px}
.wrap{max-width:1100px;margin:0 auto;padding:0 22px}
a{color:inherit}
h1,h2,h3{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;text-transform:uppercase;line-height:.95}
/* Original Stadtpuls-Nav (1:1) */
.nav{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;background:rgba(0,0,0,0.95);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,45,0,0.15)}
.nav-logo{padding:14px 20px;border-right:1px solid rgba(255,45,0,0.1);display:flex;align-items:center;gap:8px;text-decoration:none;flex-shrink:0}
.logo-txt{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;letter-spacing:4px;font-size:19px;color:#e8e4d9}
.ldot{width:7px;height:7px;border-radius:50%;background:#ff2d00;animation:blink 2s infinite;flex-shrink:0}
@keyframes blink{0%,100%{box-shadow:0 0 0 0 rgba(255,45,0,0.7)}50%{box-shadow:0 0 0 6px rgba(255,45,0,0)}}
.nav-links{display:flex;flex:1;overflow-x:auto;scrollbar-width:none}
.nav-links::-webkit-scrollbar{display:none}
.nav-link{padding:14px 16px;font-size:9px;letter-spacing:3px;color:rgba(232,228,217,0.3);text-decoration:none;text-transform:uppercase;white-space:nowrap;transition:color .2s;border-right:1px solid rgba(255,45,0,0.06)}
.nav-link:hover{color:#e8e4d9}
.nav-link.active{color:#ff2d00}
.nav-cta{padding:10px 18px;margin:8px 14px;background:#ff2d00;color:#04040a;font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:14px;letter-spacing:2px;text-transform:uppercase;border-radius:2px;white-space:nowrap;flex-shrink:0;text-decoration:none;display:flex;align-items:center}
.crumb{font-family:'DM Mono';font-size:11px;letter-spacing:1px;color:#7a7a7a;text-transform:uppercase;margin:26px 0 14px}
.crumb a{color:#9a9a9a;text-decoration:none}
h1.title{font-size:clamp(40px,7vw,80px);color:var(--cream)} h1.title .g{color:var(--kc)}
.intro{border-left:3px solid var(--kc);padding:8px 0 8px 20px;margin:16px 0 30px;max-width:820px;font-size:14px;line-height:1.7;color:#b9b6ac}
h2.sec{font-size:clamp(26px,4vw,38px);margin:34px 0 18px;color:var(--cream)} h2.sec .g{color:var(--kc)}
.feed{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.card{display:block;border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:20px;background:rgba(255,255,255,.02);transition:transform .2s,border-color .2s,box-shadow .2s}
.card:hover{transform:translateY(-4px);border-color:var(--kc);box-shadow:0 14px 40px -14px var(--kc)}
.card .cimg{width:100%;height:130px;object-fit:cover;border-radius:9px;margin-bottom:14px;display:block}
.card .toprow{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.ktag{font-size:10px;letter-spacing:1px;text-transform:uppercase;padding:4px 10px;border-radius:5px;background:__COL__22;color:var(--kc);text-decoration:none}
.card .cat{font-size:10px;letter-spacing:2px;color:#7a7a7a;text-transform:uppercase}
.card h3{font-size:21px;color:var(--cream);margin-bottom:9px;line-height:1.12}
.card h3 a{text-decoration:none} .card p{font-size:12.5px;color:#a5a29a;line-height:1.55}
.card .foot{margin-top:14px;font-size:10.5px;color:#7a7a7a;display:flex;justify-content:space-between;align-items:center}
.readmore{color:var(--kc);font-weight:500}
.empty{grid-column:1/-1;text-align:center;padding:50px 20px;border:1px dashed rgba(255,255,255,.12);border-radius:16px}
.empty .disp{font-family:'Barlow Condensed';font-style:italic;font-weight:900;font-size:40px;color:#2a2a30}
.empty p{color:#7a7a7a;font-size:13px;margin:8px 0 16px}
.wb{background:var(--volt);color:#04040a;font-family:'Barlow Condensed';font-style:italic;font-weight:900;font-size:16px;text-transform:uppercase;border-radius:6px;padding:12px 22px;text-decoration:none}
.faq-item{border:1px solid rgba(255,255,255,.08);border-radius:12px;margin-bottom:10px;overflow:hidden;background:rgba(255,255,255,.02)}
.faq-item summary{cursor:pointer;padding:15px 18px;font-family:'Barlow Condensed';font-style:italic;font-weight:900;font-size:19px;text-transform:uppercase;color:var(--cream);list-style:none;display:flex;justify-content:space-between}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:'+';color:var(--volt)} .faq-item[open] summary::after{content:'–'}
.faq-a{padding:0 18px 16px;font-size:13px;color:#a5a29a;line-height:1.6}
.others{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 50px}
.kchip{font-size:11px;letter-spacing:1px;text-transform:uppercase;padding:8px 14px;border:1px solid rgba(255,255,255,.14);border-radius:22px;color:#b7b4ab;text-decoration:none}
.kchip:hover{border-color:var(--cream);color:var(--cream)}
/* Original Stadtpuls-Footer (1:1) */
footer{background:#04040a;border-top:1px solid rgba(255,45,0,0.1)}
.ftk{background:rgba(255,45,0,.06);padding:.4rem 0;overflow:hidden;white-space:nowrap;border-bottom:1px solid rgba(255,45,0,.1)}
.fti{display:inline-block;animation:tkr 22s linear infinite}
.fti span{font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.14em;color:rgba(255,45,0,.45);text-transform:uppercase;margin:0 2rem}
@keyframes tkr{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.fg{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2rem;max-width:1320px;margin:0 auto;padding:2.5rem 1.5rem 2rem}
@media(max-width:768px){.fg{grid-template-columns:1fr 1fr;padding:2rem 1.5rem}.footer-brand{grid-column:span 2}}
.fbl{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:1.6rem;letter-spacing:.1em;display:flex;align-items:center;gap:.6rem;margin-bottom:.7rem;color:#e8e4d9}
.fbdot{width:8px;height:8px;background:#ff2d00;border-radius:50%;box-shadow:0 0 8px #ff2d00;flex-shrink:0}
.footer-brand p{font-family:'DM Mono',monospace;font-size:.7rem;color:rgba(232,228,217,0.4);line-height:1.9;max-width:280px}
.fc h5{font-family:'DM Mono',monospace;font-size:.6rem;letter-spacing:.28em;text-transform:uppercase;color:#ff2d00;margin-bottom:1rem;font-weight:500}
.fc ul{list-style:none;margin:0;padding:0}
.fc li{font-family:'DM Mono',monospace;font-size:.75rem;margin-bottom:.6rem}
.fc li a{color:rgba(232,228,217,0.45);text-decoration:none;transition:color .2s}
.fc li a:hover{color:#e8e4d9}
.fbot{max-width:1320px;margin:0 auto;padding:1.2rem 1.5rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;border-top:1px solid rgba(255,255,255,0.05)}
.fbot p{font-family:'DM Mono',monospace;font-size:.65rem;letter-spacing:.1em;color:rgba(232,228,217,0.25);text-transform:uppercase;margin:0}
</style>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R1B1HL5W61"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-R1B1HL5W61');
</script>
</head>
<body>
<script src="/location-links.js"></script>
<nav class="nav">
  <a href="index.html" class="nav-logo"><div class="ldot"></div><span class="logo-txt">STADTPULS</span></a>
  <div class="nav-links">
    <a href="gastro.html" class="nav-link">GASTRO</a>
    <a href="/kultur.html" class="nav-link">KULTUR</a>
    <a href="nachtleben.html" class="nav-link">NACHTLEBE</a>
    <a href="events.html" class="nav-link">EVENTS</a>
    <a href="shopping.html" class="nav-link">SHOPPING</a>
    <a href="news.html" class="nav-link active">NEWS</a>
    <a href="dating.html" class="nav-link">DATES</a>
  </div>
  <a href="login.html" class="nav-cta">MITMACHE</a>
<button class="sp-nav-burger" onclick="spNavToggle()" aria-label="Menü"><span></span><span></span><span></span></button>
</nav>
<div class="wrap">
  <div class="crumb"><a href="/">Stadtpuls</a> › <a href="/news.html">News</a> › <span>Kreis __K__ Zürich</span></div>
  <h1 class="title">NEWS KREIS __K__ <span class="g">ZÜRICH</span></h1>
  <div class="intro">__INTRO__</div>

  <h2 class="sec">AKTUELLI <span class="g">STORYS</span> · KREIS __K__</h2>
  <div class="feed">__CARDS__</div>

  <h2 class="sec">HÜFIGI <span class="g">FRÅGE</span> · KREIS __K__ __NAME__</h2>
  __FAQ__

  <h2 class="sec">ANDERI <span class="g">KREIS</span></h2>
  <div class="others">__OTHERS__</div>
</div>
<footer>
  <div class="ftk"><div class="fti">
    <span>STADTPULS 2026</span><span>NEUE ÄRA</span><span>DÄ PULS VO DÄ STADT</span><span>ZÜRICH</span><span>LIFESTYLE & CITY GUIDE</span><span>SOCIAL MEDIA & MARKTPLATTFORM</span><span>DER VIRTUELLE SPIELPLATZ</span><span>by raimondo*</span><span>STADTPULS 2026</span><span>NEUE ÄRA</span><span>DÄ PULS VO DÄ STADT</span><span>ZÜRICH</span><span>LIFESTYLE & CITY GUIDE</span><span>SOCIAL MEDIA & MARKTPLATTFORM</span><span>DER VIRTUELLE SPIELPLATZ</span><span>by raimondo*</span>
  </div></div>
  <div class="fg">
    <div class="footer-brand"><div class="fbl"><div class="fbdot"></div>STADTPULS</div><p>dä puls vo dä stadt<br><br>Interaktiver Lifestyle & City Guide für Zürich. Social Media & Marktplattform. Der virtuelle Spielplatz für Erwachsene.<br><br>© 2026 by raimondo* — Zürich</p></div>
    <div class="fc"><h5>Entdecken</h5><ul>
      <li><a href="gastro.html">Gastro & Bars</a></li><li><a href="nachtleben.html">Nachtleben</a></li><li><a href="shopping.html">Shopping</a></li><li><a href="events.html">Events</a></li><li><a href="quartiere.html">Quartiere</a></li><li><a href="musik.html">Musik & Sound</a></li><li><a href="mobilitaet.html">Mobilität</a></li><li><a href="/kultur.html">Kultur</a></li>
    </ul></div>
    <div class="fc"><h5>Community</h5><ul>
      <li><a href="community.html">Feed & Posts</a></li><li><a href="dating.html">People & Dates</a></li><li><a href="jobs.html">Jobs Züri</a></li><li><a href="news.html">News & Stories</a></li><li><a href="gps.html">GPS — Wo bisch du?</a></li><li><a href="partners.html">Kooperatione</a></li>
    </ul></div>
    <div class="fc"><h5>Mitmache</h5><ul>
      <li><a href="login.html">Einlogge</a></li><li><a href="login.html">Profil aalege</a></li><li><a href="community.html">Blogger werde</a></li><li><a href="immobilien.html">Inserat schalte</a></li><li><a href="partners.html">Partner werde</a></li><li><a href="kontakt.html">Kontakt</a></li>
    </ul></div>
  </div>
  <div class="fbot">
    <p>© 2026 depuls.ch — by raimondo* — Zürich</p>
    <p style="display:flex;gap:14px"><span>AGB</span> · <a href="datenschutz.html" style="color:rgba(232,228,217,0.25);text-decoration:none">Datenschutz</a> · <a href="impressum.html" style="color:rgba(232,228,217,0.25);text-decoration:none">Impressum</a></p>
  </div>
</footer>
</body>
</html>"""

import datetime
def iso_date(o):
    v=o.get("published_at") or o.get("created_at") or o.get("datum")
    return str(v) if v else datetime.date.today().isoformat()
def disp_date(o):
    v=o.get("published_at") or o.get("created_at") or o.get("datum")
    if not v:
        t=datetime.date.today(); return f"{t.day}.{t.month}.{t.year}"
    try:
        y,m,d=str(v)[:10].split("-"); return f"{int(d)}.{int(m)}.{y}"
    except Exception:
        return str(v)

STORY_HTML = r"""<!DOCTYPE html>
<html lang="gsw-CH">
<head>
<base href="/">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__META_DESC__">
<meta name="keywords" content="__KEYWORDS__">
<meta name="author" content="__AUTOR__">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="__CANON__">
<meta property="og:type" content="article"><meta property="og:title" content="__H1__"><meta property="og:description" content="__META_DESC__"><meta property="og:url" content="__CANON__"><meta property="og:locale" content="de_CH"><meta property="og:site_name" content="Stadtpuls">__OGIMG__
<meta property="article:published_time" content="__ISODATE__"><meta property="article:modified_time" content="__ISODATE__"><meta property="article:section" content="__KAT__"><meta property="article:author" content="__AUTOR__">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="__H1__"><meta name="twitter:description" content="__META_DESC__">__TWIMG__
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">__SCHEMA_NA__</script>
<script type="application/ld+json">__SCHEMA_BC__</script>
__SCHEMA_FAQ__
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,900;1,900&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#04040a;--rot:#ff2d00;--volt:#c8ff00;--cream:#e8e4d9;--kc:__COL__}
body{background:var(--bg);color:var(--cream);font-family:'DM Mono',monospace;padding-top:47px}
.wrap{max-width:820px;margin:0 auto;padding:0 22px}
a{color:inherit}
h1,h2,h3{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;text-transform:uppercase;line-height:.95}
.nav{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;background:rgba(0,0,0,0.95);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,45,0,0.15)}
.nav-logo{padding:14px 20px;border-right:1px solid rgba(255,45,0,0.1);display:flex;align-items:center;gap:8px;text-decoration:none;flex-shrink:0}
.logo-txt{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;letter-spacing:4px;font-size:19px;color:#e8e4d9}
.ldot{width:7px;height:7px;border-radius:50%;background:#ff2d00;animation:blink 2s infinite;flex-shrink:0}
@keyframes blink{0%,100%{box-shadow:0 0 0 0 rgba(255,45,0,0.7)}50%{box-shadow:0 0 0 6px rgba(255,45,0,0)}}
.nav-links{display:flex;flex:1;overflow-x:auto;scrollbar-width:none}.nav-links::-webkit-scrollbar{display:none}
.nav-link{padding:14px 16px;font-size:9px;letter-spacing:3px;color:rgba(232,228,217,0.3);text-decoration:none;text-transform:uppercase;white-space:nowrap;border-right:1px solid rgba(255,45,0,0.06)}
.nav-link:hover{color:#e8e4d9}.nav-link.active{color:#ff2d00}
.nav-cta{padding:10px 18px;margin:8px 14px;background:#ff2d00;color:#04040a;font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:14px;letter-spacing:2px;text-transform:uppercase;border-radius:2px;white-space:nowrap;flex-shrink:0;text-decoration:none;display:flex;align-items:center}
.crumb{font-family:'DM Mono';font-size:11px;letter-spacing:1px;color:#7a7a7a;text-transform:uppercase;margin:30px 0 16px}
.crumb a{color:#9a9a9a;text-decoration:none}
.art-tag{display:inline-block;font-size:10px;letter-spacing:1px;text-transform:uppercase;padding:5px 11px;border-radius:5px;background:__COL__22;color:var(--kc);margin-bottom:14px}
h1.art{font-size:clamp(34px,6vw,62px);color:var(--cream);margin-bottom:16px}
.art-meta{display:flex;gap:14px;flex-wrap:wrap;font-size:11px;color:#8a8a8a;text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid rgba(255,255,255,.08);padding-bottom:20px;margin-bottom:24px}
.art-meta .live{color:var(--volt)}
.hero-img{width:100%;border-radius:16px;margin-bottom:26px;border:1px solid rgba(255,255,255,.08)}
.art-body p{font-size:15px;line-height:1.85;color:#cfccc3;margin-bottom:18px}
.art-body h2{font-size:clamp(22px,3.4vw,30px);color:var(--cream);margin:36px 0 14px;line-height:1.05}
.tldr{background:rgba(200,255,0,.05);border-left:3px solid var(--volt);border-radius:0 10px 10px 0;padding:14px 18px;margin:0 0 26px}
.tldr .l{display:block;font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--volt);margin-bottom:6px}
.tldr p{font-size:14px;line-height:1.7;color:#d7d4cb;margin:0}
.art-faq{margin:42px 0 6px}
.art-faq h2{font-size:clamp(24px,4vw,34px);color:var(--cream);margin-bottom:16px}
.faq-item{border:1px solid rgba(255,255,255,.08);border-radius:12px;margin-bottom:10px;overflow:hidden;background:rgba(255,255,255,.02)}
.faq-item summary{cursor:pointer;padding:14px 16px;font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:18px;text-transform:uppercase;color:var(--cream);list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:'+';color:var(--volt)}.faq-item[open] summary::after{content:'–'}
.faq-a{padding:0 16px 15px;font-size:13.5px;color:#a5a29a;line-height:1.65}
.rx{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:26px 0 6px;padding:16px 0;border-top:1px solid rgba(255,255,255,.08);border-bottom:1px solid rgba(255,255,255,.08)}
.rx-btn{display:inline-flex;align-items:center;gap:8px;font-family:'DM Mono',monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#b7b4ab;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.12);border-radius:24px;padding:10px 16px;cursor:pointer;transition:.15s}
.rx-btn svg{width:16px;height:16px}
button.rx-btn:hover{border-color:var(--kc);color:var(--cream)}
.rx-like.liked{color:var(--kc);border-color:var(--kc)}
.rx-like.liked svg{fill:var(--kc)}
.rx-views{cursor:default}
.entity-link{display:inline-flex;align-items:center;gap:8px;margin-top:10px;padding:13px 22px;background:var(--kc);color:#04040a;font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:900;font-size:16px;letter-spacing:1px;text-transform:uppercase;text-decoration:none;border-radius:7px}
.back-link{display:inline-block;margin:34px 0 10px;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--kc);text-decoration:none;border:1px solid var(--kc);padding:11px 20px;border-radius:22px}
footer{background:#04040a;border-top:1px solid rgba(255,45,0,0.1);margin-top:40px}
.fbot{max-width:1320px;margin:0 auto;padding:1.4rem 1.5rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
.fbot a,.fbot span{font-family:'DM Mono',monospace;font-size:.65rem;letter-spacing:.1em;color:rgba(232,228,217,0.25);text-transform:uppercase;text-decoration:none}
</style>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R1B1HL5W61"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-R1B1HL5W61');
</script>
</head>
<body>
<script src="/location-links.js"></script>
<nav class="nav">
  <a href="index.html" class="nav-logo"><div class="ldot"></div><span class="logo-txt">STADTPULS</span></a>
  <div class="nav-links"><a href="gastro.html" class="nav-link">GASTRO</a><a href="kultur.html" class="nav-link">KULTUR</a><a href="nachtleben.html" class="nav-link">NACHTLEBE</a><a href="events.html" class="nav-link">EVENTS</a><a href="shopping.html" class="nav-link">SHOPPING</a><a href="news.html" class="nav-link active">NEWS</a><a href="dating.html" class="nav-link">DATES</a></div>
  <a href="login.html" class="nav-cta">MITMACHE</a>
<button class="sp-nav-burger" onclick="spNavToggle()" aria-label="Menü"><span></span><span></span><span></span></button>
</nav>
<div class="wrap">
  <div class="crumb"><a href="/">Stadtpuls</a> › <a href="news.html">News</a> › <a href="/kreis-__K__/news/">Kreis __K__</a> › <span>__H1__</span></div>
  <article>
    <span class="art-tag">KREIS __K__ · __NAME__ · __KAT__</span>
    <h1 class="art">__H1__</h1>
    <div class="art-meta"><span class="live">● LIVE</span><span>__KAT__</span><span>__AUTOR__</span><span>__DATE__</span></div>
    __TLDR__
    __IMG__
    <div class="art-body">__BODY__</div>
    __FAQ_BLOCK__
    <div class="rx" data-sid="__SID__">
      <button class="rx-btn rx-like" type="button" title="Like — nur iglogged"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-4.5-9.5-9C1 9 2.5 5.5 6 5.5c2 0 3.2 1.2 4 2.3.8-1.1 2-2.3 4-2.3 3.5 0 5 3.5 3.5 6.5C19 16.5 12 21 12 21z"/></svg><span class="rx-likecount">0</span> Likes</button>
      <span class="rx-btn rx-views"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg><span class="rx-viewcount">–</span> Views</span>
      <button class="rx-btn rx-share" type="button" title="Teile"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg> Teile</button>
    </div>
    __LINK__
    <div><a class="back-link" href="/kreis-__K__/news/">← Zrugg zu de News vom Kreis __K__</a></div>
  </article>
</div>
<footer><div class="fbot"><span>© 2026 depuls.ch — by raimondo* — Zürich</span><span><a href="datenschutz.html">Datenschutz</a> · <a href="impressum.html">Impressum</a></span></div></footer>
<script>
(function(){
  var SB='https://pnynkzrqnfoshojqfqxn.supabase.co';
  var KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ';
  var box=document.querySelector('.rx'); if(!box) return;
  var sid=box.getAttribute('data-sid'); if(!sid) return;
  var H={apikey:KEY,'Content-Type':'application/json'};
  function sess(){try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf('-auth-token')>-1){var v=JSON.parse(localStorage.getItem(k))||{};var s=v.currentSession||v;var at=s.access_token;var uid=s.user&&s.user.id;if(at&&uid)return{token:at,uid:uid};}}}catch(e){}return null;}
  var S=sess();
  var likeBtn=box.querySelector('.rx-like'), lc=box.querySelector('.rx-likecount'), vc=box.querySelector('.rx-viewcount');
  if(!localStorage.getItem('sv-'+sid)){fetch(SB+'/rest/v1/rpc/story_add_view',{method:'POST',headers:H,body:JSON.stringify({sid:sid})}).then(function(){localStorage.setItem('sv-'+sid,'1');}).catch(function(){});}
  fetch(SB+'/rest/v1/news_stories?id=eq.'+sid+'&select=views',{headers:H}).then(function(r){return r.json();}).then(function(d){if(d&&d[0]!=null)vc.textContent=d[0].views||0;}).catch(function(){});
  var liked=false;
  function loadLikes(){fetch(SB+'/rest/v1/story_reactions?story_id=eq.'+sid+'&select=user_id',{headers:H}).then(function(r){return r.json();}).then(function(d){if(!Array.isArray(d))return;lc.textContent=d.length;if(S){liked=d.some(function(x){return x.user_id===S.uid;});likeBtn.classList.toggle('liked',liked);}}).catch(function(){});}
  loadLikes();
  likeBtn.addEventListener('click',function(){
    if(!S){location.href='/login.html';return;}
    var ah={apikey:KEY,'Content-Type':'application/json',Authorization:'Bearer '+S.token,Prefer:'return=minimal'};
    if(liked){fetch(SB+'/rest/v1/story_reactions?story_id=eq.'+sid+'&user_id=eq.'+S.uid,{method:'DELETE',headers:ah}).then(loadLikes);}
    else{fetch(SB+'/rest/v1/story_reactions',{method:'POST',headers:ah,body:JSON.stringify({story_id:sid,user_id:S.uid})}).then(loadLikes);}
  });
  box.querySelector('.rx-share').addEventListener('click',function(){
    var u=location.href,t=document.title,b=this;
    if(navigator.share){navigator.share({title:t,url:u}).catch(function(){});}
    else if(navigator.clipboard){navigator.clipboard.writeText(u);var o=b.innerHTML;b.textContent='Link kopiert ✓';setTimeout(function(){b.innerHTML=o;},1800);}
  });
})();
</script>
</body>
</html>"""

def story_page(k, o):
    d=KREISE[k]; name=d["name"]
    titel=o.get("titel") or o.get("title") or "Ohni Titel"
    teaser=o.get("teaser") or ""
    inhalt=o.get("inhalt") or teaser or ""
    kat=o.get("kategorie") or "Quartier"
    autor=o.get("autor") or "@stadtpuls"
    slug=o.get("slug") or slugify(titel)
    img=o.get("bild_url") or ""
    date=iso_date(o)
    canon=f"{SITE}/kreis-{k}/news/{slug}"
    alt=f"{titel} / Stadtpuls Kreis {k} Zürich"
    plain=re.sub(r"\s+"," ",inhalt or teaser or "").strip()
    wordcount=len(plain.split())
    kws=keywords_for(k,kat)
    author_obj={"@type":"Organization","name":autor} if autor.lower().startswith("redakt") else {"@type":"Person","name":autor}
    na={"@context":"https://schema.org","@type":"NewsArticle","headline":titel[:110],"description":(teaser or titel)[:250],"datePublished":date,"dateModified":date,"articleSection":kat,"inLanguage":"gsw-CH","isAccessibleForFree":True,"wordCount":wordcount,"keywords":kws,"articleBody":plain,"author":author_obj,"publisher":{"@type":"Organization","name":"Stadtpuls","url":SITE,"logo":{"@type":"ImageObject","url":SITE+"/favicon.svg"}},"contentLocation":{"@type":"Place","name":f"Kreis {k}, Zürich","address":{"@type":"PostalAddress","addressLocality":"Zürich","addressRegion":"ZH","addressCountry":"CH"}},"speakable":{"@type":"SpeakableSpecification","cssSelector":["h1.art",".tldr"]},"mainEntityOfPage":{"@type":"WebPage","@id":canon},"url":canon}
    if img: na["image"]=[img]
    faq_json=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faq"]]},ensure_ascii=False)
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Stadtpuls","item":SITE},{"@type":"ListItem","position":2,"name":"News","item":SITE+"/news"},{"@type":"ListItem","position":3,"name":f"News Kreis {k} Zürich","item":f"{SITE}/kreis-{k}/news/"},{"@type":"ListItem","position":4,"name":titel,"item":canon}]}
    imgtag=f'<img class="hero-img" src="{esc(img)}" alt="{esc(alt)}" loading="lazy">' if img else ""
    body=render_body(inhalt,teaser)
    tldr=f'<div class="tldr"><span class="l">Kurz &amp; knapp</span><p>{linkify(esc(teaser))}</p></div>' if teaser else ""
    faq_blk=faq_block_html(k)
    ogimg=f'<meta property="og:image" content="{esc(img)}">' if img else ""
    twimg=f'<meta name="twitter:image" content="{esc(img)}">' if img else ""
    link=""
    if o.get("link_label"):
        link=f'<a class="entity-link" href="{esc(o.get("link_url") or "#")}">{esc(o.get("link_label"))} →</a>'
    tok={"__K__":str(k),"__NAME__":esc(name),"__COL__":d["c"],"__TITLE__":esc(f"{titel} | News Kreis {k} Zürich | Stadtpuls"),"__H1__":esc(titel),"__META_DESC__":esc((teaser or titel)[:155]),"__KEYWORDS__":esc(kws),"__CANON__":canon,"__KAT__":esc(kat),"__AUTOR__":esc(autor),"__DATE__":esc(disp_date(o)),"__ISODATE__":esc(date),"__SID__":esc(o.get("id") or ""),"__IMG__":imgtag,"__OGIMG__":ogimg,"__TWIMG__":twimg,"__TLDR__":tldr,"__BODY__":body,"__FAQ_BLOCK__":faq_blk,"__LINK__":link,"__SCHEMA_NA__":json.dumps(na,ensure_ascii=False),"__SCHEMA_BC__":json.dumps(bc,ensure_ascii=False),"__SCHEMA_FAQ__":f'<script type="application/ld+json">{faq_json}</script>'}
    out=STORY_HTML
    for t,v in tok.items(): out=out.replace(t,v)
    return out, slug

def main():
    total=0; storycount=0
    for k in KREISE:
        stories=fetch_stories(k)
        d=f"kreis-{k}/news"
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d,"index.html"),"w",encoding="utf-8") as f:
            f.write(page(k, stories))
        # Detailsyte pro Story
        for o in stories:
            sp_html, slug = story_page(k, o)
            sd=os.path.join(d, slug)
            os.makedirs(sd, exist_ok=True)
            with open(os.path.join(sd,"index.html"),"w",encoding="utf-8") as f:
                f.write(sp_html)
            storycount+=1
        total+=1
        print(f"✅ /kreis-{k}/news/  ({KREISE[k]['name']}) — {len(stories)} Story-Detailsyte")
    print(f"\nFertig: {total} Kreis-Hubs + {storycount} Story-Detailsyte gnereiert.")

if __name__=="__main__":
    main()
