#!/bin/bash
# Rewrites the "media" branch so it holds exactly one <id>.mp4 per reel still waiting to post (Instagram or YouTube), then force-pushes it.
# Run from the repo root after rendering. History of this branch is not kept, so the repo stays small.
set -e
root=$(pwd); tmp=$(mktemp -d)
missing=0
for f in queue/*.json; do
  id=$(basename "$f" .json)
  # keep it while Instagram hasn't posted it, or YouTube hasn't and it was due in the last 3 days
  python3 - "$f" <<'PY' || continue
import json, sys, datetime as dt
s = json.load(open(sys.argv[1]))
if s.get("status") == "queued": sys.exit(0)
recent = dt.datetime.fromisoformat(s["post_at"]) > dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3)
sys.exit(0 if s.get("status") == "posted" and (s.get("youtube") or {}).get("status") != "posted" and recent else 1)
PY
  if [ -f "out/$id/reel.mp4" ]; then cp "out/$id/reel.mp4" "$tmp/$id.mp4"; else echo "missing video: $id"; missing=1; fi
done
[ $missing = 0 ] || { echo "Render the missing reels first."; exit 1; }
remote=$(git remote get-url origin)
# the public website lives on the same GitHub Pages site (static pages only; the Pro API needs Cloudflare)
cp site/index.html site/terms.html site/refunds.html site/page.css "$tmp/"
cd "$tmp" && touch .nojekyll && git init -q -b media && git add -A
git -c user.name="savesort-bot" -c user.email="savesort-bot@users.noreply.github.com" commit -q -m "Upcoming reels"
git push -q -f "$remote" media
echo "media branch now has $(ls *.mp4 | wc -l) reels + the website"
cd "$root"; rm -rf "$tmp"
