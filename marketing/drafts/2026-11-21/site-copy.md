# Bios and site copy (D6 #54/#55/#57/#59, 21 Nov 2026). Drafts only: the owner decides.

## Bios (owner to-do #2)
- **Instagram** (105/150): `What's your number? Ours: 156 saved reels, 30 Do it. Sort yours free, in your browser. Nothing uploaded ↓` Link: `savesortai.com/#try`
- **TikTok** (73/80). TikTok only allows a bio link with a business account or 1,000 followers, so the site name goes in the text: `Sort your Instagram saved reels free at savesortai.com. Nothing uploaded.`
- **YouTube:** last week's description (`drafts/2026-11-14/site-copy.md`) is unchanged.
- **Pins:** Sorty Ep 1 and Ep 2 on Instagram and TikTok (best watch time; Ep 1 is the only reel ever shared).
- **Disclosure line** for reels with a made-up count pointed at the viewer ("You saved 500"): `Sorty's voice is AI. Our sample report (156 saves) is real.`

## Site copy, before → after (owner to-do #3)
Owner approves; then edit `site/src/`, run `node site/build.mjs`, commit `src/` and `public/` together (CLAUDE.md website rules). Line numbers are `site/src/pages/index.html` as of 21 Nov.

1. Line 33 H1 `30 worth doing.` → `30 to do.` Same in line 1 ogDescription: `Here are the 30 worth doing.` → `Here are the 30 to do.`
2. Line 123 steps path: `… <b>Saved</b> › <b>All time</b>, <b>HTML</b>` → `… <b>Saved</b> › <b>Download to device</b> › <b>All time</b>, <b>HTML</b>`
3. Lines 141–145, the "No file yet?" list, written so a first-timer can follow it:
   `<li>Tap <b>Get my file from Instagram</b>, or in the app go to Settings › Accounts Center › Your information and permissions</li><li><b>Download your information</b> › Some of your information › tick only <b>Saved</b> (under Your Instagram activity)</li><li>Choose <b>Download to device</b>, date range <b>All time</b>, format <b>HTML</b>, then create the file</li><li>Instagram emails you when the zip is ready. Come back and drop it anywhere on this page</li>`
4. FAQ step 4 and the matching JSON-LD answer: `Pick date range All time and format HTML, then create the file.` → `Choose Download to device, pick date range All time and format HTML, then create the file.`
5. Line 216: `Locked-guide detector ("comment GUIDE" reels)` → `Locked label for "comment GUIDE" and "DM me" reels`
6. Line 183 upsell button (it only scrolls to the pricing section): `Unlock breakdowns for A$1.99 a week` → `See Pro: A$1.99 a week`
7. `site/public/app.js` line 28 error message: `Try refreshing, or email us.` → `Try refreshing. Still stuck? Our email is on the About page.`
8. Blog posts (open since 14 Nov): `comment-for-the-guide-reels.html` line 3 `We call these gated guides … 22 were gated` → `SaveSort labels these Locked … 22 were Locked`. `how-to-organise-instagram-saved-posts.html` line 31 → `30 Do it, 65 Watch it (the caption said almost nothing), 10 Skip it (hype) and 22 <a …>Locked</a>`.

## Rule files with old label names (owner to-do #3; bots may not edit these)
- `CHECKER.md` line 11: "worth doing / needs the video / hype / gated guide" → "Do it / Watch it / Skip it / Locked".
- `content/sorty.md` lines 40–43 and 52: stamp lines → "Cap. Straight to Skip it." / "That's Locked. That's a DM trap." / "Okay. This one's a Do it. Rare."; numbers line → "30 Do it, 65 Watch it, 10 Skip it, 22 Locked".
- `accounts/hypecheck.md` lines 4 and 21: "worth doing, needs more info, or be careful" → "Do it, Watch it or Skip it"; "Be careful filter" → "Skip it filter".
