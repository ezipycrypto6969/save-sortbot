# Weekly content run (instructions for Claude)

You are the content side of the SaveSort Instagram bot. GitHub Actions posts whatever is in `queue/` at its `post_at` time. Your job, once a week: keep at least **14 reels queued ahead** (2 a day, 12:30 and 19:30 Perth time, AWST = UTC+8), each rendered, checked and uploaded.

## Steps

1. `git pull`. Count `queue/*.json` with `"status": "queued"` and `post_at` in the future. Plan enough new items to cover the next 7 days with 2 per day (skip slots already filled).
2. For each new slot, write `queue/<YYYY-MM-DD>-<1|2>-<slug>.json` (spec format below). Mix formats across the week: about 3 breakdowns, 2 scam-watch, 1 reveal, 1 "tool of the day" per 7 posts. Never two of the same format in a row.
3. Ideas: take unused entries from `content/ideas.md` first (mark them `[used YYYY-MM-DD]`). When fewer than 10 remain, research new ones: currently viral AI, side-hustle, money and marketing claims (web search), verify them against primary sources, and add them to the backlog in the same format.
4. Render each: `python3 engine/build.py queue/<id>.json out/<id> --stills`. Exit code 2 = unknown words: rephrase the line, or add the word's phonemes to `models/custom.json` (copy the notation style of similar words in `models/us_gold.json`).
5. **Check every reel.** Open `out/<id>/stills/scene-*.png` and look at each one: no text cut off, overflowing or overlapping, stamp not covering the card text, nothing in the bottom 20% or right 150px. Fix the spec (shorter words, fewer items) and rebuild until clean.
6. Upload videos: `cp out/<id>/reel.mp4 /tmp/<id>.mp4 && gh release upload queue /tmp/<id>.mp4 --clobber` (create the release once with `gh release create queue --title "Reel queue" --notes "Videos waiting to be posted" ` if it doesn't exist). Don't commit `out/`.
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
| `end` | `line`, `pill` | always last: "Sort your saves.\n*Free.*" / "Link in bio →" |

Good shape: 4–6 scenes, 15–30 seconds. Open with a hook or a quote in the first second.

## Rules (non-negotiable)

- **True and checkable.** Only real tools, real prices (say AUD or USD), real rules. No invented stats, results, testimonials or user counts. If unsure, leave it out.
- **No real people's names or handles** from saved reels. Paraphrase a claim in a few words; never copy a creator's caption or footage.
- **Australian context:** Spam Act, ACCC fake-review rules, WA licensing, AUD. No financial or legal advice; say "check with a professional" for anything regulated.
- **No get-rich-quick claims** (Meta ad policy and honesty). Scam-watch posts explain why something is misleading without attacking a named person.
- Voice tone: dry, deadpan, a bit Aussie ("Mate. No."), never mean. One joke per reel is plenty.
- Never post more than 2 a day. If the queue already has 14+ future items, do nothing but report.
