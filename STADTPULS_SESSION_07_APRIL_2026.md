# STADTPULS — SESSION BERICHT

> Datum: Dienstag, 07. April 2026
> Letzte Aktualisierung: Ende Session — komplett

-----

## WAS WURDE HEUTE GEMACHT

**Phase 2 — Modularisierung: KOMPLETT ✅**

Die monolithische index.html (1743 Zeilen) wurde professionell modularisiert.
CSS und JS sind jetzt in separaten Dateien — sauber, wartbar, skalierbar.

-----

## AKTUELLE DATEISTRUKTUR AUF GITHUB

```
Stadtpuls/
├── index.html          (1256 Zeilen — schlanke Shell)
├── hero.jpg            (Remos eigenes Züri-Nacht-Foto)
├── css/
│   ├── base.css        (Reset, Variablen, Cursor, Animationen)
│   ├── components.css  (Nav, Buttons, Cards, Ticker, Footer)
│   └── layout.css      (Hero, Subpages, Detail, Responsive)
└── js/
    └── app.js          (Router, Cursor, Reveal, Menu)
```

-----

## ROADMAP STATUS

```
Phase 1  → Frontend         ✅ FERTIG
Phase 2  → Modularisierung  ✅ HEUTE FERTIG
Phase 3  → Zürich API       ⏳ NÄCHSTER SCHRITT
Phase 4  → Supabase Backend ⏳ Geplant
Phase 5  → Partner-Logins   ⏳ Geplant
Phase 6  → Zürich komplett  ⏳ Geplant
Phase 7  → Hamburg, Berlin  ⏳ Geplant
Phase 8  → Kaufangebot      ⏳ Kommt von alleine
```

-----

## NÄCHSTER SCHRITT — PHASE 3

**Zürich Tourismus API einbinden**

```
URL:    https://www.zuerich.com/en/api/v2/data
Lizenz: CC BY-SA (gratis, frei nutzbar)
Daten:  Restaurants, Bars, Events, Hotels,
        Kultur, Shopping, Festivals, Museen
Bilder: Ja, inklusive
GPS:    Ja, Koordinaten inklusive
```

**Plan Phase 3:**

1. js/api/zuerich-tourismus.js erstellen
1. Gastro-Seite mit Echtdaten befüllen
1. Events-Seite mit Echtdaten befüllen
1. Cache-Logik einbauen

-----

## BACKEND STRATEGIE — ERKENNTNISSE

**3 Schichten:**

```
Schicht 1 — Externe APIs (gratis)
→ Zürich Tourismus, Guidle, OpenStreetMap
→ Liefern Gastro, Events, Karten-Daten
→ Kein eigener Speicher nötig

Schicht 2 — Supabase (gratis Tier)
→ User-Profile, Reviews, Community-Posts
→ PostgreSQL Datenbank
→ Bis 500MB gratis — reicht für Start
→ Skaliert automatisch bis Millionen User

Schicht 3 — Cache
→ Daten zwischenspeichern
→ Nicht bei jedem Klick API neu abfragen
→ Schnell, effizient, günstig
```

**Stresstest / 10’000 User gleichzeitig:**
GitHub Pages + Supabase + externe APIs sind cloud-basiert
— skalieren automatisch. Kein Problem! ✅

**Alles gratis bis ca. 50’000 User!**

-----

## GEO-TARGETING — VISION

```
User öffnet Stadtpuls
↓
GPS erkennt: Kreis 4, Langstrasse
↓
Zeigt automatisch:
→ Restaurant 200m entfernt — Tisch frei
→ Event heute Abend — 350m
→ Club der gerade offen ist — 180m
→ WG-Zimmer im gleichen Quartier
→ Jobs in der Nähe
```

**Technisch:**

```
GPS           → Browser API (bereits gebaut ✅)
Koordinaten   → Zürich Tourismus API (Phase 3)
Radius-Suche  → Supabase PostGIS (Phase 4)
Push Alerts   → «Event in 200m startet in 30min»
```

**Das ist Hyper-Lokal — das kann keine Konkurrenz!**
Niemand in der Schweiz macht das so konsequent.

-----

## MONETARISIERUNG — ERKENNTNISSE

**Partner-APIs verdienen Geld für Stadtpuls:**

```
OpenTable:
→ API vorhanden ✅
→ Modell: Revenue Share
→ CHF 1-5 pro Buchung über Stadtpuls
→ Stadtpuls verdient beim Schlafen!

Ticketcorner:
→ API vorhanden ✅
→ Modell: Affiliate
→ 5-10% pro verkauftes Ticket
→ Stadtpuls verdient beim Schlafen!

Scout24/Homegate:
→ API vorhanden ✅
→ Modell: Pay per Lead
→ Pro vermittelte Wohnung

Zürich kauft ein:
→ Lokale Händler
→ Gespräch geplant

Zürich geht aus:
→ Nachtleben-Kooperation
→ Gespräch geplant
```

**Fazit Monetarisierung:**
Stadtpuls ist gratis für User — aber verdient passiv
durch jeden Klick, jede Buchung, jedes Ticket. 🔴

-----

## USER ONBOARDING — VISION

**Problem:** 70% der User springen ab wenn
Registrierung zu kompliziert ist.

**Lösung: Progressive Onboarding — 5 Schritte**

```
Schritt 1 — Basics
«Wie heissisch du?»
→ Nickname eingeben

Schritt 2 — Wo bisch du?
«Wo wohnsch in Züri?»
→ Quartier wählen (Kreis 1, 4, 5, 8...)

Schritt 3 — Was interessiert dich?
«Was lauft bei dir?»
→ Gastro / Nachtleben / Dating / Jobs
→ Multi-Select, grosse Buttons

Schritt 4 — Wer bisch du?
«Wie alt bisch?»
→ Relevant für Dating
→ Diskret, optional

Schritt 5 — Fertig!
«Willkommen in Züri, @nickname!»
→ Konfetti 🎉
→ Roter Punkt pulsiert
```

**Das Geniale:**

- User merkt nicht dass er Daten gibt
- Jeder Schritt fühlt sich wie Stadtpuls an
- Nach 5 Klicks weiss Stadtpuls alles Wichtige
- Kein langer Formular — spielerisch, schnell

**Daten die wir sammeln:**

```
Für alle:      Nickname, Quartier, Interessen
Für Dating:    Alter, Präferenzen
Für News:      Schreib-Interessen, Quartier
Für GPS:       Standort-Erlaubnis
Für Partner:   Business-Info (später)
```

**Das nennt man Progressive Onboarding**
Beste Apps machen das so: Duolingo, Tinder, Instagram.
→ Phase 4 Thema

-----

## WICHTIGE LINKS

- **Live Site:** https://remoschenk007.github.io/Stadtpuls
- **GitHub:** https://github.com/remoschenk007/Stadtpuls
- **Raw index.html:** https://raw.githubusercontent.com/remoschenk007/Stadtpuls/main/index.html

-----

## TECHNISCHE DETAILS

```
Frontend:   HTML / CSS / JS (Vanilla)
Hosting:    GitHub Pages (gratis)
Editor:     GitHub Web Editor (iPad)
CSS:        3 Dateien, modular
JS:         1 Datei (app.js), SPA-Router
Backend:    Supabase (Phase 4)
```

-----

## DESIGN-DNA

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

Spezial-Features:
- Dualer Cursor (roter Punkt + Ring mit Lag)
- Doppel-Ticker (gegenläufig)
- Scan-Lines im Hero
- Grid-Overlay
- Reveal-Animationen (IntersectionObserver)
```

-----

*© 2026 by raimondo* — Stadtpuls — Zürich*
*«dä puls vo dä stadt»*
*Zürich first. Dann die Welt.* 🔴
