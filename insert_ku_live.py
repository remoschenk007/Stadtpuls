#!/usr/bin/env python3
# ============================================================
# SP_KU_LIVE v1: Kreis-Universum wirklich zum Leben erwecken.
#
# Die HTML/CSS fuer die Blasen-Galaxie (#kuGalaxy, .ku-bub, .ku-chip,
# #kuSheet usw.) existiert schon vollstaendig in index.html - aber es
# gab NIRGENDS JavaScript, das sie befuellt (mehrfach geprueft: weder
# in index.html noch in location-links.js). Die Blasen waren also
# leer/tot. Dieses Skript fuegt das fehlende JS ein:
#  - Kreis-Umschalter (1-12) in #kuChips
#  - Live-Blasen fuer Gastro/Nachtlebe/Kultur/Shopping/Events mit
#    echten Zahlen pro Kreis aus Supabase
#  - Klick auf Blase -> Sheet mit echten Top-Treffern + Link zur Seite
#  - Suchleiste (#kuq/#kuGo) durchsucht ALLE Kategorien nach
#    Stichwort + Kreis (z.B. "Sushi im Kreis 4")
#
# Idempotent: Marker SP_KU_LIVE v1 verhindert Doppel-Ausfuehrung.
# ============================================================
PFAD = 'index.html'

with open(PFAD, encoding='utf-8') as f:
    src = f.read()

if 'SP_KU_LIVE v1' in src:
    raise SystemExit('Schon eingebaut — nichts zu tun.')

marker = '<div class="ku-toast" id="kuToast"></div>'
if src.count(marker) != 1:
    raise SystemExit(f'FEHLER: Marker {src.count(marker)}x gefunden (erwartet 1) — Abbruch.')

script = r'''
<!-- SP_KU_LIVE v1: Kreis-Universum mit echten Daten + Suche -->
<script>
(function(){
  var SU='https://pnynkzrqnfoshojqfqxn.supabase.co';
  var SK='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ';
  var KREISE=[[1,'ALTSTADT'],[2,'ENGE'],[3,'WIEDIKON'],[4,'LANGSTRASSE'],[5,'INDUSTRIE'],[6,'UNTERSTRASS'],[7,'FLUNTERN'],[8,'SEEFELD'],[9,'ALTSTETTE'],[10,'HÖNGG'],[11,'OERLIKON'],[12,'SCHWAMENDINGE']];
  var CATS=[
    {key:'gastro',label:'GASTRO',unit:'Lokal',ico:'🍴',c:'#ff2d00',pos:[50,12],table:'locations',flt:'kategorie=eq.gastro',nf:function(r){return r.name;},prof:function(r){return 'gastro-profil.html?id='+r.id;}},
    {key:'nachtleben',label:'NACHTLEBE',unit:'Club',ico:'🎵',c:'#9333ea',pos:[82,34],table:'locations',flt:'kategorie=eq.nachtleben',nf:function(r){return r.name;},prof:function(r){return (window.SP_LOCATION_LINKS&&window.SP_LOCATION_LINKS[r.id])||('nachtleben-profil.html?slug='+encodeURIComponent(r.slug||r.id));}},
    {key:'kultur',label:'KULTUR',unit:'Ort',ico:'🎭',c:'#00f5ff',pos:[18,34],table:'locations',flt:'kategorie=eq.kultur',nf:function(r){return r.name;},prof:function(r){return 'kultur-profil.html?id='+r.id;}},
    {key:'shopping',label:'SHOPPING',unit:'Shop',ico:'🛍️',c:'#c8ff00',pos:[80,72],table:'locations',flt:'kategorie=eq.shopping',nf:function(r){return r.name;},prof:function(r){return 'shopping-profil.html?id='+r.id;}},
    {key:'events',label:'EVENTS',unit:'Event',ico:'🎉',c:'#ec4899',pos:[50,90],table:'eventfrog_events',flt:'aktiv=eq.true',nf:function(r){return r.titel;},prof:function(r){return 'event-profil.html?id='+(r.ef_id||r.id);}}
  ];
  var CATPAGE={gastro:'gastro.html',nachtleben:'nachtleben.html',kultur:'kultur.html',shopping:'shopping.html',events:'events.html'};
  var st={kreis:1,counts:{}};

  function h(s){return String(s==null?'':s).replace(/[<>&]/g,function(c){return{'<':'&lt;','>':'&gt;','&':'&amp;'}[c];});}

  async function kuFetch(url){
    var r=await fetch(url,{headers:{apikey:SK,Authorization:'Bearer '+SK,Prefer:'count=exact'}});
    var range=r.headers.get('content-range');
    var total=range?parseInt(range.split('/')[1]):null;
    var data=await r.json();
    return {data:data,total:total};
  }

  async function kuCount(cat,kreis){
    try{
      var url=SU+'/rest/v1/'+cat.table+'?'+cat.flt+'&kreis=eq.'+kreis+'&select=id&limit=1';
      var res=await kuFetch(url);
      return res.total||0;
    }catch(e){return 0;}
  }

  function renderChips(){
    var wrap=document.getElementById('kuChips');
    if(!wrap)return;
    wrap.innerHTML=KREISE.map(function(k){
      return '<div class="ku-chip'+(k[0]===st.kreis?' on':'')+'" data-k="'+k[0]+'"><span class="kn">'+k[0]+'</span><small>'+k[1]+'</small></div>';
    }).join('');
    Array.prototype.forEach.call(wrap.querySelectorAll('.ku-chip'),function(el){
      el.onclick=function(){selectKreis(parseInt(el.getAttribute('data-k'),10));};
    });
  }

  function kreisName(n){var k=KREISE.find(function(x){return x[0]===n;});return k?k[1]:'ZÜRICH';}

  async function selectKreis(n){
    st.kreis=n;
    renderChips();
    var starK=document.getElementById('kuStarK'),starNm=document.getElementById('kuStarNm'),starAct=document.getElementById('kuStarAct');
    if(starK)starK.textContent=n;
    if(starNm)starNm.textContent=kreisName(n);
    if(starAct)starAct.textContent='LÄDT …';
    var counts=await Promise.all(CATS.map(function(c){return kuCount(c,n);}));
    var total=0;
    CATS.forEach(function(c,i){st.counts[c.key]=counts[i];total+=counts[i];});
    if(starAct)starAct.textContent=total+' ORT';
    renderBubbles();
  }

  function renderBubbles(){
    var gal=document.getElementById('kuGalaxy');
    if(!gal)return;
    Array.prototype.forEach.call(gal.querySelectorAll('.ku-bub'),function(b){b.remove();});
    var maxCount=Math.max.apply(null,CATS.map(function(c){return st.counts[c.key]||0;}));
    CATS.forEach(function(cat,i){
      var count=st.counts[cat.key]||0;
      var w=Math.max(66,Math.min(150,66+Math.sqrt(count)*9));
      var x=cat.pos[0],y=cat.pos[1];
      var isHot=count>0&&count===maxCount;
      var div=document.createElement('div');
      div.className='ku-bub';
      div.setAttribute('data-cat',cat.key);
      div.style.cssText='left:'+x+'%;top:'+y+'%;width:'+w+'px;height:'+w+'px;margin-left:-'+(w/2)+'px;margin-top:-'+(w/2)+'px;--c:'+cat.c;
      div.innerHTML=
        '<div class="ku-gl" style="--fd:'+(7+i)+'s;--dl:'+(i*0.35)+'s">'+
          '<div class="ku-shell"></div><div class="ku-rim"></div>'+
          '<div class="ku-col" style="background:'+cat.c+'"></div>'+
          '<div class="ku-shine"></div><div class="ku-shine2"></div>'+
        '</div>'+
        '<div class="ku-orbit" style="--c:'+cat.c+';--od:'+(9+i)+'s"><div class="ku-odot"></div></div>'+
        (isHot?'<div class="ku-badge">TOP</div>':'')+
        '<div class="ku-cont" style="color:'+cat.c+'">'+
          '<span class="ku-ico">'+cat.ico+'</span>'+
          '<span class="ku-bn">'+cat.label+'</span>'+
          '<span class="ku-bm">'+count+' '+cat.unit+'</span>'+
        '</div>';
      if(isHot)div.className+=' hot';
      div.onclick=function(){openCatSheet(cat);};
      gal.appendChild(div);
      setTimeout(function(){div.classList.add('show');},40+i*70);
    });
  }

  function closeSheet(){
    var sheet=document.getElementById('kuSheet'),bk=document.getElementById('kuBk');
    if(sheet)sheet.classList.remove('on');
    if(bk)bk.classList.remove('on');
  }

  function openSheetShell(ico,iconBg,title,sub){
    var kuIco=document.getElementById('kuIco'),kuTitle=document.getElementById('kuTitle'),kuSub=document.getElementById('kuSub');
    if(kuIco){kuIco.textContent=ico;kuIco.style.background=iconBg;}
    if(kuTitle)kuTitle.textContent=title;
    if(kuSub)kuSub.textContent=sub;
    var sheet=document.getElementById('kuSheet'),bk=document.getElementById('kuBk');
    if(sheet)sheet.classList.add('on');
    if(bk)bk.classList.add('on');
  }

  function renderRows(items,cat){
    var rows=document.getElementById('kuRows');
    if(!rows)return;
    if(!items.length){
      rows.innerHTML='<div style="padding:16px 0;text-align:center;font-size:11px;color:rgba(232,228,217,.3)">Kei Treffer gfunde.</div>';
      return;
    }
    rows.innerHTML=items.map(function(r){
      var name=cat.nf(r)||'—';
      var meta=r.adresse||r.venue_name||(r.kreis?'Kreis '+r.kreis:'');
      return '<a class="ku-row" href="'+cat.prof(r)+'" style="text-decoration:none;color:#e8e4d9">'+
        '<span>'+h(name)+'</span><span class="ku-rx">'+h(meta)+'</span></a>';
    }).join('');
  }

  async function openCatSheet(cat){
    openSheetShell(cat.ico,cat.c+'33',cat.label,'Kreis '+st.kreis+' · '+kreisName(st.kreis));
    var liveTag=document.getElementById('kuLiveTag');
    if(liveTag)liveTag.style.display=(st.counts[cat.key]||0)>0?'':'none';
    var cta=document.getElementById('kuCta'),route=document.getElementById('kuRoute');
    if(cta){cta.textContent='ALLI '+(st.counts[cat.key]||0)+' '+cat.label+' AASCHAUE →';cta.style.background=cat.c;cta.style.color='#04040a';cta.onclick=function(){location.href=CATPAGE[cat.key]||'index.html';};}
    if(route)route.textContent='Kreis '+st.kreis+' · '+kreisName(st.kreis);
    try{
      var url=SU+'/rest/v1/'+cat.table+'?'+cat.flt+'&kreis=eq.'+st.kreis+'&limit=6';
      var res=await kuFetch(url);
      renderRows(res.data||[],cat);
    }catch(e){renderRows([],cat);}
  }

  function toast(msg){
    var t=document.getElementById('kuToast');
    if(!t)return;
    t.textContent=msg;
    t.classList.add('on');
    setTimeout(function(){t.classList.remove('on');},2600);
  }

  function parseQuery(q){
    var kreis=st.kreis;
    var m=q.match(/kreis\s*(\d{1,2})/i);
    if(m){var n=parseInt(m[1],10);if(n>=1&&n<=12){kreis=n;q=q.replace(m[0],'').trim();}}
    q=q.replace(/^im\s+/i,'').replace(/\s+im$/i,'').trim();
    return {kw:q,kreis:kreis};
  }

  async function runSearch(){
    var input=document.getElementById('kuq');
    var raw=(input&&input.value||'').trim();
    if(!raw){toast('Gib zerst öppis i — z.B. «Sushi im Kreis 4»');return;}
    var p=parseQuery(raw);
    openSheetShell('🔍','rgba(255,255,255,.08)','SUECHRESULTAT','«'+raw+'»');
    var liveTag=document.getElementById('kuLiveTag');
    if(liveTag)liveTag.style.display='none';
    var cta=document.getElementById('kuCta'),route=document.getElementById('kuRoute');
    if(cta){cta.textContent='SUECHI ZRUGGSETZE';cta.style.background='rgba(255,255,255,.1)';cta.style.color='#e8e4d9';cta.onclick=function(){if(input)input.value='';closeSheet();};}
    if(route)route.textContent=p.kw?('Über alli Kategorie · Kreis '+p.kreis):('Über alli Kategorie · Kreis '+p.kreis);
    var rows=document.getElementById('kuRows');
    if(rows)rows.innerHTML='<div style="padding:16px 0;text-align:center;font-size:11px;color:rgba(232,228,217,.3)">Sueche läuft …</div>';
    var results=[];
    await Promise.all(CATS.map(async function(cat){
      try{
        var nameCol=cat.table==='eventfrog_events'?'titel':'name';
        var orf='or=('+nameCol+'.ilike.*'+encodeURIComponent(p.kw)+'*,beschreibung.ilike.*'+encodeURIComponent(p.kw)+'*)';
        var kreisF=p.kw?('&kreis=eq.'+p.kreis):('&kreis=eq.'+p.kreis);
        var url=SU+'/rest/v1/'+cat.table+'?'+cat.flt+kreisF+(p.kw?('&'+orf):'')+'&limit=4';
        var res=await kuFetch(url);
        (res.data||[]).forEach(function(r){results.push({r:r,cat:cat});});
      }catch(e){}
    }));
    if(!rows)return;
    if(!results.length){
      rows.innerHTML='<div style="padding:16px 0;text-align:center;font-size:11px;color:rgba(232,228,217,.3)">Kei Treffer für «'+h(raw)+'» im Kreis '+p.kreis+'.</div>';
      return;
    }
    rows.innerHTML=results.map(function(x){
      var name=x.cat.nf(x.r)||'—';
      var meta=x.cat.label+' · '+(x.r.adresse||x.r.venue_name||'');
      return '<a class="ku-row" href="'+x.cat.prof(x.r)+'" style="text-decoration:none;color:#e8e4d9">'+
        '<span>'+h(name)+'</span><span class="ku-rx">'+h(meta)+'</span></a>';
    }).join('');
  }

  function wireSearch(){
    var go=document.getElementById('kuGo'),input=document.getElementById('kuq');
    if(go)go.onclick=runSearch;
    if(input)input.addEventListener('keydown',function(e){if(e.key==='Enter')runSearch();});
  }

  function wireClose(){
    var bk=document.getElementById('kuBk');
    if(bk)bk.onclick=closeSheet;
    document.addEventListener('keydown',function(e){if(e.key==='Escape')closeSheet();});
  }

  function init(){
    if(!document.getElementById('kuGalaxy'))return;
    renderChips();
    wireSearch();
    wireClose();
    selectKreis(1);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>
'''

src = src.replace(marker, marker + '\n' + script)

with open(PFAD, 'w', encoding='utf-8') as f:
    f.write(src)

print('✓ index.html gepatcht — Kreis-Universum ist jetzt live mit echten Daten + Suche ueber alle Kategorien.')
