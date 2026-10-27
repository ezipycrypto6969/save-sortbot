# SaveSort website

Static site (`index.html`, `terms.html`, `refunds.html`) plus Pro API in `functions/` (Cloudflare Pages Functions).

Deploy: Cloudflare → Workers & Pages → Create → Pages → Connect to Git → this repo.
Root directory (advanced): `site`. Build command: none. Build output directory: `.` (so `functions/` is picked up as the API).

Secrets (Pages project → Settings → Variables and secrets, type Secret): `STRIPE_SECRET_KEY`, `ANTHROPIC_API_KEY`, `TOKEN_SECRET`. Optional `MODEL`.

Stripe: two Payment Links (A$59/year and A$7.99/month), each with a 7-day free trial, "After payment" → redirect to
`https://YOURDOMAIN/?session_id={CHECKOUT_SESSION_ID}`. Paste both links and the customer-portal login link into `CONFIG` in `index.html`.
