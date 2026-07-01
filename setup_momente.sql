-- ============================================================
-- ZÜRI MOMÄNT — Freischalt-Feld für die Startseite
-- Einmal im Supabase SQL-Editor ausführen.
-- ============================================================
alter table feedback add column if not exists status text default 'neu';
update feedback set status='neu' where status is null;

-- FREISCHALTE (machst du selber, z.B. so):
--   1) Anschauen:  select id, text, created_at from feedback where typ='moment' and status='neu' order by created_at desc;
--   2) Freigeben:  update feedback set status='approved' where id='<DIE-ID>';
--   3) Zurückziehen: update feedback set status='neu' where id='<DIE-ID>';
-- Die Startseite zeigt automatisch die 3 neuesten mit status='approved'.
