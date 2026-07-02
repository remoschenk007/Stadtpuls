-- ============================================================
-- INBOX + KI-ZUKUNFT — einmal im Supabase SQL-Editor ausführen
-- ============================================================
-- Kontaktformular-Tabelle (falls noch nicht vorhanden) + Gelesen-Status
create table if not exists kontakt_submissions (
  id uuid primary key default gen_random_uuid(),
  wer text, was text, nachricht text, email text,
  status text default 'neu',
  created_at timestamptz default now()
);
alter table kontakt_submissions add column if not exists status text default 'neu';
update kontakt_submissions set status='neu' where status is null;

-- KI-Zukunft: Feedback (inkl. Momänt) KI-moderierbar machen.
-- Sobald die moderate-Edge-Function feedback prüft, zeigt die Zentrale
-- automatisch ✓sicher/⚠prüfen/⛔schwer — unsichere Fälle bleiben bei dir.
alter table feedback add column if not exists ki_urteil text;
alter table feedback add column if not exists ki_konfidenz numeric;
alter table feedback add column if not exists ki_grund text;
