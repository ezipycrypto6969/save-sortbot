# Bio + site copy (D6, 14 Nov). Drafts only: the owner decides.

## Bios (new label names)
- **Instagram** (119/150): `Our 156 saved reels: 30 Do it, 65 Watch it, 10 Skip it, 22 Locked. Sort yours free, in your browser. Nothing uploaded ↓` Link: `savesortai.com/#try`
- **TikTok** (79/80): `Sort your saved reels free: Do it, Watch it, Skip it, Locked. Nothing uploaded.` Website: `savesortai.com/#try`
- **YouTube channel description:** `SaveSort sorts your saved Instagram reels by topic and labels them Do it, Watch it, Skip it or Locked. Free, in your browser, nothing uploaded. Our sample report: 156 saves, 30 Do it, 65 Watch it, 10 Skip it, 22 Locked. Not affiliated with Instagram or Meta.` Link: `https://savesortai.com/#try`
- Pins on Instagram: `guess-useful` and `find-that-reel`.

## Site copy (owner approves; edit `site/src/`, run `node site/build.mjs`, commit `src/` and `public/` together)
1. `site/src/blog/comment-for-the-guide-reels.html` line 3: "We call these gated guides. In our sample report of 156 saved reels, 22 were gated: about one in seven." → "SaveSort labels these Locked. In our sample report of 156 saved reels, 22 were Locked: about one in seven."
2. `site/src/blog/how-to-organise-instagram-saved-posts.html` line 31: "…found 30 worth doing, 65 where the caption said almost nothing, 10 that looked like hype and 22 <a …>gated guides</a>." → "…found 30 Do it, 65 Watch it (the caption said almost nothing), 10 Skip it (hype) and 22 <a …>Locked</a>."
3. `site/src/pages/index.html` line 216: `Locked-guide detector ("comment GUIDE" reels)` → `Locked label for "comment GUIDE" and "DM me" reels`
4. `site/src/pages/index.html` line 123, steps: `… Some of your information › <b>Saved</b> › <b>All time</b>, <b>HTML</b>` → `… Some of your information › <b>Saved</b> › <b>Download to device</b> › <b>All time</b>, <b>HTML</b>`. Same in the getfile list: "Date range All time, format HTML" → "Choose Download to device, then date range All time, format HTML". (Check the current Instagram menu wording first.)
5. Optional: H1 "Here are the 30 worth doing." (and og/twitter description, og:image alt) → "Here are the 30 to Do." Words only, no styling change.

## Rule files (owner's call; bots may not edit these)
- `CHECKER.md` rule 1: list Do it / Watch it / Skip it / Locked, and add "hold any reel that uses an old label name".
- `AGENT.md`: the `react` verdicts, `quote` stamps and the "Part 2 … be careful" ask example still use old names.
- `content/sorty.md` catchphrases: "Straight to Be Careful" → "Straight to Skip it."; "Gated guide" → "That's Locked."; "Needs the video" → "Watch it."; "Worth doing" → "Do it."
- `accounts/hypecheck.md`: "worth doing / be careful" → "Do it / Skip it / Locked".
