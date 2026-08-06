-- ============================================================
-- STADTPULS · DB-Diagnose users-Tabelle
-- Zeigt, ob Profil-Änderungen pro User korrekt gespeichert werden:
-- (1) welche Spalten es gibt, (2) ob RLS aktiv ist, (3) welche Rechte.
-- Im Supabase SQL-Editor ausführen und die 3 Resultate zurückschicken.
-- Nur lesend — ändert nichts.
-- ============================================================

-- 1) Welche Spalten hat users?  (das Dashboard schreibt: nickname, kreis, bio,
--    interessen[], vibe, geburtsjahr, geschlecht, website, profil_oeffentlich,
--    bookmarks_oeffentlich, kontakt_erlaubt, notification_typen[])
select column_name, data_type
from information_schema.columns
where table_schema='public' and table_name='users'
order by ordinal_position;

-- 2) Ist RLS (Row Level Security) auf users aktiv?
select relname as tabelle, relrowsecurity as rls_aktiv
from pg_class where relname='users';

-- 3) Welche RLS-Policies gibt es? Wichtig: darf ein eingeloggter User
--    seine EIGENE Zeile lesen (SELECT) und ändern (UPDATE)?
--    -> Es sollte je eine SELECT- und eine UPDATE-Policy geben mit
--       qual/with_check in der Art: auth_id = auth.uid()
select policyname, cmd, roles, qual, with_check
from pg_policies
where schemaname='public' and tablename='users'
order by cmd, policyname;
