# STADTPULS — KI-HERZ & MONETARISIERUNG · BLUEPRINT
**Stand:** 28. Juni 2026 · **Pflege:** lebendes Dokument (wie der Masterplan). Jede Session ergänzt unten im Changelog.
**Zweck:** Komplette Übereinstimmung zwischen Remo, Claude (auch neue Chats) und dem System. Wer hier liest, weiss, *was* wir bauen, *warum*, *womit* und *in welcher Reihenfolge*.

---

## 0 · LEITGEDANKE
Stadtpuls soll nicht „noch ein Lokalverzeichnis" sein, sondern **die App, die jedem Zürcher genau das zeigt, was ihn jetzt interessiert** — und ihm Bescheid gibt, bevor es alle wissen. Das Herz dafür ist ein **personalisierter Empfehlungs- & Benachrichtigungs-Motor**: *Wer ist der User? Was will er? Was findet er geil? — und wie kriegen wir diese Daten sauber?*

Zwei Wahrheiten, an denen wir uns ausrichten:
- **Wahrheit lebt in der DB. Die KI halluziniert nie Lokale.** Deterministische Engine zuerst, LLM-Magie (ZÜRI-BOT) später obendrauf.
- **Gratis muss gut sein.** Geld kommt über *mehr* Sichtbarkeit (Boosts/Pro), nie über eine Mauer. Ziel: ~CHF 3'000/Monat — das sind ein paar Dutzend zahlende Lokale, kein Massengeschäft.

---

## 1 · WAS WIR ÜBER JEDEN USER SCHON WISSEN  (Tabelle `users`)
Das Onboarding (`onboarding.html`, 5 Schritte) schreibt bereits in `users` (via `auth_id`):

| Feld | Werte | Quelle |
|---|---|---|
| `kreis` | 1–12 | Schritt 1 |
| `interessen` | text[] aus: `GASTRO, NACHTLEBE, SHOPPING, EVENTS, JOBS, WOHNE, KULTUR, WELLNESS` | Schritt 2 |
| `vibe` | `NACHTMENSCH, STADTMENSCH, MUSIKMENSCH, FOODIE, DATESMENSCH, AKTIVMENSCH` | Schritt 3 |
| `geburtsjahr` | Jahr (→ Alter, 18-Gate für Nachtleben/Dates) | Schritt 3 |
| `notification_typen` | text[] aus: `pulse_moment, popup_event, ki_top_pick, kreis_battle` | Schritt 4 |
| `bio`, `bookmarks_oeffentlich`, `nickname`, `id`, `auth_id` | — | Profil/Dashboard |

**Wichtig:** Die Notif-Typen sind schon definiert und matchen exakt unser Ziel:
- `popup_event` → „Neui Events & Pop-Ups in dim Kreis — bevor's jede weiss"
- `ki_top_pick` → „Persönlichi Empfehlige basierend uf dim Vibe"
- `pulse_moment` → „Kreis explodiert, 500+ gliichzitig"
- `kreis_battle` → „Kreisrivalität"

→ **Fundament steht.** Wir fragen beim Anmelden schon das Richtige ab.

---

## 2 · WAS WIR ÜBER DIE INHALTE WISSEN  (Matching-Material)
- **`locations`**: `kategorie` (gastro/nachtleben/shopping/kultur/sport/wellness), `subkategorie`, `kreis`, **`stimmung_tags`**, `lat`/`lng`, `rating`, `oeffnungszeiten`, `featured`, `boost_until`, `boost_tier`, `aktiv`.
- **`eventfrog_events`**: `kategorie`, `kreis`, `datum_start`/`datum_ende`, **`popup`** (Pop-up-Flag), `venue_name`, `titel`, `bild_url`, `ticket_url`, `aktiv`. Wird vom **Auto-Sync täglich** befüllt (GitHub Action 04:00).
- **`dating_votes`**: `vote` (ja/nein) — echtes Verhaltens-Signal.

Filter/Suche, die es heute gibt (Taxonomie für's Matching): Kreis · subkategorie/Küche · `stimmung_tags` · „JETZT OFFE" · Freitext `?q=` (SearchAction). GPS-Radius-UI existiert in `gastro.html`, ist aber Platzhalter.

---

## 2.5 · CONTENT-VERTICALS — ALLES fliesst in EINE DNA
Das Herz ist **content-agnostisch**: `ziel_typ` verallgemeinert jeden Typ. Ein User hat **EINE** Geschmacks-DNA, gespeist aus ALLEN Verticals. Wer Pizza bookmarkt, Food-Stories liest und einen Food-Markt liked, verstärkt alle „food"-Tags. Der „Für dich"-Feed mischt das Beste aus allen Verticals; Push respektiert die `notification_typen`.

| Vertical | Tabelle | `ziel_typ` | Haupt-Signal | Bookmark = | Push | Notiz |
|---|---|---|---|---|---|---|
| Gastro/Nachtleben/Shopping/Kultur/Sport/Wellness | `locations` | `location` | view_profile, „jetzt offe", bookmark | merken | popup_event, ki_top_pick | Kern, läuft |
| Events & Pop-ups | `eventfrog_events` | `event` | view, bookmark | merken | popup_event | Pop-up-Flag = zeitkritisch |
| **People & Dates** | `dating_votes` (+ Profile) | `date_profile` | swipe ja/nein (**stärkstes Signal**) | geliked/gemerkt | „neues Match/Like in dim Kreis" | **18+**, Privacy heikel, eigene Achse |
| **Minimarket / Marktplatz** | `inserate` | `inserat` | view, Kontakt-Klick, bookmark | merken | „neues Inserat in dinere Kategorie" | Moderation aktiv |
| **News & Stories** | `news_stories` | `news` | öffnen, Lesezeit, save | speichern | „neui Story us dim Kreis" | Moderation aktiv |
| **Musik & Sound** | `musik` (Seite folgt) | `musik`/`set`/`artist` | abspielen/hören, save | merken | „neui Session/Set" | Seite noch bauen (Masterplan §170) |
| Jobs | `jobs` | `job` | view, „bewerben"-Klick, save | merken | „neui Stell Gastro/Nightlife" | Umsatz-Säule (Job-Börse) |
| Wohnen/Immobilien | `immobilien` | `immobilie` | view, save | merken | „neui Wohnig im Kreis" | optional |

**Vertical-spezifische Regeln:**
- **People & Dates:** 18+ zwingend. Likes/Votes sind sensibel → NIE öffentlich ohne Consent; „öpper het dich gliked"-Push nur opt-in. Eigene DNA-Achse `dating`, getrennt von Gastro-Geschmack.
- **Pop-ups/Events:** zeitkritisch → höchste Push-Priorität (das „bevor's jede weiss").
- **News/Stories:** Lesezeit als Signalstärke (kurz angetippt ≠ gelesen).
- **Marktplatz/Jobs/Immobilien:** Match v.a. über Kategorie + Kreis (weniger „Stimmung").
- **Musik:** sobald die Seite steht, sofort mit `sp-track.js` verdrahten (gleiche Bookmarks/Interactions).

→ **Konsequenz:** `bookmarks.ziel_typ` und `interactions.ziel_typ` sind bewusst freie Text-Felder (kein Enum), damit jeder neue Vertical ohne Schema-Änderung andockt. Der Matcher (Schritt 3) iteriert über alle Typen.

---

## 3 · WAS FEHLT  (die Lücken zum „Herz")
1. **Bookmarks werden NICHT gespeichert** — im Code steht „bookmarks Tabelle noch nicht angebunden". Stärkstes Signal geht verloren. → **Schritt 1 fixt das.**
2. **Keine Verhaltens-Spur** (Views/Klicks/Filter). Profil ist statisch (nur Onboarding), lernt nicht. → **Schritt 1.**
3. **Kein Geschmacks-Profil** (berechnete DNA). → Schritt 2.
4. **Kein Matcher**, **kein „Für dich"-Feed**. → Schritt 3.
5. **`notifications` wird nur gelesen** (Bell im Dashboard), nie befüllt. → Schritt 4.
6. **Kein Web-Push**, **kein echtes GPS**. → Schritt 5 (App-Moment).

---

## 4 · DAS KONZEPT — „GESCHMACKS-DNA"
Pro User ein lebender Satz Tag-Gewichte, z.B.
`{ "pizza":0.8, "italienisch":0.7, "kreis-4":1.0, "spätabends":0.6, "techno":0.3 }`

Eine DNA, gespeist aus **allen Verticals** (§2.5) — Gastro, Events, Dates, Marktplatz, News, Musik, Jobs, Wohnen. Quellen:
- **Explizit** (haben wir): Onboarding Kreis/Vibe/Interessen → Startgewichte (Kaltstart gelöst).
- **Implizit** (Schritt 1 sammelt): Bookmark = starkes +, Dates-Vote „ja" = +, Profil lang offen = leichtes +, „jetzt offe" geklickt = Gewohnheit, Suche/Filter = explizite Absicht. Jedes Signal verschiebt die DNA.

### Der Matcher (deterministisch, läuft immer)
Score eines neuen Items (Pop-up/Event/Location) für einen User =
`w1·KreisTreffer + w2·TagÜberlappung(stimmung_tags ∩ DNA) + w3·Vibe/Interessen-Match + w4·Frische + w5·Nähe(GPS, später) + w6·Angesagt(pulse)`.
Startgewichte grob: Kreis 1.0, Tags 1.5, Vibe/Interessen 1.0, Frische 0.8, Nähe 1.2, Angesagt 0.5. (Tunebar.)

### Zwei Ausgänge, eine Engine
- **„FÜR DICH"-Feed** (Pull): personalisierte Startseite. „Friitig Kreis 4 — wie immer?" (Die `ki-card` in `gastro.html` deutet das schon an.)
- **Benachrichtigung** (Push): dieselben Top-Scores → Zeilen in `notifications`, gefiltert nach den `notification_typen` des Users. Später Web-Push.

---

## 5 · DATENMODELL (neu)
> Schritt-1-Tabellen sind in `setup_ki.sql`. Schritt-2+ hier als Spezifikation festgehalten.

### `bookmarks` (Schritt 1) — explizites Top-Signal
`id uuid pk · user_id uuid · ziel_typ (location|event|date_profile|inserat|news|musik|job|immobilie) · ziel_id text · kategorie text · kreis int · tags text[] · created_at` · UNIQUE(user_id,ziel_typ,ziel_id) — **ziel_typ ist freier Text, jeder neue Vertical dockt ohne Migration an**

### `interactions` (Schritt 1) — leichtes Verhaltens-Log
`id bigint pk · user_id uuid (null=anon) · aktion (view_profile|click|open_list|filter|search|vote) · ziel_typ · ziel_id · kategorie · kreis · tags text[] · meta jsonb · created_at` · Index(user_id,created_at)

### `taste_profiles` (Schritt 2) — die berechnete DNA
`user_id uuid pk · tags jsonb (tag→gewicht) · kategorien jsonb · top_kreis int · vibe text · updated_at` — wird periodisch (Edge Function/Cron) aus Onboarding + bookmarks + interactions + dating_votes neu berechnet.

### `notifications` (existiert, Schritt 4 befüllt sie)
`id · user_id · typ · titel · text · gelesen bool · created_at` — Bell liest schon. Generator schreibt rein.

---

## 6 · BAU-REIHENFOLGE (Status)
1. **Signale einsammeln** — `bookmarks` + `interactions` Tabellen + `sp-track.js` Modul. **← JETZT (Schritt 1, in Arbeit)**
   - Danach: Bookmarks in `gastro.html`/`dashboard.html` etc. anbinden (Herz-Button), `spTrack()` auf Profil-Views/Filter streuen.
2. **Geschmacks-DNA** — `taste_profiles` + Berechnungs-Funktion (Edge Function `taste-build`, Cron).
3. **Matcher + „Für dich"-Feed** — Edge Function/Query, neue Sektion auf Startseite/Dashboard.
4. **Benachrichtigungs-Generator** — Edge Function `notify-build`: matcht neue Pop-ups gegen Profile + `notification_typen`, schreibt `notifications`. (Hängt am Auto-Sync.)
5. **Web-Push** → dann **GPS/PWA/App** — der „App-Moment".

---

## 7 · EHRLICHE REALITÄTS-GRENZEN (nicht vergessen!)
- **Kein E-Mail-Feld in `users`** (bewusst, GDPR) → Benachrichtigung läuft über **In-App + Web-Push**, nicht Mail.
- **Web-Push:** Android/Desktop top; **iPhone nur als installierte PWA** (Safari, „zum Home-Bildschirm"). 100% Push auf allen iPhones = erst mit App.
- **GPS-„du bist in der Nähe" im Hintergrund:** Browser kann das nicht zuverlässig (Seite zu). Während App offen: ok. Background-Geofencing → native App/PWA.
- → **Deshalb: deterministische Engine + In-App-Feed zuerst.** Push/GPS sind Ausbaustufen, kein Startblocker.

---

## 8 · MONETARISIERUNG (Stand unseres Denkens)
Ziel **~CHF 3'000/Monat** (Remo will im Ausland gut leben). Kein „Geldmaschinen"-Look.

**Schon gebaut (Kommandozentrale v3 + platzierung.html):**
- **Boosts** = bezahlte Platzierung MIT Ablaufdatum (Featured 20 / Boost 50 / Premium 100 pro Woche; 1/2/4 Wochen). Countdown, Auto-Ablauf, Verlängern/Stoppen.
- **Claim-Flow** (`platzierung.html`): Inhaber meldet sich („Das isch mis Lokal"), wählt Tier+Tage, **zahlt**, Remo **verifiziert & schaltet frei** in der Zentrale (Tab „Verkauf"). Entscheidung: *Freischalten erst nach Remos Freigabe.*
- **Zahlung-Empfehlung:** **Stripe + TWINT** (TWINT Pflicht in CH, via Stripe-Dashboard ohne Extra-Vertrag, ~2.9%). **Start: Manuell-Modus** (PAYMODE='manual'), Stripe-Functions liegen bereit (`create-checkout`, `stripe-webhook`). Günstigere CH-Alternative später: Payrexx/wallee (~1.35–1.65%).

**Künftige Umsatz-Säulen (priorisiert):**
1. **Pro-Abo für Lokale** (wiederkehrend, der grösste Hebel): selbst posten, Verifiziert-Badge, **Statistiken** (Views/Klicks — kommen aus `interactions`!). ~CHF 19–49/Mt. *100 Pro-Abos = Ziel erreicht.*
2. **Job-Börse** (schnellster Franken, baut auf JARVIS auf): Stelleninserate CHF 30–100.
3. **Nativer „Sponsored Spot"** statt Werbebanner (über Boost-System; Ästhetik bleibt).
4. **Affiliate** auf Reservationen/Tickets (passiv, skaliert mit Traffic).
5. **Stadtpuls Deals** (Happy Hour etc., Provision; zieht zusätzlich User).

→ **Synergie:** Das KI-Herz (`interactions`) liefert genau die **Statistiken**, die das Pro-Abo verkaufbar machen. Erst Signale sammeln, dann Pro-Abo.

**Traffic/Realismus:** Word-of-Mouth kommt NACH dem ersten Schub, nicht davor. Erste 50–100 Lokale + erste User selbst holen (Quartier für Quartier). Realistisch 6–18 Monate bis 3'000/Mt. Google/KI-Index = auffindbar, noch nicht Traffic.

---

## 9 · KONVENTIONEN (gelten überall)
- **Supabase:** `SU='https://pnynkzrqnfoshojqfqxn.supabase.co'`, anon-Key public im Code. Supabase **Auth** ist im Einsatz (`sb.auth.getUser()`), `users.auth_id` ↔ `auth.uid()`.
- **Design-DNA:** bg `#04040a`, rot `#ff2d00`, volt `#c8ff00`, cyan `#00f5ff`, purple `#9333ea`, pink `#ec4899`, cream `#e8e4d9`. Barlow Condensed Italic 900 (Headlines), DM Mono (Body). **Hex immer, nie CSS-var.** Sprache: Hochdeutsch mit Remo, **Züridütsch** für On-Site-Copy.
- **Workflow:** Claude baut in `/mnt/user-data/outputs/`, validiert (Div-Balance, `node --check`), zippt, `present_files`. Remo lädt runter (ZIP! Terminal-Paste korrumpiert) und pusht selbst: `git add … && git commit … && git pull --rebase origin main && git push origin main`. „Your name and email…" = Info, kein Fehler.
- **Auto-Sync:** GitHub Action `stadtpuls-sync.yml` täglich 04:00 (Eventfrog + ZT → Supabase). `import.html` ist archiviert/gelöscht.
- **Kommandozentrale:** `kommandozentrale.html` (Login-gated). Tabs: Übersicht, Moderation, Anfragen, Verkauf, Boosts, Finanzen, Users, Inhalte, System, KI, Audit. KI-Moderation via Edge Function `moderate` (optional scharf).

---

## 10 · OFFENE PUNKTE / NÄCHSTE SCHRITTE
- [ ] **Schritt 1 fertig anbinden:** Herz-Button (Bookmark) in `gastro.html`, `shopping.html`, `nachtleben.html`, `events.html`, Profilseiten; `spTrack()` auf Profil-Views + Filter.
- [ ] Boost öffentlich sichtbar machen: Listen-Queries nach `featured`/`boost_tier` sortieren (Boost-Kreis schliessen).
- [ ] „Das isch mis Lokal"-Button in die Profilseiten einbauen (Link zu `platzierung.html?id=…`).
- [ ] Schritt 2: `taste-build` Edge Function.
- [ ] Entscheidung Pro-Abo: wann starten (nach genug `interactions`-Daten für sinnvolle Statistiken).

---

## CHANGELOG
- **2026-06-28 (b)** — §2.5 Content-Verticals ergänzt: People&Dates, Minimarket, News&Stories, Musik&Sound, Jobs, Immobilien — alle plugen via freiem `ziel_typ` in EINE DNA. Vertical-Regeln (18+ Dates, Lesezeit News, Push-Prio Pop-ups) festgehalten.
- **2026-06-28** — Blueprint erstellt. Daten-Audit abgeschlossen (User-Profil-Felder, Content-Felder, Lücken). Konzept Geschmacks-DNA + Matcher + 2 Ausgänge festgehalten. Monetarisierung (Boosts/Claim/Stripe-TWINT manuell-first) dokumentiert. **Schritt 1 gestartet** (bookmarks + interactions + sp-track.js).
