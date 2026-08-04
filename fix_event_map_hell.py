#!/usr/bin/env python3
# ============================================================
# SP_MAP_MATCH v1: Event-Kartenmodul (event-profil.html) auf die
# gleiche helle Google-Maps-Darstellung umstellen wie bei
# gastro-profil.html (statt der dunklen Leaflet/CartoDB-Karte).
# Idempotent: Marker SP_MAP_MATCH v1 verhindert Doppel-Ausfuehrung.
# ============================================================
import re, sys

PFAD = 'event-profil.html'

with open(PFAD, encoding='utf-8') as f:
    src = f.read()

if 'SP_MAP_MATCH v1' in src:
    raise SystemExit('Schon gepatcht — nichts zu tun.')

# 1) Leaflet-CSS-Link im <head> entfernen (nicht mehr gebraucht)
old_link = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'
if src.count(old_link) != 1:
    raise SystemExit(f'FEHLER: Leaflet-CSS-Link {src.count(old_link)}x gefunden (erwartet 1) — Abbruch.')
src = src.replace(old_link, '<!-- SP_MAP_MATCH v1: Leaflet ersetzt durch Google-Maps-Embed (wie gastro-profil.html) -->\n')

# 2) Map-HTML im render() ersetzen: Leaflet-Div -> Google-Maps-iframe (helle Optik)
old_map_html = '''      <div class="section-title">LOCATION</div>
      <div class="map-box" id="map-wrap">
        <div id="map-leaflet"></div>
        <button class="map-cta" onclick="window.open('https://maps.google.com/?q=${encodeURIComponent((ev.adresse||'')+' '+(ev.venue_name||'')+(ev.plz?' '+ev.plz:'')+('+Zürich'))}','_blank')">📍 ROUTE ÖFFNE</button>
      </div>
      <div class="map-addr">${ev.venue_name||''}${ev.adresse?' · '+ev.adresse:''}${ev.plz?' · '+ev.plz:''}</div>'''
if src.count(old_map_html) != 1:
    raise SystemExit(f'FEHLER: Map-HTML-Block {src.count(old_map_html)}x gefunden (erwartet 1) — Abbruch.')
new_map_html = '''      <div class="section-title">LOCATION</div>
      <div class="map-box" id="map-wrap">
        <iframe src="https://www.google.com/maps?q=${encodeURIComponent((ev.adresse||ev.venue_name||'Zürich')+(ev.plz?' '+ev.plz:'')+' Zürich')}&output=embed&z=16&hl=de" width="100%" height="260" style="border:0;display:block;opacity:.85;mix-blend-mode:luminosity" loading="lazy" allowfullscreen></iframe>
        <button class="map-cta" onclick="window.open('https://maps.google.com/?q=${encodeURIComponent((ev.adresse||'')+' '+(ev.venue_name||'')+(ev.plz?' '+ev.plz:'')+('+Zürich'))}','_blank')">📍 ROUTE ÖFFNE</button>
      </div>
      <div class="map-addr">${ev.venue_name||''}${ev.adresse?' · '+ev.adresse:''}${ev.plz?' · '+ev.plz:''}</div>'''
src = src.replace(old_map_html, new_map_html)

# 3) Aufruf von initMap() entfernen (Funktion wird nicht mehr gebraucht)
old_call = '  setTimeout(()=>initMap(ev), 100);\n'
if src.count(old_call) != 1:
    raise SystemExit(f'FEHLER: initMap-Aufruf {src.count(old_call)}x gefunden (erwartet 1) — Abbruch.')
src = src.replace(old_call, '  // SP_MAP_MATCH v1: initMap() nicht mehr noetig (Google-Maps-Embed statt Leaflet)\n')

# 4) Ganze initMap()-Funktion entfernen (von "async function initMap" bis zur Zeile vor "function showErr")
start_marker = 'async function initMap(ev){'
end_marker = 'function showErr(msg){'
start_idx = src.find(start_marker)
end_idx = src.find(end_marker)
if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
    raise SystemExit('FEHLER: initMap()-Funktionsgrenzen nicht gefunden — Abbruch.')
src = src[:start_idx] + src[end_idx:]

with open(PFAD, 'w', encoding='utf-8') as f:
    f.write(src)

print('✓ event-profil.html gepatcht — Karte nutzt jetzt Google-Maps-Embed wie gastro-profil.html.')
