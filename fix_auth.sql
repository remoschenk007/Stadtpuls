-- ============================================================
-- STADTPULS — AUTH-FIX (einmal im Supabase SQL-Editor ausführen)
-- Behebt: fehlende Profile, Duplikate, Google/Apple ohne Profil.
-- ============================================================

-- 1) DUPLIKATE bereinigen (gleiche auth_id mehrfach):
--    abhängige Daten auf den ältesten Eintrag umhängen, Rest löschen.
with keep as (
  select distinct on (auth_id) id, auth_id from users
  where auth_id is not null order by auth_id, created_at asc nulls last, id
), dupes as (
  select u.id dup_id, k.id keep_id from users u
  join keep k on k.auth_id=u.auth_id and k.id<>u.id
)
update bookmarks b set user_id=d.keep_id from dupes d where b.user_id=d.dup_id;

with keep as (
  select distinct on (auth_id) id, auth_id from users
  where auth_id is not null order by auth_id, created_at asc nulls last, id
), dupes as (
  select u.id dup_id, k.id keep_id from users u
  join keep k on k.auth_id=u.auth_id and k.id<>u.id
)
update interactions i set user_id=d.keep_id from dupes d where i.user_id=d.dup_id;

with keep as (
  select distinct on (auth_id) id, auth_id from users
  where auth_id is not null order by auth_id, created_at asc nulls last, id
)
delete from users u where u.auth_id is not null
  and u.id not in (select id from keep);

-- 2) EINMAL-ACCOUNT-GARANTIE: eine auth_id = genau ein Profil
create unique index if not exists users_auth_id_unique on users(auth_id);

-- 3) AUTO-PROFIL-TRIGGER: JEDER neue Auth-User (E-Mail, Google, Apple)
--    bekommt automatisch sein users-Profil — kein Client-Code nötig.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path=public as $$
begin
  insert into public.users (auth_id, nickname, role, aktiv)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'nickname', split_part(new.email,'@',1), 'zuerianer'),
    'user', true
  )
  on conflict (auth_id) do nothing;
  return new;
end; $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- 4) BACKFILL: bestehende Auth-User ohne Profil nachziehen
insert into public.users (auth_id, nickname, role, aktiv)
select a.id,
       coalesce(a.raw_user_meta_data->>'nickname', split_part(a.email,'@',1), 'zuerianer'),
       'user', true
from auth.users a
left join public.users u on u.auth_id=a.id
where u.id is null
on conflict (auth_id) do nothing;

-- 5) KONTROLLE: beide Zahlen sollten gleich sein, dupes=0
select
 (select count(*) from auth.users) auth_users,
 (select count(*) from users where auth_id is not null) profile,
 (select count(*) from (select auth_id from users where auth_id is not null group by auth_id having count(*)>1) d) dupes;
