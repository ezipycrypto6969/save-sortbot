// Shared helpers for SaveSort Pro (Cloudflare Pages Functions).
// Secrets (Cloudflare → Pages project → Settings → Variables and secrets):
//   STRIPE_SECRET_KEY  restricted key: read Checkout Sessions, Subscriptions, Customers
//   ANTHROPIC_API_KEY  Claude API key
//   TOKEN_SECRET       any long random string (signs Pro codes)
//   MODEL              optional, defaults to claude-haiku-5-5
//   OWNER_KEY          the owner's password for free Pro (savesortai.com/?owner=...)
const enc = new TextEncoder();
const b64u = buf => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const fromB64u = s => atob(s.replace(/-/g, "+").replace(/_/g, "/"));

async function hmac(secret, data) {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return b64u(await crypto.subtle.sign("HMAC", key, enc.encode(data)));
}

// Compare two strings without leaking how much of them matched (stops timing attacks on keys and signatures).
export function same(a, b) {
  if (typeof a !== "string" || typeof b !== "string") return false;
  const x = enc.encode(a), y = enc.encode(b);
  let d = x.length ^ y.length;
  for (let i = 0; i < Math.max(x.length, y.length); i++) d |= (x[i] || 0) ^ (y[i] || 0);
  return d === 0;
}

// Owner codes are tied to the current OWNER_KEY: change OWNER_KEY in Cloudflare and every old owner code stops working.
const ownerTag = env => hmac(env.TOKEN_SECRET, "owner:" + (env.OWNER_KEY || ""));

// Rate limit helper: uses a Cloudflare rate-limit binding if it exists, otherwise lets the request through.
export async function allowed(limiter, key) {
  if (!limiter) return true;
  try { return (await limiter.limit({ key })).success; } catch { return true; }
}

export const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export async function stripe(env, path) {
  const r = await fetch("https://api.stripe.com/v1/" + path, { headers: { Authorization: `Bearer ${env.STRIPE_SECRET_KEY}` } });
  if (!r.ok) throw new Error(`Stripe ${r.status}`);
  return r.json();
}

// A Pro code = payload.signature. Payload holds the Stripe subscription id and when to re-check it.
export async function makeCode(env, sub) {
  const body = sub === "owner" ? { sub, own: await ownerTag(env) } : { sub, chk: Date.now() + 24 * 3600e3 };
  const payload = b64u(enc.encode(JSON.stringify(body)));
  return payload + "." + await hmac(env.TOKEN_SECRET, payload);
}

export const LIVE = new Set(["trialing", "active"]);

// Returns { sub, code } if the code is genuine and the subscription is still trialing/active, else null.
export async function checkCode(env, code) {
  if (typeof code !== "string" || !code.includes(".")) return null;
  const [payload, sig] = code.split(".");
  if (!same(sig, await hmac(env.TOKEN_SECRET, payload))) return null;
  let p; try { p = JSON.parse(fromB64u(payload)); } catch { return null; }
  if (p.sub === "owner") return env.OWNER_KEY && same(p.own, await ownerTag(env)) ? { sub: "owner", code } : null;  // owner pass: no Stripe check, dies when OWNER_KEY changes
  if (Date.now() < p.chk) return { sub: p.sub, code };
  const s = await stripe(env, `subscriptions/${encodeURIComponent(p.sub)}`);  // re-check once a day
  if (!LIVE.has(s.status)) return null;
  return { sub: p.sub, code: await makeCode(env, p.sub) };
}
