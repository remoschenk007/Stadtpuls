# STADTPULS — MASTERPLAN UPDATE
### Session vom 24.–25. Juni 2026 — Universum-Dashboard, Index-Verschlankung, Footer-Konsistenz

---

## WICHTIG FÜR NEUEN CHAT: SO HAT CLAUDE DIESE SESSION GEARBEITET

- **Geometrie nie geraten, immer durchgerechnet.** Bei jedem Bubble-Layout (Universum) wurde vorher mit Python ein Geometrie-Check gemacht: Bubble-vs-Bubble-Kollision, Bubble-vs-Center-Star, Header-Abstand, Bounds-Overflow — sowohl für Mobile als auch Desktop, im Worst-Case (max. Bubble-Grösse bei vollem Score/passendem Vibe).
- **JS-Syntax nie nur durch Klammerzählen geprüft — immer mit `node --check`** auf den extrahierten `<script>`-Inhalt. Klammern zählen reicht nicht (siehe Bug unten).
- **Bei Unsicherheit über Original-Inhalte (Footer): nicht aus dem Gedächtnis rekonstruiert, sondern aktiv im Backup gesucht** (`grep`/`sed` Schritt für Schritt), bis der exakte Original-Code gefunden war.
- **Bei riskanten Operationen (Datei überschreiben): immer zuerst Backup vorschlagen und committen lassen, bevor überschrieben wird.**
- **Bei eigenen Fehlern: offen benannt, nicht beschönigt** (z.B. Geometrie nur für Mobile geprüft, Desktop vergessen — wurde explizit zugegeben statt verschwiegen).

---

## ① GEFUNDENER UND BEHOBENER BUG: Tasks-Rendering Syntaxfehler

**Symptom:** Dashboard-Universum blieb komplett leer (nur Center-Star sichtbar, keine Kategorie-Bubbles).
**Ursache:** In `renderProfile()` gab es eine Zeile mit kaputtem, doppelt-escaptem Quote-Verschachtelung im Tasks-`onclick`-Handler:
```js
// VORHER (kaputt):
onclick="${t.done?'':'notif(\\'+'+t.pts+' PTS WENN ERLEDIGT!\\')'}"
```
Das brach das **gesamte Script** beim Parsen ab — `buildUniverse()` wurde nie aufgerufen.
**Fix:** `data-`-Attribute statt verschachtelter Strings, Event-Listener danach separat zugewiesen. Bug war auch in der **echten** `dashboard.html` (nicht nur Preview) — wurde dort ebenfalls gefixt, bevor er live ging.
**Lektion:** Klammern-Zählen allein reicht nicht zur Validierung — seitdem immer `node --check`.

---

## ② DASHBOARD.HTML — "DIS UNIVERSUM" (Bubble-Galaxie)

**Status: FERTIG UND LIVE**, mehrfach iteriert.

### Architektur
- 9 Bubbles im `.universe-wrap` Container (680px hoch Desktop, height variiert Mobile via Media Query)
- Center-Star = User selbst (Nickname, Score, Kreis), Bubbles drumherum
- Jede Bubble hat `pos` (Desktop %) und `posM` (Mobile %) — **beide separat geometrisch verifiziert**, das war initial vergessen (nur Mobile gecheckt) und musste nachträglich für Desktop ergänzt werden

### Die 9 Bubbles (aktueller Stand)
1. **GASTRO** — Live-Count aus `locations?kategorie=eq.gastro`
2. **NACHTLEBE** — Grösse abhängig von `vibe==='NACHTMENSCH'`, Pulse-Moment-Ring (gold, rotierender Punkt) wenn `activePulseKreise.includes(p.kreis)` — aktuell hartcodiert `[4]`, **strukturell vorbereitet für echte Live-Abfrage in Phase 6**
3. **✨ ZÜRI-BOT** — NEU diese Session, Phase-6-Vorgriff. Eigener Shimmer-Gradient-Stil (lila-cyan, `background-size:200% 200%` Animation), Sparkle-Icon-Pulsieren. Klick öffnet Card mit Beispiel-Queries und "BENACHRICHTIGE MICH"-Button. Bewusst nicht funktional, aber visuell klar als "kommt noch" markiert.
4. **EVENTS** — Live-Count aus `eventfrog_events`
5. **PEOPLE & DATES** — Voting-Phase-Hinweis
6. **SHOPPING** — Live-Count
7. **NEWS & STORIES** — verlinkt zu `news.html`
8. **MARKTPLATZ** — Live-Count aus `inserate?status=eq.approved` (siehe Bug-Fix unten)
9. **📍 GPS** — NEU diese Session, ehrlicher Phase-5-Platzhalter. Gedämpfte Opacity (0.6), gestrichelter Rand statt durchgezogen, klar als "noch nicht aktiv" erkennbar (nicht als Fake-Live-Feature getarnt)

### Klick-Modal — KOMPLETT UMGEBAUT diese Session
Vorher: simples Bottom-Sheet von unten hochfahrend.
Jetzt: zentriertes Glow-Modal im Stil von `feedback.html` (ZÜRI MOMENT-Vorbild):
- Farbiger Top-Akzentstreifen (`.bc-topbar`) in Kategorie-Farbe
- Icon mit `box-shadow: currentColor` Glow
- Titel mit Text-Shadow-Glühen
- Backdrop mit `backdrop-filter: blur(6px)`
- Scale+Fade-Animation aus der Mitte statt Slide-from-bottom

### Bekannte, behobene Probleme dieser Session
- **Race Condition / null-Crash:** `loadDashboard()` konnte `PROFILE = null` lassen wenn der `users`-Insert fehlschlug (z.B. wegen `nickname` UNIQUE-Constraint von einem früheren Test-Registrierungsversuch). Jetzt: echtes Error-Handling mit user-freundlicher Fehlermeldung + "NOMAL VERSUECHE"-Button statt stillem Crash.
- **Sternenfeld-Canvas Bug:** War `position:fixed` ohne CSS-Regel definiert, lief im normalen Dokumentfluss mit, "trennte" sich beim Scrollen optisch von der Galaxie. Fix: Canvas physisch in `.universe-wrap` verschachtelt, `position:absolute;inset:0`, Resize-Berechnung auf Container-Grösse statt `window.innerWidth/Height`.
- **Lesbarkeits-Problem:** Bubble-Texte hatten keinen Text-Shadow, verschwammen mit hellem Hintergrund-Glow. Fix: `text-shadow` auf `.b-name`/`.b-meta`, Bubble-Farbsättigung von `77`/`1a` Hex-Alpha auf `aa`/`55`/`28` verstärkt, Konturen von 1.5px auf 2px verdickt.
- **Titel-Lesbarkeit:** "DIS UNIVERSUM" kollidierte mit Header bzw. war zu schwach lesbar gegen Glow. Fix: eigener dunkler Hintergrund-Chip (`background:rgba(4,4,10,0.55);backdrop-filter:blur(8px)`) statt nur Text-Shadow-Tricks.
- **`sbCount()` HTTP-Fehler:** Lieferte bei z.B. 400-Fehler (Marktplatz-Inserate-Abfrage) einen Konsolenfehler statt sauber auf `0` zurückzufallen. Fix: `if(!r.ok)return 0;` Check eingebaut.

### Account-Debugging dieser Session (wichtige Erkenntnis für künftige Bugs)
Remo hatte sich über `login.html` registriert (Account `remoschenk@me.com`, Nickname **RemoTest** nicht "zuerifuchs" — letzteres war nur Claudes Demo-Platzhalter-Name!). Es existierte ein `auth.users`-Eintrag, aber **kein** zugehöriger `public.users`-Eintrag → `PROFILE` blieb `null` → Crash. Gelöst durch manuellen SQL-Insert:
```sql
INSERT INTO public.users (auth_id, nickname, role, aktiv)
VALUES ('71b0efa7-4941-4ada-ae5e-514c9abfa3fd', 'RemoTest', 'user', true);
UPDATE public.users SET punkte=145, kreis=4, vibe='NACHTMENSCH' WHERE auth_id='71b0efa7-4941-4ada-ae5e-514c9abfa3fd';
```
**Lektion:** `public.users` hat bewusst **kein** `email`-Feld (DSGVO-Datensparsamkeit, Email lebt nur in `auth.users`) — wichtig für künftige SQL-Debugging-Queries, nicht nach `email` in `public.users` suchen.

---

## ③ INDEX.HTML — RADIKAL VERSCHLANKT

**Status: FERTIG UND LIVE.**

Die alte `index.html` war eine One-Page-Architektur mit über 30 eingebetteten Pseudo-Seiten (Events, Gastro, Nachtleben, alle 4 Quartiere einzeln, GPS, Jobs, News, Soundtrack, Mobilität, Partner — alles dupliziert mit hartcodierten Fake-Zahlen wie "348 Lokale"), parallel dazu existierten längst bessere, einzelne Seiten (`gastro.html`, `events.html` etc.) mit echten Live-Daten.

**Neue `index.html`:** Reine Hub/Landing-Seite — Hero, **echter Live-Ticker aus Supabase** (Gastro/Nachtleben/Events-Counts), Kategorie-Kacheln die zu den fertigen Einzelseiten verlinken, Quartiere-Strip (4 von 12 Kreisen angeteasert, Rest auf `quartiere.html` verwiesen — **diese Seite existiert noch nicht**), Community-CTA, Footer.

**Backup der alten Version gesichert:** `index_BACKUP_20260624.html` liegt im Repo (`git log` zeigt vorherige Commits: `9ccef8e`, `5bc268c`, `af59700` falls Rückgriff nötig).

### Mobile-Nav-Fix
"NACHTLEBE" wurde in der horizontal scrollenden Mobile-Nav mitten im Wort abgeschnitten ohne Hinweis. Fix: Fade-Out-Schatten am rechten Rand (`::after` mit `linear-gradient`) signalisiert "hier geht's weiter", kleinere Schrift auf Mobile (8px statt 9px).

---

## ④ NEWS.HTML — NEU GEBAUT DIESE SESSION

**Status: FERTIG.** GODMODE-Level wie gastro/nachtleben/events. Echte Anbindung an `news_stories`-Tabelle:
- Nur `status='approved'` Artikel öffentlich sichtbar
- Featured-Artikel + Grid-Liste, Kategorie-Filter-Chips
- "SCHRIB DINI STORY"-CTA mit Login-Check, KI-Moderations-Hinweis ("sauberi Storys: sofort live · Hate/Spam: sofort abglehnt · Unsicher: manuelli Prüfig ~24h")
- Pending-Count wird separat abgefragt (nicht öffentlich gelistet, nur als Zahl im Stats-Bereich)

---

## ⑤ ORIGINAL-FOOTER — REKONSTRUIERT UND ÜBERALL EINGEBAUT

**Status: FERTIG, in allen 13 Footer-Seiten live.**

### Warum das nötig war
Claude hatte in `index_neu.html` ursprünglich einen eigenen, neuen (schlankeren) Footer geschrieben statt den echten Original-Footer zu verwenden. Remo wollte explizit den **echten Original-Footer aus der alten index.html**, überall identisch.

### Wie der Original-Footer gefunden wurde
Der Footer lag **nicht** als normales `<footer>`-HTML im Body, sondern als `<template id="ftpl">` (unsichtbares Template-Element), das per JS zur Laufzeit injiziert wurde (`document.importNode(tpl.content,true)`). Gefunden via:
```bash
grep -n "footer-brand\|id=\"ftpl\"" index_BACKUP_20260624.html
sed -n '652,680p' index_BACKUP_20260624.html | fold -w 200
```
CSS dazu lag in externen Dateien `css/components.css` und `css/layout.css` (nicht inline) — gefunden via:
```bash
grep -n "ftk\|fbdot\|footer-brand" index.html css/*.css 2>/dev/null
```

### Original-Footer-Struktur (jetzt Standard für alle Seiten)
1. **`.ftk` Ticker-Streifen** oben: "STADTPULS 2026 · NEUE ÄRA · DÄ PULS VO DÄ STADT · ..." (Endlos-Scroll-Animation `tkr 22s linear infinite`)
2. **`.fg` 4-Spalten-Grid:**
   - Brand (Logo-Punkt + "STADTPULS" + Tagline + Beschreibung + Copyright)
   - "Entdecken" (7 Links: Gastro, Nachtleben, Shopping, Events, Quartiere, Musik & Sound, Mobilität)
   - "Community" (6 Links: Feed & Posts, People & Dates, Jobs Züri, News & Stories, GPS, Kooperatione)
   - "Mitmache" (6 Links: Einlogge, Profil aalege, Blogger werde, Inserat schalte, Partner werde, Kontakt)
3. **`.fbot` Bottom-Bar:** Copyright + AGB/Datenschutz/Impressum

**Wichtige Anpassung beim Übertragen:** Alte `onclick="go('xyz')"`-Aufrufe (One-Page-Routing) wurden zu echten `<a href="xyz.html">`-Links umgebaut, passend zur neuen Mehrseiten-Architektur.

### Eingebaut in (13 von 13 Footer-Seiten, alle syntaktisch validiert):
`index.html`, `nachtleben.html`, `nachtleben-profil.html`, `news.html`, `datenschutz.html`, `dating.html`, `event-profil.html`, `events.html`, `gastro-profil.html`, `gastro.html`, `impressum.html`, `shopping-profil.html`, `shopping.html`

**Hinweis:** Mehrere der referenzierten Footer-Links führen zu Seiten, die **noch nicht existieren**: `quartiere.html`, `musik.html`, `mobilitaet.html`, `community.html`, `gps.html`, `partners.html`. Das sind 404-Links bis diese Seiten gebaut sind — bewusst so gelassen, da der Footer-Auftrag nur "Footer korrekt einbauen" war, nicht "fehlende Zielseiten bauen".

---

## ⑥ NEU GEFUNDENER BUG, NICHT BEHOBEN (für nächste Session)

**`gastro.html` hat `renderKreisSheet()` zweimal definiert** (Zeile ~1567 und ~1639). JavaScript nimmt automatisch die letzte Definition — funktional läuft es vermutlich, aber die erste ist totes Code-Leichenteil. Die zweite/spätere Version ist klar die bessere (nutzt `getFiltered()` für korrekt gefilterte Zählung statt ungefilterter `allLocs.length`, ruft `sheetSetKreis()` statt älterem `setKreis()` auf). **Nicht angefasst diese Session** — eigenständige Aufräumarbeit für eine andere Runde, hat nichts mit Footer/Universum-Auftrag zu tun.

---

## OFFENE PUNKTE FÜR NÄCHSTE SESSION

1. **🔴 PRIORITÄT — Roter Puls-Punkt / Bubble-Menu fehlt auf der neuen `index.html`.** Im Original gab es ein schwebendes, kaum sichtbares, atmendes rotes Punkt-Element (vermutlich unten rechts), das bei Klick in mehrere Blasen explodiert (Feedback/Kontakt/Impressum/Datenschutz-Schnellzugriff). Wurde beim Verschlanken der `index.html` komplett vergessen/nicht übernommen. **Muss noch aus dem Backup extrahiert und eingebaut werden** — gleiche Methode wie beim Footer (im Backup suchen, nicht aus dem Gedächtnis rekonstruieren).

2. **`gastro.html` Doppel-Funktion `renderKreisSheet()` aufräumen** (siehe Punkt ⑥ oben) — alte, schlechtere Version entfernen.

3. **Fehlende Footer-Zielseiten bauen:** `quartiere.html` (12 Kreise mit Filter, höchste Priorität laut Remo — "ich will eine Seite was passiert diese Woche"), `musik.html`, `mobilitaet.html`, `community.html`, `gps.html` (als echte Phase-5-Funktionsseite, nicht nur Footer-Link), `partners.html`. `jobs.html`, `immobilien.html`, `marktplatz.html` waren schon in einer früheren Session als fehlend identifiziert.

4. **🟡 GROSSES, NOCH NICHT ANGEGANGENES THEMA — Pop-up-/Event-Daten-Pipeline und personalisierte Verteilung.** Remo hat das explizit als seine grösste Sorge benannt (Grund für 4 Wochen Pause vor dem geplanten Launch am 4. Juni). Kernfrage: Wie kommen Pop-up-Events strukturiert rein (aktuell nur Eventfrog-Import, manuell getriggert, kein Cron-Job), und wie werden sie **im richtigen Moment an den richtigen User** ausgespielt (Vibe-Matching, Kreis-Matching, Zeitfenster-Logik)? Claude hat vorgeschlagen, das **bewusst nicht nebenbei zu lösen**, sondern eine eigene, ruhige Session dafür einzuplanen — das Datenmodell (`notification_typen`, `notifications`-Tabelle) ist als Grundlage schon vorhanden, aber die eigentliche Matching-/Trigger-Logik (wann zeigen? Cron oder DB-Trigger? wie granular nach Vibe filtern?) ist komplett offen und sollte nicht in Eile zwischen anderen Aufgaben entstehen.

5. **Pulse-Moment-Logik ist noch hartcodiert** (`activePulseKreise = [4]` in `dashboard.html`) — strukturell vorbereitet für Phase 6, aber noch keine echte Live-Aktivitäts-Abfrage. Hängt mit Punkt 4 zusammen.

6. **Züri-Bot-Bubble ist rein visuell, nicht funktional** — bewusst so gelassen als ehrliches "kommt noch"-Signal statt leerem Versprechen mit zu viel Anspruch. Erst bauen wenn Phase 6 wirklich an der Reihe ist.

---

## ZÜRIDEUTSCH-GLOSSAR-ERINNERUNG (weiterhin gültig)
Aus Master_v2 beachten: DIS/DIN/DINI je nach Genus, NÖD/ÖPPIS/WÜRKLI etc. Casual Swiss/Hochdeutsch in Konversation mit Remo, Zürideutsch nur für On-Site-Copy.

## SUPABASE-ZUGANG (unverändert)
URL: `https://pnynkzrqnfoshojqfqxn.supabase.co`
Anon Key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ`

## GIT-WORKFLOW-MUSTER (das in dieser Session konsequent verwendet wurde)
1. Claude baut Datei(en) in `/mnt/user-data/outputs/`
2. Validierung: HTML Div-Balance (Python `count`) + echte JS-Syntax (`node --check` auf extrahiertem `<script>`-Inhalt, JSON-LD-Blöcke separat als JSON validieren, nicht als JS)
3. ZIP erstellen, `present_files`
4. Remo: `cd ~/Downloads && unzip -o X.zip -d X && cp X/*.html /Users/alessandrachristen/stadtpuls/ && cd /Users/alessandrachristen/stadtpuls && git add . && git commit -m "..." && git push origin main`
5. Bei Unsicherheit über bestehenden Inhalt: **immer zuerst per Terminal-Befehl im Backup/aktueller Datei suchen lassen**, nie aus dem Gedächtnis raten — besonders bei Footer/Layout-Fragen, wo der exakte Original-Code zählt.
