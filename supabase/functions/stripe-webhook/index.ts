// ============================================================
// STADTPULS — Edge Function: stripe-webhook
// Pfad:    supabase/functions/stripe-webhook/index.ts
// Deploy:  supabase functions deploy stripe-webhook --no-verify-jwt
// Secrets: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET (aus Stripe Dashboard > Webhooks)
//          SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY (automatisch da)
//
// Markiert eine Boost-Anfrage als bezahlt, sobald Stripe die Zahlung bestätigt.
// (Freischalten machst DU danach in der Kommandozentrale.)
// Im Stripe-Dashboard einen Webhook auf dieses Endpoint legen, Event:
//   checkout.session.completed
// ============================================================
import Stripe from "https://esm.sh/stripe@16?target=deno";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!, { apiVersion: "2024-06-20" });
const WH = Deno.env.get("STRIPE_WEBHOOK_SECRET")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

Deno.serve(async (req) => {
  const sig = req.headers.get("stripe-signature");
  const body = await req.text();
  let event: any;
  try {
    event = await stripe.webhooks.constructEventAsync(body, sig!, WH);
  } catch (e) {
    return new Response("bad signature: " + String(e), { status: 400 });
  }
  if (event.type === "checkout.session.completed") {
    const s = event.data.object;
    const rid = s?.metadata?.request_id;
    if (rid) {
      await fetch(`${SUPABASE_URL}/rest/v1/boost_requests?id=eq.${rid}`, {
        method: "PATCH",
        headers: { apikey: SERVICE, Authorization: `Bearer ${SERVICE}`, "Content-Type": "application/json", "Prefer": "return=minimal" },
        body: JSON.stringify({ bezahlt: true, status: "bezahlt", stripe_session: s.id }),
      });
    }
  }
  return new Response("ok", { status: 200 });
});
