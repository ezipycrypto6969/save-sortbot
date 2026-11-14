# Owner to-do, week of Mon 16 Nov 2026 (from the marketing council, Sat 14 Nov)

At most 5 items, most urgent first. Last week's #1, #2 and #4 are done; #3 (trial reels) no longer applies because Instagram refuses trial reels below 1,000 followers.

1. **Still open (since 7 Nov), now with the new label names: bio, link and pins.** (5 min)
   Why: almost every reel says "link in bio". People who like a reel check the profile in about 3 seconds, and the old draft bio said "worth doing / be careful", which no longer matches the site.
   Steps: Instagram → Edit profile → bio: `Our 156 saved reels: 30 Do it, 65 Watch it, 10 Skip it, 22 Locked. Sort yours free, in your browser. Nothing uploaded ↓` Link: `savesortai.com/#try`. Pin "I saved 156 Instagram reels. How many were actually useful?" and "You saved that reel months ago. Here's how to find it". TikTok and YouTube versions are in `marketing/drafts/2026-11-14/site-copy.md` (top).

2. **Old label names in the queued reels and the sorter screens.** (2 min to decide, +10 min if you run the capture)
   Why: the 3 queued reels (tonight 19:30 `watch-it-sort`, Sun 03:00 `22-gated`, Sun 07:00 `lost-found-closes`) say "worth doing / be careful / gated guides", and `engine/screens/` still shows the old chips, while the site says Do it / Watch it / Skip it / Locked. The writer can only re-capture the screens with your real 156-save export; it isn't in the repo, and the 40-caption sample must never be shown as the 156.
   Steps: (a) let those 3 post as they are, or delete their files in `queue/` to skip them (tonight's goes at 19:30). (b) Put your real `saved_posts.html` where Sunday's writer can use it (or run `node engine/capture/capture_site.js <site> <fonts> engine/screens <path to saved_posts.html>` yourself) before the 9:38am run.

3. **Ep 1 caption: the "Follow for Ep 2" promise and the TikTok sound.** (3 min)
   Why: Ep 1 promises "Ep 2: Sorty vs your recipe saves", but nothing is queued, and your rule allows a part-2 promise only if it's queued within 48 h (Mon 16 Nov ~17:50). There's also no Recipes topic to show. Its TikTok post got a muted trending sound ("Time Back"), and your rule says episodes use only your own track.
   Steps: either ship Ep 2 by Monday evening (sorted by topic, no Recipes folder on screen) or edit the caption on each platform to drop the Ep 2 line. On TikTok, swap the sound for your "reel sound ai" track if the app lets you, or leave it muted.

4. **Say yes (or no) to the label-name clean-up in the rule files and site.** (2 min to reply)
   Why: `CHECKER.md` rule 1, `AGENT.md` (scene table and ask examples), `content/sorty.md` stamp lines and `accounts/hypecheck.md` still use the old names, so the writer and checker keep passing them. The site has 3 stale spots (2 blog posts say "gated guides", the pricing list says "Locked-guide detector") and the "get your file" steps miss "Download to device". The weekly bots can't change these files or site copy without you.
   Steps: read `marketing/drafts/2026-11-14/site-copy.md` (exact before → after) and reply "yes, rename the labels" to Claude; it can then make the edits.

5. **Connect Google Search Console.** (5 min)
   Why: search is the only thing reaching strangers (how-to YouTube titles: 60–82 views vs 3 for the rest). Without Search Console the SEO worker can't see which pages people find. Open in `site/seo-log.md` since 11 Nov.
   Steps: search.google.com/search-console → Add property → Domain `savesortai.com` → add the TXT record at your domain host → Verify → Sitemaps → submit `sitemap.xml`.

**When you have time (not this week):** the niche accounts (create gym / kitchen / hype check on IG, TikTok, YouTube and connect Upload-Post profiles `savesort-gym`, `savesort-kitchen`, `savesort-hypecheck`); the TikTok keyword tool (add "instagram saved reels" to the top 3 TikToks, 2 min); the product notes in `marketing/drafts/2026-11-14/faq-and-product-notes.md` (click tracking, post-time slot fix, hook-score recalibration, "Unsorted" chip). Also ready in that folder: a refreshed reply bank, an "unsave all" blog outline, a community answer and a creator DM.
