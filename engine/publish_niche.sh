#!/bin/bash
# Rewrites the "media-niche" branch with the media for every niche-account item still waiting to post:
#   <account>/<id>.mp4 for reels, <account>/<id>/slide-N.jpg for slideshows. Then force-pushes it.
# Run from the repo root after rendering (reels: out/<account>/<id>/reel.mp4, slideshows: out/<account>/<id>/slide-*.jpg).
set -e
root=$(pwd); tmp=$(mktemp -d); missing=0
for f in accounts/*/queue/*.json; do
  [ -e "$f" ] || continue
  acct=$(basename "$(dirname "$(dirname "$f")")"); id=$(basename "$f" .json)
  python3 -c "import json,sys; s=json.load(open(sys.argv[1])); sys.exit(0 if s.get('status')=='queued' else 1)" "$f" || continue
  fmt=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('format',''))" "$f")
  src="out/$acct/$id"
  if [ "$fmt" = "slideshow" ]; then
    if ls "$src"/slide-*.jpg >/dev/null 2>&1; then mkdir -p "$tmp/$acct/$id"; cp "$src"/slide-*.jpg "$tmp/$acct/$id/"; else echo "missing slides: $acct/$id"; missing=1; fi
  else
    if [ -f "$src/reel.mp4" ]; then mkdir -p "$tmp/$acct"; cp "$src/reel.mp4" "$tmp/$acct/$id.mp4"; else echo "missing video: $acct/$id"; missing=1; fi
  fi
done
[ $missing = 0 ] || { echo "Render the missing items first."; exit 1; }
remote=$(git remote get-url origin)
cd "$tmp" && touch .keep && git init -q -b media-niche && git add -A
git -c user.name="savesort-bot" -c user.email="savesort-bot@users.noreply.github.com" commit -q -m "Upcoming niche posts"
git push -q -f "$remote" media-niche
echo "media-niche branch: $(find . -name '*.mp4' | wc -l) reels, $(find . -name 'slide-1.jpg' | wc -l) slideshows"
cd "$root"; rm -rf "$tmp"
