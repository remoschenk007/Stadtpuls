/* ═══════════════════════════════════════════════════════════
   STADTPULS — app.js
   Router · Cursor · Reveal · Menu · Scroll · Supabase · API
   © 2026 by raimondo*
═══════════════════════════════════════════════════════════ */

/* ═══════════════════════════════
   SUPABASE CONFIG
═══════════════════════════════ */
const SUPABASE_URL = 'https://pnynkzrqnfoshojqfqxn.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ';

/* ═══════════════════════════════
   ROUTER — SPA Navigation
═══════════════════════════════ */
function go(page) {
  document.querySelectorAll('.pg').forEach(p => p.classList.remove('on'));

  const target = document.getElementById('pg-' + page);
  if (target) {
    target.classList.add('on');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  document.querySelectorAll('.nlinks a[data-p]').forEach(a => {
    a.classList.toggle('on', a.dataset.p === page);
  });

  injectFooter(page);

  if (page === 'gastro') loadLocations('gastro');
  if (page === 'nachtleben') loadLocations('nachtleben');
  if (page === 'shopping') loadLocations('shopping');
  if (page === 'events') loadLocations('events');

  setTimeout(initReveal, 100);
}

/* ═══════════════════════════════
   SUPABASE — Locations laden
═══════════════════════════════ */
async function loadLocations(kategorie) {
  const containerId = 'supabase-locations-' + kategorie;
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = '<p style="color:#e8e4d9;opacity:.5;padding:1rem;">Laden…</p>';

  try {
    const res = await fetch(
      SUPABASE_URL + '/rest/v1/locations?select=*&kategorie=eq.' + kategorie,
      {
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': 'Bearer ' + SUPABASE_KEY
        }
      }
    );

    const data = await res.json();

    if (!data || data.length === 0) {
      container.innerHTML = '<p style="color:#e8e4d9;opacity:.5;padding:1rem;">Noch keine Einträge.</p>';
      return;
    }

    container.innerHTML = data.map(loc => `
      <div class="ec rv">
        <span class="etag">${loc.subkategorie || loc.kategorie}</span>
        <h3>${loc.name}</h3>
        <div class="meta"><strong>${loc.adresse} · Kreis ${loc.kreis}</strong></div>
        <span class="earr">↗</span>
      </div>
    `).join('');

    setTimeout(initReveal, 100);

  } catch(err) {
    container.innerHTML = '<p style="color:#ff2d00;padding:1rem;">Fehler: ' + err.message + '</p>';
  }
}

/* ═══════════════════════════════
   ZÜRICH API — Import in Supabase
═══════════════════════════════ */
async function importZuerichAPI() {
  const ZUERICH_URL = 'https://www.zuerich.com/en/api/v2/data?id=100';

  try {
    const res = await fetch(ZUERICH_URL);
    const data = await res.json();

    if (!data || !data['@graph']) {
      alert('Zürich API: Keine Daten gefunden.');
      return;
    }

    const items = data['@graph'];
    let importiert = 0;
    let fehler = 0;

    for (const item of items) {
      const location = mapZuerichItem(item);
      if (!location) continue;

      const insertRes = await fetch(
        SUPABASE_URL + '/rest/v1/locations',
        {
          method: 'POST',
          headers: {
            'apikey': SUPABASE_KEY,
            'Authorization': 'Bearer ' + SUPABASE_KEY,
            'Content-Type': 'application/json',
            'Prefer': 'resolution=ignore-duplicates'
          },
          body: JSON.stringify(location)
        }
      );

      if (insertRes.ok || insertRes.status === 201 || insertRes.status === 409) {
        importiert++;
      } else {
        fehler++;
      }
    }

    alert('Import fertig: ' + importiert + ' Locations · ' + fehler + ' Fehler');

  } catch(err) {
    alert('Zürich API Fehler: ' + err.message);
  }
}

function mapZuerichItem(item) {
  if (!item.name || !item.address) return null;

  const name = typeof item.name === 'object' ? item.name.de || item.name.en || '' : item.name;
  const adresse = item.address?.streetAddress || '';
  const plz = item.address?.postalCode || '';
  const lat = item.geo?.latitude || null;
  const lng = item.geo?.longitude || null;
  const beschreibung = typeof item.disambiguatingDescription === 'object'
    ? item.disambiguatingDescription.de || item.disambiguatingDescription.en || ''
    : item.disambiguatingDescription || '';

  const typ = item['@type'] || '';
  let kategorie = 'gastro';
  let subkategorie = 'restaurant';

  if (typ.includes('BarOrPub') || typ.includes('NightClub')) {
    kategorie = 'nachtleben';
    subkategorie = 'bar';
  } else if (typ.includes('CafeOrCoffeeShop')) {
    kategorie = 'gastro';
    subkategorie = 'cafe';
  } else if (typ.includes('FastFood')) {
    kategorie = 'gastro';
    subkategorie = 'street food';
  }

  const cats = (item.category || []).map(c => (c.name?.de || c.name?.en || '').toLowerCase());
  if (cats.some(c => c.includes('vegeta') || c.includes('vegan'))) subkategorie = 'vegisch';
  if (cats.some(c => c.includes('asia') || c.includes('japan') || c.includes('chin') || c.includes('thai'))) subkategorie = 'asiatisch';
  if (cats.some(c => c.includes('ital') || c.includes('medit'))) subkategorie = 'mediterran';
  if (cats.some(c => c.includes('brunch') || c.includes('frühstück'))) subkategorie = 'brunch';
  if (cats.some(c => c.includes('techno') || c.includes('club'))) { kategorie = 'nachtleben'; subkategorie = 'techno'; }
  if (cats.some(c => c.includes('jazz'))) { kategorie = 'nachtleben'; subkategorie = 'jazz'; }

  const slug = name.toLowerCase()
    .replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue')
    .replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');

  return {
    name,
    kategorie,
    subkategorie,
    adresse,
    plz,
    lat,
    lng,
    beschreibung,
    slug,
    aktiv: true,
    quelle: 'zuerich-tourismus'
  };
}

/* ═══════════════════════════════
   FOOTER INJECT
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
  const key = 'f' + page.replace('-', '');
  const footerSlot = document.getElementById(key);
  if (footerSlot && footerSlot.innerHTML.trim() === '') {
    footerSlot.innerHTML = footerHTML;
  }
}

/* ═══════════════════════════════
   DUAL CURSOR
═══════════════════════════════ */
function initCursor() {
  const cur  = document.getElementById('cur');
  const cur2 = document.getElementById('cur2');
  if (!cur || !cur2) return;

  let mx = 0, my = 0, cx = 0, cy = 0;

  document.addEventListener('mousemove', e => {
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

  document.addEventListener('mouseover', e => {
    if (e.target.matches('a, button, .btn, .ec, .ic, .bt, .qcard, .tc, .pill, .ftag, .ct')) {
      cur2.style.width  = '52px';
      cur2.style.height = '52px';
      cur2.style.borderColor = 'rgba(255,45,0,.8)';
    }
  });
  document.addEventListener('mouseout', e => {
    if (e.target.matches('a, button, .btn, .ec, .ic, .bt, .qcard, .tc, .pill, .ftag, .ct')) {
      cur2.style.width  = '32px';
      cur2.style.height = '32px';
      cur2.style.borderColor = 'rgba(255,45,0,.4)';
    }
  });
}

/* ═══════════════════════════════
   REVEAL — IntersectionObserver
═══════════════════════════════ */
function initReveal() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.rv:not(.in)').forEach(el => observer.observe(el));
}

/* ═══════════════════════════════
   MOBILE MENU
═══════════════════════════════ */
function toggleMenu() {
  document.getElementById('mobm').classList.toggle('open');
}

function closeMenu() {
  document.getElementById('mobm').classList.remove('open');
}

/* ═══════════════════════════════
   INIT
═══════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  initCursor();
  initReveal();
  injectFooter('home');

  window.addEventListener('scroll', () => {
    document.querySelectorAll('.rv:not(.in)').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.92) {
        el.classList.add('in');
      }
    });
  }, { passive: true });
});
