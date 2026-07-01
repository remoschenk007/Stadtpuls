-- ============================================================
-- STADTPULS — LIVE-STATISTIK (öffentliche Aggregat-Zähler)
-- Gibt nur ZAHLEN zurück (keine Einzeldaten) -> privacy-safe.
-- Im Supabase SQL-Editor einmal ausführen.
-- ============================================================
create or replace function public.stadtpuls_stats(p_typ text, p_id text)
returns json
language sql
security definer
set search_path = public
as $$
  select json_build_object(
    'merkt', (select count(*) from bookmarks
              where ziel_typ = p_typ and ziel_id = p_id),
    'views', (select count(*) from interactions
              where aktion = 'view_profile' and ziel_typ = p_typ and ziel_id = p_id
                and created_at > now() - interval '7 days')
  );
$$;

grant execute on function public.stadtpuls_stats(text, text) to anon, authenticated;
