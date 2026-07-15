-- ============================================================
-- STADTPULS · TUUSCHE v2 — Zentrale-Feed (maskiert) + Event-Index
-- Idempotent.
-- ============================================================
-- 1) Performance: Index für die Event-Listen-Query
create index if not exists idx_ev_aktiv_datum on eventfrog_events(aktiv, datum_start);

-- 2) Zentrale-Feed: anonymisiert (Mail maskiert, Miete gerundet).
--    Volli Date gsehsch nur du im Table Editor.
create or replace function stadtpuls_tuusche_feed()
returns table(biete_kreis int, biete_zimmer numeric, miete_ca int,
              suche_kreis int, suche_zimmer numeric, mail_maskiert text, erfasst timestamptz)
language sql stable security definer
set search_path = public as $$
  select biete_kreis, biete_zimmer,
         (round(coalesce(biete_miete,0)/50.0)*50)::int as miete_ca,
         suche_kreis, suche_zimmer,
         case when email like '%@%'
              then left(email,1) || '***@' || split_part(email,'@',2)
              else '***' end as mail_maskiert,
         created_at as erfasst
  from wohnig_tuusche
  order by created_at desc
  limit 200;
$$;
grant execute on function stadtpuls_tuusche_feed() to anon;

-- Kontrolle:
select count(*) as warteliste from wohnig_tuusche;
