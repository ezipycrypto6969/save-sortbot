# FAQ and product notes (D10 #95/#96/#100, D8, D9; 21 Nov 2026). Drafts only: the owner decides.

## FAQ (matches what the site does today)
- **Safe?** Sorting runs in your browser. Drop in the zip Instagram emails you. Only saved_posts.html is opened. Nothing is uploaded and there's no Instagram login.
- **Free?** Yes, no limit and no account needed. Pro is optional: A$1.99 a week for AI breakdowns written from a save's caption. Cancel any time, with a full refund within 14 days of a charge. *(Depends on owner to-do #3: AGENT.md still says Pro isn't launched.)*
- **Effort?** You ask Instagram once: Accounts Center › Your information and permissions › Download (or Export) your information › Some of your information › Saved › Download to device › All time, HTML. The email usually arrives within hours. Drop the zip in without unzipping it. Try the sample while you wait.
- **Labels?** Do it: the steps are in the caption. Watch it: the caption says almost nothing. Skip it: hype. Locked: "comment GUIDE" or "DM me", and it can overlap the others. Every save gets a topic; only some get a label.
- **Does it watch videos?** No, it reads captions. **TikTok or YouTube saves? An app?** Not today.
- **Come back later?** Your last sort stays on your device. Drop in a new export to update it.

## Product notes for the owner (from marketing; still no real user questions to pass on)
1. **Screens:** old label names are on screen in all 19 engine reels and both episodes (13 Nov captures). Re-capture with the real export (owner to-do #1).
2. **No Watch it filter shot:** `capture_site.js` captures the Do it / Skip it / Locked filters only. Adding `report-thin.png` would let a Watch it reel pay off on a real screen.
3. **We can't see past the view:** 0 TikTok profile views ever, no IG profile-visit field, no click or sorter-run tracking. A per-reel `?r=<slug>` link counted on our own Worker (no third-party tracker, per CLAUDE.md) would show which reels lead to a sort.
4. **Tag the episodes:** both episode queue files lack `style`, `hook_type` and `duration`, so their 13 s can't become a % watched and summary.md counts them as "base". Suggest `"style": "episode"` and a duration.
5. **hook_score doesn't predict watch time** for us (r ≈ −0.02 with IG avg watch, n=42; −0.07 with TikTok, n=39; 77.8 on 22 of 42 reels). The 60+ floor is your rule and stays; recalibration is your call.
6. **Crazy-hook test design:** the lessons put the warning at 03:00 and the challenge at 19:30, so slot and style are mixed up (n=1 each). Same slot for both next time would separate them.
7. **"Callouts fail on IG" may really be the 3am slot:** both callout reels went out at 3am; all-time 3am IG median 17.5 vs 47.5 at 19:30. TikTok is flat across slots.
8. **No recipe topic,** so the kitchen account has no honest "found your recipe" screen. **51 of 156 saves get no Do it / Watch it / Skip it label;** consider an "Unsorted" chip.
9. **Stats glitches:** `156-zero` and `full-tutorial` show watch time longer than the reel; `no-login` and `saved-at-2am` say TikTok posted but have no TikTok stats.
10. **Muted trending TikTok sounds:** `post_tiktok.py` adds one (lines ~39–53) and nothing checks it's from the Commercial Music Library. Episodes got "Time Back" and "Take Me (To The Moon)". Suggest off for episodes.
