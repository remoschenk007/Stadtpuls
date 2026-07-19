#!/usr/bin/env python3
# STADTPULS · generate_event_pages.py — SP_PRETTY v1
# Baut fuer jedes kommende Event eine eigene, fertig vorgerenderte Seite:
#   /events/<slug>/index.html   statt   event-profil.html?id=<uuid>
# Liest event-profil.html als Vorlage (Layout/CSS/JS bleiben identisch, nur
# Titel/Beschreibung/Schema werden pro Event eingesetzt).
# Schreibt zusaetzlich event-links.js (Browser) und event-links.json (fuer
# generate_sitemap.py). Alte, nicht mehr aktuelle Event-Ordner werden entfernt.
# Nur Standardbibliothek. Reihenfolge im nightly Job: DIESES Skript zuerst,
# danach generate_sitemap.py.
import json, urllib.request, os, re, shutil, unicodedata, datetime, html as _html

SU = "https://pnynkzrqnfoshojqfqxn.supabase.co"
SK = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ"
TODAY = datetime.date.today().isoformat()
OUT_DIR = "events"
TEMPLATE_FILE = "event-profil.html"

DAYS = ['So','Mo','Di','Mi','Do','Fr','Sa']
MONTHS = ['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez']


def fetch(path):
    req = urllib.request.Request(SU + path, headers={"apikey": SK, "Authorization": "Bearer " + SK})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def slugify(text):
    text = unicodedata.normalize('NFKD', text or '').encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')[:60].strip('-')


def event_slug(ev):
    base = slugify(ev.get('titel') or 'event')
    short = (ev.get('id') or '')[:8]
    return f"{base}-{short}" if base else short


def fmt_date(ev):
    try:
        d = datetime.date.fromisoformat(ev['datum_start'])
        jsday = (d.weekday() + 1) % 7  # 0=So ... 6=Sa, wie JS getDay()
        return f"{DAYS[jsday]}, {d.day}. {MONTHS[d.month-1]} {d.year}"
    except Exception:
        return ev.get('datum_start') or ''


def render_page(template, ev):
    slug = event_slug(ev)
    url_path = f"/events/{slug}/"
    canonical = f"https://depuls.ch{url_path}"
    titel = ev.get('titel') or 'Event'
    titel_esc = _html.escape(titel)
    beschreibung_raw = (ev.get('beschreibung') or '').strip()
    desc_short = beschreibung_raw[:160] if beschreibung_raw else f"{titel} — {fmt_date(ev)} in Zürich. Tickets und Details auf Stadtpuls."
    desc_esc = _html.escape(desc_short)
    bild = ev.get('bild_url') or 'https://depuls.ch/og-events.jpg'
    full_title = f"{titel_esc} — Event Zürich | Stadtpuls"

    out = template

    out = out.replace(
        '<title>Event Zürich | Stadtpuls</title>',
        f'<title>{full_title}</title>', 1)

    out = out.replace(
        '<meta name="description" content="Event in Zürich — Details, Tickets, Karte und Bewertungen auf Stadtpuls.">',
        f'<meta name="description" content="{desc_esc}">\n<link id="canonical" rel="canonical" href="{canonical}">', 1)

    out = out.replace('content="https://depuls.ch/og-events.jpg"', f'content="{bild}"')
    out = out.replace(
        '<meta id="og-title" property="og:title" content="Event Zürich | Stadtpuls">',
        f'<meta id="og-title" property="og:title" content="{titel_esc} | Stadtpuls Zürich">', 1)
    out = out.replace(
        '<meta id="og-desc" property="og:description" content="Event in Zürich auf Stadtpuls.">',
        f'<meta id="og-desc" property="og:description" content="{desc_esc}">', 1)
    out = out.replace(
        '<meta id="og-url" property="og:url" content="https://depuls.ch/event-profil.html">',
        f'<meta id="og-url" property="og:url" content="{canonical}">', 1)
    out = out.replace(
        '<meta id="tw-title" name="twitter:title" content="Event Zürich | Stadtpuls">',
        f'<meta id="tw-title" name="twitter:title" content="{titel_esc} | Stadtpuls">', 1)
    out = out.replace(
        '<meta id="tw-desc" name="twitter:description" content="Event in Zürich auf Stadtpuls.">',
        f'<meta id="tw-desc" name="twitter:description" content="{desc_esc}">', 1)

    schema = {
        "@context": "https://schema.org", "@type": "Event",
        "name": titel, "description": desc_short, "url": canonical,
        "startDate": ev['datum_start'] + (f"T{ev['uhrzeit_start']}" if ev.get('uhrzeit_start') else ''),
        "endDate": ev.get('datum_ende') or ev['datum_start'],
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "inLanguage": "de-CH",
        "isAccessibleForFree": ev.get('eintritt_typ') == 'kostenlos',
        "location": {"@type": "Place", "name": ev.get('venue_name') or 'Zürich',
                     "address": {"@type": "PostalAddress", "streetAddress": ev.get('adresse') or '',
                                 "postalCode": ev.get('plz') or '', "addressLocality": "Zürich", "addressCountry": "CH"}},
        "organizer": {"@type": "Organization", "name": "Stadtpuls", "url": "https://depuls.ch"},
        "image": bild,
        "offers": {"@type": "Offer",
                   "price": "0" if ev.get('eintritt_typ') == 'kostenlos' else "",
                   "priceCurrency": "CHF", "availability": "https://schema.org/InStock",
                   "url": ev.get('ticket_url') or canonical}
    }
    schema_json = json.dumps(schema, ensure_ascii=False).replace('</', '<\\/')
    out = out.replace(
        '</head>',
        f'<script id="event-schema" type="application/ld+json">{schema_json}</script>\n</head>', 1)

    out = out.replace('<body>', f'<body data-event-id="{ev["id"]}">', 1)

    fallback = (
        f'<div class="ssr-fallback" style="max-width:640px;margin:40px auto;padding:0 20px;'
        f'font-family:\'DM Mono\',monospace;color:#e8e4d9">'
        f'<h1 style="font-size:22px;margin-bottom:8px">{titel_esc}</h1>'
        f'<p style="color:#999;font-size:12px;margin-bottom:14px">'
        f'{_html.escape(fmt_date(ev))}'
        f'{(" · " + _html.escape(ev["uhrzeit_start"][:5]) + " Uhr") if ev.get("uhrzeit_start") else ""}'
        f' · {_html.escape(ev.get("venue_name") or "Zürich")}</p>'
        f'<p style="font-size:13px;line-height:1.6">{desc_esc}</p>'
        f'</div>'
    )
    out = out.replace('<div id="page"></div>', f'<div id="page">{fallback}</div>', 1)

    out = out.replace(
        '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>',
        '<script src="/event-links.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>', 1)

    for name in ['index.html', 'gastro.html', 'nachtleben.html', 'events.html', 'shopping.html',
                 'dating.html', 'sp-track.js', 'favicon.svg']:
        out = out.replace(f'href="{name}"', f'href="/{name}"')
        out = out.replace(f'src="{name}"', f'src="/{name}"')

    return out, slug, url_path


def main():
    evs = fetch(
        f"/rest/v1/eventfrog_events?select=id,ef_id,titel,beschreibung,datum_start,datum_ende,"
        f"uhrzeit_start,venue_name,adresse,plz,kreis,eintritt_typ,ticket_url,bild_url,aktiv"
        f"&datum_start=gte.{TODAY}&aktiv=eq.true&order=datum_start.asc&limit=3000"
    )
    template = open(TEMPLATE_FILE, encoding='utf-8').read()

    links = {}
    valid_slugs = set()
    for ev in evs:
        if not ev.get('id') or not ev.get('datum_start'):
            continue
        html_out, slug, url_path = render_page(template, ev)
        valid_slugs.add(slug)
        d = os.path.join(OUT_DIR, slug)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html_out)
        links[ev['id']] = url_path
        if ev.get('ef_id') and ev['ef_id'] != ev['id']:
            links[ev['ef_id']] = url_path

    # veraltete Event-Ordner aufraeumen (Event ist vorbei / nicht mehr aktiv)
    removed = 0
    if os.path.isdir(OUT_DIR):
        for name in os.listdir(OUT_DIR):
            full = os.path.join(OUT_DIR, name)
            if os.path.isdir(full) and name not in valid_slugs:
                shutil.rmtree(full)
                removed += 1

    open('event-links.js', 'w', encoding='utf-8').write('window.SP_EVENT_LINKS=' + json.dumps(links, ensure_ascii=False) + ';')
    open('event-links.json', 'w', encoding='utf-8').write(json.dumps(links, ensure_ascii=False))

    print(f"generate_event_pages.py: {len(valid_slugs)} Seiten geschrieben, {removed} veraltete entfernt, {len(links)} Links-Einträge.")


if __name__ == '__main__':
    main()
