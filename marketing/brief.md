# Marketing brief, week of Mon 30 Nov 2026 (by the CMO)

Written Sat 28 Nov from `content/lessons.md` (analyst, today 16:17), `stats/summary.md` (28 Nov 16:23) and reports from all nine departments (D2–D10). Order of authority: AGENT.md → CHECKER.md → lessons.md → this brief.

**⚠ Read first.** (1) **Instagram has posted nothing since 26 Nov 03:00**: the poster's `sudo apt-get install ffmpeg` gets 404s on the new ubuntu-26.04 runner (no `apt-get update` first). YouTube and TikTok still post. When it's fixed, `post.py` will post the backed-up reels oldest-first, up to 6 runs a day (owner to-do #5 covers both). (2) **8 reels (26–28 Nov) are live on YouTube/TikTok but missing from the stats**: `stats.py` only counts `status: posted`, and they stay `queued` while Instagram fails. (3) Screens in `engine/screens/` still show the old labels (16 Nov capture), so team rule 1 from last week still applies. Sun 29 is already queued (07:00 `watched-never-saved` is held), so the writer's 21 slots are **Mon 30 Nov 03:00 → Sun 6 Dec 19:30**.

## Scorecard
- **Reels posted 22–25 Nov (12): 2,272 views, median 171** (15–21 Nov, 18 reels: 3,224, median 158). They're younger (3–6 days vs 7–13), so the total drop is partly age. (D8 checked.)
- **Instagram 240 views, median 10** (was 697, median 24.5); a real drop, not noise. **YouTube 941, median 47.5** (was 388, 17.5), 41% of all views (was 12%). TikTok 1,091 (8 of 12 reels have data).
- Median % watched **8%** (unchanged). Best: `pov-never-opened` 444 (YT 442, "How to go through old Instagram saves fast"; its 10.5 s watch is from 2 IG viewers, ignore it). Best IG: `who-sees-saves` IG 114 / 5.0 s. Worst with full data: `unsave-regret` 124 (`sorty-broke` shows 6 but has no TikTok data).
- 0 new followers. Site/sorter signal: **unknown** (not tracked; Search Console not connected). YouTube watch time: not collected.

## The bottleneck
**Instagram has stopped delivering (reach −75% from 20 Nov, posting broken since 26 Nov), so YouTube search is our only door to strangers, and only reels that answer a question people type get through it.** Evidence: YT median 14 → 41; the search-question titles took 442, 134 and 46–56; inside-joke reels reach nobody. (D2, D5, D7, D8.) Fixing Instagram is the owner's job (to-do #5); everything the writer does this week is built for search.

## This week's campaign: "Your saves questions, answered: 31 days to 2027"
Every reel answers one plain question people ask about their saved reels (who can see them, folders, search, new phone, what's in the download, is it safe), with the year-end clock behind it. Each one is a YouTube search answer and a Help-Centre-checkable fact, so it's useful to anyone with a pile of saves, not just tech people. Wed 2 Dec is a year-end "recap" moment (Spotify's recap is predicted that day, not confirmed; say "recap", never "Wrapped"). The week ends Sunday on "One pile tonight. Done."

## Slot plan (the writer follows this)
Times Perth. ★ = the 3 strongest. Mix (lessons.md): base 15 (3 real-question ★Q, 2 before-2027, 1 story, 0 guess, 9 others), funny-ad 2 (07:00), exp-crazy-hook 2 (1 warning, 1 challenge), exp-pov 1 (judged on YouTube), exp-before-after 1 = 21. No `-b` reels, no part 1 → 2 pairs. Draft 3 cold opens each and score them (60+); the ones below are starting points. Every `yt_title` below is unused in the last 2 weeks. **Any answer the claims check can't confirm on Instagram's Help Centre → swap the question, don't soften it.**

| Day | Time | Style | Concept | Cold open | Niche | CTA |
|---|---|---|---|---|---|---|
| Mon 30 | 03:00 | exp-crazy-hook (warning) | What happens to a save when the creator deletes the reel (checker verifies). Payoff: sort the export so the useful ones are listed. yt "What happens to a saved reel when it's deleted" | "Deleted reels vanish from Saved." | how-to | link |
| Mon 30 | 07:00 | base ★Q1 | Folders for saves: Instagram Collections exist but you file each post by hand; SaveSort sorts the whole pile by topic (never say it makes Collections). yt "How to put Instagram saved posts in folders" | "Folders for your saves?" | how-to | link |
| Mon 30 | 19:30 ★ | exp-pov | Follow-up to our best YT reel, "you" all the way: you, 500 saves, one evening; drop → tap a topic → open one. yt "How to go through hundreds of saved reels quickly" | "POV: 500 saves, one evening." | general | link |
| Tue 1 | 03:00 | base | What's in the zip Instagram emails you, and the one file SaveSort reads (saved_posts.html). yt "What's in your Instagram data download" | "Instagram emailed you a zip." | how-to | link |
| Tue 1 | 07:00 | funny-ad | The viewer's gym saves "for January" (joke on the pile, not Sorty); Health & lifestyle topic only. yt "How to use saved workout reels for a new year plan" | "Leg day, booked for January." | gym | link |
| Tue 1 | 19:30 | base (before-2027 #1) | True countdown: 31 days to 2027 on Tue 1 Dec. Sort before the new year, keep the Do it pile. yt "How to clean up Instagram saves before the new year" | "31 days to 2027." | general | link |
| Wed 2 | 03:00 | base ★Q2 | Who can see your saved collections (only people in a collaborative one; Help Centre). yt "Who can see your saved collections on Instagram" | "Who sees your collections?" | general | link |
| Wed 2 | 07:00 | base | Is it safe: SaveSort opens only saved_posts.html, no login, nothing uploaded. yt "Is it safe to sort Instagram saves online" | "Your saves. Uploaded where?" | general | link |
| Wed 2 | 19:30 ★ | base (before-2027 #2) | Year-end recap of the real sample report (156 / 30 / 65 / 10 / 22 mid-reel as proof, not a guess); payoff a real topic tap. yt "Instagram saved reels recap: what did you save" | "Your year, in saves." | general | link + send line |
| Thu 3 | 03:00 | exp-before-after | Messy pile (`hook` grid) → topic bars → open a topic. Real screens only, no chips. yt "How to turn a messy saved tab into topics" | "Messy pile. Ten seconds." | general | link |
| Thu 3 | 07:00 | base | Waiting on Instagram's email? How long it takes (checker verifies on Help Centre, else say "Instagram emails you when it's ready"); try the 40-save sample meanwhile, never called the 156. yt "How long does Instagram take to send your data" | "Waiting on Instagram's email?" | how-to | save |
| Thu 3 | 19:30 ★ | base (story) | "Gym at 6": which saved workout do you do? Stake + deadline, twist, payoff on the Health & lifestyle screen. yt "How to find a saved workout fast" | "Gym at 6. Which save?" | gym | link + send line |
| Fri 4 | 03:00 | base | New phone: are your saves still there (they're on your account; checker verifies). yt "Do Instagram saves transfer to a new phone" | "New phone. Saves gone?" | how-to | link |
| Fri 4 | 07:00 | funny-ad | The viewer's recipe pile vs what they cook; screen says "sorted by topic" (no Recipes topic). The 47 is aimed at a typical viewer, never shown as a result. yt "How to sort saved recipe reels on Instagram" | "47 recipes saved. Made toast." | kitchen | link |
| Fri 4 | 19:30 | base ★Q3 | Can you search your saved posts? (checker must confirm "no" at the source; fallback question: "Can you see when you saved a post?"). Sort by topic instead. yt "Can you search your saved posts on Instagram" | "Search your saves? Try it." | general | link |
| Sat 5 | 03:00 | base | The Watch it pile: saves whose caption says nothing (65 of 156). yt "How to find saved reels with no caption" | "No caption. No clue." | general | link |
| Sat 5 | 07:00 | base | Sort on a laptop: SaveSort runs in any browser. yt "How to see Instagram saved posts on a computer" (checker verifies) | "Phone full? Use your laptop." | how-to | link |
| Sat 5 | 19:30 | exp-crazy-hook (challenge) | Keep only 3 saves for 2027; the Do it pile makes the pick. yt "How to decide which Instagram saves to keep" | "Keep 3 saves. Only 3." | general | link |
| Sun 6 | 03:00 | base | Do one save this week: tap the Do it pile, pick one. yt "How to turn saved reels into a weekly plan" | "Do one save this week." | general | link |
| Sun 6 | 07:00 | base | Clear out old saves but keep the good ones: sort first, then unsave. yt "How to clear out old Instagram saves and keep the good ones" | "Unsave 100? Keep the good." | how-to | link |
| Sun 6 | 19:30 | base | Campaign finale: every question this week, one answer: sort, then one pile a night. yt "Best way to organise Instagram saved reels" | "One pile tonight. Done." | general | link |

## Niche accounts
None is connected (`accounts/status.json`: `ready: false`; poster log 28 Nov "not connected yet"), so writers make nothing for them. When one connects (#48 with #16–#18): 14 slideshows (2 a day) + 7 reels (19:30), slide 1 a concrete situation or a real question, SaveSort slide last, current labels. Re-run hook: none yet (nothing posted).
### gym
"Busy December: 10-minute workouts, no equipment." Mix: routine 3, beginner 3, story 2, saved-vs-did 2, mistakes 2, myth 2. Hooks: "December's busy. 10 minutes works." · "40 ab workouts. Did none." · "Scared of the gym? Start here." Rule: safety line on harder moves; screens show Health & lifestyle only.
### kitchen
"Cooking for one in December: 15-minute dinners." Mix: recipe 4, pantry 3, story 2, saved-vs-made 2, prep 2, hack-check 1. Hooks: "40 recipes. Ordered pizza." · "Rice, eggs, one sad onion." · "One shop. Five dinners." Rule: no Recipes topic exists; name allergens and safe doneness.
### hypecheck
"New year, new hustle? Checking the 'by 2027' reels." Mix: verdict 3, red-flags 3, real-cost 3, gated 2, worth-it 2, story 1. Hooks: "\"Quit your job by January\"" · "5 signs that reel sells you." · "What 'comment GUIDE' actually sends." Rule: labels Skip it / Locked only (its playbook still has old names, owner to-do #3); no creator names, no income claims.

## Rules for this week from the team
1. **Cold opens:** none starts "You saved" or "Saved" (16 of last week's 21 did), no first two words repeated in the week; on ★Q reels scene 1 is the searched question itself, ≤5 words. Still no old label word visible on any still (use `drop.png`, `topics.png`, `topics-*`/`topic-*`, `stat` scenes). (#23, #84, #86)
2. **Keep the question open:** scene 2 asks or sharpens the question, never answers it; ask it again around scene 8; the `payoff` (second-last) answers it on a **real screen tap** (a topic opening), not the `stat` 30 card. At most 7 of 21 reels end on a `stat`. (#36, #26, #31)
3. **Second person, short lines:** the viewer is the main character in every `vo`; at most one Sorty-about-Sorty line; no pay, rent or "broke" jokes. No scene `vo` over 10 words (split it). Numbers as digits in `vo` ("10 topics", not "Ten topics"). (#24, #30, #34, #89)
4. **Every item gets a hand-written `yt_description`:** line 1 answers the `yt_title` in one sentence; line 2 "Free, in your browser: savesortai.com" (typed domain, works whether or not the link taps); then 2–3 short lines; `#Shorts` + 3 tags. Template in `drafts/2026-11-28/yt-channel.md`. (#52, #54, #69)
5. **Facts:** every question's answer checked on Instagram's Help Centre (or the claims check drops it). Never say Watch history "only goes back about a month" (unverified; that's what got `watched-never-saved` held). (#82, #15)
6. **Judging while Instagram is down:** judge on YouTube views (and TikTok watch time); quote IG watch time only on reels with 20+ IG views. (#73, #74)

## Department calls
- **D2 Research:** question reels are the only ones strangers find; no real viewer words exist. → Campaign, ★Q2 (collections, Help Centre), "31 days to 2027" countdown, Wed recap.
- **D3 Creative:** one template: 16/21 openers "Saved…", 11/21 end on `stat` 30; best reel is all "you". → Rules 1–3, folders ★Q1, pov follow-up, recipe funny-ad.
- **D4 Retention:** our watch figures are tiny-sample; scene 2 answers too early; 13–17-word scenes. → Rules 2, 3, 6; YouTube watch time to owner (#5).
- **D5 Platforms:** IG broken twice (reach + ffmpeg); backlog would post 6 a day. → Owner to-do #5 with exact fix; niche plan; new yt_titles.
- **D6 Copy:** every YT description opens with the same line; Shorts links may not tap; site H1 still "30 worth doing". → Rule 4; YouTube channel paste folded into to-do #2; 3 site edits in drafts.
- **D7 Growth:** no page answers our best YouTube question; privacy post outlined, never written. → SEO worker writes `can-people-see-what-you-save-instagram` + one new H2 (drafts/seo-page.md); community answer drafted.
- **D8 Analytics:** 8 reels unmeasured; IG drop real (p<0.001), YT rise real (p=0.02); hook_score r≈−0.02. → Scorecard, warning ③, stats fix in to-do #5.
- **D9 Quality:** rule files and site still use old labels; TikTok attaches others' trending sounds at volume 0 on every reel; quotes all clean. → Rule 1, to-do #3, `TIKTOK_SOUND=off` in the later list.
- **D10 Product:** no screen can show one save tagged Do it; objections (safe, wait) answer well as search questions. → Wed 07:00 safe, Thu 07:00 wait, Tue 03:00 zip; missing shots + tracking in product notes.

## Decisions between departments
- **Screen by 3 s (lessons) vs "stop counting it as the fix" (D4):** both. SaveSort stays on screen by scene 3, but scene 2 must not answer (rule 2).
- **Drop hook_score as a gate (D8) vs AGENT.md "60+ only":** AGENT.md wins; 60+ is a floor, not a predictor. D8's finding goes to the owner.
- **"Worst reel" (D8: `unsave-regret`) vs lessons (`sorty-broke`):** lessons stand on funny-ad as a style (median 93); the TikTok gap goes in the stats fix.
- **Year-end recap on Wed (D2) vs trademark/date risk:** keep it, say "recap", show only the real report; move it if Spotify's date shifts.
- **URL lines in YT descriptions (D7) vs Shorts links may not tap (D6):** typed domain on line 2 (works both ways); blog URL optional on line 3.
- **3am to YT/TikTok only (last week's D5):** moot while Instagram is down; stays an owner decision.
