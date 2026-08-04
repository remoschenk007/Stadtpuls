#!/usr/bin/env python3
# ============================================================
# SP_KU_CTA_KREIS v1: Der "ALLI X AASCHAUE"-Button im Kreis-Universum
# (auf der Startseite) verlinkt bisher OHNE Kreis-Parameter auf die
# Kategorie-Seite. Jetzt, wo gastro/kultur/shopping/events echte
# ?kreis=-Filter unterstuetzen (siehe SP_KREIS_FIX v1), soll der Button
# den aktuell gewaehlten Kreis mitgeben.
# Idempotent: Marker SP_KU_CTA_KREIS verhindert Doppel-Ausfuehrung.
# ============================================================
PFAD = 'index.html'

with open(PFAD, encoding='utf-8') as f:
    src = f.read()

if 'SP_KU_CTA_KREIS' in src:
    raise SystemExit('Schon gepatcht — nichts zu tun.')

old = "cta.onclick=function(){location.href=CATPAGE[cat.key]||'index.html';};"
if src.count(old) != 1:
    raise SystemExit(f'FEHLER: erwarteter Code {src.count(old)}x gefunden (erwartet 1) — Abbruch.')
new = "cta.onclick=function(){location.href=(CATPAGE[cat.key]||'index.html')+'?kreis='+st.kreis;}; // SP_KU_CTA_KREIS v1"
src = src.replace(old, new)

with open(PFAD, 'w', encoding='utf-8') as f:
    f.write(src)

print('✓ index.html gepatcht — Button gibt jetzt den gewaehlten Kreis an die Zielseite weiter.')
