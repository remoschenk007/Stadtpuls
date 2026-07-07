-- ============================================================
-- STADTPULS · SP_BOOST v2 — Money-Loop
-- Events boostbar machen + Expire-Funktion für BEIDE Tabellen.
-- Idempotent: mehrfach ausführen = gefahrlos.
-- ============================================================

-- 1) Boost-Spalten auf eventfrog_events (locations hat sie bereits)
alter table if exists eventfrog_events add column if not exists featured boolean default false;
alter table if exists eventfrog_events add column if not exists boost_until timestamptz;
alter table if exists eventfrog_events add column if not exists boost_tier text;

-- 2) Indizes für die Boost-Queries (Listen + GRAD ANGSAGT)
create index if not exists idx_loc_boost on locations(boost_tier, boost_until) where boost_tier is not null;
create index if not exists idx_ev_boost  on eventfrog_events(boost_tier, boost_until) where boost_tier is not null;

-- 3) Expire-Funktion: räumt jetzt BEIDE Tabellen auf.
--    Zusätzlich Sicherheitsnetz: auch Einträge ohne boosts-Zeile fallen zurück.
create or replace function stadtpuls_expire_boosts() returns void as $$
begin
  update locations l set featured=false, boost_until=null, boost_tier=null
   from boosts b
   where b.ziel_typ='location' and b.ziel_id=l.id::text
     and b.status='aktiv' and b.ende < now();

  update eventfrog_events e set featured=false, boost_until=null, boost_tier=null
   from boosts b
   where b.ziel_typ='event' and b.ziel_id=e.id::text
     and b.status='aktiv' and b.ende < now();

  -- Sicherheitsnetz (unabhängig von boosts-Tabelle)
  update locations        set featured=false, boost_tier=null, boost_until=null
   where boost_until is not null and boost_until < now();
  update eventfrog_events set featured=false, boost_tier=null, boost_until=null
   where boost_until is not null and boost_until < now();

  update boosts set status='abgelaufen' where status='aktiv'  and ende  < now();
  update boosts set status='aktiv'      where status='geplant' and start <= now() and ende > now();
end;
$$ language plpgsql;

-- 4) RLS-Policies für eventfrog_events (nur falls RLS aktiv ist; ändert den
--    RLS-Status selbst NICHT). Zentrale (anon) muss update dürfen zum Freischalten.
do $$ begin
  if exists (select 1 from pg_tables where schemaname='public' and tablename='eventfrog_events') then
    begin
      drop policy if exists sp_ev_select on public.eventfrog_events;
      create policy sp_ev_select on public.eventfrog_events for select using (true);
      drop policy if exists sp_ev_update on public.eventfrog_events;
      create policy sp_ev_update on public.eventfrog_events for update using (true) with check (true);
    exception when others then null; -- Policies optional, kein Abbruch
    end;
  end if;
end $$;

-- 5) Kontrolle: aktive Boosts anzeigen
select 'locations' as tabelle, id::text, name, boost_tier, boost_until
  from locations where boost_until is not null and boost_until >= now()
union all
select 'events', id::text, titel, boost_tier, boost_until
  from eventfrog_events where boost_until is not null and boost_until >= now();
