"""Posts the next due reel from queue/ to TikTok through Upload-Post (an audited TikTok posting service).

Runs inside GitHub Actions after the Instagram and YouTube steps, using the same queue and the same video
from the "media" branch. Needs secret UPLOAD_POST_API_KEY and repo variable UPLOAD_POST_USER (the profile
name you created in Upload-Post and connected TikTok to). If they aren't set yet it does nothing.
Marks the queue file with "tiktok": {"status": "submitted"|"posted"|"failed", "request_id", "url"}.
Usage: python3 poster/post_tiktok.py          post the next due reel (and finish checking earlier ones)
       python3 poster/post_tiktok.py --check  only check the API key works
Repo variables: PAUSED=true stops posting, DRY_RUN=true rehearses without uploading.
"""
import datetime as dt, glob, json, os, subprocess, sys, time, urllib.parse, urllib.request

API = "https://api.upload-post.com/api"
KEY = "".join(os.environ.get("UPLOAD_POST_API_KEY", "").split())
USER = os.environ.get("UPLOAD_POST_USER", "").strip()
DRY = os.environ.get("DRY_RUN", "").lower() == "true"
MAX_LATE = dt.timedelta(days=3)
DONE = {"completed", "failed"}


def fail(msg):
    msg = msg.replace(KEY, "***") if KEY else msg
    print(f"::error title=TikTok said no::{msg}")
    raise SystemExit(msg)


def get(path, params=None):
    url = f"{API}/{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Apikey {KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = " ".join(e.read().decode(errors="replace").split())
        if e.code == 404: return {"status": "not_found", "message": body}
        fail(f"Upload-Post error {e.code} on {path}: {body}")


def tiktok_result(st):
    for r in st.get("results") or []:
        if r.get("platform") == "tiktok": return r
    return None


def resolve(path, spec):
    """Check a submitted upload and record the outcome. Returns True when it's finished."""
    tk = spec["tiktok"]
    st = get("uploadposts/status", {"request_id": tk["request_id"]})
    r = tiktok_result(st) or {}
    print(f"TikTok status for {spec['id']}: {st.get('status')} {r}")
    if st.get("status") not in DONE and r.get("success") is None: return False
    spec = json.load(open(path))  # re-read: earlier steps may have changed it
    if r.get("success"):
        spec["tiktok"].update(status="posted", url=r.get("url") or r.get("post_url") or "", message=r.get("message", ""))
        print(f"Posted to TikTok: {spec['tiktok']['url'] or '(link not returned)'}")
    else:
        spec["tiktok"].update(status="failed", message=r.get("message") or st.get("message") or "unknown")
        print(f"::error title=TikTok couldn't post {spec['id']}::{spec['tiktok']['message']}")
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2)
    return True


def due_item():
    now = dt.datetime.now(dt.timezone.utc)
    items = []
    for p in sorted(glob.glob("queue/*.json")):
        spec = json.load(open(p))
        if spec.get("status") not in ("queued", "posted"): continue
        if spec.get("check") == "pending": continue  # not yet passed by the claims checker
        if spec.get("tiktok"): continue  # already submitted, posted or failed
        when = dt.datetime.fromisoformat(spec["post_at"])
        if now - MAX_LATE <= when <= now + dt.timedelta(minutes=20): items.append((when, p, spec))
    return min(items)[1:] if items else (None, None)


def main():
    if not (KEY and USER):
        print("TikTok isn't set up yet (no UPLOAD_POST_API_KEY secret / UPLOAD_POST_USER variable); skipping."); return
    if os.environ.get("PAUSED", "").lower() == "true":
        print("PAUSED is set; not posting."); return
    if "--check" in sys.argv:
        st = get("uploadposts/status", {"request_id": "connection-test"})
        print(f"Upload-Post API key works (test lookup answered: {st.get('status') or st})"); return
    # finish checking anything submitted earlier
    for p in sorted(glob.glob("queue/*.json")):
        spec = json.load(open(p))
        if (spec.get("tiktok") or {}).get("status") == "submitted": resolve(p, spec)
    path, spec = due_item()
    if not path:
        print("Nothing due for TikTok."); return
    subprocess.run(["git", "fetch", "--depth", "1", "origin", "media"], check=True)
    with open("tiktok.mp4", "wb") as f:
        r = subprocess.run(["git", "show", f"FETCH_HEAD:{spec['id']}.mp4"], stdout=f)
    if r.returncode:
        print(f"::warning title=TikTok skipped::No video for {spec['id']} on the media branch."); return
    caption = spec["caption"][:2200]
    print(f"Posting {spec['id']} to TikTok ({os.path.getsize('tiktok.mp4')/1e6:.1f} MB)")
    if DRY:
        print("DRY_RUN: would post with caption:\n" + caption); return
    cmd = ["curl", "-sS", "--max-time", "600", "-H", f"Authorization: Apikey {KEY}",
           "-F", "video=@tiktok.mp4", "-F", f"user={USER}", "-F", "platform[]=tiktok",
           "-F", f"title={caption}", "-F", f"tiktok_title={caption}",
           "-F", "privacy_level=PUBLIC_TO_EVERYONE", "-F", "is_aigc=true",  # AI voice and animation: label it
           "-F", f"cover_timestamp={spec.get('cover_offset_ms', 1000)}", "-F", "async_upload=true",
           "-F", f"external_id={spec['id']}", f"{API}/upload"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    try: resp = json.loads(out.stdout)
    except Exception: fail(f"Upload-Post answered: {out.stdout[:500]} {out.stderr[:300]}")
    rid = resp.get("request_id") or resp.get("job_id")
    if not rid:
        res = resp.get("results")
        tk = res.get("tiktok") if isinstance(res, dict) else tiktok_result(resp)
        if resp.get("success") and tk and tk.get("success"):
            spec = json.load(open(path)); spec["tiktok"] = {"status": "posted", "url": tk.get("url", "")}
            json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2); print("Posted to TikTok."); return
        fail(f"Upload-Post didn't accept the video: {json.dumps(resp)[:800]}")
    # record the submission straight away, so a later run can never post it twice
    spec = json.load(open(path))
    spec["tiktok"] = {"status": "submitted", "request_id": rid,
                      "submitted_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2)
    print(f"Submitted to TikTok (request {rid}); waiting for TikTok to publish it")
    for _ in range(30):  # up to ~10 minutes; if still busy, the next run picks it up
        time.sleep(20)
        if resolve(path, spec): return
    print("TikTok is still processing; the next run will record the result.")


if __name__ == "__main__":
    main()
