# Owner to-do, week of Mon 23 Nov 2026 (from the marketing council, Sat 21 Nov)

At most 5 items. The 4 still open from earlier weeks come first. **#5 is the only one with a deadline tonight (before 3am Perth).** Last week's Ep 1 "Follow for Ep 2" item is closed (Ep 2 is out); its TikTok sound issue moved to "When you have time".

1. **Still open (since 13 Nov): re-capture the sorter screens with your real export.** (10 min)
   Why: every reel and both episodes this week said "Do it" out loud but showed the old chips and stat cards ("Worth doing / Needs the video / Be careful / Gated guides") from the 13 Nov captures. The writer can't fix it: it needs your real 156-save file, and the 40-caption sample must never be shown as the 156.
   Steps: put your `saved_posts.html` somewhere Sunday's writer can reach it, or run `node engine/capture/capture_site.js <site> <fonts> engine/screens <path to saved_posts.html>` yourself, then copy the new files into the next episode's screens folder too. Optional: ask Claude to add a "Watch it" filter shot to the capture script (there isn't one, so Tuesday's Watch it guess reel can only show the number).

2. **Still open (since 7 Nov): bio, link and pins, now pinning the two episodes.** (5 min)
   Why: the episodes hold people 13 s, three times anything else, and Ep 1 is the only reel anyone has shared. People who check the profile should see them first.
   Steps: Instagram → Edit profile → bio: `What's your number? Ours: 156 saved reels, 30 Do it. Sort yours free, in your browser. Nothing uploaded ↓` Link: `savesortai.com/#try`. Pin Ep 1 and Ep 2 on Instagram and TikTok. TikTok bio (no link until 1,000 followers or a business account): `Sort your Instagram saved reels free at savesortai.com. Nothing uploaded.` Copy is in `marketing/drafts/2026-11-21/site-copy.md`.

3. **Still open (since 14 Nov): say yes or no to the label-name clean-up, and settle Pro.** (3 min to reply)
   Why: `CHECKER.md` (line 11), `content/sorty.md` (stamp lines 40–43, 52) and `accounts/hypecheck.md` still say worth doing / be careful / gated, and the site headline still says "30 worth doing" and leaves "Download to device" out of the steps. Also `PRODUCT.md` says Pro is live at A$1.99 a week, while `AGENT.md` and `CHECKER.md` say Pro isn't launched and prices must be in USD, so the writer and checker disagree about what can be said.
   Steps: read `marketing/drafts/2026-11-21/site-copy.md` (exact before → after) and reply to Claude "yes, rename the labels and apply the site copy", plus one line on Pro: "Pro is live, mention it in A$/USD" or "don't mention Pro".

4. **Still open (since 11 Nov): connect Google Search Console.** (5 min)
   Why: search is our only way to strangers, and there are now 5 blog posts (with 2 more outlined) whose traffic nobody can see.
   Steps: search.google.com/search-console → Add property → Domain `savesortai.com` → add the TXT record at your domain host → Verify → Sitemaps → submit `sitemap.xml`.

5. **New, tonight before 3am: check Sunday's 03:00 reel `says-nothing`.** (1 min)
   Why: its scene-1 line ends "Seriously.", which today's lessons drop, and its quote "Wait for it... (no caption)" can't be found in any save in the repo. That's the same mistake that got 2 reels held this week, and the caption says "the saves and numbers are real".
   Steps: if you can't confirm the quote is a real save's caption, delete `queue/2026-11-22-1-says-nothing.json` on GitHub (the slot just stays empty). Otherwise let it post.

**When you have time (not this week):**
- Turn off trending TikTok sounds for episodes (Ep 1 got "Time Back" and Ep 2 got "Take Me (To The Moon)", both muted, but your rule is your own track only). Set `TIKTOK_SOUND=off` or skip `trending_sound` for episodes.
- Add a search phrase to Ep 2's YouTube title ("Sorty Ep 2: The 10K Bet | how to sort Instagram saved reels") and put both episodes in a YouTube Shorts Series.
- Decide the 3am slot: Instagram gets a median of 9 views there, but TikTok and YouTube don't care about slot. Option: set 03:00 reels to `"platforms": ["youtube","tiktok"]`.
- Paste the text of real comments and DMs into a note each week. The team has no real viewer words to work from.
- Product notes (click tracking, tag the episodes, hook-score, "Unsorted" chip) are in `marketing/drafts/2026-11-21/faq-and-product-notes.md`. Also ready there: reply bank, 2 blog outlines, a community answer, a creator DM, episode share lines.
- The niche accounts: create gym / kitchen / hype check on IG, TikTok and YouTube and connect the Upload-Post profiles `savesort-gym`, `savesort-kitchen`, `savesort-hypecheck`.
