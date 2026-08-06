#!/usr/bin/env python3
# STADTPULS · generate_location_pages.py — SP_PRETTY_LOC v1
# Baut fuer jedes aktive Gastro- und Shopping-Lokal eine eigene, fertig
# vorgerenderte Seite:  /gastro/<slug>/index.html  bzw.  /shopping/<slug>/
# statt gastro-profil.html?id=<uuid> / shopping-profil.html?id=<uuid>.
# Liest gastro-profil.html / shopping-profil.html als Vorlage.
# Schreibt location-links.js (Browser) und location-links.json (fuer
# generate_kreis_pages.py + generate_sitemap.py). Nachtleben bleibt
# unangetastet (nutzt schon ?slug= statt ?id=).
# Reihenfolge im nightly Job: dieses Skript VOR generate_kreis_pages.py
# und VOR generate_sitemap.py.
import json, urllib.request, os, re, shutil, unicodedata, html as _html

SU = "https://pnynkzrqnfoshojqfqxn.supabase.co"
SK = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ"

CATEGORIES = {
    'gastro': dict(
        template_file='gastro-profil.html', out_dir='gastro', schema_type='Restaurant',
        og_title='Lokal-Profil — Gastro Zürich | Stadtpuls',
        og_desc='Restaurant-, Café- und Bar-Profile aus Zürich: Öffnungszeiten, Kreis, Bewertungen — handkuratiert auf Stadtpuls.',
        og_url_old='https://depuls.ch/gastro-profil.html',
        title_suffix=' | Stadtpuls Zürich',
    ),
    'shopping': dict(
        template_file='shopping-profil.html', out_dir='shopping', schema_type='Store',
        og_title='Laden-Profil — Shopping Zürich | Stadtpuls',
        og_desc='Laden-Profile aus Zürich: Öffnungszeiten, Kreis und Charakter — handkuratiert auf Stadtpuls.',
        og_url_old='https://depuls.ch/shopping-profil.html',
        title_suffix=' | Stadtpuls Zürich',
    ),
    'nachtleben': dict(
        template_file='nachtleben-profil.html', out_dir='nachtleben', schema_type='NightClub',
        og_title='Club & Bar Profil — Nachtleben Zürich | Stadtpuls',
        og_desc='Club- und Bar-Profile aus Zürich: Öffnungszeiten, Events und Vibe — der ehrliche Nightlife-Guide.',
        og_url_old='https://depuls.ch/nachtleben-profil.html',
        title_suffix=' | Stadtpuls Zürich',
    ),
    'kultur': dict(
        template_file='kultur-profil.html', out_dir='kultur', schema_type='TouristAttraction',
        og_title='Kultur-Ort Profil — Kultur Zürich | Stadtpuls',
        og_desc='Museen, Galerien, Theater, Oper, Film und Musik in Zürich: handkuratiert auf Stadtpuls.',
        og_url_old='https://depuls.ch/kultur-profil.html',
        title_suffix=' | Stadtpuls Zürich',
    ),
}

ROOTIFY = ['index.html', 'gastro.html', 'nachtleben.html', 'events.html', 'shopping.html', 'kultur.html',
           'dating.html', 'community.html', 'datenschutz.html', 'gps.html', 'marktplatz.html',
           'impressum.html', 'jobs.html', 'kontakt.html', 'login.html', 'mobilitaet.html',
           'musik.html', 'news.html', 'partners.html', 'platzierung.html', 'quartiere.html',
           'sp-track.js', 'favicon.svg']

# SP_KULTUR v1 -- selbi Klassifizierig wie in kultur.html/kultur-profil.html (JS
# KULTUR_DEFS), hier fuer den statischen SEO/Crawler-Schema-Typ pro einzelnem Ort.
KULTUR_SCHEMA_DEFS = [
    ('museum',  'Museum',                    ['museum', 'sammlung', 'ausstellungshaus', 'kunsthaus']),
    ('galerie', 'ArtGallery',                ['galerie', 'kunstraum', 'artspace', 'atelier', 'skulptur']),
    ('theater', 'PerformingArtsTheater',     ['theater', 'bühne', 'schauspiel', 'kabarett']),
    ('buehne',  'PerformingArtsTheater',     ['oper', 'ballett', 'tanzhaus', 'tanz', 'philharmonie', 'orchester']),
    ('film',    'MovieTheater',              ['kino', 'film', 'lichtspiel']),
    ('musik',   'MusicVenue',                ['konzert', 'musiksaal', 'tonhalle', 'jazz', 'livemusik']),
]


def kultur_schema_type(loc):
    sk = (loc.get('subkategorie') or '').lower()
    for sub_id, schema, words in KULTUR_SCHEMA_DEFS:
        if sk == sub_id:
            return schema
    text = ((loc.get('name') or '') + ' ' + (loc.get('beschreibung') or '') + ' ' + (loc.get('beschreibung_kurz') or '')).lower()
    for sub_id, schema, words in KULTUR_SCHEMA_DEFS:
        if any(w in text for w in words):
            return schema
    return 'TouristAttraction'


def fetch(path):
    req = urllib.request.Request(SU + path, headers={"apikey": SK, "Authorization": "Bearer " + SK})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def slugify(text):
    text = unicodedata.normalize('NFKD', text or '').encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')[:60].strip('-')
    if re.match(r'^kreis-\d+$', text) or not text:
        text = 'lokal-' + text if text else 'lokal'
    return text


def loc_slug(loc, cat_key=None):
    # Nachtleben hat schon eindeutige, handgepflegte Slugs im Umlauf (?slug=...)
    # -- die wiederverwenden statt neu zu erfinden, damit nichts bricht.
    if cat_key == 'nachtleben' and loc.get('slug'):
        s = slugify(loc['slug'])
        if s:
            return s
    base = slugify(loc.get('name') or 'lokal')
    short = (loc.get('id') or '')[:8]
    return f"{base}-{short}" if base else short


def render_page(template, loc, cat_key, cfg):
    slug = loc_slug(loc, cat_key)
    url_path = f"/{cfg['out_dir']}/{slug}/"
    canonical = f"https://depuls.ch{url_path}"
    name = loc.get('name') or 'Lokal'
    name_esc = _html.escape(name)
    kreis = loc.get('kreis') or '?'
    sub_defaults = {'gastro': 'Restaurant', 'shopping': 'Laden', 'nachtleben': 'Club', 'kultur': 'Kultur-Ort'}
    sub = loc.get('subkategorie') or sub_defaults.get(cat_key, 'Lokal')
    sub_esc = _html.escape(sub)
    title = f"{name_esc} — {sub_esc} Kreis {kreis}{cfg['title_suffix']}"
    beschreibung_raw = (loc.get('beschreibung_kurz') or loc.get('beschreibung') or '').strip()
    desc_short = beschreibung_raw[:160] if beschreibung_raw else f"{name} — {sub} in Zürich, Kreis {kreis}. Details auf Stadtpuls."
    desc_esc = _html.escape(desc_short)
    bild = loc.get('bild_url') or 'https://depuls.ch/og-image.png'
    adresse = loc.get('adresse') or ''
    adresse_esc = _html.escape(adresse)

    out = template

    # <title id="page-title">
    out = re.sub(
        r'<title id="page-title">[^<]*</title>',
        f'<title id="page-title">{title}</title>', out, count=1)

    # meta description id="page-desc"
    out = re.sub(
        r'<meta name="description" id="page-desc" content="[^"]*">',
        f'<meta name="description" id="page-desc" content="{desc_esc}">', out, count=1)

    # canonical id="page-canonical"
    out = re.sub(
        r'<link rel="canonical" id="page-canonical" href="[^"]*">',
        f'<link rel="canonical" id="page-canonical" href="{canonical}">', out, count=1)

    # OG/Twitter (per-Kategorie Platzhalter -> echte Werte)
    out = out.replace(f'<meta id="og-title" property="og:title" content="{cfg["og_title"]}">',
                       f'<meta id="og-title" property="og:title" content="{title}">', 1)
    out = out.replace(f'<meta id="og-desc" property="og:description" content="{cfg["og_desc"]}">',
                       f'<meta id="og-desc" property="og:description" content="{desc_esc}">', 1)
    out = out.replace(f'<meta id="og-url" property="og:url" content="{cfg["og_url_old"]}">',
                       f'<meta id="og-url" property="og:url" content="{canonical}">', 1)
    out = out.replace(f'<meta id="tw-title" name="twitter:title" content="{cfg["og_title"]}">',
                       f'<meta id="tw-title" name="twitter:title" content="{title}">', 1)
    out = out.replace('content="https://depuls.ch/og-image.png">', f'content="{bild}">')

    # JSON-LD id="schema-ld" (leeres <script> in der Vorlage -> befuellt)
    schema_type = kultur_schema_type(loc) if cat_key == 'kultur' else cfg['schema_type']
    schema = {
        "@context": "https://schema.org", "@type": schema_type,
        "name": name, "description": desc_short, "url": canonical,
        "address": {"@type": "PostalAddress", "streetAddress": adresse,
                     "postalCode": loc.get('plz') or '', "addressLocality": "Zürich", "addressCountry": "CH"},
        "telephone": loc.get('telefon') or '', "image": bild,
    }
    if cat_key == 'gastro':
        schema["servesCuisine"] = sub
        schema["priceRange"] = "CHF"
    schema_json = json.dumps(schema, ensure_ascii=False).replace('</', '<\\/')
    out = re.sub(
        r'<script type="application/ld\+json" id="schema-ld"></script>',
        f'<script type="application/ld+json" id="schema-ld">{schema_json}</script>', out, count=1)

    # <body> -> data-location-id
    out = out.replace('<body>', f'<body data-location-id="{loc["id"]}">', 1)

    # statischer Fallback-Inhalt fuers SEO/Social-Crawling (wird von JS ueberschrieben,
    # sobald geladen -- exakt dieselben Werte, also fuer echte Besucher unsichtbar).
    if cat_key == 'nachtleben':
        # Nachtleben-Template hat keinen #main-content-Block, sondern feste IDs
        # (hero-name/hero-addr/desc-box), die die JS load()-Funktion per
        # textContent/innerHTML befuellt -- hier dieselben Werte vorab reinschreiben.
        repls_nl = [
            ('<div class="hero-name" id="hero-name">LADED...</div>',
             f'<div class="hero-name" id="hero-name">{name_esc}</div>'),
            ('<div class="hero-addr" id="hero-addr">\n      <span class="hero-addr-dot"></span>\n      <span>ZÜRICH</span>\n    </div>',
             f'<div class="hero-addr" id="hero-addr"><span class="hero-addr-dot"></span><span>{adresse_esc or "Zürich"}</span><span class="hero-addr-dot"></span><span>KREIS {kreis}</span></div>'),
            ('<div class="desc-box" id="desc-box">Informationen werden geladen...</div>',
             f'<div class="desc-box" id="desc-box">{desc_esc}</div>'),
        ]
        for old_s, new_s in repls_nl:
            if out.count(old_s) != 1:
                raise RuntimeError(f"SSR-Platzhalter nicht eindeutig gefunden ({out.count(old_s)}x): {old_s[:60]!r} fuer {loc.get('id')}")
            out = out.replace(old_s, new_s, 1)
    else:
        fallback = (
            f'<div class="ssr-fallback" style="max-width:640px;margin:30px auto;padding:0 20px;'
            f'font-family:\'DM Mono\',monospace;color:#e8e4d9">'
            f'<h1 style="font-size:22px;margin-bottom:8px">{name_esc}</h1>'
            f'<p style="color:#999;font-size:12px;margin-bottom:14px">'
            f'{sub_esc} · Kreis {kreis}{(" · " + adresse_esc) if adresse else ""}</p>'
            f'<p style="font-size:13px;line-height:1.6">{desc_esc}</p>'
            f'</div>'
        )
        loading_block = (
            '<div id="main-content">\n'
            '  <div class="loading-wrap">\n'
            '    <div class="loading-dots"><div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div></div>\n'
            '    <div class="loading-txt">LÄDT PROFIL...</div>\n'
            '  </div>\n'
            '</div>'
        )
        if out.count(loading_block) != 1:
            raise RuntimeError(f"main-content Platzhalter nicht eindeutig gefunden ({out.count(loading_block)}x) fuer {loc.get('id')}")
        out = out.replace(loading_block, f'<div id="main-content">{fallback}</div>', 1)

    # location-links.js einbinden -- schon im Vorlagen-Patch als <script src=...> vor SU/SK
    # eingefuegt; hier nichts weiter zu tun.

    for name_f in ROOTIFY:
        out = out.replace(f'href="{name_f}"', f'href="/{name_f}"')
        out = out.replace(f'src="{name_f}"', f'src="/{name_f}"')

    return out, slug, url_path


def main():
    links = {}
    for cat_key, cfg in CATEGORIES.items():
        locs = fetch(
            f"/rest/v1/locations?select=*&kategorie=eq.{cat_key}&aktiv=eq.true&limit=3000"
        )
        template = open(cfg['template_file'], encoding='utf-8').read()

        valid_slugs = set()
        for loc in locs:
            if not loc.get('id') or not loc.get('name'):
                continue
            html_out, slug, url_path = render_page(template, loc, cat_key, cfg)
            valid_slugs.add(slug)
            d = os.path.join(cfg['out_dir'], slug)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html_out)
            links[loc['id']] = url_path

        # veraltete Lokal-Ordner aufraeumen -- Kreis-Landingpages (kreis-N) NIE anfassen,
        # die gehoeren generate_kreis_pages.py
        removed = 0
        if os.path.isdir(cfg['out_dir']):
            for name in os.listdir(cfg['out_dir']):
                full = os.path.join(cfg['out_dir'], name)
                if not os.path.isdir(full):
                    continue
                if re.match(r'^kreis-\d+$', name):
                    continue
                if name not in valid_slugs:
                    shutil.rmtree(full)
                    removed += 1
        print(f"generate_location_pages.py [{cat_key}]: {len(valid_slugs)} Seiten geschrieben, {removed} veraltete entfernt.")

    open('location-links.js', 'w', encoding='utf-8').write(
        'window.SP_LOCATION_LINKS=' + json.dumps(links, ensure_ascii=False) + ';')
    open('location-links.json', 'w', encoding='utf-8').write(json.dumps(links, ensure_ascii=False))
    print(f"generate_location_pages.py: {len(links)} Links insgesamt (location-links.js/json).")


if __name__ == '__main__':
    main()
