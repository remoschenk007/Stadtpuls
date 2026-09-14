# STADTPULS · MASTER-UPDATE · Session Aug–Sep 2026

**Stand:** 12.09.2026 · depuls.ch · Repo `remoschenk007/Stadtpuls` (lokal `/Users/alessandrachristen/stadtpuls/`)
**Für neuen Chat:** Dieses Doc + `STADTPULS_master_v2` + `NEUER_CHAT_BRIEFING.md` lesen.

---

## 0 · Kurzfassung

In dieser Session-Reihe wurde der **komplette AEO-/SEO-Ausbau** abgeschlossen und die **Event-Daten vollständig angereichert**. Technisch ist die Seite jetzt auf Top-Niveau. Der offene Hebel ist **nicht mehr Code, sondern der Cold-Start** (echte Lokale + User) — siehe Abschnitt 5.

---

## 1 · Was erledigt & LIVE ist

### AEO-Block (komplett live)
- **Kreis-Kategorie-Seiten intern verlinkt.** `/gastro/kreis-N/` (+ nachtleben/shopping/kultur) waren crawlbar, aber verwaist. Jetzt: sichtbare, keyword-starke „Nach Kreis"-Navigation auf allen 4 Hubs + „Ässe nach Kreis"-Block auf der Startseite. (commit 29e2f07e3)
- **News↔Gastro pro Kreis verzahnt.** Jede Kategorie-Kreis-Seite verlinkt auf den News-Hub des Kreises und umgekehrt — mit Datei-Existenz-Check (kein 404). (commit 1cd1851e2)
- **News-Hub statisch:** `news/index.html` hat statische 12-Kreis-Fallback-Liste (Progressive Enhancement).
- **Hub-Top-24:** gastro/nachtleben/shopping/kultur.html backen die Top-24-Lokale statisch ins HTML (per `generate_kreis_pages.py`, Marker-Ansatz; nachtleben nutzt `locations-grid` statt `mgrid`). (commit 093aeb891)
- **Profil-Öffnungszeiten:** `openingHours` im Restaurant-Schema von 624/735 Profilen. (commit 57a234f9b)
- **Startseite verifiziert optimal:** Title + keyword-H1, statische „WAS ISCH STADTPULS?"-Prosa, vollständiges JSON-LD (Organization, WebSite+SearchAction, ItemList, FAQPage mit 6 Fragen) — alles **statisch** im HTML. lang=de-CH, Canonical, OG.
- **Fundament:** Sitemap-Index (pages/locations/events/news), robots.txt offen für alle KI-Bots (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, …), `llms.txt` vorhanden.

### Event-Anreicherung (live seit 12.09., commit 0d9657a53)
Auslöser: Remo bemerkte, dass importierte Event-Daten dürftiger waren als die Eventfrog-Quelle.
- **import_eventfrog.py:** zieht jetzt den Volltext `descriptionAsHTML.de` (statt nur `shortDescription`), dazu `organizerName` → `veranstalter` und `emblemCredits` → `bild_credit`. Neuer `_clean_html`-Helper filtert auf sichere Tags (p, br, ul, ol, li, strong, em, b, i, a[href]) — AGB-konform (Inhalt unverändert) + XSS-sicher.
- **Upsert:** mit `SUPABASE_KEY` (service_role) macht der Import `merge-duplicates` und **aktualisiert bestehende Events** (nicht nur neue). Ohne Key sicher Insert-only.
- **generate_event_pages.py:** SSR-Fallback mit Endzeit (09:00–20:00), Veranstalter, Volltext-HTML, Bild-Credit; `uhrzeit_ende`/`veranstalter`/`bild_credit` im select; Meta-Desc per HTML-strip.
- **event-profil.html:** Endzeit im Zeit-Label, Veranstalter-Zeile, Bild-Credit-Overlay, `.profil-desc`-CSS für HTML.
- **DB:** 2 neue Spalten `veranstalter`, `bild_credit` (add_event_columns.sql, ausgeführt).
- **Ergebnis:** letzter Import 3931 Events geschrieben; Volltext in Seiten bestätigt (z. B. 102 B.ARBIE-Seiten mit voller Beschreibung).

### AGB-Klärung Eventfrog (§17 API / §20 Nutzungsrechte, CH-Recht)
Anzeige der API-Daten auf eigener Webseite ist **ausdrücklich erlaubt** (API-Zweck). Auflagen: Inhalt unverändert wiedergeben, täglich aktualisieren + nicht mehr verfügbare Events entfernen, nur zur Event-Ankündigung nutzen, Bild-Copyright zeigen, keine Weitergabe an Dritte, Key sicher.

---

## 2 · Aktueller Live-Zustand (Systemüberblick)

- **Seiten live:** index, gastro, nachtleben, shopping, kultur, events, news/ (+12 Kreis-News-Hubs), 28 Kreis-Kategorie-Seiten, ~735 Profilseiten, ~3000 Event-Detailseiten, wohnungstausch/, dating/community/etc., platzierung, login/dashboard, impressum, datenschutz.
- **Auth komplett** (Registrierung→Mail→Onboarding→Dashboard, Passwort-Reset, Account-Löschen revDSG).
- **Kommandozentrale v3**, Momänt-Feedback-Loop, Boost-System sichtbar auf Startseite.
- **Auto-Sync:** GitHub Action täglich (Eventfrog + Zürich Tourismus → Supabase), generiert Sitemaps + Kreis-Seiten.

---

## 3 · Technische Stolpersteine & Workflow-Regeln (WICHTIG für nächsten Chat)

1. **service_role-Key für Bestandsevent-Updates:** Der Import aktualisiert bestehende Events nur mit gesetztem `SUPABASE_KEY` (service_role, aus Supabase Settings→API, Secret Key `sb_secret_…`). Ablauf: `export SUPABASE_KEY='<key>'` → `python3 import_eventfrog.py` (Modus muss „🟢 WRITE (+ Update & Cleanup)" zeigen). **Key ist Secret:** nur env, nie in Code/Commit, danach `unset SUPABASE_KEY`. Platzhalter-Fehler vermeiden — echten Key einsetzen (sonst HTTP 401 / latin-1-Crash bei `…`-Zeichen im Key).
2. **Sitemap-/Event-Merge-Konflikt (wiederkehrend!):** Der nächtliche Sync benennt Event-Ordner um/löscht sie, während man lokal welche baut → `rename/rename`- und `rename/delete`-Konflikte beim Push. **Lösung:** `git checkout --ours .` → `git add -A` → `git commit --no-edit` → `git push`. **Besser vorbeugen:** IMMER `git pull origin main` VOR dem lokalen Generieren (bei sauberem Tree = fast-forward, kein Konflikt). TODO-Idee: lokalen Lauf so bauen, dass er automatisch erst pullt.
3. **Event-Fetch-Limit:** Import holt ~4000 von ~7000+ Events. Sehr weit in der Zukunft liegende Events behalten evtl. noch den kurzen Text. Bei Bedarf Fetch-Umfang erhöhen (Paging/MAX_PAGES).
4. **`cancelled`-Feld unzuverlässig:** Eventfrog liefert teils `cancelled:true` bei laufenden Events → NICHT als Filter nutzen.
5. **GitHub-Pages-Cache:** nach Push ~Minuten Verzug; zum Verifizieren Commit-SHA in der raw-URL nutzen oder `?v=2` im Privat-Tab.
6. **Deploy-Disziplin:** Multi-Line-Patches immer als ZIP liefern (Terminal zerbricht Heredoc-Paste). Python-`str.replace` mit `assert count==1`. Nach unzip immer Beweis-grep. `py_compile` vor Push.
7. **`insert_ku_live.py`** = altes Einmal-Skript für Startseiten-Kreis-Galaxie, unabhängig von Events. „Marker 0x" → ignorieren.

---

## 4 · Offene Punkte (priorisiert)

1. **Money-Loop / Bezahl-Link (Umsatz = CHF 0):** `platzierung.html` steht auf `PAYMODE='manual'` — Wirt sieht „MERCI", aber keine Zahlungsinfo. *Option A (schnell):* TWINT/IBAN + Referenz auf MERCI-Seite. *Option B:* Stripe (create-checkout + webhook bereits programmiert) scharfschalten (Konto/Secrets macht Remo selbst). Dazu: „Das isch mis Lokal"-Button auf alle Profilseiten (→ platzierung.html?id=…), Listen-Sortierung nach `boost_tier`, Badges.
2. **Custom SMTP** (`no-reply@depuls.ch` via Hosttech) — Launch-Blocker (Supabase-Mail hat Rate-Limits).
3. **Kleinigkeiten:** `agb.html` fehlt (Footer-Link tot); `cleanup_demo.sql` ausführen; KI-Herz Schritt 2 (taste-build/„Für dich"-Feed).
4. **Niedrig:** ~3762 generierte Seiten verlinken Nav/Footer auf `/news.html` statt `/news/` (Redirect-Hop, für Google harmlos). Optional via Generator-Nav-Template.

---

## 5 · Ehrliche strategische Einordnung (bitte lesen)

**Die Technik ist fertig und exzellent.** Weitere Code-Optimierung bewegt die Suchzahlen NICHT.

**Traffic-Realität (GSC, Sept 2026):** Ø-Position ~19–25 (Seite 2–3), CTR ~1 %, ~509 Klicks / 36k Impressionen (3 Monate). Die Delle seit August ist **klassische „Honeymoon"-Normalisierung** nach der Massen-Indexierung Ende Juli — sie begann VOR den SEO-Änderungen und ist NICHT durch die Arbeit verursacht. Viele 1-Impression-Nischenqueries = Signatur zu vieler dünner Auto-Seiten.

**Was die Nadel jetzt bewegt (nicht Code):**
- **Cold-Start:** die ersten ~10 zahlenden Lokale und ~50 aktive User holt Remo persönlich → echte Nutzersignale → mehr Google-Vertrauen.
- **Autorität/Erwähnungen:** Links/Nennungen von anderen Zürcher Seiten, lokalen Blogs, Reddit.
- **Qualität statt Quantität:** wenige gehaltvolle Seiten schlagen tausende dünne (genau wozu die Event-Anreicherung dient). Ggf. überlegen, ob alle Auto-Seiten indexiert bleiben sollen.
- **Chance-Nische:** „wohnungstausch zürich" (Top-Query, 119 Impr) — wenig Konkurrenz, gezielt ausbauen.

**Recovery** ist nicht garantiert und braucht Wochen. Der ehrliche nächste Schritt ist Vertrieb/Community, nicht ein weiterer technischer Fix.

---

## 6 · Stil-/Arbeitsregeln (unverändert)
Vollgas, proaktiv, **Diagnose vor Fix**, alles validieren, eigene Fehler offen zugeben und korrigieren, Schritt-für-Schritt mit Beweis-Checks, PM-Blick aufs Ganze. Hochdeutsch mit Remo, Züridütsch für On-Site-Copy (Ausnahme: SEO/FAQ/Meta bewusst Hochdeutsch). Design-DNA: bg #04040a · rot #ff2d00 · volt #c8ff00 · Barlow Condensed Italic 900 + DM Mono · Hex nie CSS-Var · Emojis nie als Funktions-Icons (SVG).
