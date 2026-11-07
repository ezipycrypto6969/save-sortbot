// POST /api/owner { key } → { code }: free Pro for the site owner. Set the OWNER_KEY secret in Cloudflare (long and random).
// Use it as savesortai.com/#owner=KEY (the # part never reaches the server or its logs). Changing OWNER_KEY revokes old owner codes.
import { json, makeCode, same, allowed } from "../_lib.js";

export async function onRequestPost({ request, env }) {
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  if (!await allowed(env.OWNER_LIMIT, "owner:" + ip)) return json({ error: "Too many tries. Wait a minute." }, 429);  // stops key guessing
  let body; try { body = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  if (!env.OWNER_KEY || !env.TOKEN_SECRET) return json({ error: "Owner pass isn't set up yet (add OWNER_KEY and TOKEN_SECRET in Cloudflare)." }, 503);
  if (!same(body.key, env.OWNER_KEY)) return json({ error: "Wrong owner key." }, 403);
  return json({ code: await makeCode(env, "owner") });
}
