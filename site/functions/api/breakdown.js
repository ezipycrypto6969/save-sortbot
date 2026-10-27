// POST /api/breakdown { code, caption, url } → { breakdown, code } for Pro members.
import { json, checkCode } from "../_lib.js";

const SYSTEM = `You write "breakdowns" of saved Instagram reels for SaveSort Pro. The user gives you a reel's caption.
Explain what the reel is actually about and how to act on it, honestly and practically, for a worldwide audience.
Rules:
- Only name real tools, websites and services you are confident exist. Give a URL only if you are sure it is the official homepage; otherwise leave url empty.
- Prices: give rough USD figures only if you are confident, and say "about"; otherwise write "Check current pricing".
- If the claim is hype, a scam pattern, a fake feature or a get-rich-quick promise, say so plainly in "catch" and set verdict to "be_careful".
- If the caption has no real information (only "comment X" or a teaser), say what the topic probably is, give the general technique, and set verdict to "needs_video".
- No legal, tax or financial advice; for anything regulated say "check the rules where you live".
- Never include the creator's name or handle. Never copy the caption.
Reply with JSON only, no prose, matching:
{"what": "1-2 sentences", "verdict": "worth_doing|needs_video|be_careful", "tools": [{"name": "", "url": "", "note": ""}], "steps": ["3-6 short steps"], "cost": "short", "catch": "short"}`;

export async function onRequestPost({ request, env }) {
  let body; try { body = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  const caption = String(body.caption || "").slice(0, 2200).trim();
  if (!caption) return json({ error: "This save has no caption in your file, so there's nothing to break down." }, 400);
  let who; try { who = await checkCode(env, body.code); } catch { return json({ error: "Couldn't check your Pro status. Try again." }, 502); }
  if (!who) return json({ error: "Your Pro code isn't valid or the subscription has ended." }, 403);
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model: env.MODEL || "claude-haiku-5-5", max_tokens: 900, system: SYSTEM,
      messages: [{ role: "user", content: `Caption of the saved reel:\n"""${caption}"""` }] }),
  });
  if (!r.ok) return json({ error: "The breakdown service is busy. Try again in a minute." }, 502);
  const out = await r.json();
  const text = (out.content || []).map(c => c.text || "").join("");
  let bd; try { bd = JSON.parse(text.slice(text.indexOf("{"), text.lastIndexOf("}") + 1)); } catch { return json({ error: "Couldn't read the breakdown. Try again." }, 502); }
  return json({ breakdown: bd, code: who.code });
}
