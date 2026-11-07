# Owner to-do, week of Mon 9 Nov 2026 (from the marketing council, Sat 7 Nov)

Nothing is still open from last week, because this is the first list. At most 5 items, most urgent first.

1. **Done (7 Nov): Sunday content run confirmed.** "SaveSort weekly reels" is enabled and runs Sun 8 Nov at 9:38am Perth, and the claims check runs at 3:07pm. Only the `PAUSED` repo variable is left to check, if you set it. (was 2 min)
   Why: 0 reels are queued. The last one posted Fri 6 Nov at 19:30, so nothing posts tonight and nothing more will until the writer runs.
   Steps: check that the weekly content task (AGENT.md) is scheduled for Sunday 8 Nov and isn't paused, and that the repo variable `PAUSED` isn't `true`. If you want posts sooner, start the content run now.

2. **Done (7 Nov), owner said "up to you": website fixed.** Numbers now read 156/30/65/10, the monthly/search promises are gone, Pro features are labelled Pro, and the creator handles are out of the sample. Pro checkout stays live, because Pro is built (Stripe, breakdown API). (was 15–20 min)
   Why: reels say 156 saved / 30 worth doing. The site hero says "You saved 312 reels… 21 worth doing", and the stats strip says 24/61/7. The page also promises Pro features that aren't launched ("step-by-step plans", "fresh report every month", "search"), and the "Get Pro · A$1.99 a week" button opens a live Stripe checkout. Everyone who taps the link from a reel lands on this.
   Steps: open `marketing/drafts/2026-11-07/site-copy.md`, which has every change as exact before → after text. Decide whether Pro checkout stays live (if not, set `CONFIG.link` to `""`), then edit `site/public/index.html` or ask Claude to make the change.

3. **Yes or no: let the trial reels test "Sorty talks first" instead of the white title card.** (1 min)
   Why: the cold open is your rule. This week's white-title openers got 27–46 Instagram views. The reels that opened with Sorty talking got 115–121. Topics were similar, but this isn't proven. 5 Instagram-only trial reels would settle it by 21 Nov, and your main reels stay unchanged.
   Steps: tick the box below before Sunday's content run. Leave it blank for "no".
   - [x] Approved: trial `-b` reels open with Sorty talking (same line). Owner said yes on 7 Nov.

4. **Done (7 Nov), owner approved: AI-voice label.** `poster/post_youtube.py` now sends `containsSyntheticMedia: true`, and brief rule 6 adds the caption line. (was 5 min)
   Why: Sorty's voice is AI and says "I saved 156 reels" in the first person. Meta and YouTube ask for a label on realistic synthetic voices, and a missing label can mean penalties. TikTok already sends the AI flag. The niche poster sets YouTube's flag, but the main `poster/post_youtube.py` doesn't. The brief adds a caption line: "Sorty's voice is AI. The saves and numbers are real."
   Steps: if you agree, ask Claude to set `status.containsSyntheticMedia: true` in `poster/post_youtube.py`. If you'd rather not have the caption line, delete rule 6's second sentence in `marketing/brief.md`.

5. **Approved; still open, only the owner can do it in the Instagram app: bio and pins.** (5 min)
   Why: people who like a reel check the profile in about 3 seconds. Both pinned reels will show the real numbers.
   Steps: in Instagram → Edit profile, set the bio to "Saved 156 reels. Only 30 worth doing. Sort yours free: by topic, worth doing or be careful. In your browser, nothing uploaded ↓". Set the link to `savesortai.com/#try`. On your grid, pin "I saved 156 reels. Guess how many were worth doing" and "You saved that reel months ago. Here's how to find it". Ideally do this after #2, so the site matches.

**When you have time (not this week):** the TikTok decision (the analyst and D5 suggest a 1-week slideshow-only test), connecting the gym, kitchen and hype check accounts (create the accounts and the Upload-Post profiles `savesort-gym` / `savesort-kitchen` / `savesort-hypecheck`), and the product notes in `marketing/drafts/2026-11-07/faq-and-product-notes.md` (recipe/gift topics, per-reel links). The reply bank, a creator DM, a community answer and an SEO page outline are also ready in that folder.
