// GET /api/activate?session_id=cs_... → { code } after a Stripe Checkout (A$1.99/week Pro) completes.
import { json, stripe, makeCode, LIVE, allowed } from "../_lib.js";

export async function onRequestGet({ request, env }) {
  if (!await allowed(env.OWNER_LIMIT, "activate:" + (request.headers.get("cf-connecting-ip") || "unknown"))) return json({ error: "Too many tries. Wait a minute." }, 429);
  const id = new URL(request.url).searchParams.get("session_id") || "";
  if (!/^cs_(test|live)_[A-Za-z0-9]+$/.test(id)) return json({ error: "Bad session id" }, 400);
  try {
    const s = await stripe(env, `checkout/sessions/${id}`);
    if (s.status !== "complete" || !s.subscription) return json({ error: "Checkout isn't complete yet." }, 402);
    const sub = await stripe(env, `subscriptions/${s.subscription}`);
    if (!LIVE.has(sub.status)) return json({ error: "Subscription isn't active." }, 402);
    return json({ code: await makeCode(env, sub.id), status: sub.status });
  } catch (e) {
    return json({ error: "Couldn't check with Stripe. Try again in a minute." }, 502);
  }
}
