# STADTPULS — Projekt Briefing

> Dieses Dokument am Anfang jeder neuen Chat-Session einlesen.
> Letzte Aktualisierung: April 2026

-----

## 1. WER BIN ICH

**Name:** Remo Schenk  
**GitHub:** remoschenk007  
**E-Mail:** remoschenk@me.com  
**Hintergrund:** Ehemaliger Gründer von Homespeed.ch (grosses Schweizer Immobilienportal)  
**Arbeitsgerät:** iPad  
**Sprache:** Schweizerdeutsch / Deutsch

-----

## 2. WAS IST STADTPULS

**Tagline:** «dä puls vo dä stadt»  
**Konzept:** Interaktiver Lifestyle & City Guide für Zürich — «Shopping Center Prinzip», alles auf einer Plattform.  
**Vision:** Was 2006 als Idee begann, wird 2026 mit KI gebaut.  
**Strategie:** Zürich first, perfekt machen — dann Hamburg, Berlin.  
**Monetarisierung:** Gratis für User. Kooperationen mit Partnern. Später Kaufangebot.  
**Copyright:** © 2026 by raimondo*

**Social Media:**

- Instagram: @stadtpuls_zh
- Auch gesichert: @stadtpuls_hamburg, @stadtpuls_berlin

**GitHub Live:** https://remoschenk007.github.io/Stadtpuls

-----

## 3. DESIGN-DNA

```
Hintergrund:    #04040a  (Midnight-Schwarz)
Akzent 1:       #ff2d00  (Lava-Rot)
Akzent 2:       #c8ff00  (Volt-Grün)
Akzent 3:       #00f5ff  (Cyber-Cyan)
Akzent 4:       #9333ea  (Lila / Dating)
Text:           #e8e4d9  (Warm-Weiss)

Fonts:
- Headlines:    Barlow Condensed Italic 900
- Body/Code:    DM Mono
- Logo:         Bebas Neue

Spezial-Features:
- Dualer Cursor (roter Punkt + Ring mit Lag)
- Doppel-Ticker (gegenläufig)
- Scan-Lines im Hero
- Grid-Overlay
- Reveal-Animationen (IntersectionObserver)
```

-----

## 4. TECH-STACK

```
Frontend:       HTML / CSS / JavaScript (Vanilla)
Hosting:        GitHub Pages (gratis)
Editor:         VS Code Web (vscode.dev)
KI-Assistent:   Claude Pro (Anthropic)
Code-Helper:    GitHub Copilot (gratis freigeschaltet)
Versionierung:  GitHub (remoschenk007)
```

**Noch ausstehend:**

- Backend: Supabase (geplant, gratis Tier)
- Datenbank: PostgreSQL via Supabase
- Auth: Supabase Auth / Apple Sign-In

-----

## 5. AKTUELLE DATEI-STRUKTUR (Stand April 2026)

```
stadtpuls/ (noch als einzelne HTML)
├── index.html     (1600+ Zeilen — muss modularisiert werden!)
└── hero.jpg       (Remos eigenes Züri-Nacht-Foto)
```

**Nächster Schritt — Masterplan Modularisierung:**

```
stadtpuls/
├── index.html          (Shell, <100 Zeilen)
├── css/
│   ├── base.css
│   ├── components.css
│   └── pages.css
├── js/
│   ├── router.js
│   ├── cursor.js
│   ├── gps.js
│   └── api/
│       ├── opentable.js
│       └── ticketcorner.js
└── pages/
    ├── home.html
    ├── events.html
    ├── gastro.html
    └── ... (alle Seiten)
```

-----

## 6. SEITEN (bereits gebaut)

```
✅ Home              Hero, Ticker, Suche, Bento-Grid
✅ Events            Liste, Featured, Pop-Ups
✅ Event Detail      Vollständige Detailseite
✅ Gastro            Liste, OpenTable-Integration
✅ Gastro Detail     Vollständige Detailseite
✅ Nachtleben        Clubs, Bars, Genres
✅ Club Detail       Vollständige Detailseite
✅ Shopping          Shops, Sale, Pop-Ups
✅ Immobilien        Inserate, Suche
✅ Immo Detail       Besichtigungs-Anfrage
✅ Marktplatz        Kategorien, Inserate
✅ Markt Detail      Kontaktformular
✅ Community         Feed, Blogger, Posts
✅ Post Detail       Reviews, Likes, Kommentare
✅ Profil            User-Profil, Posts, Follower
✅ Dating            People & Dates
✅ Dating Profil     Vollständiges Profil
✅ Jobs              Stellenangebote
✅ Job Detail        Bewerbungsformular
✅ News              Stories, Featured
✅ News Detail       Vollständiger Artikel
✅ Musik             Soundtrack, Live-Bars
✅ GPS               Standort-Erkennung
✅ Mobilität         ZVV, Velo, Scooter
✅ Partners          Kooperationen
✅ Quartiere         Übersicht
✅ Kreis 1, 4, 5, 8  Quartier-Seiten
✅ Login/Register    Tabs, Quartier-Wahl
```

-----

## 7. OFFENE GRATIS APIs (für echte Daten)

```
Zürich Tourismus API
URL:      https://www.zuerich.com/en/api/v2/data
Lizenz:   CC BY-SA (gratis, frei nutzbar)
Daten:    Restaurants, Bars, Nachtleben, Hotels,
          Kultur, Shopping, Open Airs, Festivals,
          Live Music, Wellness, Museen
Bilder:   Ja, inklusive
Geodaten: Ja, GPS-Koordinaten

Guidle AG API
Daten:    Lokale Events, Partys, Veranstaltungen
Lizenz:   Offen

Stadt Zürich Open Data
URL:      data.stadt-zuerich.ch
Daten:    900+ Datensätze, Geodaten, VBZ,
          Wetter, Passantenfrequenzen, Parkplätze

OpenStreetMap
Daten:    Karten, Quartiere, GPS-Layer
Lizenz:   Gratis
```

-----

## 8. KOOPERATIONEN (geplant)

```
OpenTable       → Gastro-Reservation (Aktiv geplant)
Ticketcorner    → Event-Tickets (In Planung)
Scout24         → Immobilien-Feed (In Planung)
ZVV / SBB       → Live-Abfahrten (Geplant)
Zürich kauft ein → Lokaler Handel (Gespräch)
Zürich geht aus → Nachtleben (Gespräch)
```

-----

## 9. SEO / TECHNISCHE PRIORITÄTEN

```
- Meta Tags für jede Seite
- Open Graph (Social Sharing)
- Schema.org (Google versteht Stadtpuls)
- Mobile First
- Ladezeit optimieren (Google PageSpeed)
- Quartier-Keywords (z.B. «Kreis 4 Restaurant»)
```

-----

## 10. PERSÖNLICHKEIT & KOMMUNIKATION

```
Sprache:        Schweizerdeutsch / Züri-Slang
Ton:            Direkt, kein Bullshit, authentisch
Wichtige Phrasen:
  - «dä puls vo dä stadt»
  - «Was lauft i däre stadt?»
  - «Kei Umwäg»
  - «Echts Züri»
  - «Kei Chichi»
  - «Mir sind Matchmaker»
  - «Keis Rumsurfe»

Remo arbeitet auf iPad — immer Datei für Datei,
nie zu viel auf einmal, kein Timeout riskieren.
```

-----

## 11. VISION IN EINEM SATZ

> «Was TAMEDIA, Axel Springer und Scout 2006 nicht
> geglaubt haben — bauen wir 2026 mit KI, einem iPad,
> GitHub und null Budget. Zürich first. Dann die Welt.»

-----

*Dieses Dokument bei jeder neuen Session am Anfang einfügen.*  
*Remo & Claude — Stadtpuls 2026* 🔴
## 12. ROADMAP — PHASENPLAN

Phase 1  → Frontend ✅ Fertig
Phase 2  → Modularisierung
           css/ js/ pages/
Phase 3  → Zürich Tourismus API
           Echte Live-Daten einbinden
Phase 4  → Backend Supabase
           User-Profile, Login, Auth
Phase 5  → Partner-Logins
           OpenTable, Ticketcorner direkt
Phase 6  → Zürich komplett & perfekt
Phase 7  → Hamburg, Berlin
Phase 8  → Kaufangebot kommt von alleine
## 13. GPS & STANDORT-FEATURE

GPS-Seite bereits gebaut:
- Browser fragt nach Standort
- Erkennt automatisch Züri-Quartier
- Kreis 1, 3, 4, 5, 6, 8, 9
- Zeigt was 200m um User passiert
- Restaurants, Events, Clubs in Nähe
- GPS App geplant (Beta-Waitlist)
- Hyper-lokal ist Kern-DNA von Stadtpuls

## 14. SOCIAL MEDIA STATUS

Instagram @stadtpuls_zh — LIVE
Bio:
🔴 dä puls vo dä stadt
Was lauft i däre stadt?
Events · Gastro · Stadtläbe · People
Hyperlokal. Echts Züri. Kei Umwäg
more to come..

Auch gesichert:
@stadtpuls_hamburg (Deutsch/Hamburger Slang)
@stadtpuls_berlin (Deutsch/Berliner Slang)

Logo: Schwarz, STADT weiss, PULS rot,
kleiner roter Leuchtpunkt

## 15. KONKURRENZ-ANALYSE

Mapin.social (Schweiz, seit 2024)
→ Nur Events & Nachtleben
→ App-only, keine Web-Version
→ Kein Gastro, Immo, Jobs, Dating
→ Keine Community
→ Stadtpuls ist deutlich breiter

## 16. DATEN-STRATEGIE

Philosophie: 100% gratis, 100% legal
Kein Scraping, kein Backdoor
Nur offene APIs anzapfen

Zürich Tourismus API liefert:
→ Café Plüsch Kreis 3 bereits drin
→ Alle 2900 Züri-Restaurants
→ Bilder, GPS, Öffnungszeiten
→ Alles automatisch aktuell

## 17. WICHTIGE ARBEITS-HINWEISE

- Remo arbeitet auf iPad
- Immer Datei für Datei
- Nie zu viel auf einmal
- Kein Timeout riskieren
- Code in Chunks schreiben
- Neue Konversation pro Thema
- Claude Pro — Limit Di 08:00 reset
- GitHub Copilot gratis freigeschaltet
- vscode.dev für Editor im Browser

## 18. OFFENE PUNKTE NÄCHSTE WOCHE

Priorität 1: Modularisierung
→ css/base.css
→ css/components.css  
→ css/pages.css
→ js/router.js
→ js/cursor.js
→ js/gps.js
→ pages/ (jede Seite separat)

Priorität 2: Erste echte API
→ Zürich Tourismus API einbinden
→ Gastro-Seite mit Echtdaten

Priorität 3: SEO Grundstruktur
→ Meta Tags
→ Open Graph
→ Schema.org

Priorität 4: Backend planen
→ Supabase Setup
→ User-Tabelle definieren
→ Auth vorbereiten

## 19. HERO-FOTO

Remos eigenes Foto — hero.jpg
Zürich Bar bei Nacht, Glühbirnen,
Regen, Schwarz-Weiss
Kein Stock-Photo — echte Züri-DNA
Liegt im GitHub Repository

## 20. FINANCIAL & KOSTEN

Aktuell 100% gratis:
→ GitHub Pages — gratis
→ Zürich Tourismus API — gratis
→ GitHub Copilot — gratis
→ OpenStreetMap — gratis
→ Supabase — gratis Tier

Einzige Kosten:
→ Claude Pro CHF 20.–/Mt via Apple
→ Limit: 75% pro Woche
→ Reset: Dienstag 08:00

Strategie: Gratis für alle User
Monetarisierung via Partner später
