# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The general public with an overgrown Instagram Saved tab: everyday people who save reels about recipes, workouts, money, side hustles, AI tools and self-improvement, then never open them again. Most arrive on a phone, often straight from a SaveSort reel on Instagram, YouTube Shorts or TikTok. They are not developers or AI enthusiasts; someone who could build SaveSort themselves is not the customer (owner, confirmed 12 Nov 2026).

Their job: turn hundreds of saved reels into a short list of things worth doing, without logging in anywhere or handing over their data.

## Product Purpose

SaveSort reads the Saved file from Instagram's own data export and sorts every save by niche (AI, fitness, food, money and about 20 more) and by type (How-to & tips, Tools & apps, News & updates, Info & explainers, Motivation & quotes, Brainrot & memes), with one of four labels: **Do it**, **Watch it**, **Skip it**, **Locked**. Success means a visitor drops in their zip (or loads the sample), sees their saves sorted, and acts on the Do it list. Some go on to Pro for AI breakdowns.

## Positioning

The sorting happens entirely in the visitor's browser. The file is never uploaded, there is no Instagram login, and it uses Instagram's official export rather than scraping. SaveSort also calls out hype and "comment GUIDE" gating in plain words instead of selling it.

## Operating Context

- Visitor gets their file: Instagram → Settings → Accounts Center → Your information and permissions → Download your information (some accounts: Export your information) → Some of your information → Saved → format HTML. Instagram emails a zip, usually within hours.
- They drop the zip (no unzipping) on savesortai.com. Only `saved_posts.html` inside is opened.
- Static site built from `site/src` by `node site/build.mjs` and served by a Cloudflare Worker (`site/worker.js`) that also runs the Pro API.
- A weekly SEO bot publishes blog posts in `site/src/blog/`, and reels are captured from the live site by `engine/capture/capture_site.js`.

## Capabilities and Constraints

- **Free sorter (live):** sorts by niche and by type (how-tos, tools and apps, news, explainers, motivation, brainrot and memes; captions too short to tell are marked "Not enough caption"), labels Do it / Watch it / Skip it, flags Locked ("comment GUIDE" / DM gating), runs in the browser, no limit, re-sort any time, remembers the last report on the device only.
- **Pro (live):** A$1.99 a week through a Stripe Payment Link, no free trial. AI breakdowns (what it is, tools, steps, cost, the catch) written from a reel's caption with Anthropic's Claude. Pro code to use it on other devices. Cancel any time; full refund within 14 days of a charge.
- **Does not exist (never promise):** TikTok or YouTube saves, watching videos or transcripts, an app, monthly refresh, accounts.
- No third-party requests: self-hosted fonts (Bricolage Grotesque, Figtree), no analytics, strict CSP in `site/public/_headers`.
- Page hooks used by the reel capture script must keep their names: `#try`, `#drop`, `#file`, `#report`, `#r-stats .rstat`, `#r-topics .bar`, `.chip[data-l]`, `.nav`, `SAMPLE`, `buildReport`.
- Build-enforced SEO rules: title ≤ 60 characters, description 70–160, one h1, alt text on images, posts link to `/#try` and another post.
- Not affiliated with Instagram or Meta.

## Brand Commitments

- Name: SaveSort (domain savesortai.com).
- Mascot: **Sorty**, a blue bookmark-ribbon character (head colour #4C5CFF): blunt, deadpan, a bit smug, secretly helpful. Roasts the saves, never the visitor. Character bible: `content/sorty.md`.
- Labels are exactly **Do it, Watch it, Skip it, Locked** (owner, 11 Nov 2026).
- Voice: plain words, short sentences, a professional software product. Prices stated as A$ on the site.
- Location: don't mention Perth or Western Australia outside the legal pages. No country-specific laws in marketing copy.

## Evidence on Hand

- **Our sample report:** one real Saved tab, October 2026. 156 saves: 30 Do it, 65 Watch it, 10 Skip it, 22 Locked (owner wants this called "our sample report", not "our founder's saves", confirmed 12 Nov 2026).
- **The loadable sample** on the home page (`SAMPLE` in `site/public/app.js`) is 40 real captions from that same Saved tab. It does not reproduce the 156 totals, so the site must never say loading it shows the 156 report.
- Three example Pro breakdowns in `app.js` (`BREAKDOWNS`), written from real saved captions.
- Four blog guides in `site/src/blog/`.
- **Absent, never fabricate:** user counts, reviews, testimonials, customer logos, press, ratings, results, growth figures.

## Product Principles

1. Only true numbers. Every figure comes from the real report or it isn't shown.
2. Nothing leaves the device for the free sort. Privacy is the product, not a footnote.
3. Promise only what ships today.
4. Honest over hype: no get-rich-quick claims, no financial or legal advice, say what SaveSort can't do.
5. Phone first: the visitor is usually one tap away from a reel.

## Accessibility & Inclusion

WCAG 2.2 AA: text contrast, 44px tap targets on phones, keyboard-operable sorter, reduced-motion respected for every animation. Lighthouse accessibility, SEO and best practices 95+ on mobile.
