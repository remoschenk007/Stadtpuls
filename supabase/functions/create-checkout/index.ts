// ============================================================
// STADTPULS — Edge Function: create-checkout
// Pfad:    supabase/functions/create-checkout/index.ts
// Deploy:  supabase functions deploy create-checkout --no-verify-jwt
// Secrets: supabase secrets set STRIPE_SECRET_KEY=sk_live_...   (oder sk_test_...)
//          supabase secrets set SITE_URL=https://depuls.ch
//
// Erstellt eine Stripe-Checkout-Session (TWINT + Karte) für eine Boost-Anfrage.
// platzierung.html ruft das auf, wenn PAYMODE='stripe'.
// ============================================================
import Stripe from "https://esm.sh/stripe@16?target=deno";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!, { apiVersion: "2024-06-20" });
const SITE = Deno.env.get("SITE_URL") || "https://depuls.ch";
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const { request_id, tier, tage, preis, name, email } = await req.json();
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      payment_method_types: ["card", "twint"],
      customer_email: email || undefined,
      line_items: [{
        quantity: 1,
        price_data: {
          currency: "chf",
          unit_amount: Math.round(Number(preis) * 100),
          product_data: { name: `Stadtpuls Platzierung – ${name}`, description: `${tier} · ${tage} Tage` },
        },
      }],
      metadata: { request_id: String(request_id || ""), tier: String(tier || ""), tage: String(tage || "") },
      success_url: `${SITE}/platzierung.html?bezahlt=1`,
      cancel_url: `${SITE}/platzierung.html?abbruch=1`,
    });
    return new Response(JSON.stringify({ url: session.url }), { headers: { ...cors, "Content-Type": "application/json" } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 400, headers: { ...cors, "Content-Type": "application/json" } });
  }
});
