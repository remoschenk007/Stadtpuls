-- Einmalig im Supabase SQL-Editor (bereits ausgefuehrt — nur zur Sicherheit beigelegt).
ALTER TABLE eventfrog_events ADD COLUMN IF NOT EXISTS veranstalter text;
ALTER TABLE eventfrog_events ADD COLUMN IF NOT EXISTS bild_credit  text;
