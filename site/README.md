# SaveSort website

- `public/`: the static site (index, terms, refunds).
- `worker.js`: Cloudflare Worker that serves `public/` and the Pro API (`/api/activate`, `/api/breakdown`, code in `functions/`).
- Deploys automatically to Cloudflare Workers on every push to `main` (config: `wrangler.jsonc` in the repo root).

Secrets (Cloudflare → Workers & Pages → save-sortbot → Settings → Variables and Secrets, type Secret):
`STRIPE_SECRET_KEY` (restricted, read-only: Checkout Sessions, Subscriptions), `ANTHROPIC_API_KEY`, `TOKEN_SECRET`. Optional `MODEL`.

Stripe: two Payment Links (A$59/year and A$7.99/month), each with a 7-day free trial, "After payment" → redirect to
`https://savesortai.com/?session_id={CHECKOUT_SESSION_ID}`. Paste both links and the customer-portal login link into `CONFIG` in `public/index.html`.

## SEO (keep this when editing the site)

- Every page keeps: `<title>`, `<meta name="description">`, `<link rel="canonical">`, and the `og:` / `twitter:` link-preview tags.
- `public/og.png` (1200×630) is the picture shown when someone shares savesortai.com. Only true numbers on it (156 saves, 30 worth doing).
- `index.html` has JSON-LD structured data (app + FAQ). If you change an FAQ answer that's in the JSON-LD, change it there too. Don't add Pro features or prices to it.
- New public page? Add it to `public/sitemap.xml` using the short address (`/terms`, not `/terms.html`: Cloudflare redirects the `.html` one). `public/robots.txt` lets every crawler in (AI search included) except `/api/`.
- `public/404.html` is the not-found page (`not_found_handling` in `wrangler.jsonc`).
- `jszip.min.js` loads only when someone drops in a zip. Don't put it back as a normal `<script>` tag.
