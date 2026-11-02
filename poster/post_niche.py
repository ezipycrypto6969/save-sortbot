"""Posts the niche accounts (gym, kitchen, hype check, ...) through Upload-Post, to Instagram and TikTok.

Runs in the same GitHub Actions job as the main account. For every niche account in accounts.json it:
  1. looks up its Upload-Post profile and which platforms are connected, and records that in accounts/status.json
     (the Sunday writers only write for accounts that are connected);
  2. finishes checking uploads submitted earlier;
  3. posts at most one due item: a slideshow (photo carousel) or a reel (video).
Media come from the "media-niche" branch (engine/publish_niche.sh): <account>/<id>.mp4 or <account>/<id>/slide-N.jpg.
Needs secret UPLOAD_POST_API_KEY. Repo variables: PAUSED=true stops posting, DRY_RUN=true rehearses.
Queue items are marked with "upload": {"status": "submitted"|"posted"|"partial"|"failed", "request_id", "results"}.
"""
import datetime as dt, glob, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

API = "https://api.upload-post.com/api"
KEY = "".join(os.environ.get("UPLOAD_POST_API_KEY", "").split())
DRY = os.environ.get("DRY_RUN", "").lower() == "true"
MAX_LATE = dt.timedelta(days=3)
NOW = dt.datetime.now(dt.timezone.utc)


def say(kind, title, msg):
    print(f"::{kind} title={title}::{msg.replace(KEY, '***') if KEY else msg}")


def get(path, params=None):
    url = f"{API}/{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Apikey {KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return {"status": "error", "code": e.code, "message": " ".join(e.read().decode(errors="replace").split())[:500]}


def save(path, spec):
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2)


def captions(spec):
    """(instagram caption, tiktok caption, short tiktok title)."""
    ig = spec.get("ig_caption") or spec.get("caption", "")
    tt = spec.get("tiktok_caption") or re.sub(r"\blink in bio\b", "savesortai.com", spec.get("caption", ""), flags=re.I)
    title = (spec.get("tiktok_title") or spec.get("caption", "").split("\n")[0])[:90]
    return ig[:2200], tt[:2200], title


def resolve(path, spec, key="upload"):
    """Check an earlier async upload; record each platform's result."""
    st = get("uploadposts/status", {"request_id": spec[key]["request_id"]})
    res = st.get("results") or []
    if isinstance(res, dict): res = [{"platform": k, **v} for k, v in res.items()]
    busy = [r for r in res if r.get("status") in ("processing", "pending", "queued", "in_progress", "uploading")]
    if busy or (st.get("status") not in ("completed", "failed") and not res): return
    spec = json.load(open(path))
    out = {r.get("platform"): {"success": bool(r.get("success")), "url": r.get("url") or r.get("post_url") or "",
                               "message": r.get("message") or r.get("error") or ""} for r in res if r.get("platform")}
    ok = [p for p, r in out.items() if r["success"]]
    spec[key].update(results=out, status="posted" if ok and len(ok) == len(out) else "partial" if ok else "failed")
    save(path, spec)
    for p, r in out.items():
        if not r["success"]: say("error", f"{spec['id']} didn't post to {p}", r["message"] or "unknown reason")
        else: print(f"Posted {spec['id']} to {p}: {r['url'] or '(no link returned)'}")


def due(acct):
    items = []
    for p in sorted(glob.glob(f"accounts/{acct}/queue/*.json")):
        s = json.load(open(p))
        if s.get("status") != "queued" or s.get("check") != "passed" or s.get("upload"): continue
        when = dt.datetime.fromisoformat(s["post_at"])
        if NOW - MAX_LATE <= when <= NOW + dt.timedelta(minutes=20): items.append((when, p, s))
    return [x[1:] for x in sorted(items, reverse=True)]  # newest first: a missed old one never blocks tonight's


def media(acct, spec):
    """Fetch this item's files from the media-niche branch. Returns a list of local paths, or None."""
    if spec.get("format") == "slideshow":
        files = []
        for i in range(1, len(spec["slides"]) + 1):
            dst = f"/tmp/{spec['id']}-{i}.jpg"
            with open(dst, "wb") as f:
                if subprocess.run(["git", "show", f"FETCH_HEAD:{acct}/{spec['id']}/slide-{i}.jpg"], stdout=f, stderr=subprocess.DEVNULL).returncode:
                    return None
            files.append(dst)
        vid = f"/tmp/{spec['id']}-video.mp4"
        with open(vid, "wb") as f:
            got = not subprocess.run(["git", "show", f"FETCH_HEAD:{acct}/{spec['id']}/video.mp4"], stdout=f, stderr=subprocess.DEVNULL).returncode
        return files + ([vid] if got else [])
    dst = f"/tmp/{spec['id']}.mp4"
    with open(dst, "wb") as f:
        if subprocess.run(["git", "show", f"FETCH_HEAD:{acct}/{spec['id']}.mp4"], stdout=f, stderr=subprocess.DEVNULL).returncode:
            return None
    return [dst]


def submit(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True)
    try: return json.loads(out.stdout)
    except Exception: return {"success": False, "message": f"{out.stdout[:400]} {out.stderr[:200]}"}


def record(path, key, resp, plats, acct):
    """Save the outcome of one upload call under spec[key]. Returns True if Upload-Post accepted it."""
    rid = resp.get("request_id") or resp.get("job_id")
    spec = json.load(open(path))
    if rid: spec[key] = {"status": "submitted", "request_id": rid, "platforms": plats, "submitted_at": NOW.isoformat(timespec="seconds")}
    elif resp.get("success"): spec[key] = {"status": "posted", "platforms": plats, "results": resp.get("results")}
    else:
        spec[key] = {"status": "failed", "platforms": plats, "message": json.dumps(resp)[:500]}
        say("error", f"Upload-Post refused {acct}/{spec['id']} ({', '.join(plats)})", json.dumps(resp)[:500])
    if spec[key]["status"] != "failed": spec.update(status="posted", posted_at=NOW.isoformat(timespec="seconds"))
    save(path, spec)
    return spec[key]["status"] != "failed"


def post(acct, profile, platforms, path, spec, files):
    ig, tt, title = captions(spec)
    plats = [p for p in spec.get("platforms", platforms) if p in platforms]
    if not plats:
        print(f"{spec['id']}: none of its platforms are connected yet; leaving it queued."); return
    slideshow = spec.get("format") == "slideshow"
    photos = [f for f in files if f.endswith(".jpg")]
    video = next((f for f in files if f.endswith(".mp4")), None)
    yt_title = (spec.get("yt_title") or title)[:100]
    yt_desc = (spec.get("yt_description") or f"{yt_title}\n\n{re.sub(r'(?i)link in bio', 'savesortai.com', spec.get('caption', ''))}\n\n#Shorts")[:4900]
    base = ["curl", "-sS", "--max-time", "600", "-H", f"Authorization: Apikey {KEY}", "-F", f"user={profile}",
            "-F", "async_upload=true", "-F", "privacy_level=PUBLIC_TO_EVERYONE"]
    yt_fields = ["-F", f"youtube_title={yt_title}", "-F", f"youtube_description={yt_desc}", "-F", "privacyStatus=public",
                 "-F", "selfDeclaredMadeForKids=false"]
    calls = []  # (key, platforms, curl command)
    if slideshow:
        social = [p for p in plats if p != "youtube"]
        if social:
            cmd = base + ["-H", f"Idempotency-Key: {spec['id']}", "-F", f"title={ig}", "-F", f"external_id={spec['id']}"]
            for p in social: cmd += ["-F", f"platform[]={p}"]
            for f in photos: cmd += ["-F", f"photos[]=@{f}"]
            calls.append(("upload", social, cmd + ["-F", f"tiktok_title={title}", "-F", f"tiktok_description={tt}",
                                                   "-F", "auto_add_music=true", "-F", "photo_cover_index=0", f"{API}/upload_photos"]))
        if "youtube" in plats and video:  # YouTube Shorts takes video only: the slideshow as a short video
            calls.append(("upload_yt", ["youtube"], base + ["-H", f"Idempotency-Key: {spec['id']}-yt", "-F", f"title={yt_title}",
                          "-F", f"external_id={spec['id']}-yt", "-F", "platform[]=youtube", "-F", f"video=@{video}"] + yt_fields + ["-F", "containsSyntheticMedia=false", f"{API}/upload"]))
    else:
        cmd = base + ["-H", f"Idempotency-Key: {spec['id']}", "-F", f"title={ig}", "-F", f"external_id={spec['id']}"]
        for p in plats: cmd += ["-F", f"platform[]={p}"]
        cmd += ["-F", f"video=@{video}", "-F", f"tiktok_title={tt}", "-F", "is_aigc=true",  # AI voice and animation: label it
                "-F", f"cover_timestamp={spec.get('cover_offset_ms', 1000)}"]
        if "youtube" in plats: cmd += yt_fields + ["-F", "containsSyntheticMedia=true"]
        calls.append(("upload", plats, cmd + [f"{API}/upload"]))
    if not calls:
        print(f"{spec['id']}: nothing to post it with yet (no slides or video for its connected platforms)."); return
    print(f"Posting {acct}/{spec['id']} ({'slideshow, %d slides' % len(photos) if slideshow else 'reel'}) to "
          + "; ".join(", ".join(c[1]) for c in calls))
    if DRY:
        print(f"DRY_RUN: Instagram caption:\n{ig}\n--- TikTok caption:\n{tt}\n--- YouTube title: {yt_title}"); return
    keys = [k for k, plats_, cmd in calls if record(path, k, submit(cmd), plats_, acct)]
    for _ in range(15):  # up to ~5 minutes, then the next run finishes the check
        if not keys: break
        time.sleep(20)
        for k in list(keys):
            resolve(path, json.load(open(path)), k)
            if json.load(open(path))[k]["status"] != "submitted": keys.remove(k)


def main():
    accounts = [a for a in json.load(open("accounts.json"))["accounts"] if a["id"] != "main" and a.get("upload_post_profile")]
    if not KEY:
        print("No UPLOAD_POST_API_KEY secret; niche accounts not set up yet."); return
    profs = get("uploadposts/users").get("profiles") or []
    by_name = {}
    for p in profs:
        connected = [k for k, v in (p.get("social_accounts") or {}).items() if v]
        for n in (p.get("username"), p.get("display_name")):
            if n: by_name[n.strip().lower()] = (p.get("username"), connected, p.get("reauth_required"))
    status = {}
    for a in accounts:
        user, connected, reauth = by_name.get(a["upload_post_profile"].lower(), (None, [], None))
        live = [p for p in a.get("platforms", ["instagram", "tiktok", "youtube"]) if p in connected]
        status[a["id"]] = {"profile": user, "connected": live, "ready": bool(user and live),
                           "reauth_required": bool(reauth), "checked": NOW.isoformat(timespec="seconds")}
        if reauth: say("warning", f"Reconnect {a['name']}", f"Upload-Post says profile '{user}' needs reconnecting.")
    old = json.load(open("accounts/status.json")) if os.path.exists("accounts/status.json") else {}
    if {k: {**v, "checked": None} for k, v in status.items()} != {k: {**v, "checked": None} for k, v in old.items()}:
        json.dump(status, open("accounts/status.json", "w"), indent=2); open("accounts/status.json", "a").write("\n")
    for a in accounts: print(f"{a['name']}: {'ready on ' + ', '.join(status[a['id']]['connected']) if status[a['id']]['ready'] else 'not connected yet'}")
    if os.environ.get("PAUSED", "").lower() == "true":
        print("PAUSED is set; not posting."); return
    fetched = False
    for a in accounts:
        st = status[a["id"]]
        for p in sorted(glob.glob(f"accounts/{a['id']}/queue/*.json")):
            s = json.load(open(p))
            for k in ("upload", "upload_yt"):
                if (s.get(k) or {}).get("status") == "submitted": resolve(p, json.load(open(p)), k)
        if not st["ready"]: continue
        items = due(a["id"])
        if not items: print(f"{a['name']}: nothing due."); continue
        if not fetched:
            if subprocess.run(["git", "fetch", "--depth", "1", "origin", "media-niche"]).returncode:
                say("error", "No niche media", "The media-niche branch is missing; the Sunday run uploads it."); return
            fetched = True
        for path, spec in items:
            files = media(a["id"], spec)
            if files: post(a["id"], st["profile"], st["connected"], path, spec, files); break
            say("warning", "Niche item skipped", f"No media for {a['id']}/{spec['id']} on media-niche; marking it skipped.")
            spec["upload"] = {"status": "skipped", "message": "media not on the media-niche branch"}; save(path, spec)


if __name__ == "__main__":
    main()
