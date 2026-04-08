STADTPULS — TECHNISCHES BRIEFING
Stand: 08. April 2026

════════════════════════════════
1. FILTER & TABS — FERTIG ✅
════════════════════════════════

Events      → Hüt · Wochenende · Konzert · Kultur · 
              Open Air · Sport · Typisch Züri · Gratis
Gastro      → Znacht · Zmittag · Brunch · Vegisch · 
              Asiatisch · Mediterran · Jetzt offe · 📍
Nachtleben  → Techno · House · Jazz · Hip-Hop · 
              Live Music · Afterhour · Cocktailbar · 📍
Shopping    → Mode · Vintage · Design · Lokal · 
              Sale · Pop-Up · 📍
Immobilien  → WG-Zimmer · 1-Zi · 2-Zi · 3+ Zi · 
              Büro · Atelier · 📍
Marktplatz  → Velos · Möbel · Kleider · Tickets · 
              Elektronik · 📍

Globale Logik:
→ 📍 In der Nähe = GPS triggert PostGIS Radius-Suche
→ Kreis-Filter kommt via GPS automatisch
→ Kreis 1 abends → Oper/Theater prominent
→ Kreis 4 abends → Clubs/Bars prominent
→ Kreis 5 abends → Techno/Industrie prominent

════════════════════════════════
2. DATENSTRUKTUR SUPABASE
════════════════════════════════

locations
├── id
├── name
├── kategorie      (gastro/event/club/shopping...)
├── subkategorie   (jazz/techno/oper/vietnamesisch...)
├── kreis          (1-12)
├── lat / lng      (GPS Koordinaten)
├── adresse
├── oeffnungszeiten
├── tags           (array: vegisch, live-music, oper...)
├── preis_niveau   (1-4)
├── quelle         (zuerich-tourismus/guidle/user)
└── aktiv          (true/false)

user_preferences
├── user_id
├── kreis_home
├── interessen     (array)
├── history        (array von location_ids)
└── stimmung       (last known)

Schlüssel-Prinzip:
→ Filter = Tags in der DB
→ Neue Filter = nur neuer Tag, kein Umbau
→ PostGIS: ST_DWithin() für 200m Radius
→ Skaliert Zürich → Hamburg ohne Umbau

════════════════════════════════
3. GEO-TECHNOLOGIE STACK
════════════════════════════════

Supabase + PostGIS = richtige Wahl 2026
→ Gratis bis 50'000 User
→ ST_DWithin() → Radius in 1 SQL-Zeile
→ Kreis via Polygon-Daten Stadt Zürich
→ Echtzeit via Supabase Realtime

════════════════════════════════
4. SEO STRATEGIE — VOR LAUNCH!
════════════════════════════════

Problem jetzt:
→ Single Page App = Google sieht nur 1 Seite

Was wir brauchen:
→ stadtpuls.ch/gastro
→ stadtpuls.ch/events
→ stadtpuls.ch/nachtleben
→ stadtpuls.ch/kreis/4
→ stadtpuls.ch/restaurant/langstrasse-77

Phase 3 → Basis SEO
  Meta Tags, Schema.org, Open Graph

Phase 4 → Technisches SEO
  URL Routing pro Page und Location
  Ladezeit unter 2 Sekunden

Phase 5 → Content SEO
  Community schreibt täglich
  Google indexiert täglich

Ziel:
→ «Restaurant Kreis 4 Zürich» → Stadtpuls #1
→ Google AI: «Laut Stadtpuls…» 🔴

════════════════════════════════
5. KI FEATURES — PHASE 5-6
════════════════════════════════

1. Züri-Bot → «Was mach ich heute Abend?»
2. Personalisierter Feed → lernt was du magst
3. Video Import → KI erkennt Züri-Locations
4. Predictive Events → «Freitag Kreis 4 — wie immer?»
5. Stimmungs-Matching → müde/energetisch/romantisch
6. Push Alerts → «Event 200m · startet in 30min»

Voraussetzung: Datenstruktur jetzt sauber aufbauen!

════════════════════════════════
6. ROADMAP
════════════════════════════════

✅ Phase 1 → Frontend
✅ Phase 2 → Modularisierung
✅ Filter & Tabs → HEUTE FERTIG
⏳ Phase 3 → Zürich API + Basis SEO
⏳ Phase 4 → Supabase + URL Routing + SEO
⏳ Phase 5 → Partner-Logins + KI Features
⏳ 4. Juni → SOFT LAUNCH 🎂🔴
