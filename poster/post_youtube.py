"""Uploads the next due reel from queue/ to YouTube as a Short (YouTube Data API v3, videos.insert).

Runs inside GitHub Actions, right after the Instagram step, using the same queue and the same video
from the "media" branch. Needs secrets YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN; if they aren't
set yet it does nothing, so Instagram keeps working on its own.
Marks the queue file with "youtube": {"status": "posted", "video_id", "url"}.
Usage: python3 poster/post_youtube.py          post the next due reel
       python3 poster/post_youtube.py --check  only check the login works (prints the channel name)
Repo variables: PAUSED=true stops posting, DRY_RUN=true rehearses without uploading,
SITE_URL (optional) is put at the top of each description.
"""
import datetime as dt, glob, json, os, re, subprocess, sys, urllib.parse, urllib.request

CID = os.environ.get("YT_CLIENT_ID", "").strip()
SECRET = os.environ.get("YT_CLIENT_SECRET", "").strip()
REFRESH = "".join(os.environ.get("YT_REFRESH_TOKEN", "").split())
DRY = os.environ.get("DRY_RUN", "").lower() == "true"
SITE = os.environ.get("SITE_URL", "").strip()
MAX_LATE = dt.timedelta(days=3)  # don't upload reels that were due more than 3 days ago
HIDE = [s for s in (SECRET, REFRESH) if s]


def fail(msg):
    for s in HIDE: msg = msg.replace(s, "***")
    print(f"::error title=YouTube said no::{msg}")
    raise SystemExit(msg)


def http(method, url, data=None, headers=None, raw=False):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r if raw else json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        hint = ""
        if "invalid_grant" in body:
            hint = (" -- The YouTube refresh token was revoked or expired. Make a new one in the OAuth Playground"
                    " and update the YT_REFRESH_TOKEN secret. (If the Google app is still in 'Testing', publish it"
                    " to 'In production' first, or the token dies after 7 days.)")
        elif "quotaExceeded" in body or "uploadLimitExceeded" in body:
            hint = " -- Daily YouTube upload limit reached; it will retry at the next slot."
        fail(f"YouTube error {e.code} on {url.split('?')[0]}: {body}{hint}")


def access_token():
    body = urllib.parse.urlencode({"client_id": CID, "client_secret": SECRET,
                                   "refresh_token": REFRESH, "grant_type": "refresh_token"}).encode()
    tok = http("POST", "https://oauth2.googleapis.com/token", body,
               {"Content-Type": "application/x-www-form-urlencoded"})["access_token"]
    HIDE.append(tok)
    return tok


def due_item():
    now = dt.datetime.now(dt.timezone.utc)
    items = []
    for p in sorted(glob.glob("queue/*.json")):
        spec = json.load(open(p))
        if spec.get("status") not in ("queued", "posted"): continue
        if (spec.get("youtube") or {}).get("status") == "posted": continue
        when = dt.datetime.fromisoformat(spec["post_at"])
        if now - MAX_LATE <= when <= now + dt.timedelta(minutes=20): items.append((when, p, spec))
    return min(items)[1:] if items else (None, None)


def title_for(spec):
    if spec.get("yt_title"): t = spec["yt_title"]
    else:
        first = spec["caption"].strip().split("\n")[0]
        first = re.sub(r"[^\w\s$%&'’,.?!:()\-\"“”]", "", first)  # drop emoji
        first = re.sub(r"\s+", " ", first).strip()
        t = first
    t = t.replace("<", "").replace(">", "")
    if len(t) > 90: t = t[:87].rsplit(" ", 1)[0] + "..."
    return f"{t} #Shorts"


def description_for(spec):
    d = spec["caption"]
    if SITE:
        d = re.sub(r"link in bio", "link below", d, flags=re.I)
        d = f"Sort your saved reels free: {SITE}\n\n{d}"
    else:
        d = re.sub(r"link in bio", "link on our channel", d, flags=re.I)
    return d.replace("<", "").replace(">", "")[:4900]


def tags_for(spec):
    return [t.lstrip("#") for t in re.findall(r"#\w+", spec["caption"])][:15] + ["SaveSort", "shorts"]


def main():
    if not (CID and SECRET and REFRESH):
        print("YouTube isn't set up yet (no YT_* secrets); skipping."); return
    if os.environ.get("PAUSED", "").lower() == "true":
        print("PAUSED is set; not posting."); return
    token = access_token()
    auth = {"Authorization": f"Bearer {token}"}
    if DRY or "--check" in sys.argv:
        ch = http("GET", "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", headers=auth)
        if not ch.get("items"): fail("Logged in, but this Google account has no YouTube channel. Create one at youtube.com first.")
        print(f"YouTube login OK for channel: {ch['items'][0]['snippet']['title']}")
        if "--check" in sys.argv: return
    path, spec = due_item()
    if not path:
        print("Nothing due for YouTube."); return
    subprocess.run(["git", "fetch", "--depth", "1", "origin", "media"], check=True)
    with open("short.mp4", "wb") as f:
        r = subprocess.run(["git", "show", f"FETCH_HEAD:{spec['id']}.mp4"], stdout=f)
    if r.returncode:
        print(f"::warning title=YouTube skipped::No video for {spec['id']} on the media branch."); return
    size = os.path.getsize("short.mp4")
    meta = {"snippet": {"title": title_for(spec), "description": description_for(spec),
                        "tags": tags_for(spec), "categoryId": "27"},  # 27 = Education
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False, "embeddable": True}}
    print(f"Uploading {spec['id']} ({size/1e6:.1f} MB) as: {meta['snippet']['title']}")
    if DRY:
        print("DRY_RUN: would upload with description:\n" + meta["snippet"]["description"]); return
    # 1. start a resumable upload session
    start = http("POST", "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                 json.dumps(meta).encode(),
                 {**auth, "Content-Type": "application/json; charset=UTF-8",
                  "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, raw=True)
    upload_url = start.headers["Location"]
    # 2. send the video
    with open("short.mp4", "rb") as f:
        v = http("PUT", upload_url, f.read(), {**auth, "Content-Type": "video/mp4"})
    url = f"https://youtube.com/shorts/{v['id']}"
    spec = json.load(open(path))  # re-read: the Instagram step may have just updated it
    spec["youtube"] = {"status": "posted", "video_id": v["id"], "url": url,
                       "posted_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2)
    print(f"Posted to YouTube: {url}")


if __name__ == "__main__":
    main()
