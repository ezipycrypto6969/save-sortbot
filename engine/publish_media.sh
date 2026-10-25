#!/bin/bash
# Rewrites the "media" branch so it holds exactly one <id>.mp4 per still-queued reel, then force-pushes it.
# Run from the repo root after rendering. History of this branch is not kept, so the repo stays small.
set -e
root=$(pwd); tmp=$(mktemp -d)
missing=0
for f in queue/*.json; do
  id=$(basename "$f" .json)
  [ "$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('status'))" "$f")" = "queued" ] || continue
  if [ -f "out/$id/reel.mp4" ]; then cp "out/$id/reel.mp4" "$tmp/$id.mp4"; else echo "missing video: $id"; missing=1; fi
done
[ $missing = 0 ] || { echo "Render the missing reels first."; exit 1; }
remote=$(git remote get-url origin)
cd "$tmp" && git init -q -b media && git add -A
git -c user.name="savesort-bot" -c user.email="savesort-bot@users.noreply.github.com" commit -q -m "Upcoming reels"
git push -q -f "$remote" media
echo "media branch now has $(ls *.mp4 | wc -l) reels"
cd "$root"; rm -rf "$tmp"
