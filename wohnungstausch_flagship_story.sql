-- ============================================================
-- STADTPULS · Flagship-Story "Vergiss Homegate"
-- SEO-Hauptartikel zum Wohnungstausch (Hochdeutsch für Reichweite).
-- Autor: Redaktion Stadtpuls · Status: live · Kreis 4 (Langstrasse)
-- Recht korrekt: Art. 264 OR (vorzeitige Rückgabe / Nachmieter),
--   NICHT Art. 263 OR (das betrifft Geschäftsräume).
--
-- Ausführen im Supabase SQL-Editor (Role: postgres).
-- Danach: python3 generate_kreis_news.py  +  committen & pushen.
-- ============================================================

insert into news_stories (kreis, titel, slug, teaser, inhalt, kategorie, autor, status) values
(4,
 $$Vergiss Homegate: Warum Zürcher ihre Wohnungen jetzt tauschen$$,
 $$vergiss-homegate-warum-zuercher-ihre-wohnungen-tauschen$$,
 $$300 Bewerber pro Besichtigung, Mietexplosionen und Kündigungsangst: Der Zürcher Wohnungsmarkt steht still. Ein anonymes, kreisgenaues Tausch-Matching bricht die Starre – legal nach Art. 264 OR.$$,
 $$Wer in Zürich eine bezahlbare Wohnung hat, zieht freiwillig nicht mehr aus. Das Resultat ist eine kollektive Blockade: Paare in Wiedikon ersticken in 2,5 Zimmern, während Pensionierte im Kreis 6 allein auf 120 Quadratmetern sitzen – weil jede kleinere Neuwohnung teurer wäre als ihre über Jahre gewachsene Altmiete.
Auf klassischen Portalen wie Homegate oder ImmoScout24 findet dieser Austausch schlicht nicht statt. Ihr Geschäftsmodell baut auf Einzelinseraten auf – ein Wohnungstausch passt nicht ins Raster. Und wer kündigt, bevor die neue Wohnung sicher ist, geht im Zürcher Markt ein unkalkulierbares Risiko ein.
🔺 Das Dreiecks-Problem – endlich gelöst
Der direkte Tausch scheitert meist an den Präferenzen: Person A möchte die Wohnung von Person B, aber B will in den Kreis 4, wo eigentlich C sitzt. Über Kleinanzeigen kommt so eine Kette nie zustande.
Genau hier setzt das Tausch-Matching von Stadtpuls an. Ein anonymes System gleicht Angebot und Nachfrage über alle zwölf Stadtkreise ab und erkennt auch Dreiecks- und Kettentausche (A → B → C → A), die von Hand niemand je zusammenbringen würde. Du hinterlegst, was du hast und was du suchst – den Rest übernimmt der Abgleich.
⚖️ Die Rechtslage: Wohnungstausch ist legal (Art. 264 OR)
Ein Wohnungstausch beziehungsweise die vorzeitige Rückgabe an einen Nachmieter ist in der Schweiz ausdrücklich zulässig – geregelt in Art. 264 OR. Drei Punkte sind entscheidend:
1. Zumutbarer Nachmieter: Die Verwaltung muss einen Ersatzmieter akzeptieren, sofern er zahlungsfähig und bereit ist, den Vertrag zu den gleichen Bedingungen zu übernehmen. Als Faustregel gilt ein Nettolohn von mindestens dem Dreifachen der Miete und ein sauberer Betreibungsauszug.
2. Neue Mietverträge: In der Praxis stellen Zürcher Verwaltungen meist neue Verträge aus. Ein eingespielter Tausch mit zwei bezugsbereiten Dossiers spart dem Vermieter jedoch Zeit und Leerstand – ein starkes Argument am Verhandlungstisch.
3. Erst matchen, dann anfragen: Kontaktiere die Verwaltung erst, wenn der passende Tauschpartner feststeht. So verhandelst du aus einer Position der Stärke statt aus der Kündigungsangst.
Das ist eine allgemeine Einordnung und keine Rechtsberatung – im konkreten Fall lohnt sich ein kurzer Check beim Mieterinnen- und Mieterverband.
👉 [Jetzt eigene Wohnung eintragen und anonym im Zürcher Tausch-Radar matchen](https://depuls.ch/wohnungstausch/)$$,
 $$Wohne$$, $$Redaktion Stadtpuls$$, $$live$$);
