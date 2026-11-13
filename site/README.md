# SaveSort website

## How it fits together

- `src/`: what you edit. `src/pages/` holds the home page, about, privacy, terms, refunds and the not-found page. `src/blog/` holds one file per blog post.
- `build.mjs`: wraps every file in `src/` in the shared header and footer and writes the finished pages to `public/`. It also writes the blog index, `sitemap.xml` and `feed.xml`. Run it from the repo root: `node site/build.mjs` (no install needed).
- `public/`: what Cloudflare serves. The pages in here are **built files: don't edit them by hand**, edit `src/` and run the build. Files you do edit directly in `public/`: `site.css` (all styles), `app.js` (the sorter, sample report and Pro), `robots.txt`, `llms.txt` (plain fact sheet for AI tools: keep it true, see SEO.md), `_headers`, `og.png`, `fonts/`.
- `worker.js`: Cloudflare Worker that serves `public/` and the Pro API (`/api/activate`, `/api/breakdown`, code in `functions/`).
- Deploys automatically to Cloudflare Workers on every push to `main` (config: `wrangler.jsonc` in the repo root). The build does **not** run on deploy, so always commit `src/` and the rebuilt `public/` together.

## Adding a blog post

The weekly SEO worker does this by following `SEO.md` in the repo root; these are the mechanics.

1. Copy an existing file in `src/blog/` and rename it. The file name is the address: `src/blog/my-topic.html` becomes `savesortai.com/blog/my-topic`. Never rename a published post (the old link would break).
2. Fill in the details comment on the first line: `title` (for Google, under 60 characters), `h1` (the headline on the page), `short` (2 to 4 words for the footer), `description` (one sentence, under 160 characters), `date` (YYYY-MM-DD), `readMins`. When you change a post later, add `"updated": "YYYY-MM-DD"`.
3. Write the post in plain HTML: `<p>`, `<h2>`, `<ul>`, `<ol>`, `<strong>`, `<a>`. Use `<p class="note">` for a boxed note. The headline, date and the "Sort my saves" box at the end are added for you.
4. Run `node site/build.mjs` and commit everything.

Blog rules (same as the reels): every claim true and checkable, only the real numbers (156 saves, 30 Do it, 65 Watch it, 10 Skip it, 22 Locked, called "our sample report"), no real people's names or handles, only features that exist today, no financial, legal or tax advice. Link each post to `/#try` and to at least one other post. One post answers one question people actually search for.

## Pro and Stripe

One Stripe Payment Link: A$1.99 a week, no free trial, "After payment" → redirect to `https://savesortai.com/?session_id={CHECKOUT_SESSION_ID}`. It goes in `CONFIG.link` in `public/app.js`. `CONFIG.portal` is the Stripe customer-portal login link; while it is empty, the "manage or cancel" link opens an email to us instead.

Secrets (Cloudflare → Workers & Pages → save-sortbot → Settings → Variables and Secrets, type Secret):
`STRIPE_SECRET_KEY` (restricted, read-only: Checkout Sessions, Subscriptions), `ANTHROPIC_API_KEY`, `TOKEN_SECRET`. Optional `MODEL`.

## SEO (keep this when editing the site)

- The build checks the basics and stops if one is broken: title 60 characters or fewer, description 70 to 160, one main heading per page, no two pages with the same title, alt text on every image, and every post linking to the sorter and to another post.
- The build gives every page its `<title>`, description, canonical address and link-preview tags from the details comment. Every page needs `title` and `description`; every page except the not-found page needs `updated` (or `date` for posts) for the sitemap.
- Design system: `DESIGN.md` in the repo root. Website rules for people and bots: `CLAUDE.md` (Website rules) and `site/WEB-INTERFACE-GUIDELINES.md`.
- `public/og.png` (1200×630) is the picture shown when someone shares savesortai.com. Only true numbers on it (156 saves, 30 Do it).
- The home page (`src/pages/index.html`) has JSON-LD structured data (app + FAQ). If you change an FAQ answer that's in the JSON-LD, change it there too. Don't add Pro features or prices to it. Blog posts get their own structured data from the build.
- `public/robots.txt` lets every crawler in (AI search included) except `/api/`.
- Fonts are served from `public/fonts/` (Bricolage Grotesque and Figtree, both SIL Open Font License), so the site makes no third-party requests. Don't add Google Fonts, analytics scripts or other outside files without the owner's say-so: "nothing leaves your device" is a selling point, and the security headers block outside files anyway.
- `jszip.min.js` loads only when someone drops in a zip. Don't put it back as a normal `<script>` tag.

## Reel screen captures

`engine/capture/capture_site.js` screenshots the real site for reels. It relies on these staying in `public/index.html` and `app.js`: `#try`, `#drop`, `#file`, `#report`, `#r-stats .rstat`, `#r-topics .bar`, `.chip[data-l]`, `.nav`, and the `SAMPLE` and `buildReport` names. Don't rename them.
