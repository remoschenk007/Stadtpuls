# STADTPULS — KOMPLETT BRIEFING

> Stand: 07. April 2026 — Für neue Chat-Sessions

-----

## 1. WER BIN ICH

**Name:** Remo Schenk
**GitHub:** remoschenk007
**E-Mail:** remoschenk@me.com
**Hintergrund:** Ehemaliger Gründer Homespeed.ch
**Arbeitsgerät:** iPad
**Sprache:** Schweizerdeutsch / Deutsch

-----

## 2. WAS IST STADTPULS

**Tagline:** «dä puls vo dä stadt»
**Konzept:** Interaktiver Lifestyle & City Guide Zürich
**Prinzip:** Shopping Center — alles auf einer Plattform
**Strategie:** Zürich first, perfekt machen → Hamburg, Berlin
**Monetarisierung:** Gratis für User. Revenue via Partner.
**Copyright:** © 2026 by raimondo*

**Live:** https://remoschenk007.github.io/Stadtpuls
**GitHub:** https://github.com/remoschenk007/Stadtpuls

**Social Media:**

- Instagram: @stadtpuls_zh
- Gesichert: @stadtpuls_hamburg, @stadtpuls_berlin

-----

## 3. DESIGN-DNA

```
#04040a  — Midnight-Schwarz (Hintergrund)
#ff2d00  — Lava-Rot (Akzent 1)
#c8ff00  — Volt-Grün (Akzent 2)
#00f5ff  — Cyber-Cyan (Akzent 3)
#9333ea  — Lila (Dating)
#e8e4d9  — Warm-Weiss (Text)

Fonts:
- Barlow Condensed Italic 900 (Headlines)
- DM Mono (Body/Code)
- Bebas Neue (Logo)

Spezial:
- Dualer Cursor (roter Punkt + Ring mit Lag)
- Doppel-Ticker (gegenläufig)
- Scan-Lines im Hero
- Grid-Overlay
- Reveal-Animationen (IntersectionObserver)
```

-----

## 4. TECH-STACK

```
Frontend:   HTML / CSS / JS (Vanilla)
Hosting:    GitHub Pages (gratis)
Editor:     GitHub Web Editor (iPad)
Backend:    Supabase (Phase 4, gratis Tier)
DB:         PostgreSQL via Supabase
Auth:       Supabase Auth
KI:         Claude Pro (Anthropic)
```

-----

## 5. AKTUELLE DATEISTRUKTUR

```
Stadtpuls/
├── index.html              (1256 Zeilen — Shell)
├── hero.jpg                (Remos Züri-Nacht-Foto)
├── STADTPULS_BRIEFING.md
├── STADTPULS_SESSION_07_APRIL_2026.md
├── css/
│   ├── base.css            (Reset, Variablen, Cursor)
│   ├── components.css      (Nav, Buttons, Cards, Footer)
│   └── layout.css          (Hero, Subpages, Responsive)
└── js/
    └── app.js              (Router, Cursor, Reveal, GPS)
```

-----

## 6. ROADMAP STATUS

```
Phase 1  → Frontend         ✅ FERTIG
Phase 2  → Modularisierung  ✅ FERTIG (07.04.2026)
Phase 3  → Zürich API       ⏳ NÄCHSTER SCHRITT
Phase 4  → Supabase Backend ⏳ Geplant
Phase 5  → Partner-Logins   ⏳ Geplant
Phase 6  → KI Features      ⏳ Nach Launch
Phase 7  → Hamburg, Berlin  ⏳ Geplant
Phase 8  → Kaufangebot      ⏳ Kommt von alleine
```

-----

## 7. ZEITPLAN

```
April    → Filter & Tabs Review (JETZT)
April    → Phase 3: Zürich API einbinden
Mai      → Phase 4: Supabase + Login
4. Juni  → SOFT LAUNCH 🎂🔴
Sommer   → User sammeln
Herbst   → Partner klopfen an
```

-----

## 8. NÄCHSTER SCHRITT — VOR API!

**Erst Filter & Tabs definieren — dann Daten einspielen!**
Sonst landet alles am falschen Ort.

```
Events:     Afternooner, Theater, Oper, Film?
Nachtleben: House, Techno, Jazz, Afterhour?
Gastro:     Preis-Filter, Quartier-Filter?
Kultur:     Eigene Seite oder unter Events?
Shopping:   Sale, Lokal, International?
Community:  Spontan, Nachbarschaft?
```

-----

## 9. BEKANNTE BUGS — SOFORT FIXEN

```
Nachtleben  → kein <div id="fnacht">   → kein Footer
Immobilien  → kein <div id="fimmo">    → kein Footer
Marktplatz  → kein <div id="fmarkt">   → kein Footer
```

Fix: Bei jeder Page vor `</div>` einfügen:

```html
<div id="fnacht"></div>
<div id="fimmo"></div>
<div id="fmarkt"></div>
```

-----

## 10. PHASE 3 — ZÜRICH TOURISMUS API

```
URL:     https://www.zuerich.com/en/api/v2/data
Lizenz:  CC BY-SA (gratis, frei nutzbar)
Daten:   Restaurants, Bars, Events, Hotels,
         Kultur, Theater, Oper, Shopping,
         Festivals, Live Music, Museen
Bilder:  Ja, inklusive
GPS:     Ja, Koordinaten inklusive
```

**Weitere gratis APIs:**

```
Guidle AG      → Lokale Events, Partys
ZVV API        → Live-Abfahrtszeiten
Meteo Schweiz  → Wetter live
Stadt Zürich   → 900+ Datensätze, Geodaten
OpenStreetMap  → Karten, GPS-Layer
```

-----

## 11. BACKEND STRATEGIE

```
Schicht 1 — Externe APIs
→ Zürich Tourismus, Guidle, OpenStreetMap
→ Gastro, Events, Karten — gratis

Schicht 2 — Supabase (gratis)
→ User-Profile, Reviews, Posts
→ PostgreSQL + PostGIS für Geo-Suche
→ Bis 500MB gratis

Schicht 3 — Cache
→ Daten zwischenspeichern
→ Schnell, effizient

Skalierung: Gratis bis 50'000 User!
```

-----

## 12. MONETARISIERUNG

```
Phase A → Zürich API, User sammeln
Phase B → 1000+ User → Partner kontaktieren
Phase C → Revenue Share automatisch

OpenTable    → CHF 1-5 pro Buchung
Ticketcorner → 5-10% pro Ticket
Scout24      → Pay per Lead
```

**Stadtpuls verdient im Schlaf!** 🔴

-----

## 13. USER GEWINNUNG

```
→ Community Content
   Echte Züri-Menschen, Geheimtipps

→ Live-Daten
   «Jetzt offen» «Noch 3 Plätze» «In 1h»

→ Dating & People
   Täglicher Magnet

→ Jobs & Marktplatz
   Täglich praktisch relevant

→ GPS Hyper-Lokal
   «Was ist 200m von mir?»

→ News & Stories
   Lokale Blogger, Quartier-News
```

-----

## 14. USER ONBOARDING — VISION

**5 Schritte, spielerisch, progressiv:**

```
Schritt 1 → Nickname
Schritt 2 → Quartier wählen
Schritt 3 → Interessen (Multi-Select)
Schritt 4 → Alter (optional, für Dating)
Schritt 5 → «Willkommen @nickname!» 🎉
```

User merkt nicht dass er Daten gibt.
70% Absprung-Rate bei komplizierten Formularen!

-----

## 15. GEO-TARGETING — VISION

```
GPS erkennt: Kreis 4, Langstrasse
↓
Zeigt automatisch:
→ Restaurant 200m — Tisch frei
→ Event heute Abend — 350m
→ Club offen — 180m
→ WG im gleichen Quartier
→ Jobs in der Nähe
```

PostGIS (Supabase) für Radius-Suche — gratis!

-----

## 16. SEO STRATEGIE

```
Phase 3 → Basis SEO
          Meta Tags, Schema.org, Open Graph

Phase 4 → Technisches SEO
          URL Routing (/gastro /events)
          Ladezeit unter 2 Sekunden

Phase 5 → Content SEO
          Community schreibt täglich
          Google indexiert täglich

Phase 6 → KI-Suche
          Google AI Answers
          Perplexity, ChatGPT Search
```

**Ziel:**
Jemand fragt Google: «Was läuft heute in Zürich?»
Google AI antwortet: «Laut Stadtpuls…» 🔴

-----

## 17. KI FEATURES — PHASE 5-6

```
1. Züri-Bot
   «Was mach ich heute Abend?»
   KI kennt Quartier, Wetter, Interessen

2. Personalisierter Feed
   KI lernt was du magst
   Besser mit jeder Nutzung

3. Video Import
   Instagram/TikTok Video importieren
   KI erkennt Züri-Locations automatisch

4. Predictive Events
   «Freitag Abend — Kreis 4 — wie immer?»

5. Stimmungs-Matching
   Müde / Energetisch / Romantisch
   KI findet perfekten Match

6. Push Alerts Hyper-Lokal
   «Event 200m von dir — startet in 30min»
```

-----

## 18. KOMMUNIKATION & TON

```
Sprache:   Schweizerdeutsch / Züri-Slang
Ton:       Direkt, kein Bullshit, authentisch

Phrasen:
«dä puls vo dä stadt»
«Was lauft i däre stadt?»
«Kei Umwäg»
«Echts Züri»
«Kei Chichi»
«Mir sind Matchmaker»
«Keis Rumsurfe»
```

-----

## 19. ARBEITS-HINWEISE

```
- Remo arbeitet auf iPad
- Immer Datei für Datei
- Nie zu viel auf einmal
- Code als Text im Chat — zum Kopieren
- Neue Konversation pro Thema
- Claude Pro Limit Di 08:00 reset
```

-----

## 20. VISION

> «Was TAMEDIA, Axel Springer und Scout 2006
> nicht geglaubt haben — bauen wir 2026 mit KI,
> einem iPad, GitHub und null Budget.
> Zürich first. Dann die Welt.» 🔴

-----

*© 2026 by raimondo* — Stadtpuls — Zürich*
*«dä puls vo dä stadt»*
