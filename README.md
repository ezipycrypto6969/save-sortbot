# SaveSort Instagram bot

Posts a reel to the SaveSort Instagram twice a day (12:20pm and 7:20pm Perth time), fully automatically.

- **Claude, every Sunday:** writes next week's 14 reels, renders them (voice, music, captions), checks each one, and adds them to `queue/`.
- **GitHub Actions, twice a day:** posts the next due reel through Instagram's official API and marks it posted.
- **GitHub Actions, every Monday:** renews the Instagram access token so it never expires.

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
- `poster/post.py` uploads the video with Instagram's resumable Reels upload and publishes it.
- `AGENT.md` is the weekly playbook Claude follows. `content/ideas.md` is the idea backlog.
