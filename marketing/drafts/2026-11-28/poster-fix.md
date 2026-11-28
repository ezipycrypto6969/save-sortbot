# Poster and stats fix (owner to-do #5) — for approval, not applied

Drafted by the marketing council (D5 #41/#47, D8 #72/#75). The CMO only writes to `marketing/`, so nothing here is changed until you say "yes, fix the poster and the stats".

## What's wrong (from the Actions log, run 46109139335, 28 Nov 04:47 UTC)
```
E: Failed to fetch https://security.ubuntu.com/.../libpipewire-0.3-0t64_1.6.2-1ubuntu1.2_amd64v3.deb  404  Not Found
E: Unable to fetch some archives, maybe run apt update or try with --fix-missing?
Posting 2026-11-26-1-watch-them-sort (26.5 MB)
subprocess.CalledProcessError: Command '['sudo', 'apt-get', 'install', '-y', '-qq', 'ffmpeg']' returned non-zero exit status 100.
```
The runner is now `ubuntu-26.04`; its package list is stale, and `post.py` installs ffmpeg without updating it.

## The change
1. `poster/post.py` `ig_ready()`: run `sudo apt-get update -qq` before `sudo apt-get install -y -qq ffmpeg` (or install ffmpeg once in a workflow step before `post.py`).
2. `poster/post.py` `due_item()`: add `MAX_LATE = dt.timedelta(days=3)` like `post_youtube.py` line 19, and only pick items with `now - MAX_LATE <= when`. Mark Instagram as skipped for the stale 26–28 Nov reels (they're already on YouTube/TikTok), so Instagram restarts with that day's reel and never posts more than 3 a day.
3. `poster/stats.py` (lines 133 and 168): count a reel when any platform says posted (`youtube.status` or `tiktok.status` == "posted"), not only `status == "posted"`. Right now 8 live reels (26–28 Nov) have no stats. Also log why 6 reels come back with empty TikTok stats.
4. `poster/stats.py`: add YouTube Analytics `averageViewDuration` / `averageViewPercentage` per video (needs the `yt-analytics.readonly` scope on the refresh token). YouTube is now 41% of our views and we have no watch time for it.
