// SaveSort on Cloudflare Workers: the website (static files in site/public) plus the Pro API under /api.
import { onRequestGet as activate } from "./functions/api/activate.js";
import { onRequestPost as breakdown } from "./functions/api/breakdown.js";
import { onRequestPost as owner } from "./functions/api/owner.js";
import { json } from "./functions/_lib.js";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "www.savesortai.com") { url.hostname = "savesortai.com"; return Response.redirect(url.toString(), 301); }
    if (url.pathname === "/api/activate" && request.method === "GET") return activate({ request, env });
    if (url.pathname === "/api/breakdown" && request.method === "POST") return breakdown({ request, env });
    if (url.pathname === "/api/owner" && request.method === "POST") return owner({ request, env });
    if (url.pathname.startsWith("/api/")) return json({ error: "Not found" }, 404);
    return env.ASSETS.fetch(request);
  },
};
