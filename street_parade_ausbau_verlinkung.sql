-- ============================================================
-- STADTPULS · Street Parade 2026 · Ausbau + Querverlinkung
-- Baut die 4 kurzen Kreis-Artikel auf 2-3 volle Absätze aus
-- (kein Thin-Content mehr) und verlinkt alle Seiten kontextuell
-- mit sprechendem Ankertext ([Text](URL)-Syntax).
--
-- Ausführen im Supabase SQL-Editor (Role: postgres).
-- Danach: Generator laufen lassen + pushen (Befehl unten in Notiz).
-- ============================================================

-- ---------- KREIS 1 · Bellevue / Anreise / Sanität ----------
update news_stories set inhalt = $$S Bellevue und de Bürkliplatz sind s geografische Härz vo de Street Parade: do biegt d Route vom Utoquai über d Quaibrugg und laufft de Seepromenade entlang bis zur Enge. Wer mittedrin sii will, isch am Bellevue am richtige Ort – aber genau drum au am dichtiste.
Anreise unbedingt mit em ÖV: Tram und Bus rund ums Seebecke sind ab em früene Nomittag komplett überlaste, und viili Haltestelle werded während de Parade umgleitet oder gsperrt. Plan Reserve ii und schau vorher d Umleitige vo de VBZ aa. Mit em Auto häre z choo isch praktisch unmöglich – kei Parkplätz, gsperrti Strasse.
Am Sechseläutenplatz und am Bürkliplatz staht je en grosse Sanitätsposchte – merk dir de Standort scho bim Aachoo. Mach mit dinere Crew en fixe Treffpunkt und e Ziit ab, well s Handy-Netz am Nomittag regelmässig zämebricht. Wenns öpperem schlächt gaht: kei Sekunde zögere, Sanität 144, Polizei 117.
📍 Meh zur Street Parade: [See-Afterparty & Abkühlig am Utoquai (Kreis 8)](https://depuls.ch/kreis-8/news/street-parade-2026-utoquai-sanitaet-und-see-afterparty/), s [ruhige Route-Ände z Enge (Kreis 2)](https://depuls.ch/kreis-2/news/street-parade-2026-enge-ziel-und-chill-out/) und de komplett [Safer-Party-Guide mit Drug-Checking (Kreis 4)](https://depuls.ch/kreis-4/news/safer-party-an-der-street-parade-2026-zuerich/).$$
where kreis = 1 and slug = $$street-parade-2026-bellevue-sanitaet-und-anreise$$;

-- ---------- KREIS 8 · Utoquai / See / Afterparty ----------
update news_stories set inhalt = $$De Utoquai im Seefeld isch de Startbereich vo de Street Parade und d Sunneseite vom Fescht: do rollt en Grossteil vo de Love Mobiles em See entlang los. Es isch offe, luftig und näb am Wasser – aber genau drum au knallheiss, wenn d Sunne brennt.
S Seebecke isch dini natürlichi Klimaanlage: churz d Füess is Wasser oder e Abchüehlig am Utoquai wirkt Wunder. Aber Achtung – nie betrunke oder uf Substanze is Wasser, jedes Jahr passiered so Unfäll. Und trink regelmässig, au wenn d nöd durstig bisch, well d Kombination us Hitz, Tanze und Konsum de Körper extrem uslaugt.
Entlang vom Utoquai staht e Reihe Sanitätsposchte; bi Schwindel, Übelkeit oder Zeiche vo Überhitzig (trockeni, rote Haut, Verwirrig) sofort häre oder Notruf 144. Nach de Parade wird s Seefeld zur Afterparty-Zone am Wasser – pass uf dini Buddies uf und gönn dim Körper Pause.
📍 Meh zur Street Parade: [Anreise & Sanität am Bellevue (Kreis 1)](https://depuls.ch/kreis-1/news/street-parade-2026-bellevue-sanitaet-und-anreise/), d [Afterparty-Clubs z Züri-West (Kreis 5)](https://depuls.ch/kreis-5/news/street-parade-2026-zueri-west-afterparty-clubs/) und de [Safer-Party-Guide mit Drug-Checking (Kreis 4)](https://depuls.ch/kreis-4/news/safer-party-an-der-street-parade-2026-zuerich/).$$
where kreis = 8 and slug = $$street-parade-2026-utoquai-sanitaet-und-see-afterparty$$;

-- ---------- KREIS 2 · Enge / Ziel / Chill-Out ----------
update news_stories set inhalt = $$D Parade-Route endet im Kreis 2, bi de Rentenaastalt und em Arboretum a de Seespitze. Do isch s ruhigere Ände vom Umzug – weniger Gedränge als am Bellevue, meh Platz zum durchschnufe.
S Arboretum und d Seeanlage sind de perfekt Ort zum abkühle, Wasser trinke und churz sitze, wenns dir z viel wird. Vo do chunnsch au schnäll wäg vom Gwühl: d Enge het en eigne Bahnhof und gueti Tram-Verbindige, drum eignet sie sich guet zum ruhige Heiweg, wenn s Zentrum überlaufe isch.
Au am Route-Ände het s Sanitätsposchte – merk dir de nächscht, bevor d en bruuchsch. Und pass uf di und dini Lüt uf: Sanität 144, und für psychischi Unterstützig d Dargebotni Hand 143.
📍 Meh zur Street Parade: de [Startbereich & Sanität am Bellevue (Kreis 1)](https://depuls.ch/kreis-1/news/street-parade-2026-bellevue-sanitaet-und-anreise/) und de komplett [Safer-Party-Guide mit Drug-Checking (Kreis 4)](https://depuls.ch/kreis-4/news/safer-party-an-der-street-parade-2026-zuerich/).$$
where kreis = 2 and slug = $$street-parade-2026-enge-ziel-und-chill-out$$;

-- ---------- KREIS 5 · Züri-West / Afterparty-Clubs ----------
update news_stories set inhalt = $$Wenn d Parade am Abig usklinget, wird Züri-West zum Afterparty-Epizentrum. Rund um d Hardbrugg und im Industriequartier reiht sich Club a Club – vo grosse Floors bis zu chline, verschwitzte Kellerpartys.
Plan dini Afterparty im Voruus: viili Partys sind im Vorverkauf usverchauft, und spontan a de Tür wird a dem Wochenänd schwierig. Sichere dir s Ticket früe und schau, wele Clubs überhaupt no Platz händ und wele Line-ups zu dir passed.
Trink zwüschedure Wasser und gib dim Körper Pause – d Nacht isch lang, und de Mischkonsum vo Alkohol und anderem isch de häufigscht Grund für Notfäll. Heiweg: Nachtbus und Nachttram fahred, sind aber rappelvoll, drum plan dini Route. Notfall: Sanität 144.
📍 Meh zur Street Parade: d [See-Afterparty am Utoquai (Kreis 8)](https://depuls.ch/kreis-8/news/street-parade-2026-utoquai-sanitaet-und-see-afterparty/) und de [Safer-Party-Guide mit Drug-Checking (Kreis 4)](https://depuls.ch/kreis-4/news/safer-party-an-der-street-parade-2026-zuerich/).$$
where kreis = 5 and slug = $$street-parade-2026-zueri-west-afterparty-clubs$$;

-- ---------- KREIS 4 · Hauptartikel: Querverlinkig aahänge ----------
update news_stories set inhalt = inhalt || $$

📍 Route & Quartier: D Parade selber laufft ums Seebecke – Infos zu [Anreise & Sanität am Bellevue (Kreis 1)](https://depuls.ch/kreis-1/news/street-parade-2026-bellevue-sanitaet-und-anreise/), zur [See-Afterparty am Utoquai (Kreis 8)](https://depuls.ch/kreis-8/news/street-parade-2026-utoquai-sanitaet-und-see-afterparty/), zum [Route-Ände z Enge (Kreis 2)](https://depuls.ch/kreis-2/news/street-parade-2026-enge-ziel-und-chill-out/) und zu de [Afterparty-Clubs z Züri-West (Kreis 5)](https://depuls.ch/kreis-5/news/street-parade-2026-zueri-west-afterparty-clubs/).$$
where kreis = 4 and slug = $$safer-party-an-der-street-parade-2026-zuerich$$;
