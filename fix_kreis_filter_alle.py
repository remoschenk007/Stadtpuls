#!/usr/bin/env python3
# ============================================================
# SP_KREIS_FIX v1: Kreis-Filter auf allen Kategorie-Seiten reparieren/bauen.
#
# Befund:
#  - kultur.html & shopping.html: haben schon Kreis-Buttons (.kr-btn) UND
#    einen ?kreis=URL-Hook, der beim Laden setKreis(...) aufruft - aber die
#    Funktion setKreis() selbst war NIRGENDS definiert. Nur die fehlende
#    Funktion wird ergaenzt (S.kreis existiert schon in getFiltered()).
#  - gastro.html: gleiches Problem (setKreis fehlt), UND es gibt noch gar
#    keinen ?kreis=URL-Hook. Beides wird ergaenzt (robust per Polling,
#    damit es unabhaengig vom genauen Ladezeitpunkt sicher funktioniert).
#  - events.html: hatte ueberhaupt keinen Kreis-Filter, nur eine
#    dekorative Kreis-Statistik-Leiste (#kreis-strip). Wird zu einem
#    echten klickbaren Filter ausgebaut + ?kreis=URL-Hook.
#  - nachtleben.html: funktioniert bereits korrekt, wird nicht angefasst.
#
# Jede Datei wird EINZELN und UNABHAENGIG gepatcht (eigener Marker) -
# wenn eine Datei schon gepatcht ist, wird sie uebersprungen, der Rest
# laeuft trotzdem durch. Idempotent und sicher mehrfach ausfuehrbar.
# ============================================================
import re, sys

RESULTS = []


def patch_simple(pfad, marker, anchor, insertion, anchor_count=1):
    """Fuegt `insertion` direkt VOR `anchor` ein, wenn `marker` noch nicht vorkommt."""
    try:
        with open(pfad, encoding='utf-8') as f:
            src = f.read()
    except FileNotFoundError:
        RESULTS.append(f'⚠ {pfad}: Datei nicht gefunden — übersprungen.')
        return
    if marker in src:
        RESULTS.append(f'– {pfad}: schon gepatcht, nichts zu tun.')
        return
    if src.count(anchor) != anchor_count:
        RESULTS.append(f'⚠ {pfad}: Anker {src.count(anchor)}x gefunden (erwartet {anchor_count}) — übersprungen, NICHTS geändert.')
        return
    src = src.replace(anchor, insertion + '\n' + anchor, 1)
    with open(pfad, 'w', encoding='utf-8') as f:
        f.write(src)
    RESULTS.append(f'✓ {pfad}: gepatcht.')


# ── 1) kultur.html — nur setKreis() ergaenzen (URL-Hook existiert schon) ──
patch_simple(
    'kultur.html',
    '/* SP_KREIS_FIX v1 */',
    'function getFiltered(){',
    '''/* SP_KREIS_FIX v1: fehlende setKreis()-Funktion ergaenzt (Buttons + URL-Hook gab es schon) */
function setKreis(btn,val){
  S.kreis=val;
  document.querySelectorAll('.kr-btn').forEach(function(b){b.classList.remove('on');});
  if(btn)btn.classList.add('on');
  buildGrid();
}
'''
)

# ── 2) shopping.html — nur setKreis() ergaenzen ──
patch_simple(
    'shopping.html',
    '/* SP_KREIS_FIX v1 */',
    'function getFiltered(){',
    '''/* SP_KREIS_FIX v1: fehlende setKreis()-Funktion ergaenzt (Buttons + URL-Hook gab es schon) */
function setKreis(btn,val){
  S.kreis=val;
  document.querySelectorAll('.kr-btn').forEach(function(b){b.classList.remove('on');});
  if(btn)btn.classList.add('on');
  buildGrid();
}
'''
)

# ── 3) gastro.html — setKreis() ergaenzen + eigener ?kreis=URL-Hook (per Polling) ──
patch_simple(
    'gastro.html',
    '/* SP_KREIS_FIX v1 */',
    'function getFiltered(){',
    '''/* SP_KREIS_FIX v1: fehlende setKreis()-Funktion + ?kreis=URL-Uebernahme ergaenzt */
function setKreis(btn,val){
  S.kreis=val;
  document.querySelectorAll('.kr-btn').forEach(function(b){b.classList.remove('on');});
  if(btn)btn.classList.add('on');
  buildGrid();
}
(function(){
  var _k=parseInt(new URLSearchParams(location.search).get('kreis'),10);
  if(!(_k>=1&&_k<=12))return;
  var tries=0;
  var iv=setInterval(function(){
    tries++;
    if(typeof allLocs!=='undefined'&&allLocs.length>0){
      clearInterval(iv);
      var _btn=[].slice.call(document.querySelectorAll('.kr-btn')).find(function(b){return (b.getAttribute('onclick')||'').indexOf('setKreis(this,'+_k+')')!==-1;});
      setKreis(_btn||null,_k);
    } else if(tries>40){clearInterval(iv);}
  },250);
})();
'''
)

# ── 4) events.html — echten Kreis-Filter bauen (gab es noch gar nicht) ──
try:
    with open('events.html', encoding='utf-8') as f:
        src = f.read()
    if '/* SP_KREIS_FIX v1 */' in src:
        RESULTS.append('– events.html: schon gepatcht, nichts zu tun.')
    else:
        ok = True

        # 4a) bKreis() klickbar machen
        old_bkreis = '''function bKreis(){
  const kreise=[1,2,3,4,5,6,7,8,9,10,11,12];
  const counts=kreise.map(k=>({k,n:A.filter(e=>e.datum_start===td()&&e.kreis===k).length}));
  const max=Math.max(...counts.map(c=>c.n),1);
  const topK=counts.reduce((a,b)=>a.n>=b.n?a:b).k;
  const strip=document.getElementById('kreis-strip');
  strip.innerHTML=counts.map(({k,n})=>{
    const pct=Math.round(n/max*100);
    const isTop=k===topK&&n>0;
    return`<div class="ks-item${isTop?' top':''}">
      <span class="ks-label">K${k}</span>
      <div class="ks-bar"><div class="ks-fill" style="width:${pct}%"></div></div>
      <span class="ks-count">${n||''}</span>
    </div>`;
  }).join('');
}'''
        if src.count(old_bkreis) != 1:
            RESULTS.append(f'⚠ events.html: bKreis()-Block {src.count(old_bkreis)}x gefunden (erwartet 1) — übersprungen, NICHTS geändert.')
            ok = False
        else:
            new_bkreis = '''/* SP_KREIS_FIX v1: Kreis-Leiste ist jetzt ein echter, klickbarer Filter */
function bKreis(){
  const kreise=[1,2,3,4,5,6,7,8,9,10,11,12];
  const counts=kreise.map(k=>({k,n:A.filter(e=>e.datum_start===td()&&e.kreis===k).length}));
  const max=Math.max(...counts.map(c=>c.n),1);
  const topK=counts.reduce((a,b)=>a.n>=b.n?a:b).k;
  const strip=document.getElementById('kreis-strip');
  strip.innerHTML=counts.map(({k,n})=>{
    const pct=Math.round(n/max*100);
    const isTop=k===topK&&n>0;
    const isOn=aK===k;
    return`<div class="ks-item${isTop?' top':''}${isOn?' on':''}" style="cursor:pointer" onclick="setK(${k},this)">
      <span class="ks-label">K${k}</span>
      <div class="ks-bar"><div class="ks-fill" style="width:${pct}%"></div></div>
      <span class="ks-count">${n||''}</span>
    </div>`;
  }).join('');
}
function setK(k,el){
  aK=(aK===k?null:k);
  document.querySelectorAll('.ks-item').forEach(b=>b.classList.remove('on'));
  if(aK&&el)el.classList.add('on');
  render();
}'''
            src = src.replace(old_bkreis, new_bkreis, 1)

        # 4b) aK-Variable deklarieren (neben aD/aF, falls vorhanden - sonst separat)
        if ok:
            marker2 = 'let aK=null;'
            if marker2 not in src:
                # vor "async function load(){" einfuegen, sicherer, immer vorhandener Anker
                anchor2 = 'async function load(){'
                if src.count(anchor2) == 1:
                    src = src.replace(anchor2, 'let aK=null; // SP_KREIS_FIX v1: aktiver Kreis-Filter\n' + anchor2, 1)
                else:
                    RESULTS.append(f'⚠ events.html: Anker fuer aK-Deklaration nicht eindeutig ({src.count(anchor2)}x) — übersprungen, NICHTS geändert.')
                    ok = False

        # 4c) render() um Kreis-Filter erweitern
        if ok:
            old_render_line = "  let evs=A;\n  if(aD)evs=evs.filter(e=>e.datum_start===aD);"
            if src.count(old_render_line) != 1:
                RESULTS.append(f'⚠ events.html: render()-Zeile {src.count(old_render_line)}x gefunden (erwartet 1) — übersprungen, NICHTS geändert.')
                ok = False
            else:
                new_render_line = "  let evs=A;\n  if(aK)evs=evs.filter(e=>e.kreis===aK); // SP_KREIS_FIX v1\n  if(aD)evs=evs.filter(e=>e.datum_start===aD);"
                src = src.replace(old_render_line, new_render_line, 1)

        # 4d) ?kreis= aus URL uebernehmen, direkt nach dem load()-Aufruf-Block
        if ok:
            anchor3 = 'bStats();bTicker();bKreis();buildDateTabs();render();'
            if src.count(anchor3) != 1:
                RESULTS.append(f'⚠ events.html: Lade-Anker {src.count(anchor3)}x gefunden (erwartet 1) — übersprungen, NICHTS geändert.')
                ok = False
            else:
                hook = '''bStats();bTicker();bKreis();buildDateTabs();render();
    // SP_KREIS_FIX v1: ?kreis= aus URL uebernehmen (z.B. vom Kreis-Universum auf der Startseite)
    try{
      const _k=parseInt(new URLSearchParams(location.search).get('kreis'),10);
      if(_k>=1&&_k<=12){
        aK=_k;
        bKreis();
        render();
      }
    }catch(_e){}'''
                src = src.replace(anchor3, hook, 1)

        if ok:
            with open('events.html', 'w', encoding='utf-8') as f:
                f.write(src)
            RESULTS.append('✓ events.html: gepatcht (echter Kreis-Filter + URL-Hook).')
except FileNotFoundError:
    RESULTS.append('⚠ events.html: Datei nicht gefunden — übersprungen.')


print()
for r in RESULTS:
    print(r)
print()
