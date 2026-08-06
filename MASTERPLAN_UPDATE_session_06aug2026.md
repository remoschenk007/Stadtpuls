# STADTPULS — MASTERPLAN-UPDATE · Session 6. August 2026

**Kurz: Riesen-Session. News/Kreis-Ablauf end-to-end fertig, komplette neue Wohnungstausch-Seite unter eigener URL, Sitemaps, IA-Aufräumung, SEO/KI-Feintuning — plus User-Profil-Audit mit erstem Fix (Kreis ändern).**

---

## 0) Grundregeln (unverändert, strikt)
- Remo: Züri, nicht technisch. **Hochdeutsch im Chat, Züridütsch für On-Site-Copy.**
- Terminal: **eine Zeile aufs Mal** (mehrzeilige Pastes zerbrechen). Reihenfolge Git: commit → `git pull --rebase` → push. Vor Push: Beweis-Grep.
- Mac von Alessandra → Committer „Alessandra Christen", egal.
- Kein Fake-/Massen-Content (Google-Penalty). Anon-Supabase-Key absichtlich öffentlich (RLS schützt).
- Hosting: GitHub Pages (statisch, kein Server-Rewrite), Repo `remoschenk007/Stadtpuls`, deployt von `main`. Backend: Supabase.

---

## 1) HEUTE ERLEDIGT & LIVE

### Kreis-News / Storys — Ablauf komplett rund
- **News-Zähler-Bug behoben** (die Kernsache): `renderAll()` auf `/news/` brach ab, weil `renderCats()` fehlte und `renderFeed()` auf ein nicht existierendes `#ns`-Element zugriff → alles nach dem Absturz (inkl. Zähler) lief nicht. Fix: `renderCats()` in `renderAll()` + Null-Guard auf `#ns`. Jetzt zählt „Storys total / Die Wuche" korrekt und tickt bei jedem freigeschalteten Artikel automatisch hoch.
- **Autor-Fix**: Test-Autor „RemoTest" → „Redaktion Stadtpuls" (DB + statische Seiten).
- **Auto-Linkify im Generator** (`generate_kreis_news.py`): URLs im Story-Text werden klickbar; neu auch **sprechende Links** `[Ankertext](URL)`.
- **SEO/KI-Ausbau pro Artikel**: NewsArticle-Schema (articleBody, wordCount, keywords, speakable), FAQPage, BreadcrumbList, TL;DR-Box, echte `<h2>`-Zwischentitel, OG/Twitter, robots.

### Street Parade 2026 — Content-Serie (5 Artikel, kein Duplicate Content)
- Kreis 4 (Safer Party, Haupt-Guide) + neue eigenständige Artikel Kreis 1 (Bellevue/Anreise/Sanität), 2 (Enge/Route-Ende), 5 (Züri-West Afterparty), 8 (Utoquai/See).
- Alle Autor „Redaktion Stadtpuls", Kategorie vereinheitlicht auf **Nachtlebe**, untereinander **mit sprechendem Ankertext** verlinkt (Hub-Struktur).
- SQL-Dateien: `street_parade_kreis_verteilung.sql`, `street_parade_ausbau_verlinkung.sql`.

### Neue Wohnungstausch-Seite → eigene URL `/wohnungstausch/`
- War vorher `/immobilien/#tuusche` (Anker, für SEO wertlos). Jetzt **eigene Keyword-URL** `depuls.ch/wohnungstausch/`.
- `/immobilien/` und `immobilien.html` **leiten sauber weiter** (noindex + canonical auf die neue URL) → kein Duplicate Content, alter SEO-Wert wandert mit.
- Voller SEO/KI-Ausbau: Title „Wohnungstausch Zürich — anonym & gratis matchen", CTA-Description, Rich Schema (WebApplication + HowTo + FAQPage + BreadcrumbList + Speakable), einzigartiger Erklär-Content (Warum tauschen, Dreieckstausch, Vermieter/rechtlich, Vergleich), sichtbare FAQ inkl. **Homegate/ImmoScout24-Frage**.
- **Interne Verlinkung**: alle 12 Kreis-News-Hubs verlinken jetzt mit Keyword-Ankertext aufs Tausch-Tool.
- Recherche-Fazit: Homegate/ImmoScout24 besetzen „Wohnungstausch" bewusst nicht; Tauschwohnung.com/Ron Orp sind national/ohne echtes Match-Tool → klare Nische.
- **Wichtig (aktueller SEO-Fakt):** Google hat **FAQ-Rich-Results per 7. Mai 2026 komplett abgeschafft** (für alle). FAQ-Schema bleibt trotzdem drin — Google liest es zum Verstehen, und **KI-Suchen (ChatGPT/Perplexity/AI-Overviews) ziehen genau dieses Q&A-Format**. FAQ zahlt also auf KI-Suche statt auf klassische Rich-Snippets ein.

### Informationsarchitektur aufgeräumt
- Footer-Link **„Inserat schalte" zeigt jetzt auf `/marktplatz.html`** (allgemeiner Hub für alle Inserate: Läden, Kulturprofile, Minimarket, Wohnungstausch), **nicht** mehr eng auf den Wohnungstausch. Site-weit (~3758 Seiten) + in den 3 Generatoren umgestellt.
- Marktplatz-Seite featured jetzt den **live Wohnungstausch** als erstes Feature (Link).

### Sitemaps
- Neue **`sitemap-news.xml`** (18 URLs: News-Hub + 12 Kreis-Hubs + Story-Detailseiten) im Generator `generate_sitemap.py`, im Sitemap-Index registriert.
- `/wohnungstausch/` in `sitemap-pages.xml`, altes `/immobilien/` raus.
- Google hat Sitemap-Index (`sitemap.xml`, 3800 Seiten) am 6.8. neu eingelesen. `/wohnungstausch/` manuell zur Indexierung eingereicht (Search Console).

---

## 2) USER-PROFIL — AUDIT (Stand heute)

**Datei: `dashboard.html` (= die User-Profil-Seite).** Login/Auth + Profil laden/anlegen (`users`-Tabelle) funktionieren.

### Funktioniert
- Bearbeiten: **Geburtsjahr, Geschlecht, Bio, Interessen, Vibe**, Privacy-/Notification-Toggles (alle schreiben in `users`).
- Punkte-/Rang-System (Anzeige), Notifications-Panel, „Meine Beiträge" (`loadMyNews` aus `news_stories`).
- **Kreis ändern → HEUTE GEFIXT** (war Platzhalter „KREIS ÄNDERE — BALD"): neues Modal mit allen 12 Kreisen, schreibt `users.kreis`. ✅ Direkt Remos Haupt-Anliegen (Umzug).
- Likes auf Storys (`story_reactions`) funktionieren auf den Detailseiten.

### Geht noch NICHT (offene Baustellen im Profil)
1. **Bookmarks** — Tabelle `bookmarks` **existiert** (setup_ki.sql: user_id, ziel_typ, ziel_id, kategorie, kreis, tags), aber **im Frontend nirgends angebunden**: kein „Bookmark"-Button auf Lokal-/Event-/Story-Seiten, kein Laden, kein Zähler (hartcodiert 0), keine Liste im Profil.
2. **Aktivitäts-Stats** (`st-bm` Bookmarks, `st-rv` Reviews, `st-btr` Beiträge, `st-ins` Inserate) — **alle hartcodiert `0`**, nicht mit echten Zahlen verdrahtet (z.B. Beiträge-Zahl aus `loadMyNews` ableiten wäre schnell).
3. **Weitere Platzhalter-Felder**: Nickname ändern, Website, E-Mail = „BALD"/Support.
4. **Likes-Ansicht im Profil** („meine gelikten/gemerkten Sachen") fehlt; Likes/Bookmarks auf Lokalen/Events gibt es noch nicht.
5. „Mini Züri / Universum"-DNA nutzt `bookmarksGastro=0`-Platzhalter.

### Empfohlene nächste Schritte (Profil), priorisiert
- **A. Bookmarks end-to-end** (grösster Nutzen): (1) „Merke/Bookmark"-Button auf Lokal-Seiten (`generate_location_pages.py`) + Event-Seiten, der in `bookmarks` schreibt (login-gated, wie Likes); (2) im Dashboard laden → Zähler `st-bm` + Liste + DNA-Universum füttern.
- **B. Aktivitäts-Stats verdrahten**: `st-btr` aus `loadMyNews`-Count, `st-bm` aus Bookmarks-Count. Schnell.
- **C. Likes-Ansicht** im Profil (aus `story_reactions`).
- (Nickname/Website-Edit = nice-to-have.)

---

## 3) WEITERE OFFENE PUNKTE (Backlog, unverändert offen)
- **Auto-Generator aktivieren** (`kreis-news-auto.yml` → `.github/workflows/` + Repo-Setting „Read and write permissions"): statische Seiten entstehen dann bei jedem freigeschalteten Beitrag von selbst, kein manueller Generator-Lauf mehr.
- **Aufräum-Logik im Generator**: gelöschte/gesperrte Storys hinterlassen verwaiste statische Ordner („Leichen") — Generator sollte sie entfernen.
- **nachtleben-Bug**: `/nachtleben/the-penthouse/` zeigt rohen HTML-Code am Ende der Beschreibung (Doppel-Escaping in `generate_location_pages.py`).
- **Custom SMTP (Hosttech)** für zuverlässige Registrierungs-Mails bei Skalierung.

---

## 4) DATEN / DATEIEN (heute berührt)
- `news/index.html` (Zähler-Fix), `generate_kreis_news.py` (Linkify, Markdown-Links, SEO-Schema, Kreis→Wohnungstausch-Link), `generate_sitemap.py` (sitemap-news + wohnungstausch), `wohnungstausch/index.html` (neu), `immobilien/index.html` + `immobilien.html` (Redirects), `marktplatz.html` (Tuusche-Link), `dashboard.html` (Kreis ändern), alle Haupt- & generierten Seiten (Footer-Link → Marktplatz), 3 Generatoren.
- Neue SQL: `street_parade_kreis_verteilung.sql`, `street_parade_ausbau_verlinkung.sql`.

## 5) STANDARD VERIFIKATION (vor Push)
`node --check` auf extrahierte `<script>`, `py_compile`, JSON-LD via `json.loads`, div/Tag-Balance, Beweis-Grep der Marker.
