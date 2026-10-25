"""Publishes the next due reel from queue/ to Instagram (official Instagram API with Instagram Login).

Runs inside GitHub Actions. Needs env: IG_USER_ID, IG_ACCESS_TOKEN.
The video for queue/<id>.json lives as <id>.mp4 on the "media" branch (rewritten weekly with only upcoming reels).
Posts at most one reel per run. Set repo variable PAUSED=true to stop posting, DRY_RUN=true to test without posting.
"""
import datetime as dt, glob, json, os, subprocess, sys, time, urllib.parse, urllib.request

API = "https://graph.instagram.com/v21.0"
IG_USER = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]
DRY = os.environ.get("DRY_RUN", "").lower() == "true"


def call(method, url, params=None, data=None, headers=None):
    if params: url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"Instagram API error {e.code} on {url.split('?')[0]}: {body}")


def due_item():
    now = dt.datetime.now(dt.timezone.utc)
    items = []
    for p in sorted(glob.glob("queue/*.json")):
        spec = json.load(open(p))
        if spec.get("status") != "queued": continue
        when = dt.datetime.fromisoformat(spec["post_at"])
        if when <= now + dt.timedelta(minutes=20): items.append((when, p, spec))
    return min(items)[1:] if items else (None, None)


def main():
    if os.environ.get("PAUSED", "").lower() == "true":
        print("PAUSED is set; not posting."); return
    if DRY:  # check the token works before anything else
        me = call("GET", f"{API}/me", {"fields": "user_id,username", "access_token": TOKEN})
        print(f"Token OK for @{me.get('username')} (user_id {me.get('user_id')})")
    path, spec = due_item()
    if not path and DRY:  # in test mode, rehearse with the next queued reel even if it isn't due yet
        nxt = sorted((json.load(open(p))["post_at"], p) for p in glob.glob("queue/*.json") if json.load(open(p)).get("status") == "queued")
        if nxt: path = nxt[0][1]; spec = json.load(open(path))
    if not path:
        print("Nothing due."); return
    vid = f"{spec['id']}.mp4"
    subprocess.run(["git", "fetch", "--depth", "1", "origin", "media"], check=True)
    with open("reel.mp4", "wb") as f:
        subprocess.run(["git", "show", f"FETCH_HEAD:{vid}"], stdout=f, check=True)
    size = os.path.getsize("reel.mp4")
    print(f"Posting {spec['id']} ({size/1e6:.1f} MB)")
    if DRY:
        print("DRY_RUN: would post with caption:\n" + spec["caption"]); return
    # 1. create a resumable Reels container
    c = call("POST", f"{API}/{IG_USER}/media", {
        "media_type": "REELS", "upload_type": "resumable", "caption": spec["caption"],
        "share_to_feed": "true", "thumb_offset": spec.get("cover_offset_ms", 1500), "access_token": TOKEN})
    cid, uri = c["id"], c["uri"]
    # 2. upload the video bytes
    with open("reel.mp4", "rb") as f:
        call("POST", uri, data=f.read(), headers={"Authorization": f"OAuth {TOKEN}", "offset": "0", "file_size": str(size)})
    # 3. wait for Instagram to process it
    for _ in range(60):
        st = call("GET", f"{API}/{cid}", {"fields": "status_code,status", "access_token": TOKEN})
        if st.get("status_code") == "FINISHED": break
        if st.get("status_code") in ("ERROR", "EXPIRED"): raise SystemExit(f"Processing failed: {st}")
        time.sleep(10)
    else:
        raise SystemExit("Timed out waiting for Instagram to process the video")
    # 4. publish
    pub = call("POST", f"{API}/{IG_USER}/media_publish", {"creation_id": cid, "access_token": TOKEN})
    info = call("GET", f"{API}/{pub['id']}", {"fields": "permalink", "access_token": TOKEN})
    spec.update(status="posted", posted_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                media_id=pub["id"], permalink=info.get("permalink"))
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2)
    print(f"Posted: {info.get('permalink')}")


if __name__ == "__main__":
    main()
