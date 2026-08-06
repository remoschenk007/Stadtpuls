-- ============================================================
-- STADTPULS · Street Parade 2026 · Kreis-Verteilung
-- Eigenständige Lokal-Artikel (KEIN Duplikat) für die Kreise,
-- welche die Parade-Route wirklich berührt.
-- Autor: Redaktion Stadtpuls · Status: live
-- Jeder Text verlinkt auf den Hauptartikel in Kreis 4.
--
-- Ausführen im Supabase SQL-Editor (Role: postgres).
-- Danach: Generator laufen lassen + pushen (siehe Notiz am Ende).
--
-- Hinweis: Willst du Kreis 5 (Afterparty-Clubs) NICHT, lösch
-- einfach den letzten (5, …)-Block vor dem Semikolon.
-- ============================================================

insert into news_stories (kreis, titel, slug, teaser, inhalt, kategorie, autor, status) values

-- ---------- KREIS 1 · Altstadt / Bellevue ----------
(1,
 $$Street Parade 2026 Bellevue Sanität und Anreise$$,
 $$street-parade-2026-bellevue-sanitaet-und-anreise$$,
 $$Alles zur Anreise, zum Haupt-Sanitätsposchte und zum Treffpunkt am Bellevue.$$,
 $$S Bellevue isch s Nadelöhr vo de Street Parade – do trifft alles zäme, vo de Quaibrugg bis zum Bürkliplatz.
Anreise: Nimm s Tram oder chum z Fuess. Am Nomittag sind d ÖV-Linie rund ums Seebecke komplett überlaste, drum plan gnueg Ziit ii.
Am Sechseläutenplatz und am Bürkliplatz staht je en grosse Sanitätsposchte – merk dir de Standort, falls dir oder öpperem schlächt wird.
Treffpunkt-Tipp: Mach mit dinere Crew en fixe Treffpunkt ab, well s Handy-Netz am Nomittag meischtens komplett überlaste isch.
Kei Sekunde zögere, wenns öpperem nöd guet gaht: Sanität 144, Polizei 117.
👉 Kompletter Safety-Guide zur Street Parade: https://depuls.ch/kreis-4/news/safer-party-an-der-street-parade-2026-zuerich/$$,
 $$Nachtlebe$$, $$Redaktion Stadtpuls$$, $$live$$),

-- ---------- KREIS 8 · Seefeld / Utoquai ----------
(8,
 $$Street Parade 2026 Utoquai Sanität und See-Afterparty$$,
 $$street-parade-2026-utoquai-sanitaet-und-see-afterparty$$,
 $$Sanitätszelt, s Seebad zum Abkühle und d Afterparties am Utoquai.$$,
 $$S Seefeld am Utoquai isch d Sunneseite vo de Parade – do rollt en Grossteil vo de Love Mobiles am See entlang.
Bi extreme Hitz isch de Zugang zum See dini beschti Abkühlig – aber niemals betrunke oder uf Substanze is Wasser.
Entlang vom Utoquai staht e Reihe Sanitätsposchte; bi Schwindel, Übelkeit oder Überhitzig sofort häre.
Nach de Parade wird s Seefeld zur Afterparty-Zone – pass uf dini Buddies uf und trink gnueg Wasser.
Warnzeiche für en Hitzschlag: trockeni, rote Haut, Verwirrig, Schwindel → sofort in Schatte und Notruf 144.
👉 Kompletter Safety-Guide zur Street Parade: https://depuls.ch/kreis-4/news/safer-party-an-der-street-parade-2026-zuerich/$$,
 $$Nachtlebe$$, $$Redaktion Stadtpuls$$, $$live$$),

-- ---------- KREIS 2 · Enge / Rentenanstalt ----------
(2,
 $$Street Parade 2026 Enge Ziel und Chill-Out$$,
 $$street-parade-2026-enge-ziel-und-chill-out$$,
 $$S ruhige Ände vo de Route bi de Rentenaastalt – Chill-Out und Abschluss.$$,
 $$D Parade-Route lauft bis zur Rentenaastalt und zum Arboretum im Kreis 2 – do isch s ruhigere Ände vom Umzug.
Wenns dir z viel wird, isch de Arboretum-Park de perfekt Ort zum durchschnufe, Wasser trinke und abkühle.
Au do het s Sanität – merk dir de nächscht Poschte, bevor d en bruuchsch.
D Enge isch guet aagbunde: vo do chunnsch mit em Tram oder z Fuess schnäll wäg vom gröschte Gwühl.
Pass uf di und dini Lüt uf – Sanität 144, Dargebotni Hand 143.
👉 Kompletter Safety-Guide zur Street Parade: https://depuls.ch/kreis-4/news/safer-party-an-der-street-parade-2026-zuerich/$$,
 $$Nachtlebe$$, $$Redaktion Stadtpuls$$, $$live$$),

-- ---------- KREIS 5 · Züri-West (optional) ----------
(5,
 $$Street Parade 2026 Züri-West Afterparty Clubs$$,
 $$street-parade-2026-zueri-west-afterparty-clubs$$,
 $$Nach de Parade: d Afterparty-Clubs z Züri-West rund um d Hardbrugg.$$,
 $$Wenn d Parade fertig isch, wird Züri-West zum Afterparty-Epizentrum – rund um d Hardbrugg reiht sich Club a Club.
Plan dini Afterparty im Voruus: viili Partys sind im Vorverkauf uus, spontan a de Tür wird schwierig.
Trink zwüschedure Wasser und gib dim Körper Pause – d Nacht isch lang.
Heiweg: de Nachtbus und s Nachttram fahred, aber sind rappelvoll – plan dini Route.
Pass uf di und dini Crew uf – Sanität 144.
👉 Kompletter Safety-Guide zur Street Parade: https://depuls.ch/kreis-4/news/safer-party-an-der-street-parade-2026-zuerich/$$,
 $$Nachtlebe$$, $$Redaktion Stadtpuls$$, $$live$$);
