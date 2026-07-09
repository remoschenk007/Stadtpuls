# STADTPULS — MASTERPLAN-UPDATE · Session 07.–09. Juli 2026
**Gehört zu: NEUER_CHAT_BRIEFING.md + STADTPULS_master_v2.md · Von Remo (Vision) + Claude (CD/PM/Dev)**

## ERLEDIGT & LIVE (alle verifiziert am Live-Repo)

### 1. MONEY-LOOP v1 — GESCHLOSSEN (Commit ec43f95 + SQL)
- Listen-Sortierung nach Boost-Tier (premium>boost>featured>rest) in gastro/nachtleben/shopping/events — Ablauf-Check (`boost_until >= now()`) direkt im Client, abgelaufene fallen automatisch zurück
- Tier-Badges + Karten-Glow (PREMIUM pink / BOOST volt / FEATURED volt)
- „GRAD ANGSAGT" auf index: max. 3 Premium-Slots, fail-silent, als Partner gekennzeichnet
- „DAS ISCH MIS LOKAL"-Button auf allen 4 Profilseiten → platzierung.html?id&typ&name&kreis (Flow VERIFIZIERT: Profil wird korrekt übergeben)
- `setup_boost_v2.sql` in Supabase AUSGEFÜHRT: eventfrog_events boostbar, `stadtpuls_expire_boosts()` räumt beide Tabellen + Sicherheitsnetz, Zentrale patcht via `spBoostTable()` auch Events
- Marker: SP_BOOST v1

### 2. BOT-FIXES v1.1/v1.2 (Commits bec9aa3, 1b9302d)
- gastro Stimmungs-Sektion: toter Klick-Handler gefixt (`spOpenById`)
- shopping-Bot: war Attrappe (nur Spruch) → empfiehlt jetzt echt (deterministisch, `spBotPick`)
- ZÜRI-BOT (gastro, CASUAL/ROMANTISCH…): „ANALYSIERT…" war Deko ohne Funktion → echter Sucher (`spBotPickG`: stimmung_tags zuerst, Subkategorie-Fallback)
- EHRLICHKEITS-FIXES: erfundener Echtzeit-Spruch („Pho Saigon frei, 4 Plätze") raus; falsches Label „Claude · Powered by Anthropic" raus → „Regelbasiert · us de Stadtpuls-Date" (LLM-Label erst wieder, wenn echter LLM-Bot läuft)
- Qualitätsschwelle: rating<3.2 wird nie empfohlen (nur wenn Rating existiert)

### 3. NAV + HYGIENE v1.3 (Commit 1b9302d + perl-Fix)
- Nav-Audit: nachtleben fehlte NEWS, events fehlte MITMACHE, index hatte KEINEN Burger, kontakt/feedback/platzierung hatten keine Nav → alles gefixt
- SP_NAV v1: einheitliches Fullscreen-Menü (8 Links) auf index/kontakt/feedback/platzierung
- platzierung.html: 10 Fremdzeichen (kyrillisch/arabisch Homoglyphen) ersetzt, „BESSERI PLATZIERIG" korrekt

### 4. SP_SOON v2 — SITE OHNE 404 (Commits d0eded3, c2e2b3c)
- 404-Audit: 10 tote Ziele (8 Footer-Links auf 13 Seiten + marktplatz + partner/partners-Duplikat)
- 9 Landing-Pages: quartiere, musik, jobs, immobilien, mobilitaet, community, gps, partners, marktplatz
- Struktur je Seite: Hero (Im-Bau-Status, ehrlich) + „Was chunnt" (3 Cards) + Live-Fakten (nur echte Features, verlinkt) + FAQ (sichtbar Zürideutsch)
- SEO/AEO: indexierbar, Canonical, OG, JSON-LD (WebPage + FAQPage + Breadcrumb, Hochdeutsch = Meta-Regel)
- partners.html = Sales-Page mit echten Preisen + CTA zu platzierung.html
- sitemap.xml war LEER (0 Bytes!) → neu mit 21 URLs; robots.txt war bereits AI-Crawler-freundlich
- index: partner.html → partners.html (kanonisch)

### Nebenbei
- Repo-Hygiene: 6 Ballast-Dateien (LIESMICH, alte ZIPs) entfernt; Sicherheitscheck: keine Secrets im Repo (Stripe via Deno.env)
- Supabase-Incident Jul 01–06 (restart/resize/create): Projekt NICHT betroffen, alle Services grün. Regel bis Resolved: kein Restart/Resize/PG-Upgrade. Geplante Wartung: 14.07., 03:00–04:00 UTC (05–06 Uhr CH)

## OFFEN (Reihenfolge)
1. **ABNAHME-TEST Money-Loop-Kette** (steht noch aus!): Test-Boost setzen (SQL Schritt A–E dokumentiert im Chat) ODER echte Kette: Button → Anfrage → Verkauf-Tab → Premium freischalten → oben+Badge+Startseite → Ablauf-Test → Aufräumen
2. **gastro-profil „Fehlermeldung"**: Code headless-verifiziert GESUND (rendert, Claim-Button erscheint). Remos exakte Fehlermeldung + URL nie geliefert → bei Wiederauftreten: wortwörtliche Meldung + Adresszeile erfragen (Kandidaten: ohne ?id geöffnet / Cache / Supabase-Moment)
3. **Filter-Symptome**: „funktionieren nicht gut" — konkrete Beispiele ausstehend (welcher Filter, erwartet vs. tatsächlich)
4. **Custom SMTP** (Hosttech no-reply@depuls.ch) — LAUNCH-BLOCKER
5. **Tischreservierung**: Felder existieren (hat_reservation, reservation_url, RES-Badge). Remo sucht Partner (OpenTable etc.), dann CTA im Profil bauen
6. Google Search Console: neue sitemap.xml einreichen
7. Danach gemäss Briefing: KI-Herz Schritt 2 (taste-build), Für-dich-Feed, cleanup_demo.sql — und VERKAUFEN (erste 10 Lokale)

## NEUE STANDING RULES (aus dieser Session)
- Beweis-Soll-Werte VOR Auslieferung verifizieren (grep-Kette bricht bei falschem Soll korrekt ab — zweimal passiert)
- Headless-Tests (jsdom + gemockter fetch) als Standard-Verifikation vor Auslieferung
- Bot-/KI-Features: niemals Fake-Labels oder erfundene Echtzeitdaten; „Powered by"-Claims nur wenn wahr
- Coming-Soon-Seiten: nie leer — immer „Was chunnt" (Vision) sauber getrennt von „Lauft scho" (nur echte Features)
