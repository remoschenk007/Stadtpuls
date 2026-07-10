-- ============================================================
-- STADTPULS · KREIS-PULS v1 — De Battle misst Mensche, nöd Bestand.
-- Score (7 Täg) = 3×Herze + 1×Klicks + 2×Events hüt, ÷ √(Lokale)
-- Idempotent: mehrfach ausführen = gefahrlos.
-- ============================================================
create or replace function stadtpuls_kreis_puls()
returns table(kreis int, herzen bigint, klicks bigint, events_hut bigint, lokale bigint, score numeric)
language sql stable as $$
with k as (select generate_series(1,12) as kreis),
b as (  -- Herze: kreis direkt, susch übers Lokal grettet
  select coalesce(bm.kreis, l.kreis) as kreis, count(*) as n
  from bookmarks bm
  left join locations l on bm.ziel_typ='location' and l.id::text = bm.ziel_id
  where bm.created_at >= now() - interval '7 days'
  group by 1),
i as (
  select coalesce(it.kreis, l.kreis) as kreis, count(*) as n
  from interactions it
  left join locations l on it.ziel_typ='location' and l.id::text = it.ziel_id
  where it.created_at >= now() - interval '7 days'
  group by 1),
e as (
  select ev.kreis, count(*) as n from eventfrog_events ev
  where ev.kreis between 1 and 12
    and ev.datum_start::date = (now() at time zone 'Europe/Zurich')::date
  group by 1),
l as (
  select loc.kreis, count(*) as n from locations loc
  where loc.aktiv = true and loc.kreis between 1 and 12
  group by 1)
select k.kreis,
  coalesce(b.n,0), coalesce(i.n,0), coalesce(e.n,0), coalesce(l.n,0),
  round( (3*coalesce(b.n,0) + coalesce(i.n,0) + 2*coalesce(e.n,0))
         / sqrt(greatest(coalesce(l.n,0),1))::numeric, 2)
from k
left join b on b.kreis = k.kreis
left join i on i.kreis = k.kreis
left join e on e.kreis = k.kreis
left join l on l.kreis = k.kreis
order by 6 desc;
$$;
-- Kontrolle:
select * from stadtpuls_kreis_puls();
