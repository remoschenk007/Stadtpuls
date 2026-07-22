# STADTPULS — BRIEFING FÜR NEUEN CHAT
**Stand: 22.07.2026 · Dieses Doc zuerst lesen, dann `MASTERPLAN_UPDATE_session_22juli2026.md` (letzte Session im Detail), dann `STADTPULS_master_v2.md` (grosses Bild) + `STADTPULS_KI_HERZ_BLUEPRINT.md` (Personalisierung & Geld).**

## ⚠ AKTIV UNGELÖSTES PROBLEM — ZUERST LESEN
Remo sieht auf **depuls.ch/index.html** (Desktop-Chrome, normales Fenster mit vielen Tabs — UND mobiles Inkognito) im Kreis-Universum (Bubble-Galaxie oben auf der Startseite) eine **alte, falsche Version**:
- 6 Blasen statt 5: Gastro, **News**, Nachtlebe, Shopping, **Dates**, Events — **Kultur fehlt komplett**, „News"/„Dates" gab es in meinem Code nie als eigene Blasen.
- Auch nach Hard-Refresh (`Cmd+Shift+R`) auf demselben Tab unverändert — also kein simples Browser-Cache-Problem.

**Bereits zweifelsfrei ausgeschlossen** (bitte nicht nochmal von vorne prüfen!):
- Git: richtige Commits (`bb15895be`, `07dbfab51`) sind an der Spitze von `main`, lokal und remote bestätigt.
- GitHub-Pages-Branch-Einstellung: Settings→Pages zeigt Source = main, Pfad `/(root)` — korrekt, kein Branch-Mismatch.
- Build: Actions läuft grün, letzter Deploy erfolgreich laut Pages-Seite.
- Kein Drittanbieter-CDN vor depuls.ch (DNS geprüft: Hosttech-Nameserver + reine GitHub-Pages-Standard-IPs 185.199.108–111.153).
- **Der Code selbst ist zu 100% korrekt:** mit Cache-Busting (`?nocache=<timestamp>`) frisch von `raw.githubusercontent.com` geholt und geprüft — `SP_KU_LIVE v1`-Marker vorhanden, `CATS`-Array hat exakt die 5 richtigen Kategorien (gastro/nachtleben/kultur/shopping/events), keine „News"/„Dates"-Blasen im `renderBubbles()`-Code. Ein früherer Fetch OHNE Cache-Busting zeigte fälschlich noch die alte Version (bekanntes unzuverlässiges Caching von `raw.githubusercontent.com` — kein verlässlicher Test ohne `?nocache=`).

→ Das Problem liegt also NICHT im Repo/Commit, sondern irgendwo im Auslieferungsweg zwischen GitHub Pages und Remos Geräten. Noch nicht geprüft / nächste Schritte:
1. Chrome DevTools → Application → Service Workers für depuls.ch prüfen, ggf. „Unregister" + neu laden.
2. Von komplett anderem Netz testen (Mobilfunk statt WLAN oder umgekehrt), um Netzwerkpfad-Caching auszuschliessen.
3. Repo nach einer zweiten, alten Kopie des Bubble-Codes durchsuchen (z.B. in `onboarding_preview.html`, `master.html` o.ä.) — noch nicht gemacht.
4. Notfalls `git commit --allow-empty -m "Force redeploy" && git push`, 10–15 Min warten, mit `?v=<neue-Zahl>` testen.

Details/Log der ganzen Diagnose in `MASTERPLAN_UPDATE_session_22juli2026.md` Abschnitt 7.

## WER & WAS
Remo Schenk = Visionär/Creative Director von **Stadtpuls** (depuls.ch), Zürich-City-Guide. Claude = Informatiker/PM/CD. **Hochdeutsch mit Remo, Züridütsch für On-Site-Copy.** Remo arbeitet auf geliehenem Mac (Committer „Alessandra Christen" = kosmetisch), pusht selbst via VS-Code-Terminal. Remo ist nicht technisch/dyslexisch — jede Terminal-Anleitung muss Zeile für Zeile, ohne Fachjargon, mit genauem Wortlaut der Tasten kommen.

## ARBEITS-WORKFLOW (bewährt, strikt einhalten)
1. Claude baut in Sandbox, validiert (Div-Balance, `node --check` Browser-Modus, Marker-Zahlen), liefert via ZIP/Einzeldatei.
2. Remo lädt runter → Zeile-für-Zeile-Terminal-Befehle (⚠ **nie mehrzeilige Blöcke auf einmal**, wenn `git pull`/`git commit` dabei ist — Risiko, dass ein Editor aufpoppt und Remo unbemerkt in dessen Buffer weitertippt statt Befehle auszuführen. Siehe Lesson Learned unten.): unzip aus ZIP → **BEWEIS-grep** (Marker-Zahl >0/erwarteter Wert, sonst STOPP!) → add/commit/push.
3. **`git config --global core.editor "true"` ist gesetzt** — verhindert, dass sich bei Merges ein Text-Editor (vim) öffnet. Trotzdem: nach jedem Push nie blind „ist live" annehmen — immer per frischem Klon (Claude-seitig) oder Live-Fetch der Live-URL gegenprüfen, was tatsächlich ankam. Und den Workflow-Run-Commit-Hash mit dem letzten Push-Hash abgleichen, bevor man „live" bestätigt.
4. SQL: Claude liefert idempotente Dateien → Remo kopiert in Supabase SQL-Editor → Run. Mehrfach ausführen = gefahrlos.
5. **Deploy:** GitHub Pages kann hängen (Fail-Mail „deploy failed") → `git commit --allow-empty -m redeploy && git push` oder Actions → Re-run. Tests immer mit Cache-Buster (`?v=2` o.ä.) oder im privaten Tab.
6. GitHub Action „Stadtpuls Daten-Sync" (workflow_dispatch, auch täglich 04:00) baut Event-/Gastro-/Shopping-Profilseiten, Kreis-Seiten und Sitemap komplett neu aus den aktuellen Templates — nach jeder Template-Änderung (z.B. gastro-profil.html) muss die Action einmal manuell laufen, damit sich der Fix auf alle ~230+ bestehenden Seiten propagiert.

## TECHNIK-FAKTEN
- Repo `remoschenk007/Stadtpuls`, branch main, lokal `/Users/alessandrachristen/stadtpuls/`. GitHub Pages = depuls.ch.
- Supabase `https://pnynkzrqnfoshojqfqxn.supabase.co`, anon-Key public im Code (voll in jeder Seite). RLS bewusst permissiv (anon select/insert/update auf Formular-/Betriebstabellen). Auth aktiv (`users.auth_id`↔auth.uid, UNIQUE).
- Design-DNA: bg #04040a · rot #ff2d00 · volt #c8ff00 · cyan #00f5ff · purple #9333ea · pink #ec4899 · cream #e8e4d9 · Barlow Condensed Italic 900 + DM Mono · **Hex, nie CSS-Var** · Emojis nie als Funktions-Icons (SVG!).
- Auto-Sync: GitHub Action täglich 04:00 (Eventfrog+ZT→Supabase, dann Event-/Location-/Kreis-Seiten + Sitemap neu bauen + auto-commit/push), SERVICE_KEY-Secret gesetzt. `datum_start` = DATE-String; „heute" immer `Europe/Zurich`.
- **Pretty URLs:** Events unter `/events/<slug>/`, Gastro unter `/gastro/<slug>/`, Shopping unter `/shopping/<slug>/` — statt `event-profil.html?id=…` etc. Generiert von `generate_event_pages.py` / `generate_location_pages.py` bei jedem Sync-Lauf, mit echtem SEO-Content (title/meta/canonical/OG/JSON-LD) pro Seite. Alte `?id=`-URLs redirecten client-seitig + haben `<link rel="canonical">`. Nachtleben ist **noch nicht** umgestellt (`?slug=` bleibt vorerst).
- **Kreis-SEO-Landingpages** (`generate_kreis_pages.py`): erzeugt statische `/gastro/kreis-N/`, `/shopping/kreis-N/`, `/nachtleben/kreis-N/` — ein **eigenständiges, einfaches Listen-Template**, komplett unabhängig vom Kreis-Universum auf der Startseite. Nicht verwechseln, wenn irgendwas mit „Kreis" komisch aussieht — erst prüfen, welches der beiden Systeme betroffen ist.
- **Eventfrog-API hat Rate-Limits (429):** `import_eventfrog.py` nutzt jetzt `ef_get()` mit Retry+Backoff (3s→6s→12s→24s→30s, max. 5 Versuche) + feste Pausen zwischen Requests — nicht wieder auf naive Direkt-Requests zurückbauen.

## SYSTEM-ZUSTAND (alles LIVE + GETESTET ✅, ausser dem Bug oben)
- **Auth komplett:** Registrieren→Mail→Onboarding-Guard→Dashboard; Trigger `handle_new_user`; Passwort-Reset; Account-Löschen (RPC `delete_my_account`). Redirect-URLs korrekt.
- **Momänt-Kette + Inbox-Tab** wie gehabt (unverändert).
- **Kommandozentrale v3:** Moderation, Verkauf, Boosts, Finanzen, Inbox, Audit — unverändert.
- **Money-Loop v1:** Listen-Sortierung nach Boost-Tier, „DAS ISCH MIS LOKAL"-Button, Zentrale-Verkauf-Flow — Status aus Vorsessionen, in dieser Session nicht neu geprüft.
- **SEO/Pretty-URLs:** Events/Gastro/Shopping haben individuelle, crawlbare URLs mit echtem Content statt generischer `?id=`-Seiten.
- **Events haben jetzt echte Adressen:** Eventfrog-Rate-Limit-Fix (`ef_get()` mit Backoff) + Backfill-Skript nachträglich für ~3000 alte Events gelaufen — 2833 Adressen nachgetragen, 167 unauflösbare Events gelöscht (auf Remos Wunsch, „schlechte Daten raus").
- **Event-Profil-Karte** farblich an Gastro angeglichen (Google-Maps-iframe, kein `mix-blend-mode` mehr — machte die Karte auf Events-Seiten blass).
- **Neues Favicon** (Puls-Symbol) live.
- **Kreis-Universum auf der Startseite gebaut** (vorher: nur CSS/HTML-Attrappe ohne jede Logik): 5 Kategorie-Blasen mit echten Live-Zählern aus Supabase, Kreis-Auswahl 1–12, Ergebnis-Sheet, „Frag Stadtpuls"-Suche über alle Kategorien, CTA gibt `?kreis=` an Zielseite weiter. **Code ist korrekt und live** — aber Remo sieht bei sich noch eine alte Version, siehe Bug-Abschnitt oben.
- **Kreis-Filter auf allen Kategorie-Seiten repariert:** gastro.html, kultur.html, shopping.html hatten tote `setKreis()`-Buttons (Funktion nie definiert — alter, unabhängiger Bug), events.html hatte gar keinen echten Filter. Alle vier jetzt funktionsfähig inkl. `?kreis=`-URL-Übernahme vom Kreis-Universum. nachtleben.html war schon korrekt.
- **Kein Fake-Content mehr live:** alte Backup-Datei mit Fake-Reviews gelöscht, doppeltes `<title>`-Tag behoben.
- **KI-Herz Schritt 1 aktiv:** sp-track.js sammelt (bookmarks/interactions), Blueprint = Quelle der Wahrheit.

## OFFENE PRIORITÄTEN (Reihenfolge, Stand 22.07.2026)
0. **Phantom-Blasen-Bug lösen** (siehe ganz oben) — höchste Priorität, weil live für alle Besucher sichtbar.
1. **Money-Loop Abnahme-Test** (aus Vorsession, Status unklar — ggf. mit Remo klären ob noch offen).
2. Gastro-/Shopping-Profil: falls noch Fake-Bookmark vorhanden, durch echtes ❤️ ersetzen (Muster: nachtleben-profil).
3. **Custom SMTP** (Hosttech no-reply@depuls.ch) — Pflicht vor Launch (Supabase-Mail-Rate-Limits!).
4. **quartiere.html** + weitere Footer-Landing-Pages (Status aus Vorsession, nicht neu geprüft).
5. **KI-Herz Schritt 2:** taste-build (Geschmacks-DNA) → „Für dich"-Feed → notify-build (Blueprint §6).
6. Design-v2/Control-Deck-Rollout auf gastro/shopping/events; Skeleton-Loading; echte Reviews.
7. Mit Remo klären: Nachtleben ebenfalls auf Pretty-URLs umstellen, oder bewusst bei `?slug=` belassen?
8. Danach: raus und verkaufen — erste 10 Lokale, 50 User (PM-Audit: „Motor stark, Sprit fehlt").

## STIL-ERWARTUNG AN CLAUDE
Vollgas, proaktiv mitdenken, ehrlich (keine Fake-Features verschweigen), Diagnose vor Fix, alles validieren, Schritt-für-Schritt-Anleitungen mit Beweis-Checks, PM-Blick aufs grosse Ganze (Cold-Start!), und den Blueprint/Masterplan bei jedem Meilenstein fortschreiben. Bei Terminal-Anleitungen: Remo ist nicht technisch — Zeile für Zeile, kein Jargon, jeden Tastendruck ausschreiben, nie mehrzeilige Blöcke bei riskanten Git-Operationen.
