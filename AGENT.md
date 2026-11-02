# Weekly content run (instructions for Claude)

You are the content side of the SaveSort Instagram bot. GitHub Actions posts whatever is in `queue/` at its `post_at` time. Each reel also goes to YouTube Shorts (`poster/post_youtube.py`) and TikTok via Upload-Post (`poster/post_tiktok.py`) in the same run, once their secrets exist. TikTok uses the `caption` (max 2,200 characters). Your job, once a week: keep at least **21 reels queued ahead** (3 a day at 03:00, 07:00 and 19:30 Perth time, AWST = UTC+8: UK evening, US evening, Australia/Asia evening), each rendered, checked and uploaded.

## Steps

1. `git pull`. Read `content/lessons.md`, `stats/summary.md`, `content/styles.md` and `marketing/brief.md` first. **Follow the "Next week's instructions for the writer" in `content/lessons.md` exactly** (mix, hooks, length and the rest): a separate analyst writes them every Saturday from the real stats. **Then follow the marketing team's brief** (`marketing/brief.md`, written Saturday evening by the CMO in `team/CMO.md`): use its slot plan, campaign and team rules for each slot, unless they clash with `content/lessons.md` or the owner rules here, which win. Where both say nothing, use **Marketing test and learn** (below). Count `queue/*.json` with `"status": "queued"` and `post_at` in the future. Plan enough new items to cover the next 7 days with 3 per day (skip slots already filled). A reel with `"status": "held"` was rejected by the claims checker: read its `hold_reasons`, and fill its slot with a new reel that avoids those problems.
2. For each new slot, write `queue/<YYYY-MM-DD>-<1|2|3>-<slug>.json` (1 = 03:00, 2 = 07:00, 3 = 19:30) (spec format below). Every new item gets `"check": "pending"`: the posters skip it until the separate claims checker (see `CHECKER.md`) sets it to `"passed"`. Never set `check` yourself. Mix formats across the week: about 3 breakdowns, 2 scam-watch, 1 reveal, 1 "tool of the day" per 7 posts. Never two of the same format in a row.
3. Ideas: take unused entries from `content/ideas.md` first (mark them `[used YYYY-MM-DD]`). When fewer than 10 remain, research new ones: currently viral AI, side-hustle, money and marketing claims (web search), verify them against primary sources, and add them to the backlog in the same format.
3b. **Creative review panel** (`team/REVIEW.md`): before rendering anything, have the panel review every new reel. Fix or replace each one until it clears the bar (every gate 7+, average 8+). No reel is rendered without passing.
4. Render each: `python3 engine/build.py queue/<id>.json out/<id> --stills`. Exit code 2 = unknown words: rephrase the line, or add the word's phonemes to `models/custom.json` (copy the notation style of similar words in `models/us_gold.json`).
5. **Check every reel.** Open `out/<id>/stills/scene-*.png` and look at each one: no text cut off, overflowing or overlapping, stamp not covering the card text, nothing in the bottom 20% or right 150px. Fix the spec (shorter words, fewer items) and rebuild until clean.
6. Upload videos: `bash engine/publish_media.sh` rebuilds the `media` branch with one `<id>.mp4` per still-queued item (from `out/<id>/reel.mp4`) and force-pushes it. Render any queued item whose video is missing first. Don't commit `out/` to main.
7. Give every new item a `yt_title` (punchy, under 70 characters, no emoji). Commit the queue JSON files, `content/ideas.md` and any `models/custom.json` changes, then push.
8. Message the owner: a short list of next week's posts (date, time, title, panel score) and a reminder that they can delete a queue file to cancel a post or set the repo variable `PAUSED` to `true` to stop all posting.

## Spec format

```json
{
  "id": "2026-10-27-2-ai-receptionist",
  "post_at": "2026-10-27T19:30:00+08:00",
  "format": "breakdown",
  "status": "queued",
  "check": "pending",
  "voice": "am_onyx*0.55+am_puck*0.45",
  "pitch": 1.5,
  "yt_title": "Optional YouTube title, under 70 characters (otherwise the caption's first line is used)",
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

Good shape: **30–60 seconds, never under 30** (owner's rule), 8–11 scenes. Model every reel on `content/ads_v5.py`: a hook, real SaveSort footage (`screen` scenes using the captures in `engine/screens/`, e.g. tap a filter chip or a topic), then genuinely useful, checkable info (a countdown or Sorty rating real claims), one or two dry jokes, and a CTA end card. Open with a hook or a quote in the first second.

| `screen` | `label`, `segs` [{`shot`, `from`, `to`, `t0`, `t1`}], optional `taps`, `highlights`, `zoom`, `drop`, `mascot` {pos: "pl"} | real SaveSort footage in a phone (see helpers in `content/ads_v5.py`) |
| `path` | `label`, `screens` [{`title`, `crumb`, `rows`, `pick`, `ticks`, `on`, `btn`}] | walk through a settings menu |

## Per-platform versions (automatic)

The same video goes to all three, but `poster/platform_copy.py` tailors the text for each, because each platform rewards different things:

- **Instagram** ranks Reels for new viewers mostly on **sends** (people DMing it to a friend), then watch time and likes per reach. The caption gets one "Send this to the friend with 500 saved reels 📩" line unless the reel already asks for a comment.
- **YouTube Shorts** lives on "viewed vs swiped away" and search. The description opens with a plain searchable line and the site link, then the caption, then `#Shorts` plus 3 tags. Write `yt_title` as a searchable phrase someone would type (under 70 characters).
- **TikTok** search reads captions, spoken words and on-screen text. The caption keeps the hook, adds a keyword line ("How to organise your Instagram saved reels, free at savesortai.com"), asks a question if there isn't one, and uses 5 hashtags. Say "savesortai.com" rather than "link in bio" in TikTok text.

To hand-write a platform's text instead, add `ig_caption`, `yt_description` or `tiktok_caption` to the queue item. Keep the first second strong on every platform: it decides the swipe on all three.

### Instagram trial reels (testing openings)

Optional fields on a queue item:
- `"ig_trial": true` posts it on Instagram as a **trial reel**: shown to non-followers first. With the default `"ig_trial_graduation": "SS_PERFORMANCE"`, Meta shares it with followers automatically if it does well (`"MANUAL"` leaves that to the owner in the app). If the account can't use trial reels, it posts normally.
- `"platforms": ["instagram"]` limits a reel to certain platforms (default: all three).

Use them to test openings: once a day at most, take a reel you've written and add a second version with a **different first scene only** (new hook line and on-screen text, same rest), queued at the same time with `"ig_trial": true` and `"platforms": ["instagram"]`, id ending `-b`. The weekly analysis compares the A and B openings and keeps the better style.

## Hooks and attention (use in every reel)

- **First second sells it.** Frame one is the hook: a callout ("Stop scrolling if you have 100+ saves"), a bold claim ("Your saved tab is lying to you"), a countdown ("3 saved reels that lied to me"), a POV, a "don't do X", or a guessing game ("Guess how many were worth doing").
- **Open a loop and close it late.** Promise something specific in the `fx.hook` banner or the first line ("Number one is illegal") and pay it off in the second-last scene, marked `payoff`.
- **Specific real numbers** beat vague words. Use only true ones.
- **Ask for one action:** a comment ("Lock in your guess. Comment it.") or the link in bio. Never both in one reel.
- **Give the ask a reason (owner rule, 1 Nov 2026).** Never a bare "like, comment, follow". The second-last scene's `vo` says the ask *and* why the viewer would want to do it, and the end card and the caption's last line repeat it. Tag every reel `"cta": "comment" | "follow" | "save" | "link"` and rotate them across the week. Reasons that work:
  - **Comment, to win or to argue:** a guess with a real reveal ("Comment your guess. I'll pin whoever's closest."), a pick-a-side ("Recipes or side hustles: which took over your saves? Wrong answers only."), a count flex ("Comment your saved count. Bet nobody's under 100."), or a mild hot take the viewer will want to argue with ("Saving a reel is procrastinating with extra steps. Change my mind."). Hot takes must be an honest opinion, playful, never at anyone's expense; no false claims, made-up outrage or fake drama (the claims checker holds them).
  - **Follow, for something specific that's coming:** "Part 2 tomorrow: the 10 saves SaveSort flagged be careful. Follow so you don't miss it." Only promise a part 2 if it is already queued within 48 hours, and name what it is. Or the series promise: "I check one viral saved reel every day so you don't have to."
  - **Save, because they'll need it later:** "Save this. You'll want the steps when you export your saves." Best on walkthroughs and how-tos.
  - **Like, as a vote:** "Like if your saved tab is also a graveyard." Use rarely.
  - **Link in bio, for the payoff:** "Want your own number? Sort your saves free, link in bio."
- **Owner rule (1 Nov 2026, evening): the reason must be something the viewer gets.** "Comment your count, I'll pin the biggest" gives them nothing, so don't use pin/flex/bragging asks. Default to the link ask with a built-in payoff: "Find out how many of yours are actually worth it. Free." / "See what's hiding in yours." / "What's your number? Find out free." Use a comment ask only when commenting gets the viewer something real (an answer they want, a part 2 that's already queued).
- **Rotate hook types** across the week; never the same hook style twice in a row.

## Marketing test and learn (every week)

The goal is better marketing: more views, follows and sign-ups for SaveSort among the general public. Each week's 21 reels are a mix:

- **About 14 `base` reels**: the owner's main format (see Owner feedback and the model reels in `content/styles.md`).
- **About 4 `funny-ad` reels**: funny product ads like "RIP my saved tab".
- **3 experiment reels** (`exp-<name>`): new marketing styles. Try 1 to 3 styles a week, pick from the ideas in `content/styles.md` or invent one, and record each in its Experiments table.

Give every new reel `"style"` (one of the names above) and `"hook_type"` (e.g. `countdown`, `pov`, `bold-claim`, `question`, `guess`).

**Judging** is done by the analyst (`ANALYST.md`) every Saturday, using these rules. Only if `content/lessons.md` has no analysis yet, judge yourself (from `stats/summary.md`; only reels marked ✓, at least 3 days old):
- Compare an experiment's reels with the `base` median views and median engagement rate over the same period.
- If an experiment beats the `base` median on views or engagement rate on at least 2 of its reels, run it again next week with up to 6 slots (taken from `base`). If it wins two weeks in a row, move it to Regular styles with its slot count.
- If it loses on both measures, retire it and write why in Retired styles. Don't retry a retired style unless it's changed in a clear way.
- Also cut a regular style's slots by 1 to 2 if it's been the worst style two weeks in a row (but keep at least 8 `base` reels a week).
- Note which `hook_type`s do best and use more of those.
- Early weeks with few views: don't over-react. With fewer than 3 judged reels in a style, leave it running.

**In the owner message**, add a short "What worked" section: the top 3 and bottom 3 reels last week (title, views), each style's result, and what you're changing this week.

## Product-first format (owner rule, 31 Oct 2026)

On YouTube the two best reels by far were `2026-10-28-2-full-tutorial` (35 s average watch, 75% viewed) and `2026-10-26-2-reveal-156` (122% viewed, people rewatched it). Both lead with **the viewer's saved-reels problem** ("156 saves, 0 ever opened"), then **show SaveSort solving it on screen** (drop the zip, sorted by topic, tap Worth doing / Be careful / Gated guides), then a clear call to action. Make most `base` reels this way, modelled on those two and on `2026-10-31-3-junk-drawer-fix`, `2026-11-01-1-156-zero`, `2026-11-01-2-find-that-reel`, `2026-11-01-3-later-never-comes` and `2026-11-02-1-to-do-list`. Tips taken from saved reels are a minority, and only as proof of what SaveSort found. Use the real report numbers: 156 saves, 30 worth doing, 65 need the video, 10 be careful, 22 gated guides. **Make the problem feel big by pointing large numbers at the viewer, not by inventing yours** (owner, 31 Oct): "Got 500 saved reels?", "If your saved tab is past 300, you need this.", "156 was bad. Some of you are sitting on 1,000." Never claim the owner had more than 156, and never show a report number that differs from the real screenshots.

## Hooks: the first 2 seconds (owner rule, 30 Oct 2026)

The first reels kept people for only 1.3–6.4 seconds of 31–48 (5–13%). They were leaving in the opening, so every reel now starts with a **cold open**:

1. **Scene 1 is a `title` with `"clean": true`** (no banner, no subtitles, no mascot), on a solid background that differs from scene 2. Use `"bg": "paper"` (white) most often, since it stands out in a dark feed. Max 5 words on screen, `vo` max 8 words, about 1–1.5 seconds.
2. **It must be one of:** a bold claim about the viewer ("You're using AI wrong."), a question they want answered ("Can you spot a fake customer?"), a warning ("This AI trick could get you sued."), a confession with a number ("10 of my saves lied to me."), or a stakes line ("No reviews? No sales."). Never generic advice or a topic label ("If you sell anything, you need proof").
3. **Scene 2 changes the picture by about 1.3 seconds**: a different background and new words (a second `title`, a `talk`, or a `quote`). Never two scenes in a row that look the same.
4. **Don't open on the grey saved-reels grid** (`hook` scenes) anymore. Use `hook` later in the reel if at all.
5. **SaveSort or "my saved reels" appears by scene 3** (within about 6 seconds).
6. Keep the `fx.hook` banner: it's hidden during the clean first scene and appears from scene 2.
7. Set `"hook_type"` to `bold-claim`, `question`, `warning`, `confession` or `stakes` so the analyst can compare them.

Models: `2026-10-30-2-ai-tutor`, `2026-11-01-1-ai-actor-reviews`, `2026-10-31-1-saves-that-lied`.

**Hook formulas:** draft 3 cold-open options per reel from `team/tools/hooks.json` and score them with `team/tools/hookscore.py` (see `team/REVIEW.md`); use the best, 60+ only, and record `hook_formula` and `hook_score`.

**Crazy hooks:** run `python3 content/hookgen.py --n 40` before writing: it generates over-the-top (but true) cold-open hooks (funeral, warning, callout, challenge, absurd) and skips any used in the last 4 weeks. Use `--json` to get ready-made `title` scenes. Score the candidates with `team/tools/hookscore.py` like any other hook, pick the best for each reel, tweak scene 2 so it flows, and set `"hook_type": "crazy-<family>"` and `"hook_source": "content/hookgen.py"`. `content/hooks.md` is the hand-written bank. Use it for `exp-crazy-hook` reels and whenever a cold open needs more punch; mark used hooks there.

## Owner feedback (29 Oct 2026, apply to every new reel)

- **Balance the saves story and the useful content.** Don't spend most of the reel on random tips from reels and only reveal at the end that they came from saved reels. Say early (first 2–3 scenes) that these came from *your saved reels* and that SaveSort found them, then give the useful bit, then the payoff. Don't swing the other way into a pure product ad either.
- **Always connect to the saves problem**: you saved it, forgot it, never did it. Show how SaveSort helps with that, not just the tip itself.
- **Countdowns and ratings need context.** Before a #3/#2/#1 or a verdict, say where they came from ("I put my saves into SaveSort. 3 worth doing on proof.").
- **Market to the general public, not AI or tech nerds.** No developer APIs, prompt-engineering tricks, gadget preorders or jargon as the main topic. Someone who could build SaveSort themselves isn't the customer.
- **Models of the right balance:** `2026-11-01-3-needs-the-video` ("Got 100+ saved reels? Most of them say nothing") and `2026-10-30-2-comment-guide` ("What comment GUIDE actually gets you"). Read both before writing.
- Reels with `"status": "scrapped"` were rejected by the owner; read their `scrap_reason` and don't repeat those mistakes. Never re-queue them.

## Rules (non-negotiable)

- **True and checkable.** Only real tools, real prices (say AUD or USD), real rules. No invented stats, results, testimonials or user counts. If unsure, leave it out.
- **No real people's names or handles** from saved reels. Paraphrase a claim in a few words; never copy a creator's caption or footage.
- **For a global audience.** No country- or state-specific laws, agencies or prices (no "in WA", no Australian acts or government sites). Prices in USD. No financial or legal advice; for anything regulated say "check the rules where you live".
- **Only promise what SaveSort does today:** the free sorter sorts saves by topic and flags worth doing / needs the video / hype / gated guides, in the browser, nothing uploaded. Step-by-step breakdowns and monthly refresh are Pro and not launched yet; don't promise them.
- **Voice, sound and pace:** `"voice": "am_onyx*0.55+am_puck*0.45"`, `"pitch": 1.5` (Sorty's voice: deep but a bit squeaky), `"music": "sfx"` (no beat, effects only) and `"speed": 1.22` on every reel. Keep lines short so cuts land every 1.5–3 seconds.
- **Every reel ends with a clear call to action** in the `end` scene's `vo`, e.g. "Tap the link in bio and sort yours now."
- **Talk about the product and the payoff:** how it works (download Instagram data, tick Saved, drop the zip in), and what it does for the viewer (saves time, saves money on hype, feels lighter and more in control). Aim for at least 2 product-focused reels a week.
- **No get-rich-quick claims** (Meta ad policy and honesty). Scam-watch posts explain why something is misleading without attacking a named person.
- Voice tone: dry, deadpan, a bit Aussie ("Mate. No."), never mean. One joke per reel is plenty.
- Never post more than 3 a day (plus at most 1 Instagram-only trial reel). If the queue already has 21+ future items, do nothing but report.
