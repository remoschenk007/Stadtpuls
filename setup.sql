-- ============================================================
-- STADTPULS KOMMANDOZENTRALE — Setup
-- Im Supabase SQL-Editor ausführen (einmal).
-- Reihenfolge egal, Skript ist idempotent (IF NOT EXISTS).
-- ============================================================

-- 1) KOMMENTARE -------------------------------------------------
create table if not exists comments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  autor_name text,
  ziel_typ text,                 -- 'location' | 'event'
  ziel_id text,
  text text not null,
  status text default 'neu',     -- neu | freigeschaltet | abgelehnt
  ki_urteil text,                -- approve | pruefen | ablehnen | schwerwiegend
  ki_konfidenz numeric,          -- 0.00 .. 1.00
  ki_grund text,
  ki_kategorien jsonb,           -- {"spam":0.1,"belaestigung":0.0,"mobbing":0.0,"sexuell":0.0}
  created_at timestamptz default now()
);

-- 2) ANFRAGEN (Platzierung / Pop-up / Event / Partnerschaft) -----
create table if not exists partner_anfragen (
  id uuid primary key default gen_random_uuid(),
  typ text not null default 'sonstiges',  -- platzierung | popup | event | partnerschaft | sonstiges
  name text,
  email text,
  lokal_name text,
  kreis int,
  location_id uuid,              -- optional: Verknüpfung zu locations.id
  nachricht text,
  budget text,
  status text default 'neu',     -- neu | in_pruefung | angenommen | abgelehnt
  prio text default 'normal',    -- normal | hoch
  created_at timestamptz default now()
);

-- 3) USER-SPERREN / Moderations-Aktionen ------------------------
create table if not exists user_sperren (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  autor_name text,
  grund text,                    -- belaestigung | mobbing | sexuell | spam | manuell
  aktion text default 'gesperrt',-- gewarnt | gesperrt
  quelle_typ text,               -- comment | news | inserat
  quelle_id text,
  erstellt_von text default 'ki',-- ki | operator
  created_at timestamptz default now()
);

-- 4) BENACHRICHTIGUNGEN an User ---------------------------------
create table if not exists notifications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  typ text,
  titel text,
  text text,
  gelesen boolean default false,
  created_at timestamptz default now()
);

-- 5) KI-Felder an bestehende Moderations-Quellen anhängen --------
alter table if exists news_stories add column if not exists ki_urteil text;
alter table if exists news_stories add column if not exists ki_konfidenz numeric;
alter table if exists news_stories add column if not exists ki_grund text;
alter table if exists inserate    add column if not exists ki_urteil text;
alter table if exists inserate    add column if not exists ki_konfidenz numeric;
alter table if exists inserate    add column if not exists ki_grund text;

-- 6) RLS + Policies ---------------------------------------------
-- Hinweis: 'anon' darf hier lesen/schreiben (passt zum bestehenden
-- Stadtpuls-Muster + Passwort-Gate im Cockpit). Für echte Sicherheit
-- später: Schreib-Aktionen NUR über die Edge Function (service_role)
-- laufen lassen und die anon-update/insert-Policies entfernen.

alter table comments         enable row level security;
alter table partner_anfragen enable row level security;
alter table user_sperren     enable row level security;
alter table notifications    enable row level security;

-- comments: jeder darf einreichen + lesen, Cockpit darf updaten
drop policy if exists comments_all on comments;
create policy comments_all on comments for all to anon using (true) with check (true);

-- partner_anfragen: Formular darf einreichen, Cockpit lesen/updaten
drop policy if exists anfragen_all on partner_anfragen;
create policy anfragen_all on partner_anfragen for all to anon using (true) with check (true);

-- user_sperren: Cockpit/Function schreiben + lesen
drop policy if exists sperren_all on user_sperren;
create policy sperren_all on user_sperren for all to anon using (true) with check (true);

-- notifications: schreiben + lesen
drop policy if exists notif_all on notifications;
create policy notif_all on notifications for all to anon using (true) with check (true);

-- 7) Beispiel-Anfragen, damit das Cockpit gleich was zeigt -------
insert into partner_anfragen (typ,name,email,lokal_name,kreis,nachricht,budget,status,prio) values
 ('platzierung','Marco Rossi','marco@trattoria-rossi.ch','Trattoria Rossi',4,'Wir möchten in Kreis 4 weiter oben erscheinen. Haben gerade neu renoviert.','CHF 200/Mt','neu','hoch'),
 ('popup','Lea Brunner','lea@nightmarket.ch','Langstrasse Night Market',4,'Pop-up Streetfood-Markt jeden Freitag im Juli. Würden gern gelistet werden.','CHF 150','neu','normal'),
 ('event','DJ Kessler','booking@kesslersound.ch','Hive Club',5,'Open Air am 12. Juli, 600 Gäste erwartet. Bitte als Featured-Event.','CHF 400','neu','hoch'),
 ('partnerschaft','Sandra Vogt','s.vogt@zuerichcard.ch','Zürich Card',NULL,'Idee für eine offizielle Partnerschaft / Rabatt-Integration. Lass uns reden.',NULL,'in_pruefung','normal');

-- 8) (OPTIONAL) Cron für die KI-Moderation -----------------------
-- Voraussetzung: Extensions pg_cron + pg_net aktiv (Supabase: Database > Extensions).
-- Ruft die Edge Function 'moderate' alle 5 Minuten auf.
-- <DEINE_REF> = pnynkzrqnfoshojqfqxn ; <SERVICE_ROLE_KEY> aus Settings > API.
--
-- create extension if not exists pg_cron;
-- create extension if not exists pg_net;
--
-- select cron.schedule('stadtpuls-moderate','*/5 * * * *', $$
--   select net.http_post(
--     url:='https://pnynkzrqnfoshojqfqxn.supabase.co/functions/v1/moderate',
--     headers:='{"Content-Type":"application/json","Authorization":"Bearer <SERVICE_ROLE_KEY>"}'::jsonb,
--     body:='{}'::jsonb
--   );
-- $$);
--
-- Stoppen:  select cron.unschedule('stadtpuls-moderate');


-- ============================================================
-- ERWEITERUNG v2 — BOOSTS / GELD / AUDIT
-- ============================================================

-- 9) BOOSTS (bezahlte Platzierungen mit Ablaufdatum) -------------
create table if not exists boosts (
  id uuid primary key default gen_random_uuid(),
  ziel_typ text default 'location',   -- location | event | inserat
  ziel_id text,                        -- locations.id (oder event/inserat id)
  ziel_name text,                      -- denormalisiert für Anzeige
  tier text default 'featured',        -- featured | boost | premium
  tier_label text,
  dauer_tage int default 7,
  start timestamptz default now(),
  ende timestamptz,
  preis_chf numeric default 0,
  bezahlt boolean default false,
  status text default 'aktiv',         -- geplant | aktiv | abgelaufen | gestoppt
  notiz text,
  created_at timestamptz default now()
);

-- 10) AUDIT-LOG (jede Aktion protokolliert) ----------------------
create table if not exists audit_log (
  id uuid primary key default gen_random_uuid(),
  aktion text,
  objekt_typ text,
  objekt_id text,
  detail text,
  akteur text default 'operator',      -- operator | ki
  created_at timestamptz default now()
);

-- 11) locations: Boost-Felder fürs Frontend ----------------------
alter table if exists locations add column if not exists boost_until timestamptz;
alter table if exists locations add column if not exists boost_tier text;
-- (locations.featured existiert bereits)

-- 12) RLS ---------------------------------------------------------
alter table boosts    enable row level security;
alter table audit_log enable row level security;
drop policy if exists boosts_all on boosts;
create policy boosts_all on boosts for all to anon using (true) with check (true);
drop policy if exists audit_all on audit_log;
create policy audit_all on audit_log for all to anon using (true) with check (true);

-- 13) Beispiel-Boosts, damit Finanzen/Boosts gleich was zeigen ----
insert into boosts (ziel_typ,ziel_name,tier,tier_label,dauer_tage,start,ende,preis_chf,bezahlt,status) values
 ('location','Trattoria Rossi','boost','Boost',14, now()-interval '2 days', now()+interval '12 days', 100, true,  'aktiv'),
 ('location','Hive Club','premium','Premium',7,    now()-interval '5 days', now()+interval '2 days',  100, true,  'aktiv'),
 ('location','Café Vlora','featured','Featured',7,  now()-interval '1 day',  now()+interval '6 days',  20,  false, 'aktiv');

-- 14) AUTO-ABLAUF serverseitig (läuft auch wenn das Cockpit zu ist)
-- Setzt abgelaufene Boosts auf 'abgelaufen' und nimmt das Featured weg.
create or replace function stadtpuls_expire_boosts() returns void as $$
begin
  update locations l set featured=false, boost_until=null, boost_tier=null
   from boosts b
   where b.ziel_typ='location' and b.ziel_id=l.id::text
     and b.status='aktiv' and b.ende < now();
  update boosts set status='abgelaufen' where status='aktiv' and ende < now();
  update boosts set status='aktiv'      where status='geplant' and start<=now() and ende>now();
end;
$$ language plpgsql;

-- Cron: stündlich ablaufen lassen (braucht pg_cron, siehe Abschnitt 8)
-- select cron.schedule('stadtpuls-expire-boosts','0 * * * *', $$ select stadtpuls_expire_boosts(); $$);


-- ============================================================
-- ERWEITERUNG v3 — CLAIM / BESSERE PLATZIERUNG (Anfragen vom Inserat)
-- ============================================================

-- 15) BOOST-ANFRAGEN von Inhabern (übers Lokal-Profil) -----------
create table if not exists boost_requests (
  id uuid primary key default gen_random_uuid(),
  listing_id text,             -- locations.id (oder event/inserat)
  listing_typ text default 'location',
  listing_name text,
  kreis int,
  rolle text,                  -- inhaber | gf | mitarbeiter | auftrag
  name text,
  email text,
  telefon text,
  tier text,                   -- featured | boost | premium
  tage int,
  preis_chf numeric,
  nachricht text,
  status text default 'neu',   -- neu | bezahlt | freigeschaltet | abgelehnt
  bezahlt boolean default false,
  zahlart text,                -- manual | stripe
  stripe_session text,
  created_at timestamptz default now()
);

alter table boost_requests enable row level security;
drop policy if exists boostreq_all on boost_requests;
create policy boostreq_all on boost_requests for all to anon using (true) with check (true);

-- Beispiel-Anfrage, damit der Verkauf-Tab gleich was zeigt
insert into boost_requests (listing_name,listing_typ,rolle,name,email,telefon,tier,tage,preis_chf,nachricht,status,bezahlt,zahlart) values
 ('Café Vlora','location','inhaber','Arben Krasniqi','arben@cafevlora.ch','079 555 12 34','boost',14,100,'Mir wänd übers Wuchenänd guet sichtbar sii.','bezahlt',true,'manual');
