/* ═══════════════════════════════════════════════════════════
   STADTPULS — app.js
   Router · Cursor · Reveal · Menu · Scroll
   © 2026 by raimondo*
═══════════════════════════════════════════════════════════ */

/* ═══════════════════════════════
   ROUTER — SPA Navigation
═══════════════════════════════ */
function go(page) {
  // Alle Pages ausblenden
  document.querySelectorAll('.pg').forEach(p => p.classList.remove('on'));

  // Gewünschte Page einblenden
  const target = document.getElementById('pg-' + page);
  if (target) {
    target.classList.add('on');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Nav-Links updaten
  document.querySelectorAll('.nlinks a[data-p]').forEach(a => {
    a.classList.toggle('on', a.dataset.p === page);
  });

  // Footer injizieren
  injectFooter(page);
    if (page === 'gastro') loadLocations();

  // Reveal neu triggern
  setTimeout(initReveal, 100);
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
  const footerSlot = document.getElementById('f' + page.replace('-', ''));
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

  // Hover-Effekt auf klickbaren Elementen
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


  // Scroll → Reveal neu checken
  window.addEventListener('scroll', () => {
    document.querySelectorAll('.rv:not(.in)').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.92) {
        el.classList.add('in');
      }
    });
  }, { passive: true });
});/
// ============================================
// SUPABASE — Locations laden
// ============================================

async function loadLocations() {
  const SUPABASE_URL = 'https://pnynkzrqnfoshojqfqxn.supabase.co'
  const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ'

  const res = await fetch(
SUPABASE_URL + '/rest/v1/locations?select=*',

    {
      headers: {
        'apikey': SUPABASE_KEY,
        'Authorization': 'Bearer ' + SUPABASE_KEY
      }
    }
  )

  const data = await res.json()
  const container = document.getElementById('supabase-locations')
  if (!container) return

  container.innerHTML = data.map(loc => `
    <div class="sp-card">
      <div class="sp-card-kat">${loc.kategorie}</div>
      <div class="sp-card-name">${loc.name}</div>
      <div class="sp-card-adresse">${loc.adresse} · Kreis ${loc.kreis}</div>
    </div>
  `).join('')
}

loadLocations()


