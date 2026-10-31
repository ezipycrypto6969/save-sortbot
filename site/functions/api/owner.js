// POST /api/owner { key } → { code }: free Pro for the site owner. Set the OWNER_KEY secret in Cloudflare.
import { json, makeCode } from "../_lib.js";

export async function onRequestPost({ request, env }) {
  let body; try { body = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  if (!env.OWNER_KEY || !env.TOKEN_SECRET) return json({ error: "Owner pass isn't set up yet (add OWNER_KEY and TOKEN_SECRET in Cloudflare)." }, 503);
  if (typeof body.key !== "string" || body.key !== env.OWNER_KEY) return json({ error: "Wrong owner key." }, 403);
  return json({ code: await makeCode(env, "owner") });
}
