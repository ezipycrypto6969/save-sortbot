# Creative review panel (every reel, before rendering)

A real marketing team never ships a first draft. After the writer has written the week's queue specs and **before** rendering, the panel reviews every new reel. The panel is a separate subagent that did not write the reels.

## Who sits on the panel

From `team/ROSTER.md`: hook writer (#23), scriptwriter (#24), comedy writer (#25), Sorty's character director (#30), head of retention (#31) and the retention team (#32–#37, #40), Instagram (#42), YouTube (#44) and TikTok (#45) specialists, CTA strategist (#53), brand voice guardian (#84), product-truth checker (#86), demo producer (#92) and the persona tester (#20).

## The 8 gates (score each 1–10)

| Gate | Passes when |
|---|---|
| 1. Stop | Scene 1 is a clean cold open, max 5 words on screen, aimed at the viewer; a stranger would stop scrolling. |
| 2. Switch | Scene 2 looks clearly different and arrives by ~1.3 s. |
| 3. Product | SaveSort or "my saved reels" appears by scene 3, ideally real `screen` footage. |
| 4. Payoff | There's a real, useful payoff, set up early and delivered late (`payoff`). |
| 5. Fun | One or two jokes that actually land; Sorty in character per `content/sorty.md`. |
| 6. Ask | One CTA, with a reason the viewer actually gets. |
| 7. Fit | Works for the general public, on all three platforms; `yt_title` is searchable. |
| 8. Brief | Matches its slot in `marketing/brief.md` and the rules in `content/lessons.md`. |

Truth and policy are **not** scored here: the claims checker owns them. But the panel flags anything that looks false or risky.

## Before the panel: hooks and captions (`team/tools/`)

1. **Three hooks per post.** The hook writer drafts 3 opening lines for every reel and slideshow, each from a different formula in `team/tools/hooks.json` (adapted to the saves problem or the account's niche; read each formula's `trap` and avoid it). Score them together: `python3 team/tools/hookscore.py hooks.txt`. Use the top one; **nothing under 60 ships** (rewrite and re-score). Record `"hook_formula": "<name>"` and `"hook_score": <n>` in the spec.
2. **Caption lint:** `python3 team/tools/caption.py <caption file> --keywords "<2-3 search terms>"`. Fix whatever it flags, especially the first 125 characters (what shows before "… more").
3. **Reels only:** time the `vo` lines with `python3 team/tools/beats.py <script file> --target <seconds>` and fix any beat that runs long.

The hook score is a floor, not a forecast: it catches slow, vague or preamble openings but can't pick a hit. The analyst compares `hook_formula` against real watch time.

## How the writer runs it

1. Spawn one subagent (not in the background) with this file, `team/ROSTER.md`, `AGENT.md`, `content/lessons.md`, `marketing/brief.md` and the list of new queue files. Tell it: you did not write these; review each reel as the panel; read-only.
2. It returns, per reel: the 8 scores, the average, and for any gate under 8 one specific fix (scene number + new wording).
3. **The bar: every gate 7 or more and an average of 8 or more.** Fix every reel below the bar, then send only the changed reels back for one more review. A reel that fails a second time is replaced with a different idea from the brief or `content/ideas.md`, not patched again.
4. Add `"review": {"avg": <n>, "rounds": <1|2>}` to each reel's spec, then render as usual.

If subagents aren't available, the writer runs the panel itself, strictly, scoring as an outsider would.
