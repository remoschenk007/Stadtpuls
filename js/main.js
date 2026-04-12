/* ═══════════════════════════════════════════════════════════
STADTPULS — main.js
Router · Cursor · Reveal · Menu · Supabase
© 2026 by raimondo*
═══════════════════════════════════════════════════════════ */

const SUPABASE_URL = ‘https://pnynkzrqnfoshojqfqxn.supabase.co’;
const SUPABASE_KEY = ‘eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ’;

/* ═══════════════════════════════
ROUTER — go()
═══════════════════════════════ */
function go(page) {
// Alle Seiten ausblenden
document.querySelectorAll(’.pg’).forEach(p => p.classList.remove(‘on’));

// Zielseite einblenden
const target = document.getElementById(‘pg-’ + page);
if (target) {
target.classList.add(‘on’);
window.scrollTo({ top: 0, behavior: ‘smooth’ });
}

// Nav-Links aktualisieren
document.querySelectorAll(’.nlinks a[data-p]’).forEach(a => {
a.classList.toggle(‘on’, a.dataset.p === page);
});

// Footer injizieren
injectFooter(page);

// Supabase Daten laden
if (page === ‘gastro’)     loadLocations(‘gastro’);
if (page === ‘nachtleben’) loadLocations(‘nachtleben’);
if (page === ‘shopping’)   loadLocations(‘shopping’);
if (page === ‘events’)     loadLocations(‘events’);

// Alle rv-Elemente sofort sichtbar machen
revealAll();
}

/* ═══════════════════════════════
REVEAL — alle rv sofort sichtbar
═══════════════════════════════ */
function revealAll() {
document.querySelectorAll(’.rv’).forEach(el => el.classList.add(‘in’));
}

/* ═══════════════════════════════
SUPABASE — loadLocations()
═══════════════════════════════ */
async function loadLocations(kategorie) {
const container = document.getElementById(‘supabase-locations-’ + kategorie);
if (!container) return;

container.innerHTML = ‘<p style="color:#e8e4d9;opacity:.5;padding:1rem;">Laden…</p>’;

try {
const res = await fetch(
SUPABASE_URL + ‘/rest/v1/locations?select=*&kategorie=eq.’ + kategorie,
{
headers: {
‘apikey’: SUPABASE_KEY,
‘Authorization’: ’Bearer ’ + SUPABASE_KEY
}
}
);
const data = await res.json();

```
if (!data || data.length === 0) {
  container.innerHTML = '<p style="color:#e8e4d9;opacity:.5;padding:1rem;">Noch keine Einträge.</p>';
  return;
}

// Tag-Farben nach Subkategorie
const tagColor = {
  'bar':        '#00f5ff',
  'club':       '#9333ea',
  'jazz':       '#c8ff00',
  'restaurant': '#ff2d00',
  'cafe':       '#e8e4d9',
  'cafe/bar':   '#00f5ff'
};

container.innerHTML = data.map(loc => {
  const sub   = (loc.subkategorie || loc.kategorie || '').toLowerCase();
  const color = tagColor[sub] || '#e8e4d9';
  const kreis = loc.kreis ? 'Kreis ' + loc.kreis : '–';
  return `
    <div class="ec">
      <span class="etag" style="background:${color};color:#04040a;">${loc.subkategorie || loc.kategorie}</span>
      <h3>${loc.name}</h3>
      <div class="meta"><strong>${loc.adresse || ''} · ${kreis}</strong></div>
      <span class="earr">↗</span>
    </div>
  `;
}).join('');

// Nach dem Laden auch neue Elemente sichtbar machen
revealAll();
```

} catch(err) {
container.innerHTML = ’<p style="color:#ff2d00;padding:1rem;">Fehler: ’ + err.message + ‘</p>’;
}
}

/* ═══════════════════════════════
FOOTER
═══════════════════════════════ */
const footerHTML = `

<footer>
  <div class="ftk">
    <div class="fti">
      <span>Stadtpuls 2026</span><span>Zürich</span>
      <span>Dä Puls vo dä Stadt</span><span>Kreis 4</span>
      <span>Kreis 5</span><span>Langstrasse</span>
      <span>By Raimondo*</span><span>Stadtpuls 2026</span>
      <span>Zürich</span><span>Dä Puls vo dä Stadt</span>
      <span>Kreis 4</span><span>Kreis 5</span>
      <span>Langstrasse</span><span>By Raimondo*</span>
    </div>
  </div>
  <div class="fg">
    <div class="footer-brand">
      <div class="fbl"><div class="fbdot"></div>STADTPULS</div>
      <p>Dä Puls vo dä Stadt.<br>Zürich · 2026 · by raimondo*</p>
    </div>
    <div class="fc">
      <h5>Entdecke</h5>
      <ul>
        <li onclick="go('events')">Events</li>
        <li onclick="go('gastro')">Gastro</li>
        <li onclick="go('nachtleben')">Nachtleben</li>
        <li onclick="go('shopping')">Shopping</li>
        <li onclick="go('immobilien')">Immobilien</li>
      </ul>
    </div>
    <div class="fc">
      <h5>Community</h5>
      <ul>
        <li onclick="go('community')">Mitmache</li>
        <li onclick="go('dating')">People & Dates</li>
        <li onclick="go('jobs')">Jobs Züri</li>
        <li onclick="go('news')">News & Stories</li>
        <li onclick="go('musik')">Musik & Sound</li>
      </ul>
    </div>
    <div class="fc">
      <h5>Stadtpuls</h5>
      <ul>
        <li onclick="go('partners')">Partner</li>
        <li onclick="go('quartiere')">Quartiere</li>
        <li onclick="go('gps')">GPS</li>
        <li onclick="go('login')">Login</li>
      </ul>
    </div>
  </div>
  <div class="fbot">
    <p>© 2026 by raimondo* · Stadtpuls · Zürich</p>
    <p>Echts Züri. Kei Chichi. Kei Umwäg.</p>
  </div>
</footer>`;

function injectFooter(page) {
const key = ‘f’ + page.replace(’-’, ‘’);
let slot = document.getElementById(key);

if (!slot) {
const pg = document.getElementById(‘pg-’ + page);
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

/* ═══════════════════════════════
CURSOR — Desktop only
═══════════════════════════════ */
function initCursor() {
const cur  = document.getElementById(‘cur’);
const cur2 = document.getElementById(‘cur2’);
if (!cur || !cur2) return;

let mx = 0, my = 0, cx = 0, cy = 0;

document.addEventListener(‘mousemove’, e => {
mx = e.clientX;
my = e.clientY;
cur.style.transform = `translate(${mx - 5}px, ${my - 5}px)`;
});

function animateCur2() {
cx += (mx - cx) * 0.15;
cy += (my - cy) * 0.15;
cur2.style.transform = `translate(${cx - 16}px, ${cy - 16}px)`;
requestAnimationFrame(animateCur2);
}
animateCur2();

const hoverTargets = ‘a, button, .btn, .ec, .ic, .bt, .qcard, .tc, .pill, .ftag, .ct’;
document.addEventListener(‘mouseover’, e => {
if (e.target.matches(hoverTargets)) {
cur2.style.width  = ‘52px’;
cur2.style.height = ‘52px’;
cur2.style.borderColor = ‘rgba(255,45,0,.8)’;
}
});
document.addEventListener(‘mouseout’, e => {
if (e.target.matches(hoverTargets)) {
cur2.style.width  = ‘32px’;
cur2.style.height = ‘32px’;
cur2.style.borderColor = ‘rgba(255,45,0,.4)’;
}
});
}

/* ═══════════════════════════════
MENU
═══════════════════════════════ */
function toggleMenu() {
document.getElementById(‘mobm’).classList.toggle(‘open’);
}

function closeMenu() {
document.getElementById(‘mobm’).classList.remove(‘open’);
}

/* ═══════════════════════════════
TABS — switchTab()
═══════════════════════════════ */
function switchTab(tabId, el) {
const parent = el.closest(’.tab-container’) || document.body;
parent.querySelectorAll(’.tab-content’).forEach(t => t.classList.remove(‘active’));
parent.querySelectorAll(’.tab-btn’).forEach(b => b.classList.remove(‘active’));
const target = document.getElementById(tabId);
if (target) target.classList.add(‘active’);
el.classList.add(‘active’);
}

/* ═══════════════════════════════
INIT
═══════════════════════════════ */
document.addEventListener(‘DOMContentLoaded’, () => {
initCursor();
injectFooter(‘home’);
revealAll();
});
window.go = go;
window.toggleMenu = toggleMenu;
window.closeMenu = closeMenu;
window.switchTab = switchTab;
