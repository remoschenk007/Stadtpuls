// ============================================================
// STADTPULS — Edge Function: moderate
// Pfad im Repo:  supabase/functions/moderate/index.ts
// Deploy:        supabase functions deploy moderate
// Secrets:       supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
//                (SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY sind automatisch da)
//
// Was sie macht:
//  - holt neue, noch ungeprüfte Beiträge (comments / news_stories / inserate)
//  - lässt Claude jeden Beitrag bewerten (JSON-Urteil)
//  - SICHER & harmlos  -> automatisch freigeschaltet
//  - UNSICHER          -> bleibt liegen (du prüfst im Cockpit)
//  - SEXUELL/MOBBING/HASS -> abgelehnt + User gesperrt + informiert
//  - SPAM/Werbung      -> abgelehnt + User gewarnt
// Aufgerufen per Cron (siehe setup.sql) oder manuell per HTTP-POST.
// ============================================================

const ANTHROPIC_API_KEY = Deno.env.get("ANTHROPIC_API_KEY")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const MODEL = "claude-haiku-4-5-20251001"; // schnell & günstig; bei Bedarf auf claude-sonnet-4-6 wechseln
const BATCH = 25; // max Beiträge pro Lauf und Quelle

const sb = (path: string, init: RequestInit = {}) =>
  fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
    ...init,
    headers: {
      "apikey": SERVICE_KEY,
      "Authorization": `Bearer ${SERVICE_KEY}`,
      "Content-Type": "application/json",
      ...(init.headers || {}),
    },
  });

type Quelle = {
  table: string;
  query: string;            // PostgREST filter für ungeprüfte Beiträge
  textOf: (r: any) => string;
  approvedStatus: string;
  rejectedStatus: string;
};

const QUELLEN: Quelle[] = [
  {
    table: "comments",
    query: "comments?status=eq.neu&ki_urteil=is.null&order=created_at.asc&limit=" + BATCH,
    textOf: (r) => r.text || "",
    approvedStatus: "freigeschaltet",
    rejectedStatus: "abgelehnt",
  },
  {
    table: "news_stories",
    query: "news_stories?status=eq.pending&ki_urteil=is.null&order=created_at.asc&limit=" + BATCH,
    textOf: (r) => `${r.titel || ""}\n${r.inhalt || ""}`,
    approvedStatus: "approved",
    rejectedStatus: "rejected",
  },
  {
    table: "inserate",
    query: "inserate?status=eq.pending&ki_urteil=is.null&order=created_at.asc&limit=" + BATCH,
    textOf: (r) => `${r.titel || ""}\n${r.beschreibung || ""}`,
    approvedStatus: "approved",
    rejectedStatus: "rejected",
  },
];

const SYSTEM = `Du bist der Moderations-Filter für Stadtpuls, einen Stadtführer für Zürich.
Bewerte einen nutzergenerierten Beitrag (Kommentar, News oder Marktplatz-Inserat).
Antworte AUSSCHLIESSLICH mit einem JSON-Objekt, ohne Markdown, ohne Erklärung davor/danach:
{"urteil":"approve|pruefen|ablehnen|schwerwiegend","konfidenz":0.0-1.0,"grund":"kurz, deutsch","kategorien":{"spam":0-1,"belaestigung":0-1,"mobbing":0-1,"sexuell":0-1,"hass":0-1}}

Regeln:
- "approve": harmlos, on-topic, respektvoll. Nutze hohe Konfidenz nur wenn eindeutig sauber.
- "pruefen": Grenzfall, unklar, evtl. beleidigend aber nicht eindeutig, oder zu wenig Kontext.
- "ablehnen": klar Spam/Werbung/irrelevant, aber nicht gefährlich.
- "schwerwiegend": sexuelle Übergriffe/Belästigung, Mobbing, Hassrede, Drohungen, Doxxing.
Sei vorsichtig: im Zweifel "pruefen", nicht "approve".`;

async function classify(text: string) {
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 300,
      system: SYSTEM,
      messages: [{ role: "user", content: text.slice(0, 4000) || "(leer)" }],
    }),
  });
  const data = await r.json();
  const raw = (data?.content?.[0]?.text || "").trim();
  try {
    const j = JSON.parse(raw.replace(/```json|```/g, "").trim());
    return {
      urteil: j.urteil || "pruefen",
      konfidenz: typeof j.konfidenz === "number" ? j.konfidenz : 0.5,
      grund: j.grund || "",
      kategorien: j.kategorien || {},
    };
  } catch {
    // Im Fehlerfall NIE blind freischalten -> zur manuellen Prüfung
    return { urteil: "pruefen", konfidenz: 0, grund: "KI-Antwort nicht lesbar", kategorien: {} };
  }
}

async function handleRow(q: Quelle, row: any) {
  const verdict = await classify(q.textOf(row));
  const patch: any = {
    ki_urteil: verdict.urteil,
    ki_konfidenz: verdict.konfidenz,
    ki_grund: verdict.grund,
  };
  if (q.table === "comments") patch.ki_kategorien = verdict.kategorien;

  let newStatus: string | null = null;
  if (verdict.urteil === "approve" && verdict.konfidenz >= 0.8) {
    newStatus = q.approvedStatus;
  } else if (verdict.urteil === "ablehnen") {
    newStatus = q.rejectedStatus;
    // Spam -> User warnen (nicht sperren)
    await warnOrBlock(q, row, "spam", "gewarnt", verdict.grund);
  } else if (verdict.urteil === "schwerwiegend") {
    newStatus = q.rejectedStatus;
    const grund =
      (verdict.kategorien?.sexuell ?? 0) >= 0.5 ? "sexuell" :
      (verdict.kategorien?.mobbing ?? 0) >= 0.5 ? "mobbing" :
      (verdict.kategorien?.hass ?? 0) >= 0.5 ? "hass" : "belaestigung";
    await warnOrBlock(q, row, grund, "gesperrt", verdict.grund);
  }
  // "pruefen" -> Status bleibt, nur ki_* gesetzt -> erscheint im Cockpit als ⚠

  if (newStatus) patch.status = newStatus;

  await sb(`${q.table}?id=eq.${row.id}`, {
    method: "PATCH",
    headers: { "Prefer": "return=minimal" },
    body: JSON.stringify(patch),
  });
}

async function warnOrBlock(q: Quelle, row: any, grund: string, aktion: string, detail: string) {
  await sb("user_sperren", {
    method: "POST",
    headers: { "Prefer": "return=minimal" },
    body: JSON.stringify({
      user_id: row.user_id ?? null,
      autor_name: row.autor_name ?? null,
      grund,
      aktion,
      quelle_typ: q.table === "news_stories" ? "news" : q.table === "inserate" ? "inserat" : "comment",
      quelle_id: row.id,
      erstellt_von: "ki",
    }),
  });
  if (row.user_id) {
    const titel = aktion === "gesperrt" ? "Konto gesperrt" : "Verwarnung";
    const text = aktion === "gesperrt"
      ? "Dein Beitrag verstösst gegen die Stadtpuls-Regeln (" + grund + "). Dein Konto wurde gesperrt."
      : "Dein Beitrag wurde als " + grund + " eingestuft und entfernt. Bitte halte dich an die Regeln.";
    await sb("notifications", {
      method: "POST",
      headers: { "Prefer": "return=minimal" },
      body: JSON.stringify({ user_id: row.user_id, typ: "moderation", titel, text }),
    });
  }
}

Deno.serve(async () => {
  const summary: Record<string, number> = {};
  try {
    for (const q of QUELLEN) {
      let rows: any[] = [];
      try {
        const res = await sb(q.query);
        if (!res.ok) { summary[q.table] = -1; continue; } // Tabelle fehlt o.ä.
        rows = await res.json();
      } catch { summary[q.table] = -1; continue; }
      for (const row of rows) {
        try { await handleRow(q, row); } catch (_e) { /* einzelne Zeile überspringen */ }
      }
      summary[q.table] = rows.length;
    }
    return new Response(JSON.stringify({ ok: true, verarbeitet: summary }), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: String(e) }), {
      status: 500, headers: { "Content-Type": "application/json" },
    });
  }
});
