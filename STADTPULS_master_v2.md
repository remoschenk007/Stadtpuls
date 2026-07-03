# STADTPULS — MASTERPLAN v2

> **Kanonisches Session-Continuity-Dokument.** Stand: 01.07.2026
> Schwester-Dokument: **`STADTPULS_KI_HERZ_BLUEPRINT.md`** (Personalisierung + Monetarisierung im Detail). Neue Chats lesen BEIDE.

---

## 0. WAS IST STADTPULS

Zürcher Lifestyle-/City-Guide-Plattform. Vision: das beste Stadtportal der Welt, „never leave the platform"-Philosophie, später Franchise auf andere Städte (depuls.hamburg etc.). Persönliche Freiheit > Firmenverkauf.

- **Live:** depuls.ch (GitHub Pages)
- **Creative Director / Owner:** Remo Schenk (alias „by Raimondo"), Zürich
- **Analytics:** Plausible (DSGVO-konform) auf depuls.ch

---

## 1. TECH & REPO

- **Stack:** Vanilla HTML/CSS/JS + Supabase Backend, deployed via GitHub Pages
- **Repo:** `remoschenk007/Stadtpuls`, Branch `main`
- **Lokaler Pfad:** `/Users/alessandrachristen/stadtpuls/`
- **Raw-Zugriff:** `https://raw.githubusercontent.com/remoschenk007/Stadtpuls/main/[datei]`

### Supabase
- **URL:** `https://pnynkzrqnfoshojqfqxn.supabase.co`
- **Anon-Key:** public, im Code als `const SK='eyJhbGci…W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ'` (im index-Modul: `const SU=url; const SK=key;`)
- **Count-Pattern:** `async function sbCount(path)` via Range / `content-range`-Header
- **Tabelle `locations`:** Felder u.a. `kategorie` (Werte: `gastro`, `nachtleben`, `shopping`), `kreis`, `aktiv`, `stimmung_tags`, `ticketcorner_url`, `reservierbar`
- **Tabelle `public.users`:** kein E-Mail-Feld (bewusst, GDPR)
- Datenbestand: 400+ Gastro, 745+ Locations total (Import via Zürich-Tourismus-API-Tool)

---

## 2. DESIGN DNA

- **Hintergrund:** `#04040a`
- **Rot:** `#ff2d00` · **Volt-Grün:** `#c8ff00` · **Cyan:** `#00f5ff` · **Lila:** `#9333ea` · **Cream:** `#e8e4d9`
- **Headlines:** Barlow Condensed Italic 900
- **Body:** DM Mono
- **Regel:** immer Hex-Werte, **nie** CSS-Variablen
- **Schema.org JSON:** doppelte Anführungszeichen Pflicht, keine Template-Literals

---

## 3. ARBEITSREGELN (Workflow)

- **Sprache:** Mit Remo **Hochdeutsch**. Zürideutsch **nur** für On-Site-Website-Copy.
- **Verify-don't-guess:** Geometrie/Logik immer durchrechnen, nie raten. **Nie Fake-Daten** — ehrliche Platzhalter bevorzugt.
- **Build-Workflow:** Claude baut in `/mnt/user-data/outputs/`, validiert (Div-Balance via Python-`count`, JS-Syntax via `node --check` auf extrahierte `<script>` — Module als `.mjs`, plain IIFEs als `.js`), zippt, `present_files`. Remo lädt runter und pusht selbst.
- **Git-Push-Pattern** (immer `pull --rebase` vor `push`, da Remo auch direkt auf GitHub editiert):
  ```bash
  cd ~/Downloads && unzip -o NAME.zip -d NAME && \
  cp NAME/*.html /Users/alessandrachristen/stadtpuls/ && \
  cd /Users/alessandrachristen/stadtpuls && \
  git add FILES && git commit -m "MSG" && \
  git pull --rebase origin main && git push origin main
  ```
- Die „Your name and email address were configured automatically…"-Meldung ist **informativ, kein Fehler**.
- Große Dateien (z.B. base64-Bilder) via raw GitHub fetchen, nicht im Editor öffnen.

---

## 4. SEITEN-INVENTAR & STATUS

### Vorhanden & live
- `index.html` — Startseite (siehe §5, neu aufgebaut)
- `gastro.html` / `gastro-profil.html` — Gastro-Liste + Profil (kreis-filterbar via `?kreis=N`)
- `nachtleben.html` / `nachtleben-profil.html`
- `shopping.html` / `shopping-profil.html`
- `events.html` — GODMODE, Canvas-Partikel-Animation, vertikale Timeline
- `event-profil.html` — Leaflet.js-Karte + Schema.org-SEO
- `dating.html`
- `news.html`
- `login.html` — Supabase Auth
- `onboarding.html` — 5-Step-Duolingo-Flow, Zürideutsch, Under-18-Detection
- `dashboard.html`, `admin.html`, `feedback.html`, `kontakt.html`, `master.html`
- `kommandozentrale.html` — Operator-Cockpit (Login-gated): Moderation (Kommentare/News/Inserate/**Momänt**), Verkauf, Boosts, Finanzen, Users, Audit
- `platzierung.html` — öffentlicher „Das isch mis Lokal"-Claim-/Zahlungs-Flow (Tier + Tage → boost_requests; PAYMODE manual, Stripe-Functions bereit)
- `import.html` — **GELÖSCHT** (ersetzt durch Auto-Sync, GitHub Action `stadtpuls-sync.yml` täglich 04:00: Eventfrog + Zürich Tourismus → Supabase)

### Footer-Status
- **Kanonischer Footer:** inline `<footer>` (`.ftk` Ticker + `.fg` Grid + `.fbot` + `.footer-brand`/`.fbl`/`.fbdot`) mit eigenem `<style>`-Block `/* ═══ ORIGINAL STADTPULS FOOTER ═══ */`. **Quelle der Wahrheit = gastro.html.**
- **Gefixter Root-Cause-Bug:** Legacy-Regel `footer{…display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr…}` (+ Mobile-Variante) quetschte den Footer in 4-Spalten-Grid → entfernt. Jetzt `footer{background:#04040a;border-top:1px solid rgba(255,45,0,0.1)}` überall.
- **13 Seiten** haben den identischen Footer ✓.
- **Ohne Footer:** login, dashboard, feedback, kontakt, admin, master.
  - **ENTSCHIEDEN (28.06., Remo): feedback.html bekommt BEWUSST KEINEN Footer** (eigenes Blasen-Universum). kontakt optional offen. login/dashboard/admin/master funktional — ohne.
- **Optional:** Rainbow-`.deco`-Linie (`linear-gradient(90deg,#ff2d00,#c8ff00,#00f5ff,#ff2d00)`) auf alle Seiten ausrollen.
- ⚠️ Im Explorer lag ein `footer_fehlend.zip` — noch zu prüfen, wo ggf. ein Footer fehlt.

### FEHLENDE Seiten (verlinkt, aber noch 404)
| Seite | Verlinkt von | Priorität |
|---|---|---|
| `quartiere.html` | Kreis-Chips + Galaxie-Sheet (`?kreis=N`) | **HOCH** (Kreis-Detail/Ziel) |
| `immobilien.html` | Bento-Card Startseite | HOCH |
| `jobs.html` | Footer | mittel |
| `musik.html` | Footer | mittel |
| `mobilitaet.html` | Footer | mittel |
| `community.html` | Footer / Bento | mittel |
| `gps.html` | Footer | niedrig |
| `partners.html` | Footer | niedrig |

---

## 5. STARTSEITE (index.html) — AKTUELLER AUFBAU

Kombiniertes Design (altes „geileres" Design + Live-Daten-Skeleton). Reihenfolge:

1. **Header/Nav** + roter Puls-Dot Logo
2. **Photographic BENTO-Cards** (Unsplash-Bilder, Live-Counts via `cnt-gastro/nachtleben/events/shopping`; immobilie/community ohne Fake-Zahl)
3. **Community-Farbquadranten** (BLOGGE rot / BEWERTET dark / UPLOADE cyan / KOMMENTIERE volt)
4. **„HÜT ABIG"** grün-akzentuierter Wrap (echte Events via `loadTonight`)
5. **KREIS-UNIVERSUM** (siehe §6 — ersetzt die alte QUARTIERE-Strip)
6. **Bubble-Menü** roter Puls-Dot → 4 `.nb` Glas-Bubbles → feedback / kontakt / impressum / datenschutz
7. **Footer** (kanonisch)

*Bewusst weggelassen:* die alte Emoji-„DAS KOMPLETTE PORTAL"-Grid (Footer deckt das ab). Ein Double-Ticker-Experiment wurde von Remo verworfen.

**Neu seit 01.07. (zwischen Universum und Community-CTA):**
8. **◉ ZÜRI MOMÄNT** (gold) — die 3 neuesten **freigeschalteten** Community-Momänt als Zitat-Karten. Unsichtbar, wenn nichts freigeschaltet.
9. **NEWS & STORIES Teaser** — die 3 neuesten `approved`-Stories (Bild + Titel), Link auf news.html. Unsichtbar wenn leer.

---

## 5.5 ZÜRI-MOMÄNT-FLOW (Community → Kuration → Startseite)

**Der gedachte Kreislauf** (Kuration durch Remo, nie automatisch):

```
feedback.html (Blase „MOMENT")  →  Tabelle feedback (typ='moment', status='neu')
        ↓
kommandozentrale.html → Tab MODERATION: erscheint als „◉ ZÜRI MOMÄNT"
        ↓  Klick „◉ Uf d Startsite"  (status='approved')
index.html → Sektion „ZÜRI MOMÄNT" zeigt die 3 neuesten automatisch
        ↺  „↩ Vo de Startsite näh" im Panel „LIVE UF DE STARTSITE" (status='neu')
```

- **Freischalten passiert AUSSCHLIESSLICH in der Kommandozentrale** (nicht per SQL). Jede Aktion landet im Audit-Log.
- **Setup einmalig:** `setup_momente.sql` (legt `feedback.status` an, Default `'neu'`).
- **News & Stories** laufen analog über die bestehende Moderation (`news_stories.status='approved'`) und erscheinen zusätzlich als Startseiten-Teaser.

---

## 6. KREIS-UNIVERSUM (Hauptarbeit dieser Session) ✅ LIVE

**Mentales Modell:** Stadt = 12 Kreise × N Sparten. Kategorie-Seite = vertikaler Schnitt; Kreis = horizontaler Schnitt (alle Sparten in einem Viertel). Galaxie, in der der **Kreis = Zentralstern** ist und die **Sparten-Blasen ihn umkreisen** (reused die DIS-UNIVERSUM-Dashboard-Mechanik).

Alle Klassen `ku-`-prefixed (Kollisionsschutz). Ersetzt die alte `kreis-strip`-Sektion zwischen `<!-- QUARTIERE STRIP -->` und `<!-- COMMUNITY`.

### Bestandteile
- **12 Kreis-Chips** (ALTSTADT, ENGE, WIEDIKON, LANGSTRASSE, INDUSTRIE, UNTERSTRASS, FLUNTERN, SEEFELD, ALTSTETTE, HÖNGG, OERLIKON, SCHWAMENDINGE).
  - **Neu: Glas-Tile-Design** (vorher billige graue Ovale): `linear-gradient`-Glas, Glanzkante (`::before`), große Italic-Nummer, **voller Name** (keine `slice(0,8)`-Abschneidung mehr), aktiver Kreis = rotes Glas-Glühen (`box-shadow` outer+inner) statt nur Rand.
  - In `.ku-chipswrap`-Scroll-Wrapper mit **rechtsseitigem Fade** (`::after`, fade zu `#04040a`) + pulsierendem **„›"-Pfeil** (`#kuMore`, `@keyframes kunudge`). Beides verschwindet am Scroll-Ende via `kuFade()` (`--fade` Custom-Property). → macht klar, dass es bis Kreis 12 weitergeht.
- **Galaxie** (6 Sparten-Blasen):
  | Sparte | Farbe | Ziel |
  |---|---|---|
  | Gastro | `#ff2d00` | `gastro.html?kreis=N` |
  | Nachtlebe | `#9333ea` | `nachtleben.html?kreis=N` |
  | Shopping | `#00f5ff` | `shopping.html?kreis=N` |
  | Events | `#c8ff00` | `events.html?kreis=N` |
  | Dates | `#ff5fa2` | `dating.html?kreis=N` |
  | News | `#3fd2ff` | `news.html?kreis=N` |
  - **Glas-3D-Blasen** im feedback.html-Stil: gestapelte Radial-Gradients (Shell-Highlight + Rim + 2 Shines + Color-Glow), per-Farbe `box-shadow`, `currentColor` Drop-Shadow auf Icons, drehende `.ku-orbit-ring`/`-dot` auf **jeder** Blase, Gold-Doppelring auf „hot", 3D-Tilt-Parallax, Float-Bob.
  - **Echte Pro-Kreis-Counts** für gastro/nachtleben/shopping via **einer** Query `locations?select=kreis,kategorie&aktiv=eq.true`, clientseitig gezählt. events/dates/news = Basisgröße, Label only (ehrlich, keine Fake-Zahl). Aktivste reale Sparte bekommt Gold-„top"-Puls.
  - Zentralstern = aktueller Kreis (Nummer + Name + „N ORT").
  - Blase tippen → Bottom-Sheet (`max-width:520px`) mit Route + Top-3 + CTA „ALLI X ZEIGE →".
- **✨ „Frag Stadtpuls" Smart-Suechi** (`#kuq` Input + `#kuGo`):
  - Clientseitiger Keyword-Parser `parseIntent()`: extrahiert Kreis (Regex `/kreis\s*(\d{1,2})/`, **single backslash, korrekt**), Quartier-Namen (Map `QN`), Sparte (Map `SKW`) → steuert Galaxie / öffnet Sheet.
  - Ehrlich gelabelt: „SMART-SUECHI · DE ZÜRI-BOT MIT ECHTER KI FOLGT" (funktionierender Seed für späteren LLM-Bot).
  - **Funktionen:** `parseIntent`, `runSearch`, `loadCounts`, `setKreis`, `openSheet`, `render`, `kuFade`.

### Mobile-Pass ✅ (diese Session)
- **Geometrie durchgerechnet** (Python-Sim, W = 300/348/390): kein Overflow, keine Stern-Überlappung, sogar Worst-Case (alle Blasen Maximalgröße). Positionierung mobil sauber.
- **3D-Tilt nur bei Maus:** `if(window.matchMedia && window.matchMedia("(pointer:fine)").matches){ … pointermove/pointerleave … }` — auf Touch ab (verhindert hängenden/jankigen Tilt beim Scrollen). Float + Ringe bleiben.
- **Resize-Handler:** debounced `resize` → `galaxy.style.transform=""; render()` (Re-Layout beim Drehen).
- **Mobile-Media:** `@media(max-width:560px){.ku-stage{height:400px}.ku-bar{gap:6px}}`.
- iOS-Input-Zoom ist durch Viewport `maximum-scale=1.0` bereits abgefangen.

### Galaxie-Geometrie (Referenz-Params)
- Stage: `width:100%`, `height:430px` (Mobile 400px); `cx=W/2`, `cy=H/2`
- `Rx=min(W*0.40,158)`, `Ry=H*0.37`
- 6 Blasen bei Winkeln `-90 + i*60`°; Größe `48 + min(1,c/maxC)*42` (48–90px), no-count = 58px
- Zentralstern 104px (Mobile via Media kompakter)

---

## 7. REVENUE-MODELL

BASIC (gratis) → FEATURED (CHF 20/Wo) → BOOST (CHF 50/Wo) → PREMIUM (CHF 100/Wo), Laufzeiten 1/2/4 Wochen mit Auto-Ablauf.
**Gebaut (28.06.):** Kommandozentrale (Verkauf/Boosts/Finanzen/Audit) + `platzierung.html`-Claim-Flow („Das isch mis Lokal": verifizieren → zahlen → Remo schaltet frei). Zahlung: Start **manuell**, Stripe+TWINT-Functions liegen bereit. Ziel ~CHF 3'000/Mt; grösster Hebel künftig **Pro-Abo** (Statistiken aus `interactions`). Details: KI-Herz-Blueprint §8.

---

## 8. OFFENE PRIORITÄTEN / NEXT STEPS

1. **`quartiere.html` bauen** — Kreis-Detail (Chips + Galaxie verlinken `?kreis=N`). Top-Priorität.
2. **Fehlende Seiten** (§4): immobilien, jobs, musik, mobilitaet, community, gps, partners (Footer-Links sind teils 404!).
3. **Money-Loop schliessen:** Listen nach `featured`/`boost_tier` sortieren + „Das isch mis Lokal"-Button auf die Profilseiten (→ platzierung.html?id=…).
4. **KI-Herz Schritt 1 fertig verdrahten:** Herz-Button + spTrack in gastro/shopping + Listen. Dann Schritt 2 (taste-build / Geschmacks-DNA). → Blueprint §6.
5. **Echter LLM Züri-Bot** für „Frag Stadtpuls" (deterministische Engine zuerst — Blueprint §0).
6. **Pro-Kreis-Daten für Events** (Geo→Kreis-Mapping) — Events/Dates/News echte Counts.
7. ~~Pop-up/Event-Daten-Pipeline + Matching-Fundament~~ ✅ **ERLEDIGT** (Auto-Sync 27.06. + KI-Herz Schritt 1 am 28.06.).

---

## 9. CHANGELOG

### Sessions 27.06.–01.07.2026 (kompakt)
- **Auto-Sync-Pipeline** (27.06.): GitHub Action `stadtpuls-sync.yml` täglich 04:00 — Eventfrog (~5'000+ Events) + ZT → Supabase. `import.html` gelöscht. `SUPABASE_SERVICE_KEY`-Secret gesetzt → nächtliches Aufräumen alter Events.
- **Kommandozentrale v3 + Monetarisierung** (28.06.): Operator-Cockpit (11 Tabs) + `platzierung.html` + setup.sql (boosts, boost_requests, comments, audit_log …). Optional KI-Moderation via Edge Function `moderate`.
- **KI-Herz Schritt 1** (28.06.): `STADTPULS_KI_HERZ_BLUEPRINT.md` (kanonisch, inkl. §2.5 Content-Verticals) + `setup_ki.sql` (bookmarks/interactions/taste_profiles) + `sp-track.js` (spTrack/spBookmarkToggle/spStats).
- **Daten-Frische-Fixes** (28.06.): „Hüt Abig" filtert ab heute (**Schweizer Datum**, `Europe/Zurich`), echte HÜT-LIVE-Zahl; events.html ebenfalls auf CH-Datum; `?kreis=` aus URL wird in gastro/shopping/nachtleben übernommen (Universum→gefilterte Liste).
- **Profile scharf** (28.06.): event-/nachtleben-profil mit echtem Bookmark (bookmarks-Tabelle), View-Tracking, ⏳ Countdown, 📅 .ics-Kalender, ❤️/👁-Live-Zähler (`setup_stats.sql`, RPC `stadtpuls_stats`). Nachtleben-Profil-Lade-Bug (Kategorie-Falle) gefixt; Liste verlinkt Karte+PROFIL-Button aufs Profil.
- **Design v2 + Menü-System** (28.06.): Nachtleben Hero-Glow, editoriale Cards, Filter-„Control-Deck", 🎲 ÜBERRASCH MI (zufälliges Lokal aus gefilterten Resultaten), Full-Screen-Hamburger-Menü, Touch-Cursor-Fix (`cursor:none` neutralisiert auf Touch), SVG statt Emoji in Funktions-Buttons.
- **Kompletter Seiten-Sweep** (01.07.): Einheitliche Nav + Hamburger auf gastro/events/shopping/dating/news; **tote `index.html?page=…`-Links entfernt**; NEWS überall in Nav. **Züridütsch-Pass, 47 Korrekturen** (ZUE, LADED, ZRUGGSETZE, HÜT/MORN, LOKAL NÖD GFUNDE …). Meta-Descriptions bewusst Hochdeutsch (SEO).
- **Momänt & Stories auf der Startseite** (01.07.): §5.5-Flow gebaut — Sektionen „◉ ZÜRI MOMÄNT" + „NEWS & STORIES", Freischalten/Zurückziehen in der Kommandozentrale (Tab Moderation), `setup_momente.sql`.
- **Entschieden:** feedback.html bewusst ohne Footer.

### Session 26.06.2026

- **Footer-Konsistenz:** index/news/nachtleben/nachtleben-profil korrigiert; Legacy-`footer{display:grid}`-Bug entfernt (gastro, gastro-profil, shopping, shopping-profil, dating). Alle 13 Footer-Seiten jetzt identisch. (Commits bis `48f2754`)
- **Kreis-Universum** in index.html integriert: Galaxie + „Frag Stadtpuls"-Suechi + 12 Kreis-Chips.
- **Kreis-Chips redesignt:** Glas-Tiles + volle Namen + Glow für aktiven Kreis.
- **Scroll-Hinweis** an Kreis-Leiste (Fade + „›"-Pfeil, weiter bis 12).
- **Mobile-Pass:** Tilt nur Maus, Resize-Relayout, kompakte Stage, Geometrie verifiziert.
- **Live:** Commit `31f96e0` (`48f2754..31f96e0 main -> main`).
