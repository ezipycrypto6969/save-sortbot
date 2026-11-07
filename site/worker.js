// SaveSort on Cloudflare Workers: the website (static files in site/public) plus the Pro API under /api.
import { onRequestGet as activate } from "./functions/api/activate.js";
import { onRequestPost as breakdown } from "./functions/api/breakdown.js";
import { onRequestPost as owner } from "./functions/api/owner.js";
import { json } from "./functions/_lib.js";

// Security headers on every response: no framing (clickjacking), scripts only from this site, HTTPS only.
const CSP = [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline'",
  "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  "font-src 'self' https://fonts.gstatic.com",
  "img-src 'self' data: blob:",
  "connect-src 'self'",
  "frame-ancestors 'none'",
  "base-uri 'none'",
  "form-action 'self'",
  "object-src 'none'",
].join("; ");
const SECURITY = {
  "Content-Security-Policy": CSP,
  "Strict-Transport-Security": "max-age=31536000",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
  "Cross-Origin-Opener-Policy": "same-origin",
};
function secure(res) {
  const r = new Response(res.body, res);
  for (const [k, v] of Object.entries(SECURITY)) r.headers.set(k, v);
  return r;
}

export default {
  async fetch(request, env) {
    return secure(await route(request, env));
  },
};

async function route(request, env) {
  {
    const url = new URL(request.url);
    if (url.hostname === "www.savesortai.com") { url.hostname = "savesortai.com"; return Response.redirect(url.toString(), 301); }
    if (url.pathname === "/api/activate" && request.method === "GET") return activate({ request, env });
    if (url.pathname === "/api/breakdown" && request.method === "POST") return breakdown({ request, env });
    if (url.pathname === "/api/owner" && request.method === "POST") return owner({ request, env });
    if (url.pathname.startsWith("/api/")) return json({ error: "Not found" }, 404);
    const res = await env.ASSETS.fetch(request);
    const type = res.headers.get("content-type") || "";
    if (/^text\/(html|css)/.test(type) && !/charset/i.test(type)) {  // always serve pages as UTF-8
      const r = new Response(res.body, res); r.headers.set("content-type", type + "; charset=utf-8"); return r;
    }
    return res;
  }
}
