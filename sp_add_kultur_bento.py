#!/usr/bin/env python3
# STADTPULS · sp_add_kultur_bento.py — SP_KULTUR_BENTO v1
# Fuegt e KULTUR-Kachle i s grossi Bild-Kachle-Gitter uf de Startsite
# (index.html, Sektion "DIS ZÜRI, DIS TEMPO") y, gliich nach Gastro --
# plus e echti Live-Zahl (cnt-kultur) wie bi de andere Kachle.
#
# Sicher zum mehrmals laufe: wenn "kultur.html" scho im Bento-Gitter
# drin isch, wird nüt gmacht.
#
# Nur Standardbibliothek. Nach em Lauf: `git diff index.html` aaluege.
import re

FN = 'index.html'
s = open(FN, encoding='utf-8').read()

if 'class="bt" data-sp-kultur-bento' in s or re.search(r'<a href="[^"]*kultur\.html" class="bt"', s):
    print(f"-- {FN}: KULTUR-Kachle scho im Bento-Gitter drin, nüt gmacht.")
    raise SystemExit(0)

# 1) Neui Kachle gliich nach de Gastro-Kachle yfüege (vor Nachtlebe)
anchor = re.compile(
    r'(<a href="gastro\.html" class="bt big">.*?</a>\s*)(<a href="nachtleben\.html" class="bt">)',
    re.S
)
kultur_tile = (
    '<a href="kultur.html" class="bt" data-sp-kultur-bento="1">\n'
    '        <div class="bt-bg" style="background-image:url(\'https://images.unsplash.com/photo-1554907984-15263bfd63bd?w=600&q=80\')"></div>\n'
    '        <div class="bt-over"></div>\n'
    '        <div class="bt-c"><span class="bt-ico">\U0001F3AD</span><div class="bt-name">Kultur</div><div class="bt-n"><span class="n" id="cnt-kultur">–</span> Museen, Theater & Musig</div></div>\n'
    '      </a>\n      '
)

m = anchor.search(s)
if not m:
    print(f"!! {FN}: Gastro/Nachtlebe-Kachle nid gfunde -- Bento-Gitter hät sich vermutlich gändered. Nüt gmacht, bitte mir Bescheid sage.")
    raise SystemExit(1)

s = s[:m.end(1)] + kultur_tile + s[m.end(1):]

# 2) Live-Zahl: sbCount fuer Kultur i s Promise.all ergänze
old_promise = "sbCount('locations?kategorie=eq.shopping&aktiv=eq.true')\n  ]);"
new_promise = "sbCount('locations?kategorie=eq.shopping&aktiv=eq.true'),\n    sbCount('locations?kategorie=eq.kultur&aktiv=eq.true')\n  ]);"
if old_promise not in s:
    print(f"!! {FN}: Promise.all-Block fuer d Live-Zahle nid gfunde -- Kachle isch gsetzt, aber d Zahl bliibt eventuell bi '–'. Bitte mir Bescheid sage.")
else:
    s = s.replace(old_promise, new_promise, 1)
    old_destr = "const [gastroCount, nachtlebenCount, eventsTotal, shoppingCount] = await Promise.all(["
    new_destr = "const [gastroCount, nachtlebenCount, eventsTotal, shoppingCount, kulturCount] = await Promise.all(["
    if old_destr in s:
        s = s.replace(old_destr, new_destr, 1)
    old_set = "document.getElementById('cnt-shopping').textContent=shoppingCount||'–';"
    new_set = old_set + "\n  document.getElementById('cnt-kultur').textContent=kulturCount||'–';"
    if old_set in s:
        s = s.replace(old_set, new_set, 1)

open(FN, 'w', encoding='utf-8').write(s)
print(f"OK {FN}: KULTUR-Kachle im Bento-Gitter yfüegt (gliich nach Gastro) + Live-Zahl verdrahtet.")
