-- ============================================================
-- STADTPULS — KI-HERZ · SCHRITT 1: Signale einsammeln
-- Im Supabase SQL-Editor ausführen. Idempotent.
-- ============================================================

-- 1) BOOKMARKS — das stärkste explizite Signal ("das gefällt mir")
create table if not exists bookmarks (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,                 -- users.id
  ziel_typ text default 'location',  -- location | event
  ziel_id text,                 -- locations.id oder eventfrog_events.ef_id
  kategorie text,               -- denormalisiert für schnelle DNA-Aggregation
  kreis int,
  tags text[],                  -- Snapshot der stimmung_tags beim Bookmarken
  created_at timestamptz default now(),
  unique(user_id, ziel_typ, ziel_id)
);

-- 2) INTERACTIONS — leichtes Verhaltens-Log (Views/Klicks/Filter/Suche)
create table if not exists interactions (
  id bigint generated always as identity primary key,
  user_id uuid,                 -- null = anonym (zählt für "angesagt", nicht für DNA)
  aktion text,                  -- view_profile | click | open_list | filter | search | vote
  ziel_typ text,
  ziel_id text,
  kategorie text,
  kreis int,
  tags text[],
  meta jsonb,                   -- z.B. {"q":"pizza"} oder {"filter":"offe"}
  created_at timestamptz default now()
);
create index if not exists idx_interactions_user on interactions(user_id, created_at desc);
create index if not exists idx_interactions_ziel on interactions(ziel_typ, ziel_id);

-- 3) TASTE_PROFILES — die berechnete Geschmacks-DNA (Schritt 2 befüllt sie)
create table if not exists taste_profiles (
  user_id uuid primary key,
  tags jsonb default '{}'::jsonb,        -- {"pizza":0.8,"techno":0.3,...}
  kategorien jsonb default '{}'::jsonb,  -- {"gastro":0.7,"nachtleben":0.4}
  top_kreis int,
  vibe text,
  updated_at timestamptz default now()
);

-- ============================================================
-- RLS — User sieht/schreibt nur seine eigenen Signale (Supabase Auth)
-- users.auth_id == auth.uid()
-- ============================================================
alter table bookmarks      enable row level security;
alter table interactions   enable row level security;
alter table taste_profiles enable row level security;

-- Helfer-Ausdruck: die users.id des eingeloggten Users
-- (in Policies inline genutzt)

-- BOOKMARKS: eigener Datensatz (lesen/schreiben/löschen)
drop policy if exists bm_own on bookmarks;
create policy bm_own on bookmarks for all to authenticated
  using (user_id = (select id from users where auth_id = auth.uid()))
  with check (user_id = (select id from users where auth_id = auth.uid()));
-- öffentliche Bookmark-Listen (bookmarks_oeffentlich) — optional, später:
-- create policy bm_public_read on bookmarks for select to anon using (
--   exists(select 1 from users u where u.id=bookmarks.user_id and u.bookmarks_oeffentlich=true));

-- INTERACTIONS: eigene schreiben/lesen; anon darf anonyme Views loggen
drop policy if exists ia_own on interactions;
create policy ia_own on interactions for all to authenticated
  using (user_id = (select id from users where auth_id = auth.uid()))
  with check (user_id = (select id from users where auth_id = auth.uid()));
drop policy if exists ia_anon_insert on interactions;
create policy ia_anon_insert on interactions for insert to anon
  with check (user_id is null);

-- TASTE_PROFILES: User liest sein eigenes; Schreiben macht die Edge Function (service_role, umgeht RLS)
drop policy if exists tp_own_read on taste_profiles;
create policy tp_own_read on taste_profiles for select to authenticated
  using (user_id = (select id from users where auth_id = auth.uid()));

-- ============================================================
-- FERTIG. Danach: sp-track.js auf den Seiten einbinden (siehe LIESMICH).
-- ============================================================
