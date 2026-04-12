/* ═══════════════════════════════════════════════════════════
   STADTPULS — main.js
   Router · Cursor · Reveal · Menu · Scroll · Supabase · API
   © 2026 by raimondo*
═══════════════════════════════════════════════════════════ */

const SUPABASE_URL = 'https://pnynkzrqnfoshojqfqxn.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ';

const tagColor = {
  'bar': '#00f5ff', 'club': '#9333ea', 'jazz': '#c8ff00',
  'restaurant': '#ff2d00', 'cafe': '#e8e4d9'
};
const tagText = {
  'bar': '#04040a', 'club': '#fff', 'jazz': '#04040a',
  'restaurant': '#fff', 'cafe': '#04040a'
};

const unsplash = [
  'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&q=80',
  'https://images.unsplash.com/photo-1598387993441-a364f854c3e1?w=800&q=80',
  'https://images.unsplash.com/photo-1571204829887-3b8d69e4094d?w=800&q=80',
  'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800&q=80'
];

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

    const featured = data[0];
    const sub0 = featured.subkategorie || featured.kategorie;
    const bg0 = tagColor[sub0] || '#ff2d00';
    const tc0 = tagText[sub0] || '#fff';

    let html = `
    <div style="display:grid;grid-template-columns:1.5fr 1fr;gap:2px;margin-bottom:2px;">
      <div class="ic rv" style="height:360px;">
        <img src="${unsplash[0]}" alt=""/>
        <div class="icc">
          <span style="background:${bg0};color:${tc0};font-family:'DM Mono',monospace;font-size:.5rem;font-weight:500;letter-spacing:.15em;padding:.2rem .6rem;text-transform:uppercase;display:inline-block;margin-bottom:.4rem;">${sub0}</span>
          <h3 style="font-size:1.9rem;">${featured.name}</h3>
          <div class="sub">${featured.adresse} · Kreis ${featured.kreis || '–'}</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:2px;">
        ${data.slice(1,4).map((loc, i) => {
          const sub = loc.subkategorie || loc.kategorie;
          const bg = tagColor[sub] || '#ff2d00';
          const tc = tagText[sub] || '#fff';
          return `<div class="ec rv" style="flex:1;">
            <span class="etag" style="background:${bg};color:${tc};">${sub}</span>
            <h3>${loc.name}</h3>
            <div class="meta"><strong>${loc.adresse} · Kreis ${loc.kreis || '–'}</strong></div>
            <span class="earr">↗</span>
          </div>`;
        }).join('')}
      </div>
    </div>
    <div class="g3 rv">
      ${data.slice(4).map(loc => {
        const sub = loc.subkategorie || loc.kategorie;
        const bg = tagColor[sub] || '#ff2d00';
        const tc = tagText[sub] || '#fff';
        return `<div class="ec rv">
          <span class="etag" style="background:${bg};color:${tc};">${sub}</span>
          <h3>${loc.name}</h3>
          <div class="meta"><strong>${loc.adresse} · Kreis ${loc.kreis || '–'}</strong></div>
          <span class="earr">↗</span>
        </div>`;
      }).join('')}
    </div>`;

    container.innerHTML = html;
    setTimeout(initReveal, 100);
  } catch(err) {
    container.innerHTML = '<p style="color:#ff2d00;padding:1rem;">Fehler: ' + err.message + '</p>';
  }
}

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

function initCursor() {
  const cur  = document.getElementById('cur');
  const cur2 = document.getElementById('cur2');
  if (!cur || !cur2) return;
  let mx = 0, my = 0, cx = 0, cy = 0;
  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
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
      cur2.style.width = '52px'; cur2.style.height = '52px';
      cur2.style.borderColor = 'rgba(255,45,0,.8)';
    }
  });
  document.addEventListener('mouseout', e => {
    if (e.target.matches('a, button, .btn, .ec, .ic, .bt, .qcard, .tc, .pill, .ftag, .ct')) {
      cur2.style.width = '32px'; cur2.style.height = '32px';
      cur2.style.borderColor = 'rgba(255,45,0,.4)';
    }
  });
}

function initReveal() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); observer.unobserve(e.target); }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.rv:not(.in)').forEach(el => observer.observe(el));
}

function toggleMenu() {
  document.getElementById('mobm').classList.toggle('open');
}

function closeMenu() {
  document.getElementById('mobm').classList.remove('open');
}

document.addEventListener('DOMContentLoaded', () => {
  initCursor();
  initReveal();
  injectFooter('home');
  window.addEventListener('scroll', () => {
    document.querySelectorAll('.rv:not(.in)').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.92) el.classList.add('in');
    });
  }, { passive: true });
});
