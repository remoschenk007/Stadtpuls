-- ============================================================
-- STADTPULS · TAUSCH-GUERILLA — Lean-Test Warteliste
-- Anonym: kei Name, kei Adresse. Nur Match-Date + Mail.
-- Datenschutz: anon darf NUR inserte. Läse: nur du (Dashboard)
-- + öffentliche Zähl-Funktion (gibt nur die Zahl zurück).
-- Idempotent.
-- ============================================================
create table if not exists wohnig_tuusche (
  id uuid primary key default gen_random_uuid(),
  biete_kreis int,
  biete_zimmer numeric,
  biete_miete int,
  suche_kreis int,          -- 0 = egal
  suche_zimmer numeric,
  email text,
  notiz text,
  created_at timestamptz default now()
);
alter table wohnig_tuusche enable row level security;
drop policy if exists tuusche_insert on wohnig_tuusche;
create policy tuusche_insert on wohnig_tuusche for insert with check (true);
-- KEINE select-Policy für anon: Wohnigs-Date sind privat.

-- Öffentliche Zähl-Funktion (Social Proof ohni Datenleck)
create or replace function stadtpuls_tuusche_count()
returns bigint language sql stable security definer
set search_path = public as $$
  select count(*) from wohnig_tuusche;
$$;
grant execute on function stadtpuls_tuusche_count() to anon;

-- Kontrolle:
select stadtpuls_tuusche_count() as warteliste;
