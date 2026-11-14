# FAQ / objection sheet + product notes (D10, D8, 14 Nov). Drafts only.

## FAQ (new labels, matches `site/public/app.js` today)
- **Is it safe?** The free sort runs in your browser. Drop in the zip Instagram emails you. SaveSort opens only saved_posts.html and uploads nothing. No Instagram login.
- **Is it free?** Yes. The sorter is free with no limit and no account. Pro is optional: A$1.99 a week for AI breakdowns written from a save's caption. Cancel any time; full refund within 14 days of a charge.
- **What do the labels mean?** Do it: the steps are in the caption. Watch it: the caption says almost nothing. Skip it: hype words. Locked: "comment GUIDE" or "DM me" gating (can overlap the others). Every save gets a topic; a save only gets a label when its caption gives a reason, so some get none (in our sample report 105 of 156 got one of the first three).
- **Too much effort?** Request it once: Accounts Center › Your information and permissions › Download (or Export) your information › Some of your information › Saved › All time, HTML. Instagram emails it, usually within hours. Drop the zip in without unzipping. Try the 40-save sample while you wait.
- **HTML or JSON?** HTML. JSON has no captions, so everything lands in Watch it.
- **Does it watch videos?** No. It reads captions.
- **Come back later?** Your last sort stays on this device. Drop a new export to update it.
- **TikTok/YouTube saves? An app?** Not today.

## Product notes for the owner (from marketing, not users: still 0 user questions)
1. Re-capture `engine/screens/` with the real 156 file (not the sample), then look at the stills. (Owner to-do #2.)
2. No food/recipe or gift topic; "workout", "exercise", "reps" aren't matched (only gym/fitness). The kitchen niche has no honest product screen.
3. Up to 51 of 156 saves get none of Do it / Watch it / Skip it. Consider an "Unsorted" chip, or say so in the report.
4. Link clicks and sorter runs are untracked, so the link ask can't be judged. A per-reel `?r=<slug>` tag counted server-side (no third-party tracker) would answer it.
5. (D8) The stats Slot column uses the scheduled time, not the real post time: `guess-useful` (due Tue 19:30) went out Wed 02:43 and `junk-drawer` (due Sun 19:30) Mon 01:07. Worth checking why evening posts slipped, and building the slot column from actual post time.
6. (D8) `hook_score` didn't track watch time this fortnight (rank correlation −0.04 vs IG watch, n=17). The guess lines scored lowest (62.6) but held best. Suggest recalibrating `team/tools/hookscore.py`; the 60+ rule is yours to change.
7. (D2) Typical TikTok length is ~20 s; ours are 30–33 s by your rule. Only a suggestion.
