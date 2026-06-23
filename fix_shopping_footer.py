import re

path = '/Users/alessandrachristen/stadtpuls/shopping-profil.html'
c = open(path).read()

# 1. FIX isOffe
c = c.replace(
    'if(!oz||!Array.isArray(oz)||!oz.length)return false;',
    'if(!oz||!Array.isArray(oz)||!oz.length)return null;'
)
print('isOffe fix:', 'return null' in c)

# 2. FIX Footer — ersetze alten <footer>...</footer>
new_footer = '''<footer style="background:#04040a;border-top:1px solid rgba(255,45,0,.08);padding:48px 40px 0">
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:40px;margin-bottom:40px">
    <div>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px">
        <div style="width:7px;height:7px;border-radius:50%;background:#ff2d00;animation:blink 2s infinite;flex-shrink:0"></div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:32px;color:#e8e4d9;letter-spacing:4px">STADTPULS</div>
      </div>
      <div style="font-size:10px;color:rgba(232,228,217,.4);margin-bottom:12px">dae puls vo dae stadt</div>
      <div style="font-size:10px;color:rgba(232,228,217,.25);line-height:1.8;margin-bottom:20px">Interaktiver Lifestyle &amp; City Guide fuer Zuerich. Social Media &amp; Marktplattform. Der virtuelle Spielplatz fuer Erwachsene.</div>
      <div style="font-size:9px;color:rgba(232,228,217,.15)">&#169; 2026 by raimondo* -- Zuerich</div>
    </div>
    <div>
      <div style="font-size:8px;letter-spacing:3px;text-transform:uppercase;color:#ff2d00;margin-bottom:20px;padding-bottom:10px;border-bottom:1px solid rgba(255,45,0,.08)">ENTDECKEN</div>
      <div style="display:flex;flex-direction:column;gap:12px">
        <a href="gastro.html" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Gastro &amp; Bars</a>
        <a href="nachtleben.html" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Nachtleben</a>
        <a href="shopping.html" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Shopping</a>
        <a href="events.html" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Events</a>
        <a href="index.html?page=quartiere" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Quartiere</a>
        <a href="index.html?page=musik" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Musik &amp; Sound</a>
        <a href="index.html?page=mobilitaet" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Mobilitaet</a>
      </div>
    </div>
    <div>
      <div style="font-size:8px;letter-spacing:3px;text-transform:uppercase;color:#ff2d00;margin-bottom:20px;padding-bottom:10px;border-bottom:1px solid rgba(255,45,0,.08)">COMMUNITY</div>
      <div style="display:flex;flex-direction:column;gap:12px">
        <a href="index.html?page=community" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Feed &amp; Posts</a>
        <a href="dating.html" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">People &amp; Dates</a>
        <a href="index.html?page=jobs" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Jobs Zueri</a>
        <a href="index.html?page=news" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">News &amp; Stories</a>
        <a href="index.html?page=gps" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">GPS -- Wo bisch du?</a>
        <a href="index.html?page=kooperationen" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Kooperatione</a>
      </div>
    </div>
    <div>
      <div style="font-size:8px;letter-spacing:3px;text-transform:uppercase;color:#ff2d00;margin-bottom:20px;padding-bottom:10px;border-bottom:1px solid rgba(255,45,0,.08)">MITMACHE</div>
      <div style="display:flex;flex-direction:column;gap:12px">
        <a href="index.html?page=login" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Einlogge</a>
        <a href="index.html?page=profil" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Profil aalege</a>
        <a href="index.html?page=blogger" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Blogger werde</a>
        <a href="index.html?page=inserat" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Inserat schalte</a>
        <a href="kontakt.html" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Partner werde</a>
        <a href="kontakt.html" style="font-size:10px;color:rgba(232,228,217,.35);text-decoration:none">Kontakt</a>
      </div>
    </div>
  </div>
  <div style="border-top:1px solid rgba(255,45,0,.06);padding:16px 0;display:flex;justify-content:space-between;align-items:center">
    <div style="font-size:8px;letter-spacing:2px;color:rgba(232,228,217,.1);text-transform:uppercase">&#169; 2026 STADTPULS.CH -- BY RAIMONDO* -- ZUERICH</div>
    <div style="display:flex;gap:24px">
      <a href="datenschutz.html" style="font-size:8px;letter-spacing:2px;color:rgba(232,228,217,.2);text-decoration:none;text-transform:uppercase">DATENSCHUTZ</a>
      <a href="impressum.html" style="font-size:8px;letter-spacing:2px;color:rgba(232,228,217,.2);text-decoration:none;text-transform:uppercase">IMPRESSUM</a>
    </div>
  </div>
</footer>'''

c = re.sub(r'<footer>.*?</footer>', new_footer, c, flags=re.DOTALL)
print('footer replaced:', 'ENTDECKEN' in c)

open(path, 'w').write(c)
print('DONE')
