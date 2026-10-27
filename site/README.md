# SaveSort website

- `public/`: the static site (index, terms, refunds).
- `worker.js`: Cloudflare Worker that serves `public/` and the Pro API (`/api/activate`, `/api/breakdown`, code in `functions/`).
- Deploys automatically to Cloudflare Workers on every push to `main` (config: `wrangler.jsonc` in the repo root).

Secrets (Cloudflare → Workers & Pages → save-sortbot → Settings → Variables and Secrets, type Secret):
`STRIPE_SECRET_KEY` (restricted, read-only: Checkout Sessions, Subscriptions), `ANTHROPIC_API_KEY`, `TOKEN_SECRET`. Optional `MODEL`.

Stripe: two Payment Links (A$59/year and A$7.99/month), each with a 7-day free trial, "After payment" → redirect to
`https://savesortai.com/?session_id={CHECKOUT_SESSION_ID}`. Paste both links and the customer-portal login link into `CONFIG` in `public/index.html`.
