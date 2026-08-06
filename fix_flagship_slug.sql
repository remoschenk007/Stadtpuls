-- ============================================================
-- STADTPULS · Slug-Korrektur Flagship-Story
-- Der Slug muss zum Titel passen (inkl. "jetzt"), sonst 404,
-- weil die /news/-Seite den Link aus dem Titel generiert.
-- Im Supabase SQL-Editor ausführen (Role: postgres).
-- ============================================================

update news_stories
set slug = 'vergiss-homegate-warum-zuercher-ihre-wohnungen-jetzt-tauschen'
where slug = 'vergiss-homegate-warum-zuercher-ihre-wohnungen-tauschen';
