# MASTERPLAN-UPDATE — Session 22. Juli 2026

## 1. Eventfrog-API-Rate-Limit gefixt
`import_eventfrog.py` warf bei vielen Requests hintereinander `429 Too Many Requests`. Neue zentrale Funktion `ef_get()` mit Retry + exponentiellem Backoff (3s→6s→12s→24s→30s, max. 5 Versuche) plus feste Pausen zwischen Requests (0.4–0.6s). Ergebnis: alle 504 Locations lösen sich auf, alle neuen Events kriegen eine echte Adresse (2414 Events importiert, 100% mit Adresse).

## 2. Adress-Backfill für alte Events
Neues Skript `backfill_adressen.py`: holt alle ~3000 bestehenden Events ohne Adresse, versucht sie über die Eventfrog-Location-API aufzulösen. Ergebnis:
- **2833 Events** bekamen eine echte Adresse nachgetragen (Upsert, andere Felder bleiben unberührt).
- **167 Events** waren auf Eventfrog nicht mehr auffindbar oder hatten dort auch keine Adresse → wurden gelöscht (auf Remos Wunsch: „Ich will die schlechten Daten aber draußen haben").

## 3. Event-Karte farblich an Gastro angeglichen
`event-profil.html`: Leaflet/CartoDB-Karte ersetzt durch dasselbe Google-Maps-iframe wie bei `gastro-profil.html`. Ein Nachfix war nötig: `mix-blend-mode:luminosity` liess die Karte auf Events-Seiten blass wirken (auf Gastro nicht, Browser-Eigenheit) → Blend-Mode entfernt, Karte jetzt vollfarbig wie gewünscht.

## 4. Neues Favicon
`favicon.svg` — Puls-Symbol (rote EKG-Linie auf schwarzem Rund) statt altem Icon. Live.

## 5. Kreis-Universum auf der Startseite gebaut
Vorher: Die komplette Bubble-Galaxie-UI (`.ku-*` CSS) existierte, aber ohne jede funktionierende JavaScript-Logik — reine Attrappe.

Jetzt (`index.html`, Marker `SP_KU_LIVE v1`): volles Modul mit
- Kreis-Auswahl (1–12, Chips)
- 5 Kategorie-Blasen mit echten Live-Zählern aus Supabase: **gastro** (#ff2d00), **nachtleben** (#9333ea), **kultur** (#00f5ff), **shopping** (#c8ff00), **events** (#ec4899)
- Klick auf Blase → Ergebnis-Sheet mit echten Top-Einträgen
- „Frag Stadtpuls"-Suche über alle Kategorien gleichzeitig
- CTA-Button im Sheet gibt den gewählten Kreis als `?kreis=N` an die Zielseite weiter (Marker `SP_KU_CTA_KREIS v1`)

Verifiziert: Remo hat Live-Zahlen gesehen (32/31/5/18/411 für Kreis 4) und funktionierende Klicks.

## 6. Kreis-Filter site-weit repariert (Fund: alter, unabhängiger Bug)
Beim Testen fiel auf: die Kreis-Filter-Buttons (`.kr-btn`, rufen `setKreis(...)` auf) waren auf **gastro.html, kultur.html, shopping.html** komplett tot — die Funktion `setKreis()` war nirgends definiert (vermutlich aus einer nie fertiggestellten früheren Bauphase). **events.html** hatte gar keinen echten Filter, nur eine dekorative Kreis-Statistik-Leiste.

Nach Remos „ja alles bearbeiten ;) lets go" wurden alle vier Seiten repariert/gebaut (`SP_KREIS_FIX v1`):
- kultur.html / shopping.html: fehlende `setKreis()` ergänzt (URL-Hook gab's schon)
- gastro.html: `setKreis()` + eigener `?kreis=`-URL-Hook per Polling ergänzt (wartet auf geladene Daten)
- events.html: echter klickbarer Kreis-Filter gebaut inkl. `?kreis=`-URL-Hook
- nachtleben.html: war schon korrekt, nicht angefasst

Alle vier Commits gepusht und bestätigt.

## 7. OFFEN / UNGELÖST: Phantom-Blasen-UI bei Remo
Nach allen Fixes berichtete Remo, dass er auf depuls.ch/index.html (Desktop-Chrome, normales Fenster, viele Tabs offen) weiterhin eine **alte, komplett andere Version** der Kreis-Universum-Blasen sieht:

- 6 Blasen statt 5: **Gastro, News, Nachtlebe, Shopping, Dates, Events** — **Kultur fehlt komplett**, dafür „News" und „Dates" als eigene Blasen (die es in meinem Code nie gab)
- Fake-wirkende Werte wie „137 Lokal", „60 Clubs", „284 Ort", „87 Shops"
- Auch nach `Cmd+Shift+R` (Hard-Refresh) auf demselben Tab weiterhin sichtbar
- Auch ein früherer Test im mobilen Inkognito-Fenster zeigte dieselben alten Blasen

**Was bereits ausgeschlossen wurde** (mit Belegen):
- **Git/Branch:** `git log --oneline -- index.html` zeigt die richtigen Commits (`bb15895be`, `07dbfab51`) klar an der Spitze, lokal UND auf `origin/main`.
- **GitHub-Pages-Branch-Konfiguration:** Settings → Pages bestätigt: Source = „Deploy from a branch", Branch = **main**, Pfad `/(root)` — kein Branch-Mismatch.
- **Build-Erfolg:** Actions/„pages build and deployment" läuft grün, letzter Deploy laut Pages-Seite „1 hour ago".
- **Drittanbieter-CDN:** DNS-Check (`dns.google/resolve`) zeigt Hosttech-Nameserver + die vier Standard-GitHub-Pages-IPs (185.199.108–111.153) — kein Cloudflare o.ä. davor.
- **Der Code selbst ist korrekt:** Ein cache-gebusteter Fetch von `raw.githubusercontent.com/.../main/index.html?nocache=...` zeigt eindeutig den richtigen Code: `SP_KU_LIVE v1`-Marker vorhanden, `CATS`-Array mit genau den 5 richtigen Kategorien (gastro/nachtleben/**kultur**/shopping/events), keine Spur von „News"- oder „Dates"-Blasen im `renderBubbles()`-Code. → Das Problem liegt NICHT im Repo/Commit selbst.
- Ein erster Fetch von `raw.githubusercontent.com` OHNE Cache-Busting zeigte fälschlicherweise noch die alte Version — bekanntes, dokumentiertes Cache-Verhalten dieser Domain, kein verlässlicher Test.

**Bisher NICHT gefunden:** die tatsächliche Quelle der alten Blasen-Version. Sie tritt bei Remo konsistent auf (Desktop + Mobile, normal + Inkognito, vor UND nach Hard-Refresh), obwohl der Quellcode im Repo nachweislich korrekt ist. Das deutet auf einen Caching-Layer zwischen GitHub Pages und Remos Endgeräten, der über normales Browser-Cache und einfaches Hard-Refresh hinausgeht — möglich wären z.B. ein hartnäckiger Service-Worker (falls die Seite mal einen registriert hatte), ein ISP-/Mobilfunk-Proxy-Cache, oder ein noch nicht lange genug abgewartetes GitHub-Pages-eigenes Edge-Caching (Fastly) für Remos spezifischen Netzwerkpfad.

**Nächste sinnvolle Schritte für den nächsten Chat:**
1. Remo bitten, in den Chrome-DevTools unter Application → Service Workers nachzuschauen, ob für depuls.ch ein Service Worker registriert ist — falls ja, „Unregister" + Seite neu laden.
2. Testen von einem komplett anderen Netz (z.B. Mobilfunk statt WLAN oder umgekehrt), um Netzwerkpfad-Caching auszuschliessen.
3. Prüfen, ob evtl. irgendwo im Repo eine zweite Kopie mit altem Bubble-Code existiert (z.B. in `onboarding_preview.html`, `master.html` oder einer anderen HTML-Datei, die versehentlich verlinkt/eingebettet wird) — noch nicht durchsucht.
4. Falls nichts hilft: `git commit --allow-empty -m "Force redeploy" && git push`, dann 10–15 Min warten und mit `?v=<neue-zahl>` an der URL testen.
