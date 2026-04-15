/* STADTPULS — main.js © 2026 by raimondo* */

const SUPABASE_URL = ‘https://pnynkzrqnfoshojqfqxn.supabase.co’;
const SUPABASE_KEY = ‘eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ’;

function go(page) {
document.querySelectorAll(’.pg’).forEach(function(p) { p.classList.remove(‘on’); });
var target = document.getElementById(‘pg-’ + page);
if (target) {
target.classList.add(‘on’);
window.scrollTo({ top: 0, behavior: ‘smooth’ });
}
document.querySelectorAll(’.nlinks a[data-p]’).forEach(function(a) {
a.classList.toggle(‘on’, a.dataset.p === page);
});
injectFooter(page);
if (page === ‘gastro’)     loadLocations(‘gastro’);
if (page === ‘nachtleben’) loadLocations(‘nachtleben’);
if (page === ‘shopping’)   loadLocations(‘shopping’);
if (page === ‘events’)     loadLocations(‘events’);
document.querySelectorAll(’.rv’).forEach(function(el) { el.classList.add(‘in’); });
}

function injectFooter(page) {
var key = ‘f’ + page.replace(’-’, ‘’);
var slot = document.getElementById(key);
if (!slot) {
var pg = document.getElementById(‘pg-’ + page);
if (pg) {
slot = document.createElement(‘div’);
slot.id = key;
pg.appendChild(slot);
}
}
if (slot && slot.innerHTML.trim() === ‘’) {
slot.innerHTML = footerHTML;
}
}

var footerHTML = ‘<footer><div class="ftk"><div class="fti"><span>Stadtpuls 2026</span><span>Zürich</span><span>Dä Puls vo dä Stadt</span><span>Kreis 4</span><span>Kreis 5</span><span>By Raimondo*</span><span>Stadtpuls 2026</span><span>Zürich</span></div></div><div class="fg"><div class="footer-brand"><div class="fbl"><div class="fbdot"></div>STADTPULS</div><p>Dä Puls vo dä Stadt.<br>Zürich · 2026 · by raimondo*</p></div><div class="fc"><h5>Entdecke</h5><ul><li onclick="go(\'events\')">Events</li><li onclick="go(\'gastro\')">Gastro</li><li onclick="go(\'nachtleben\')">Nachtleben</li><li onclick="go(\'shopping\')">Shopping</li><li onclick="go(\'immobilien\')">Immobilien</li></ul></div><div class="fc"><h5>Community</h5><ul><li onclick="go(\'community\')">Mitmache</li><li onclick="go(\'dating\')">People & Dates</li><li onclick="go(\'jobs\')">Jobs Züri</li><li onclick="go(\'news\')">News & Stories</li><li onclick="go(\'musik\')">Musik & Sound</li></ul></div><div class="fc"><h5>Stadtpuls</h5><ul><li onclick="go(\'partners\')">Partner</li><li onclick="go(\'quartiere\')">Quartiere</li><li onclick="go(\'gps\')">GPS</li><li onclick="go(\'login\')">Login</li></ul></div></div><div class="fbot"><p>© 2026 by raimondo* · Stadtpuls · Zürich</p><p>Echts Züri. Kei Chichi. Kei Umwäg.</p></div></footer>’;

function loadLocations(kategorie) {
var container = document.getElementById(‘supabase-locations-’ + kategorie);
if (!container) return;
container.innerHTML = ‘<p style="color:#e8e4d9;opacity:.5;padding:1rem;">Laden…</p>’;
fetch(SUPABASE_URL + ‘/rest/v1/locations?select=*&kategorie=eq.’ + kategorie, {
headers: { ‘apikey’: SUPABASE_KEY, ‘Authorization’: ‘Bearer ’ + SUPABASE_KEY }
})
.then(function(res) { return res.json(); })
.then(function(data) {
if (!data || data.length === 0) {
container.innerHTML = ‘<p style="color:#e8e4d9;opacity:.5;padding:1rem;">Noch keine Einträge.</p>’;
return;
}
var colors = { ‘bar’:’#00f5ff’,‘club’:’#9333ea’,‘jazz’:’#c8ff00’,‘restaurant’:’#ff2d00’,‘cafe’:’#e8e4d9’ };
container.innerHTML = data.map(function(loc) {
var sub = (loc.subkategorie || loc.kategorie || ‘’).toLowerCase();
var color = colors[sub] || ‘#e8e4d9’;
var kreis = loc.kreis ? ‘Kreis ’ + loc.kreis : ‘-’;
return ‘<div class="ec"><span class="etag" style="background:' + color + ';color:#04040a;">’ + (loc.subkategorie || loc.kategorie) + ‘</span><h3>’ + loc.name + ‘</h3><div class="meta"><strong>’ + (loc.adresse || ‘’) + ’ · ’ + kreis + ‘</strong></div><span class="earr">↗</span></div>’;
}).join(’’);
document.querySelectorAll(’.rv’).forEach(function(el) { el.classList.add(‘in’); });
})
.catch(function(err) {
container.innerHTML = ’<p style="color:#ff2d00;padding:1rem;">Fehler: ’ + err.message + ‘</p>’;
});
}

function toggleMenu() { document.getElementById(‘mobm’).classList.toggle(‘open’); }
function closeMenu()  { document.getElementById(‘mobm’).classList.remove(‘open’); }
function switchTab(tab) {
  var l = document.getElementById('form-login');
  var r = document.getElementById('form-register');
  var tl = document.getElementById('tab-login');
  var tr = document.getElementById('tab-register');
  if (!l || !r) return;
  if (tab === 'login') {
    l.style.display='block'; r.style.display='none';
    tl.style.borderBottomColor='#ff2d00';
    tr.style.borderBottomColor='rgba(255,255,255,0.08)';
  } else {
    l.style.display='none'; r.style.display='block';
    tl.style.borderBottomColor='rgba(255,255,255,0.08)';
    tr.style.borderBottomColor='#ff2d00';
  }
}


function initCursor() {
var cur = document.getElementById(‘cur’);
var cur2 = document.getElementById(‘cur2’);
if (!cur || !cur2) return;
var mx = 0, my = 0, cx = 0, cy = 0;
document.addEventListener(‘mousemove’, function(e) {
mx = e.clientX; my = e.clientY;
cur.style.transform = ‘translate(’ + (mx-5) + ‘px,’ + (my-5) + ‘px)’;
});
function animateCur2() {
cx += (mx-cx) * 0.15;
cy += (my-cy) * 0.15;
cur2.style.transform = ‘translate(’ + (cx-16) + ‘px,’ + (cy-16) + ‘px)’;
requestAnimationFrame(animateCur2);
}
animateCur2();
}

window.go         = go;
window.toggleMenu = toggleMenu;
window.closeMenu  = closeMenu;
window.switchTab  = switchTab;

document.addEventListener(‘DOMContentLoaded’, function() {
initCursor();
injectFooter(‘home’);
document.querySelectorAll(’.rv’).forEach(function(el) { el.classList.add(‘in’); });
});
