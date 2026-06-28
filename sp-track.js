/* ============================================================
   sp-track.js — STADTPULS Signal-Tracking (Schritt 1, KI-Herz)
   ------------------------------------------------------------
   Einbinden NACH supabase-js, auf jeder User-Seite:
     <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
     <script src="sp-track.js"></script>

   Globale Funktionen:
     spTrack(aktion, ziel_typ, ziel_id, extra)   -> Interaktion loggen (fire&forget)
     spBookmarkToggle(ziel_typ, ziel_id, extra)  -> Bookmark an/aus  -> {ok,bookmarked}
     spIsBookmarked(ziel_typ, ziel_id)           -> bool
     spBookmarks()                               -> Liste der Bookmarks des Users

   extra = { kategorie, kreis, tags:[...], meta:{...} }  (alles optional)
   Voraussetzung DB: setup_ki.sql ausgeführt (bookmarks + interactions + RLS).
   ============================================================ */
(function () {
  const SU = 'https://pnynkzrqnfoshojqfqxn.supabase.co';
  const SK = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueW5renJxbmZvc2hvanFmcXhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MTg3NDEsImV4cCI6MjA5MTI5NDc0MX0.W3cOPU7lQKimHIYPc7ISuZGmOeV20GB3DEW-QdDJXZQ';

  // Bestehenden Client wiederverwenden (teilt die Auth-Session), sonst neuen bauen.
  let _sb = (typeof window !== 'undefined' && window.sb) ? window.sb : null;
  if (!_sb) {
    if (window.supabase && window.supabase.createClient) {
      _sb = window.supabase.createClient(SU, SK);
    } else {
      console.warn('[sp-track] supabase-js nicht gefunden — Tracking inaktiv.');
    }
  }

  let _uidCache, _uidPromise;
  async function uid() {
    if (_uidCache !== undefined) return _uidCache;
    if (_uidPromise) return _uidPromise;
    _uidPromise = (async () => {
      try {
        const { data: { user } } = await _sb.auth.getUser();
        if (!user) { _uidCache = null; return null; }
        const { data } = await _sb.from('users').select('id').eq('auth_id', user.id).single();
        _uidCache = data ? data.id : null;
        return _uidCache;
      } catch (e) { _uidCache = null; return null; }
    })();
    return _uidPromise;
  }

  window.spTrack = async function (aktion, ziel_typ, ziel_id, extra) {
    if (!_sb) return;
    extra = extra || {};
    try {
      const u = await uid();
      await _sb.from('interactions').insert({
        user_id: u, aktion: aktion,
        ziel_typ: ziel_typ || null, ziel_id: ziel_id || null,
        kategorie: extra.kategorie || null, kreis: extra.kreis || null,
        tags: extra.tags || null, meta: extra.meta || null
      });
    } catch (e) { /* still & leise */ }
  };

  window.spIsBookmarked = async function (ziel_typ, ziel_id) {
    if (!_sb) return false;
    const u = await uid(); if (!u) return false;
    try {
      const { data } = await _sb.from('bookmarks').select('id')
        .eq('user_id', u).eq('ziel_typ', ziel_typ).eq('ziel_id', ziel_id).maybeSingle();
      return !!data;
    } catch (e) { return false; }
  };

  window.spBookmarks = async function () {
    if (!_sb) return [];
    const u = await uid(); if (!u) return [];
    try {
      const { data } = await _sb.from('bookmarks').select('*')
        .eq('user_id', u).order('created_at', { ascending: false });
      return data || [];
    } catch (e) { return []; }
  };

  window.spBookmarkToggle = async function (ziel_typ, ziel_id, extra) {
    if (!_sb) return { ok: false, reason: 'no-sb' };
    extra = extra || {};
    const u = await uid();
    if (!u) return { ok: false, reason: 'login' }; // nicht eingeloggt -> UI: "zum Merken einloggen"
    try {
      const { data: exists } = await _sb.from('bookmarks').select('id')
        .eq('user_id', u).eq('ziel_typ', ziel_typ).eq('ziel_id', ziel_id).maybeSingle();
      if (exists) {
        await _sb.from('bookmarks').delete().eq('id', exists.id);
        window.spTrack('bookmark_remove', ziel_typ, ziel_id, extra);
        return { ok: true, bookmarked: false };
      } else {
        await _sb.from('bookmarks').insert({
          user_id: u, ziel_typ: ziel_typ, ziel_id: ziel_id,
          kategorie: extra.kategorie || null, kreis: extra.kreis || null, tags: extra.tags || null
        });
        window.spTrack('bookmark_add', ziel_typ, ziel_id, extra);
        return { ok: true, bookmarked: true };
      }
    } catch (e) { return { ok: false, reason: String(e) }; }
  };
})();
