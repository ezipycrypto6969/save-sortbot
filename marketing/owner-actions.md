# Owner to-do, week of Mon 30 Nov 2026 (from the marketing council, Sat 28 Nov)

At most 5 items. The 4 still open from earlier weeks come first (last week's #5, the Sun 22 reel, is closed: it posted). **If you only do one thing, do #5: Instagram has posted nothing since 26 Nov.**

1. **Still open (since 14 Nov): say yes or no to the label clean-up, and settle Pro.** (3 min to reply)
   Why: `AGENT.md` (stamp examples), `CHECKER.md` line 11, `content/sorty.md`, `accounts/hypecheck.md` and the site headline ("30 worth doing") still use the old names while every reel says Do it. `PRODUCT.md` says Pro is live at A$1.99 a week; `AGENT.md`/`CHECKER.md` say it isn't launched and prices must be USD.
   Steps: read `marketing/drafts/2026-11-28/site-copy.md` (3 edits, cut down from last week's 8) and reply to Claude "yes, rename the labels and apply the site copy", plus one line: "Pro is live, mention it in A$/USD" or "don't mention Pro".

2. **Still open (since 7 Nov): profile and link, now YouTube first.** (8 min)
   Why: YouTube is where the views are now (median 41 a reel, our best ever 442), and a Short's viewer can reach the sorter through the channel's links. The Instagram bio and pins are still undone too.
   Steps: YouTube Studio → Customisation → Basic info: paste the channel description and add the link `savesortai.com/#try` (both in `drafts/2026-11-28/yt-channel.md`). Pin the comment from the same file on `pov-never-opened` and `forgot-why`. Then Instagram → Edit profile: bio and link from `drafts/2026-11-21/site-copy.md`; pin Ep 1 and Ep 2 on Instagram and TikTok.

3. **Still open (since 13 Nov): re-capture the sorter screens with your real export.** (10 min)
   Why: `engine/screens/` is still the 16 Nov capture showing "worth doing / need the video / be careful / Gated guides", so no reel can show the product's best moment: one save marked Do it.
   Steps: run `node engine/capture/capture_site.js <site> <fonts> engine/screens <path to your saved_posts.html>` (or put the file where Sunday's writer can reach it). Optional: ask Claude to add a Watch it filter shot and a single-save-card shot (details in `drafts/2026-11-28/product-notes.md`).

4. **Still open (since 11 Nov): connect Google Search Console.** (5 min)
   Why: search is now our main way to strangers, and there are 6 blog posts (one more coming Sunday) whose traffic nobody can see.
   Steps: search.google.com/search-console → Add property → Domain `savesortai.com` → add the TXT record at your domain host → Verify → Sitemaps → submit `sitemap.xml`.

5. **New, most urgent: get Instagram posting again, without a flood of old reels.** (5 min)
   Why: every Instagram run since 26 Nov 03:00 fails at `sudo apt-get install ffmpeg` (404s on the new ubuntu-26.04 runner, because the package list is never updated). 8 reels from 26–28 Nov went to YouTube/TikTok only. Fix just the install and the poster will post all 8 backed-up reels oldest-first, one per run, up to 6 a day (AGENT.md allows 3). Separately, Instagram reach fell 75% from 20 Nov in every slot and style, and the stats skip those 8 reels.
   Steps: (a) reply to Claude: **"yes, fix the poster and the stats"**. That means: add `sudo apt-get update` before the install; give Instagram the same 3-day lateness cap YouTube has, so the stale 26–28 Nov reels are skipped on Instagram (they're already on YouTube/TikTok); count a reel in the stats when any platform posted it; add YouTube watch time. Exact change in `drafts/2026-11-28/poster-fix.md`. (b) In the Instagram app: Settings → Account Status. Note whether anything is flagged under recommendations and tell Claude what it says.

**When you have time (not this week):**
- Set the repo variable `TIKTOK_SOUND=off` (1 min). Every TikTok post 24–28 Nov had someone else's trending track attached at volume 0 ("Self Aware", "Time Back"...), against "everything ours".
- Post one community answer (privacy question) from `drafts/2026-11-28/community.md`: find a real, recent thread first and follow that community's rules.
- Paste the text of real comments and DMs into a note each week. Both best reels got 0 comments; the team still has no real viewer words.
- Tracking idea (your call): count page loads, sample loads and finished sorts on our own Worker, no third-party script (`drafts/2026-11-28/product-notes.md`).
- The niche accounts: create gym / kitchen / hype check on IG, TikTok and YouTube and connect the Upload-Post profiles `savesort-gym`, `savesort-kitchen`, `savesort-hypecheck`.
- Older notes (3am slot, Ep 2 title, YouTube Series) are still in `drafts/2026-11-21/`.
