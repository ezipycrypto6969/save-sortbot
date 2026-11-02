# Niche accounts: weekly content run (instructions for Claude)

SaveSort runs themed accounts alongside the main one: **gym**, **kitchen** and **hype check** (see `accounts.json`). Each is a real, useful page in its niche that leads people to SaveSort, the way the apps below grew. You write one account's week per run: the account id is in your task prompt.

## What we copied from apps that grew this way (research, Nov 2026)

- **Slideshows win.** Stronger, a gym-workout app, posted ~2.5 TikTok slideshows a day; 98% of its best posts were slideshows, 11 passed 1M views, and it reports 700k+ users. The shape: **slide 1 is a hook with tension** ("Skipping legs…", "Grandpa was right"), the middle slides build the story or give the value, and **the last slide releases the tension by showing the app**, softly, as part of the story. People then ask for the app in the comments. ([Shortimize](https://shortimize.com/blog/the-slideshow-strategy-that-generated-700000-users-in-275-days))
- **Many brand-owned accounts, each a separate door into the algorithm.** Cal AI ran 12+ of its own TikTok accounts posting carousels and short videos, each with **different formats and hooks but the same core message**, from a repeatable template pipeline. ([8x.social](https://www.8x.social/en/blog/cal-ai-multi-account))
- **Text-heavy slideshows can carry a whole network.** An astrology app posted ~3.7 slideshows a day per account across language-specific accounts. ([Shortimize](https://shortimize.com/blog/tiktok-multi-account-slideshow-strategy-making-50m-views-per-month))
- **When a hook wins, reuse it** with new content. Winners are formats to repeat, not one-offs.
- **Original or nothing.** Instagram stops recommending accounts that mostly repost other people's photos and carousels ([Digital Music News](https://www.digitalmusicnews.com/2026/05/01/instagram-debuts-more-original-content-protections-for-creators/)). Some apps scraped Pinterest images; we never do. Our slides are our own designs, Sorty, and real SaveSort screens.

## Our rules (on top of every rule in `AGENT.md` and `CHECKER.md`)

- **Honest identity.** Every account is openly SaveSort's (its name says so). Never pretend to be an independent fan, a real person, or a customer. No fake stories presented as true ("my client lost 20kg"). Sorty can tell a story; it's clearly a cartoon.
- **Useful first.** 80% of the value is the niche content itself (a workout, a recipe, an honest rating). SaveSort appears on the release slide or in the last third of a reel, tied to the saves problem: *you saved this, you'll lose it, here's how to find it and actually do it.*
- **No health, nutrition or medical claims** beyond what's widely established and checkable; no weight-loss promises, no calorie or macro numbers unless from an official source, no supplements. Gym: form cues and simple routines, "if it hurts, stop and ask a professional". Kitchen: real recipes with real quantities, common allergens named.
- **Money:** no income claims, no financial advice (same as the main account).
- **Different from the main account.** Never repost a main-account reel. Different hooks, different topics.
- Each post has `"account"`, `"format"` (`slideshow` or `reel`), `"style"`, `"hook_type"` and `"cta"`.

## The weekly mix (per account, 3 posts a day = 21)

Unless `marketing/brief.md` (the CMO's niche section) or `content/lessons.md` says otherwise:
- **14 slideshows** (2 a day) and **7 reels** (1 a day, the 19:30 slot).
- Inside slideshows, rotate the account's formats from its playbook (`accounts/<id>.md`). Never the same format twice in a row.
- 2 of the 14 slideshows are **re-runs of last week's best hook** (from `accounts/summary.md`) with new content, once there's data.

## Steps

1. `git pull`. Read this file, `accounts/<id>.md`, `accounts.json`, `accounts/status.json`, `accounts/summary.md`, `marketing/brief.md`, `content/lessons.md` and `AGENT.md` (rules). **If the account isn't `ready` in `accounts/status.json`, write nothing for it** and say so in your report (the owner hasn't connected it yet).
2. Count future `queued` items in `accounts/<id>/queue/`. Fill the next 7 days to 3 per day at 03:00, 07:00 and 19:30 Perth (`+08:00`). Replace any `held` items (read `hold_reasons`).
3. Write each item as `accounts/<id>/queue/<YYYY-MM-DD>-<1|2|3>-<slug>.json` with `"check": "pending"` (never set `check` yourself). Specs below.
4. **Creative review panel** (`team/REVIEW.md`) on every item before rendering. For slideshows, gate 2 (Switch) means "slide 2 makes you swipe again", and gate 3 (Product) means "SaveSort appears by the last slide, naturally".
5. Render:
   - slideshow: `NODE_PATH="$(npm root -g)" node engine/slides.js accounts/<id>/queue/<file>.json out/<id>/<item-id>`. Exit 3 = text overflows a slide: shorten it.
   - reel: `python3 engine/build.py accounts/<id>/queue/<file>.json out/<id>/<item-id> --stills` (same rules as `AGENT.md`, but the account's own topic).
   Look at every slide and every reel still. Fix and re-render anything cut off, crowded or hard to read.
6. `bash engine/publish_niche.sh` (adds your renders to the media-niche branch and keeps the other accounts' media that is already there).
7. Commit only `accounts/<id>/queue/` (and `models/custom.json` if changed). Pull with rebase, push to main. Finish by 2:30pm Perth so the claims checker sees them.
8. Report: the week's posts (day, time, format, first line), and anything the owner must do.

## Slideshow spec

```json
{
  "id": "2026-11-09-1-leg-day-saves",
  "account": "gym",
  "format": "slideshow",
  "post_at": "2026-11-09T03:00:00+08:00",
  "status": "queued",
  "check": "pending",
  "style": "story", "hook_type": "tension", "cta": "comment",
  "caption": "Hook line.\n\nOne or two short lines.\n\nSaveSort finds what you saved, free at savesortai.com\n\n#tag1 #tag2 #tag3",
  "tiktok_title": "Under 90 characters",
  "slides": [
    {"type": "hook", "text": "Skipped legs *again*?", "sub": "same.", "mascot": "sad"},
    {"type": "list", "heading": "The 4 I actually do", "items": ["Goblet squat|3 x 10", "Romanian deadlift|3 x 8", "Walking lunges|3 x 12 each leg", "Calf raises|3 x 15"]},
    {"type": "point", "n": "1", "title": "Slow on the way down", "body": "3 seconds lowering. Lighter weight, more work."},
    {"type": "screen", "shot": "topic-LIFE.png", "y": 0, "label": "found it in my saves", "text": "Every leg workout I'd ever saved, *in one place*."},
    {"type": "end", "text": "Save this.\n*Then actually do it.*", "pill": "savesortai.com"}
  ]
}
```

Slide types: `hook` (`text`, `sub`, `kicker`), `list` (`heading`, `items` "main|small", max 5), `point` (`n`, `title`, `body`, `stamp`, `stampColor` warn/go/gate), `stat` (`value`, `label`, `body`, `color`), `quote` (`quote`, `label`, `stamp`, `note`), `screen` (`shot` from `engine/screens/`, `y` scroll offset in capture px, `label`, `text`), `text` (`heading`, `text`), `end` (`text`, `sub`, `pill`). Any slide: `bg` (`ink`/`paper`/`cobalt`, cobalt = the account's main colour), `mascot` (a Sorty mood), `mascotPos` (`br`/`tr`/`bl`). `*word*` highlights in the account's accent colour.

Slideshow shape (also from Instagram's own carousel behaviour: it can re-show a carousel starting from slide 2 to people who skipped it, so slide 2 must work as a second cover):
1. **Cover:** the hook, 6 words or fewer, big, kept away from the edges.
2. **The stake:** why it matters, one sentence, readable on its own.
3. **One idea per slide** (3–7 word headline, max ~25 words).
4. **Recap slide:** the whole thing as one screenshot-able list (the slide people send to friends).
5. **Release + one ask:** SaveSort's part of the story, then save, comment or follow (one).

Good slideshows: **6–9 slides**, slide 1 under 6 words, one idea per slide, max ~25 words per slide, the hook's tension released on the last or second-last slide. Write as if for one tired person on their couch.

## Reel spec

Same as `AGENT.md`'s spec, plus `"account": "<id>"`, `"format": "reel"`, `"platforms": ["instagram", "tiktok"]`. Same voice, cold open, length (30–60 s) and Sorty rules, but the topic comes from the account's playbook.
