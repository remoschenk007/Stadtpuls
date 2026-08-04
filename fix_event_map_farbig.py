#!/usr/bin/env python3
# ============================================================
# SP_MAP_MATCH v2: Verblassungs-Effekt (opacity/mix-blend-mode) von
# der Event-Karte entfernen, damit sie voll farbig ist wie bei Gastro
# (dort wirkt der gleiche CSS-Effekt aus Browser-Gruenden nicht,
# bei Events macht er die Karte blass-grau -> also einfach weglassen).
# Idempotent: Marker SP_MAP_MATCH v2 verhindert Doppel-Ausfuehrung.
# ============================================================
PFAD = 'event-profil.html'

with open(PFAD, encoding='utf-8') as f:
    src = f.read()

if 'SP_MAP_MATCH v2' in src:
    raise SystemExit('Schon gepatcht — nichts zu tun.')

old = "style=\"border:0;display:block;opacity:.85;mix-blend-mode:luminosity\""
if src.count(old) != 1:
    raise SystemExit(f'FEHLER: Erwarteter Style-String {src.count(old)}x gefunden (erwartet 1) — Abbruch.')
new = "style=\"border:0;display:block\" data-sp-map-match=\"v2\""
src = src.replace(old, new)

with open(PFAD, 'w', encoding='utf-8') as f:
    f.write(src)

print('✓ event-profil.html gepatcht — Karte ist jetzt voll farbig, kein Verblassungs-Effekt mehr.')
