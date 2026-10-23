#!/bin/bash
# Renders every queued item that has no video yet. Usage: bash engine/build_all.sh   (from the repo root)
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
fail=0
for f in queue/*.json; do
  id=$(basename "$f" .json)
  status=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('status'))" "$f")
  [ "$status" != "queued" ] && continue
  [ -f "out/$id/reel.mp4" ] && [ "$1" != "--force" ] && continue   # delete out/<id> to rebuild one
  echo "== $id"
  python3 engine/build.py "$f" "out/$id" --stills 2>&1 | grep -v -i "warning" || fail=1
done
exit $fail
