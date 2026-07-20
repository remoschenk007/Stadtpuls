#!/usr/bin/env python3
# STADTPULS · sp_add_kultur_navfooter.py — SP_KULTUR_NAV v1
# Fuegt den "KULTUR"-Link zu Nav, Mobile-Menu und Footer ueberall dort ein, wo
# er noch fehlt. Laeuft ueber ALLI *.html-Dateien im Repo-Root (nicht in
# Unterordnern -- die sind generierte Profil-/Kreis-Seiten und werden eh
# naechtlich neu gebaut).
#
# Sicher zum mehrmals Laufen: jede Regel prueft zuerst, ob "kultur.html"
# scho im entsprechende Abschnitt drin isch -- falls ja, wird nüt dopplet
# yygfuegt. Jede Regel wird EINZELN versucht; wenn ein Muster in ere Date
# nid vorchunt, wird sie eifach übersprunge (kei Fehler).
#
# Nur Standardbibliothek. Nach dem Lauf: `git diff` aaluege, denn commit+push.
import glob, re

REPORT = []

def patch_desktop_nl(s):
    """Desktop-Nav im 'nl'-Dialekt (gastro.html, *-profil.html, ...):
    Fuegt KULTUR gliich nach GASTRO y, egal ob GASTRO grad als <a> oder als
    aktive <span class="nl on"> drinsteit."""
    if (re.search(r'<a[^>]*class="nl[^"]*"[^>]*href="[^"]*kultur\.html"[^>]*>', s)
            or re.search(r'<a[^>]*href="[^"]*kultur\.html"[^>]*class="nl[^"]*"[^>]*>', s)
            or re.search(r'<span class="nl on">KULTUR</span>', s)):
        return s, False
    pat = re.compile(
        r'([ \t]*)(<a class="nl(?: on)?" href="[^"]*gastro\.html">GASTRO</a>|<span class="nl on">GASTRO</span>)'
    )
    m = pat.search(s)
    if not m:
        return s, False
    indent, tag = m.group(1), m.group(2)
    insert = f'\n{indent}<a class="nl" href="/kultur.html">KULTUR</a>'
    s2 = s[:m.end()] + insert + s[m.end():]
    return s2, True


def patch_mobile_menu(s):
    """Mobiles Burger-Menu (sp-menu-inner): Fuegt KULTUR gliich nach Gastro y."""
    if re.search(r'<a[^>]*href="[^"]*kultur\.html"[^>]*class="sp-menu-link[^"]*"[^>]*>|<a[^>]*class="sp-menu-link[^"]*"[^>]*href="[^"]*kultur\.html"[^>]*>', s):
        return s, False
    pat = re.compile(
        r'([ \t]*)(<a href="[^"]*gastro\.html" class="sp-menu-link(?: active)?">Gastro</a>)'
    )
    m = pat.search(s)
    if not m:
        return s, False
    indent = m.group(1)
    insert = f'\n{indent}<a href="/kultur.html" class="sp-menu-link">Kultur</a>'
    s2 = s[:m.end()] + insert + s[m.end():]
    return s2, True


def patch_index_navlink(s):
    """Startsite-Nav (index.html, 'nav-link'-Dialekt, href zuerst dann class)."""
    if (re.search(r'<a[^>]*href="[^"]*kultur\.html"[^>]*class="nav-link"[^>]*>', s)
            or re.search(r'<a[^>]*class="nav-link"[^>]*href="[^"]*kultur\.html"[^>]*>', s)):
        return s, False
    pat = re.compile(r'([ \t]*)(<a href="[^"]*gastro\.html" class="nav-link">GASTRO</a>)')
    m = pat.search(s)
    if not m:
        return s, False
    indent = m.group(1)
    insert = f'\n{indent}<a href="/kultur.html" class="nav-link">KULTUR</a>'
    s2 = s[:m.end()] + insert + s[m.end():]
    return s2, True


def patch_footer_new(s):
    """Neue Footer-Struktur (fg/fc/h5/ul/li) -- Entdecken-Liste, endet mit Mobilitaet."""
    if re.search(r'<li><a href="[^"]*kultur\.html">Kultur</a></li>', s):
        return s, False
    pat = re.compile(r'([ \t]*)(<li><a href="[^"]*mobilitaet\.html">Mobilit\xe4t</a></li>)')
    m = pat.search(s)
    if not m:
        return s, False
    indent = m.group(1)
    insert = f'\n{indent}<li><a href="/kultur.html">Kultur</a></li>'
    s2 = s[:m.end()] + insert + s[m.end():]
    return s2, True


def patch_footer_old(s):
    """Alte Footer-Struktur (fc-title/fc-link inline) -- Entdecken-Zeile."""
    if (re.search(r'<a[^>]*class="fc-link"[^>]*href="[^"]*kultur\.html"[^>]*>', s)
            or re.search(r'<a[^>]*href="[^"]*kultur\.html"[^>]*class="fc-link"[^>]*>', s)):
        return s, False
    pat = re.compile(r'(<a class="fc-link" href="[^"]*gastro\.html">Gastro(?: (?:&amp;|&) Bars)?</a>)')
    m = pat.search(s)
    if not m:
        return s, False
    insert = '<a class="fc-link" href="/kultur.html">Kultur</a>'
    s2 = s[:m.end()] + insert + s[m.end():]
    return s2, True


PATCHES = [
    ('desktop-nl-nav', patch_desktop_nl),
    ('mobile-burger-menu', patch_mobile_menu),
    ('index-nav-link', patch_index_navlink),
    ('footer-neu (fg/fc/ul)', patch_footer_new),
    ('footer-alt (fc-link)', patch_footer_old),
]


def main():
    files = sorted(glob.glob('*.html'))
    total_changed = 0
    for fn in files:
        try:
            s = open(fn, encoding='utf-8').read()
        except Exception as e:
            print(f"SKIP {fn}: kann nid gläse werde ({e})")
            continue
        orig = s
        applied = []
        for name, fn_patch in PATCHES:
            s, changed = fn_patch(s)
            if changed:
                applied.append(name)
        if s != orig:
            open(fn, 'w', encoding='utf-8').write(s)
            total_changed += 1
            print(f"OK {fn}: {', '.join(applied)}")
        else:
            print(f"-- {fn}: nüt gfunde zum patche (kei Match oder scho vorhande)")
    print(f"\nFERTIG: {total_changed} vo {len(files)} Date agepasst.")


if __name__ == '__main__':
    main()
