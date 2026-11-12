# SaveSort

Owner rules for the content bot live in `AGENT.md` (they win over anything here), the claims check in `CHECKER.md`, the SEO worker in `SEO.md`. Product facts: `PRODUCT.md`.

## Website rules

Applies to anyone (people or bots) changing savesortai.com (`site/`).

1. **Read first:** `DESIGN.md` (the look: "Sorted Under Glass") and `site/WEB-INTERFACE-GUIDELINES.md` (Vercel's interface rules), then `site/README.md` for how the site is built. Edit `site/src/` and `site/public/site.css` / `app.js`, run `node site/build.mjs`, and commit `src/` and `public/` together.
2. **Check every page you touch at 390, 768 and 1440 px wide.** No sideways scroll, nothing overlapping, no text under 12px (body text 16px or more on phones), tap targets at least 44px on phones. Look at screenshots, not just the code.
3. **Meet the targets on the home page (Lighthouse, mobile):** accessibility, SEO and best practices 95 or higher; LCP 2.5 s or less; CLS 0.1 or less. No console errors. Text passes WCAG AA contrast, and every animation stops for reduced motion or has a pause control.
4. **Never invent numbers.** Only the real report: 156 saves, 30 Do it, 65 Watch it, 10 Skip it, 22 Locked ("our sample report"). The loadable sample is 40 of those captions; never present it as the 156. No made-up users, reviews, logos, testimonials, ratings or results. Only features that exist today.
5. **Keep it ours:** no third-party requests (self-hosted fonts, no trackers), don't rename the reel-capture hooks listed in `site/README.md`, and don't mention Perth outside the legal pages.
6. **Weekly bots only measure and make small fixes.** The SEO worker and any scheduled run may fix a broken link, a typo, a contrast or tap-target failure, or add a blog post. They never redesign, restyle, reorder sections, change prices, legal text or what the sorter does. Bigger changes go to the owner as a suggestion.
