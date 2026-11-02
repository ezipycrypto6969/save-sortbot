# SaveSort Instagram bot

Posts a reel to the SaveSort Instagram twice a day (12:20pm and 7:20pm Perth time), fully automatically.

- **Claude, every Sunday:** writes next week's 14 reels, renders them (voice, music, captions), checks each one, and adds them to `queue/`.
- **GitHub Actions, twice a day:** posts the next due reel through Instagram's official API and marks it posted.
- **GitHub Actions, every Monday:** renews the Instagram access token so it never expires.

## The marketing team

SaveSort has a 100-specialist AI marketing department in `team/` (10 departments: strategy, research, creative, retention, platforms, copy, growth, analytics, quality, product marketing). See `team/ROSTER.md`.

| When | Who | What |
| --- | --- | --- |
| Sat 4:13pm | Head of insights (`ANALYST.md`) | Studies the week's stats, writes `content/lessons.md` |
| Sat 6:47pm | CMO + 9 department leads (`team/CMO.md`) | Picks the bottleneck and the campaign, writes `marketing/brief.md`, your to-do list in `marketing/owner-actions.md`, and drafts in `marketing/drafts/` |
| Sun 9:38am | Content writer (`AGENT.md`) + creative review panel (`team/REVIEW.md`) | Writes 21 reels from the brief; every reel must pass the panel before it's rendered |
| Sun 10:41am–12:53pm | Niche writers (`accounts/NICHE.md`) | One per account (gym, kitchen, hype check): 14 slideshows + 7 reels each a week |
| Sun 3:07pm | Fact-checker (`CHECKER.md`) | Verifies every claim on every account; holds anything untrue |

The team only drafts and recommends outside the reels: it never posts elsewhere, messages anyone, changes the website or spends money without you.

## Niche accounts

Besides the main account, the bot runs **SaveSort Gym**, **SaveSort Kitchen** and **SaveSort Hype Check** on Instagram and TikTok, 3 posts a day each (mostly slideshows, one reel a day), posted through Upload-Post in the same three runs as the main account. Setup and looks are in `accounts.json`, each account's plan in `accounts/<id>.md`, its queue in `accounts/<id>/queue/`, and stats in `accounts/summary.md`.

An account switches on by itself once its Instagram and/or TikTok is connected to its Upload-Post profile (`savesort-gym`, `savesort-kitchen`, `savesort-hypecheck`); `accounts/status.json` shows what's connected. To stop one account, delete its entry's `upload_post_profile` in `accounts.json` (or disconnect it in Upload-Post). `PAUSED` stops everything.

## Controls

| You want to | Do this |
| --- | --- |
| Stop all posting | Repo → Settings → Secrets and variables → Actions → **Variables** → add `PAUSED` = `true` (delete it to resume) |
| Test without posting | Add variable `DRY_RUN` = `true` |
| Cancel one post | Delete its file in `queue/` |
| Change a caption | Edit `caption` in its `queue/*.json` file |
| Post right now | Actions → **Post next reel** → **Run workflow** (posts the next item that's due) |
| Change posting times | Edit the two `cron` lines in `.github/workflows/post.yml` (times are UTC; Perth = UTC+8) and the `post_at` times |

If a run fails, GitHub emails you.

## One-time setup

1. **Instagram:** Settings → Account type and tools → Switch to professional account (Creator or Business).
2. **Meta app:** developers.facebook.com → My Apps → Create App → the Instagram use case → *API setup with Instagram login* → Add account → Generate token. Copy the **access token** and **Instagram user ID**.
3. **Secrets** (repo → Settings → Secrets and variables → Actions → New repository secret):
   - `IG_USER_ID`: the Instagram user ID
   - `IG_ACCESS_TOKEN`: the access token
   - `GH_PAT`: a GitHub fine-grained token for this repo with **Secrets: Read and write** (github.com → Settings → Developer settings → Fine-grained tokens). Used only to save the renewed Instagram token.
4. **First test:** add variable `DRY_RUN` = `true`, run **Post next reel** manually, check the log, then delete `DRY_RUN`.

## How it's built

- `engine/` turns a JSON script into a reel: `stage.html` (animated scenes, rendered frame by frame with Playwright), `tts.py` (Kokoro-82M voice, Apache-2.0), `g2p.py` (pronunciation via Misaki's dictionaries, Apache-2.0), `music.py` (original synthesised music), `build.py` (puts it together).
- Videos waiting to post live on the `media` branch (replaced weekly, so the repo stays small).
- `poster/post.py` uploads the video with Instagram's resumable Reels upload and publishes it.
- `AGENT.md` is the weekly playbook Claude follows. `content/ideas.md` is the idea backlog.
