# STADTPULS — BRIEFING FÜR NEUEN CHAT
**Stand: 04.07.2026 · Dieses Doc zuerst lesen, dann `STADTPULS_master_v2.md` (grosses Bild) + `STADTPULS_KI_HERZ_BLUEPRINT.md` (Personalisierung & Geld).**

## WER & WAS
Remo Schenk = Visionär/Creative Director von **Stadtpuls** (depuls.ch), Zürich-City-Guide. Claude = Informatiker/PM/CD. **Hochdeutsch mit Remo, Züridütsch für On-Site-Copy.** Remo arbeitet auf geliehenem Mac (Committer „Alessandra Christen" = kosmetisch), pusht selbst via VS-Code-Terminal.

## ARBEITS-WORKFLOW (bewährt, strikt einhalten)
1. Claude baut in Sandbox, validiert (Div-Balance, `node --check` Browser-Modus), liefert via ZIP/Einzeldatei.
2. Remo lädt runter → **ein** Bash-Block: unzip aus ZIP → **BEWEIS-grep** (Marker-Zahl >0, sonst STOPP!) → add/commit/pull --rebase/push. ⚠ **Downloads = Minenfeld** (alte Dateiversionen!) → nie blind `cp` aus Downloads, immer gezielt aus dem ZIP + Beweis-grep.
3. SQL: Claude liefert idempotente Dateien → Remo kopiert in Supabase SQL-Editor → Run. Mehrfach ausführen = gefahrlos.
4. **Deploy:** GitHub Pages kann hängen (Fail-Mail „deploy failed") → `git commit --allow-empty -m redeploy && git push` oder Actions→Re-run. Tests immer im privaten Tab mit `?v=2`.
5. Git-Reihenfolge: **erst committen, dann pullen** („Your name and email…" = Info, kein Fehler).

## TECHNIK-FAKTEN
- Repo `remoschenk007/Stadtpuls`, branch main, lokal `/Users/alessandrachristen/stadtpuls/`. GitHub Pages = depuls.ch.
- Supabase `https://pnynkzrqnfoshojqfqxn.supabase.co`, anon-Key public im Code (voll in jeder Seite). RLS bewusst permissiv (anon select/insert/update auf Formular-/Betriebstabellen). Auth aktiv (`users.auth_id`↔auth.uid, UNIQUE).
- Design-DNA: bg #04040a · rot #ff2d00 · volt #c8ff00 · cyan #00f5ff · purple #9333ea · pink #ec4899 · cream #e8e4d9 · Barlow Condensed Italic 900 + DM Mono · **Hex, nie CSS-Var** · Emojis nie als Funktions-Icons (SVG!).
- Auto-Sync: GitHub Action täglich 04:00 (Eventfrog+ZT→Supabase), SERVICE_KEY-Secret gesetzt (nächtliches Aufräumen). `datum_start` = DATE-String; „heute" immer `Europe/Zurich`.

## SYSTEM-ZUSTAND (alles LIVE + GETESTET ✅)
- **Auth komplett** (→ Masterplan §5.6): Registrieren→Mail→Onboarding-Guard→Dashboard; Trigger `handle_new_user` (Auto-Profil, auch OAuth); 1 User=1 Account; Passwort-Reset (Nur-E-Mail-Screen → „NÖIS PASSWORT."); Account-Löschen Danger Zone (RPC `delete_my_account`, revDSG). Stadtpuls-Mail-Templates. Redirect-URLs: onboarding/dashboard/login.
- **Momänt-Kette ✅:** feedback.html-Blase → Zentrale/Moderation „◉ ZÜRI MOMÄNT" → „Uf d Startsite" → Gold-Sektion auf index (Zurückziehen möglich). News-Teaser analog. **📥 Inbox-Tab:** Kontakt + alle Blasen, „Gelese"/mailto.
- **Kommandozentrale v3:** Login-gated; Moderation (KI-ready: ki_urteil-Felder, Edge Function `moderate` liegt bereit, nicht deployed), Verkauf (boost_requests aus platzierung.html), Boosts (Featured 20/Boost 50/Premium 100 CHF/Wo, Auto-Ablauf), Finanzen, Inbox, Audit.
- **Startseite:** Hero+Live-Stats → Hüt Abig (CH-Datum, rollt täglich) → Universum (`?kreis=` → vorgefilterte Listen) → ◉ Momänt → News → **💘 Dates-Teaser + 🎲 Überrasch-mi** → Community-CTA.
- **Alle 9 Seiten:** einheitliche Nav + Hamburger-Fullscreen-Menü, Touch-Cursor-Fix, Züridütsch (ZUE/LADED/ZRUGG…), tote ?page=-Links raus. Nachtleben: Design v2, Control-Deck, 🎲; Profile (event/nachtleben): echter ❤️-Bookmark (bookmarks-Tabelle), View-Tracking, ⏳ Countdown, 📅 .ics, ❤️/👁-Zähler (RPC `stadtpuls_stats`).
- **KI-Herz Schritt 1 aktiv:** sp-track.js sammelt (bookmarks/interactions), Blueprint = Quelle der Wahrheit.
- SQL-Funktionen live: `stadtpuls_stats`, `delete_my_account`, `handle_new_user`(Trigger), `stadtpuls_expire_boosts`.

## OFFENE PRIORITÄTEN (Reihenfolge)
1. **Money-Loop schliessen:** Listen (gastro/nachtleben/shopping/events) nach `featured`/`boost_tier` sortieren + **„Das isch mis Lokal"-Button** auf Profilseiten → platzierung.html?id=…
2. **Gastro-/Shopping-Profil:** Fake-Bookmark (alert „Phase 5") durch echtes ❤️ ersetzen (Muster: nachtleben-profil) + sp-track.
3. **Custom SMTP** (Hosttech no-reply@depuls.ch) — Pflicht vor Launch (Supabase-Mail-Rate-Limits!). Optional: Dark-Mode-Meta in Mail-Templates.
4. **quartiere.html** bauen (Footer-Links teils 404: quartiere, musik, jobs, immobilien, mobilitaet, community, gps, partners).
5. **KI-Herz Schritt 2:** taste-build (Geschmacks-DNA) → „Für dich"-Feed → notify-build (Blueprint §6).
6. Design-v2/Control-Deck-Rollout auf gastro/shopping/events; Skeleton-Loading; echte Reviews.
7. Optional: `cleanup_demo.sql` (Demo-Anfragen Rossi & Co. raus, liegt bereit).
8. Danach: raus und verkaufen — erste 10 Lokale, 50 User (PM-Audit: „Motor stark, Sprit fehlt").

## STIL-ERWARTUNG AN CLAUDE
Vollgas, proaktiv mitdenken, ehrlich (keine Fake-Features verschweigen), Diagnose vor Fix, alles validieren, Schritt-für-Schritt-Anleitungen mit Beweis-Checks, PM-Blick aufs grosse Ganze (Cold-Start!), und den Blueprint/Masterplan bei jedem Meilenstein fortschreiben.
