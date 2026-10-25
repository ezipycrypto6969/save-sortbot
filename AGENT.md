# Weekly content run (instructions for Claude)

You are the content side of the SaveSort Instagram bot. GitHub Actions posts whatever is in `queue/` at its `post_at` time. Your job, once a week: keep at least **14 reels queued ahead** (2 a day, 12:30 and 19:30 Perth time, AWST = UTC+8), each rendered, checked and uploaded.

## Steps

1. `git pull`. Count `queue/*.json` with `"status": "queued"` and `post_at` in the future. Plan enough new items to cover the next 7 days with 2 per day (skip slots already filled).
2. For each new slot, write `queue/<YYYY-MM-DD>-<1|2>-<slug>.json` (spec format below). Mix formats across the week: about 3 breakdowns, 2 scam-watch, 1 reveal, 1 "tool of the day" per 7 posts. Never two of the same format in a row.
3. Ideas: take unused entries from `content/ideas.md` first (mark them `[used YYYY-MM-DD]`). When fewer than 10 remain, research new ones: currently viral AI, side-hustle, money and marketing claims (web search), verify them against primary sources, and add them to the backlog in the same format.
4. Render each: `python3 engine/build.py queue/<id>.json out/<id> --stills`. Exit code 2 = unknown words: rephrase the line, or add the word's phonemes to `models/custom.json` (copy the notation style of similar words in `models/us_gold.json`).
5. **Check every reel.** Open `out/<id>/stills/scene-*.png` and look at each one: no text cut off, overflowing or overlapping, stamp not covering the card text, nothing in the bottom 20% or right 150px. Fix the spec (shorter words, fewer items) and rebuild until clean.
6. Upload videos: `bash engine/publish_media.sh` rebuilds the `media` branch with one `<id>.mp4` per still-queued item (from `out/<id>/reel.mp4`) and force-pushes it. Render any queued item whose video is missing first. Don't commit `out/` to main.
7. Commit the queue JSON files, `content/ideas.md` and any `models/custom.json` changes, then push.
8. Message the owner: a short list of next week's posts (date, time, title) and a reminder that they can delete a queue file to cancel a post or set the repo variable `PAUSED` to `true` to stop all posting.

## Spec format

```json
{
  "id": "2026-10-27-2-ai-receptionist",
  "post_at": "2026-10-27T19:30:00+08:00",
  "format": "breakdown",
  "status": "queued",
  "voice": "af_heart",
  "caption": "Hook line.\n\nThe value, in 3–6 short lines or a numbered list.\n\nSorted by SaveSort. Sort your saves free, link in bio.\n\n#tag1 #tag2 #tag3",
  "scenes": [ { "type": "...", "vo": "Spoken line.", ...fields } ]
}
```

Scene types (each scene stretches to fit its `vo` line; keep each line under ~12 words):

| type | fields | use |
| --- | --- | --- |
| `hook` | `lines` (2 short lines, last one gets `*marker*`), optional `slow`, `grey` | scrolling saved-reels opener |
| `quote` | `quote`, `label` (e.g. "SAVED REEL SAYS"), `note`, optional `heading`, `stamp` ("BE CAREFUL" / "GATED GUIDE"), `stampColor` ("warn"/"gate") | the claim from a reel |
| `title` | `text` (use `\n` and `*marker*`), `bg` cobalt/paper/ink | one big statement |
| `steps` | `heading`, `items` (3–4, under 6 words each) | how-to |
| `stat` | `value` (number), `label`, `color` go/warn, optional `prefix`/`suffix` | one number |
| `checks` | `heading`, `label`, `items` (4), `lastWarn` true | checklist |
| `count` | `n` (3, 2, 1), `label` | countdown lists ("3 saved reels that lied to me") |
| `end` | `line`, `pill` | always last: "Sort your saves.\n*Free.*" / "Link in bio →" |

| `talk` | `text` (speech bubble, `\n` and `*marker*`), `mood`, optional `wave` | Sorty speaks to camera |
| `react` | `quote`, `label`, `mood`, `verdict` ("BE CAREFUL" / "WORTH DOING" / "GATED GUIDE" / "NO DETAILS"), `verdictColor` warn/go/gate | Sorty reacts to a saved reel |

Any scene can take `"payoff": true` to mark where the open loop is answered.

**Sorty** is the brand mascot: a blue bookmark-ribbon character who lip-syncs to the voiceover. Moods: `happy`, `shocked`, `suspicious`, `smug`, `sad`. He appears automatically in `talk` and `react` scenes; add him to other scenes with `"mascot": {"pos": "tr", "mood": "happy"}` (`tr` = top-right for stat, count and end scenes; `bl` = bottom-left only on `hook` scenes). Use him in at least half the reels: open with a `talk` scene, react to claims with `react` scenes. He's dry, a bit cheeky, never mean.

Top-level `fx` (optional): `{"hook": "#1 IS ILLEGAL IN WA"}` shows an open-loop banner at the top until the `payoff` scene (or the end card). Word-by-word captions, the progress bar, cut flashes and a slow push-in are on by default (`"captions": false`, `"progress": false`, `"flash": false` turn them off). Captions show the `vo` text, so write numbers as digits in `vo` ("156", not "a hundred and fifty six").

Good shape: 4–6 scenes, 15–30 seconds. Open with a hook or a quote in the first second.

## Hooks and attention (use in every reel)

- **First second sells it.** Frame one is the hook: a callout ("Stop scrolling if you have 100+ saves"), a bold claim ("Your saved tab is lying to you"), a countdown ("3 saved reels that lied to me"), a POV, a "don't do X", or a guessing game ("Guess how many were worth doing").
- **Open a loop and close it late.** Promise something specific in the `fx.hook` banner or the first line ("Number one is illegal") and pay it off in the second-last scene, marked `payoff`.
- **Specific real numbers** beat vague words. Use only true ones.
- **Ask for one action:** a comment ("Lock in your guess. Comment it.") or the link in bio. Never both in one reel.
- **Rotate hook types** across the week; never the same hook style twice in a row.

## Rules (non-negotiable)

- **True and checkable.** Only real tools, real prices (say AUD or USD), real rules. No invented stats, results, testimonials or user counts. If unsure, leave it out.
- **No real people's names or handles** from saved reels. Paraphrase a claim in a few words; never copy a creator's caption or footage.
- **Australian context:** Spam Act, ACCC fake-review rules, WA licensing, AUD. No financial or legal advice; say "check with a professional" for anything regulated.
- **No get-rich-quick claims** (Meta ad policy and honesty). Scam-watch posts explain why something is misleading without attacking a named person.
- Voice tone: dry, deadpan, a bit Aussie ("Mate. No."), never mean. One joke per reel is plenty.
- Never post more than 2 a day. If the queue already has 14+ future items, do nothing but report.
