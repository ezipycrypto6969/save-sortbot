#!/bin/bash
# Updates the "media-niche" branch so it holds the media for every niche-account item still waiting to post:
#   <account>/<id>.mp4 for reels, <account>/<id>/slide-N.jpg for slideshows. Then force-pushes it.
# Starts from what's already on the branch (so each account's writer only needs its own renders), adds or replaces
# anything rendered locally (out/<account>/<id>/reel.mp4 or slide-*.jpg), and drops items that are no longer queued.
set -e
root=$(pwd); tmp=$(mktemp -d); remote=$(git remote get-url origin); missing=0
if git fetch -q --depth 1 origin media-niche 2>/dev/null; then git archive FETCH_HEAD | tar -x -C "$tmp"; fi
keep=$(mktemp)
for f in accounts/*/queue/*.json; do
  [ -e "$f" ] || continue
  acct=$(basename "$(dirname "$(dirname "$f")")"); id=$(basename "$f" .json)
  python3 -c "import json,sys; s=json.load(open(sys.argv[1])); sys.exit(0 if s.get('status')=='queued' else 1)" "$f" || continue
  fmt=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('format',''))" "$f")
  src="out/$acct/$id"
  if [ "$fmt" = "slideshow" ]; then
    echo "$acct/$id" >> "$keep"
    if ls "$src"/slide-*.jpg >/dev/null 2>&1; then rm -rf "$tmp/$acct/$id"; mkdir -p "$tmp/$acct/$id"; cp "$src"/slide-*.jpg "$tmp/$acct/$id/"
    elif [ ! -f "$tmp/$acct/$id/slide-1.jpg" ]; then echo "missing slides: $acct/$id"; missing=1; fi
  else
    echo "$acct/$id.mp4" >> "$keep"
    if [ -f "$src/reel.mp4" ]; then mkdir -p "$tmp/$acct"; cp "$src/reel.mp4" "$tmp/$acct/$id.mp4"
    elif [ ! -f "$tmp/$acct/$id.mp4" ]; then echo "missing video: $acct/$id"; missing=1; fi
  fi
done
[ $missing = 0 ] || { echo "Render the missing items first."; exit 1; }
# drop media for items that have posted or been removed
cd "$tmp"
for d in */; do [ -d "$d" ] || continue
  for x in "$d"*; do rel="${x%/}"; grep -qxF "$rel" "$keep" || rm -rf "$rel"; done
done
rm -rf .git; touch .keep; git init -q -b media-niche && git add -A
git -c user.name="savesort-bot" -c user.email="savesort-bot@users.noreply.github.com" commit -q -m "Upcoming niche posts"
git push -q -f "$remote" media-niche
echo "media-niche branch: $(find . -name '*.mp4' | wc -l) reels, $(find . -name 'slide-1.jpg' | wc -l) slideshows"
cd "$root"; rm -rf "$tmp" "$keep"
