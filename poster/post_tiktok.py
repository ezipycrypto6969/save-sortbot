"""Posts the next due reel from queue/ to TikTok through Upload-Post (an audited TikTok posting service).

Runs inside GitHub Actions after the Instagram and YouTube steps, using the same queue and the same video
from the "media" branch. Needs secret UPLOAD_POST_API_KEY and repo variable UPLOAD_POST_USER (the profile
name you created in Upload-Post and connected TikTok to). If they aren't set yet it does nothing.
Marks the queue file with "tiktok": {"status": "submitted"|"posted"|"failed", "request_id", "url"}.
Usage: python3 poster/post_tiktok.py          post the next due reel (and finish checking earlier ones)
       python3 poster/post_tiktok.py --check  only check the API key works
Repo variables: PAUSED=true stops posting, DRY_RUN=true rehearses without uploading.
"""
import datetime as dt, glob, json, os, zlib, subprocess, sys, time, urllib.parse, urllib.request

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


def trending_sound(user, seed):
    """A trending TikTok sound cleared for business use (TikTok Commercial Music Library), picked from the top 5.
    It's attached at volume 0, so viewers hear only the reel's own audio. Set the repo variable TIKTOK_SOUND=off to stop."""
    if os.environ.get("TIKTOK_SOUND", "").lower() == "off": return None
    try:
        url = f"{API}/uploadposts/tiktok/music/trending?" + urllib.parse.urlencode(
            {"profile": user, "country_code": os.environ.get("TIKTOK_SOUND_COUNTRY") or "US", "date_range": "7DAY"})
        with urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": f"Apikey {KEY}"}), timeout=60) as r:
            tracks = [t for t in json.loads(r.read() or b"{}").get("tracks") or [] if t.get("id")]
    except Exception as e:
        print(f"::warning title=No trending sound::Couldn't get TikTok's trending sounds ({e}); posting without one."); return None
    if not tracks: return None
    tracks.sort(key=lambda t: t.get("rank") or 99)
    t = tracks[zlib.crc32(seed.encode()) % min(5, len(tracks))]
    return {"id": str(t["id"]), "title": t.get("title", ""), "artist": t.get("artist", ""), "rank": t.get("rank")}


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
    busy = r.get("status") in ("processing", "pending", "queued", "in_progress", "uploading")
    if busy or (st.get("status") not in DONE and r.get("success") is None): return False  # still going
    spec = json.load(open(path))  # re-read: earlier steps may have changed it
    if r.get("success"):
        spec["tiktok"].update(status="posted", url=r.get("url") or r.get("post_url") or "", message=r.get("message", ""))
        print(f"Posted to TikTok: {spec['tiktok']['url'] or '(link not returned)'}")
    else:
        spec["tiktok"].update(status="failed", message=r.get("message") or st.get("message") or "unknown")
        print(f"::error title=TikTok couldn't post {spec['id']}::{spec['tiktok']['message']}")
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2)
    return True


def pick_profile():
    """The Upload-Post profile username to post as. Upload-Post wants the profile's exact `username`
    (not its display name). If UPLOAD_POST_USER doesn't match one, fall back to the only profile with TikTok connected."""
    profs = get("uploadposts/users").get("profiles") or []
    rows = [(p.get("username"), p.get("display_name"), bool((p.get("social_accounts") or {}).get("tiktok")), p.get("reauth_required")) for p in profs]
    for u, dn, tk, re_ in rows: print(f"Upload-Post profile: username={u!r} display_name={dn!r} tiktok_connected={tk} reauth_required={re_}")
    names = [u for u, *_ in rows]
    if USER in names: return USER
    match = [u for u, dn, tk, _ in rows if dn and dn.strip().lower() == USER.lower() and tk]
    tiktok = [u for u, _, tk, _ in rows if tk]
    pick = (match or (tiktok if len(tiktok) == 1 else [None]))[0]
    if pick:
        print(f"::warning title=Fix UPLOAD_POST_USER::'{USER}' isn't a profile username; using '{pick}'. Set the repo variable UPLOAD_POST_USER to {pick}.")
        return pick
    fail(f"UPLOAD_POST_USER is '{USER}', but your Upload-Post profile usernames are {names or 'none'}"
         f" and {'none have' if not tiktok else 'more than one has'} TikTok connected. Set UPLOAD_POST_USER to the right username.")


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
    return [x[1:] for x in sorted(items, reverse=True)]  # newest first, so an old leftover never blocks tonight's reel


def main():
    if not (KEY and USER):
        print("TikTok isn't set up yet (no UPLOAD_POST_API_KEY secret / UPLOAD_POST_USER variable); skipping."); return
    if os.environ.get("PAUSED", "").lower() == "true":
        print("PAUSED is set; not posting."); return
    if "--check" in sys.argv:
        user = pick_profile()
        print(f"Upload-Post API key works; posting as profile '{user}'")
        snd = trending_sound(user, "check")
        if snd: print(f"Trending sound check OK. Next posts get a muted trending sound, e.g. '{snd['title']}' by {snd['artist']} (#{snd['rank']}).")
        elif os.environ.get("TIKTOK_SOUND", "").lower() != "off":
            print("::warning title=No trending sounds::Couldn't list trending sounds; posts will go out without one. "
                  "In Upload-Post, reconnect TikTok so it has the music permission.")
        return
    # finish checking anything submitted earlier
    for p in sorted(glob.glob("queue/*.json")):
        spec = json.load(open(p))
        if (spec.get("tiktok") or {}).get("status") == "submitted": resolve(p, spec)
    due = due_item()
    if not due:
        print("Nothing due for TikTok."); return
    subprocess.run(["git", "fetch", "--depth", "1", "origin", "media"], check=True)
    for path, spec in due:
        with open("tiktok.mp4", "wb") as f:
            r = subprocess.run(["git", "show", f"FETCH_HEAD:{spec['id']}.mp4"], stdout=f, stderr=subprocess.DEVNULL)
        if not r.returncode: break
        # video is gone from the media branch: record it so it never blocks a later reel, then try the next one
        print(f"::warning title=TikTok skipped::No video for {spec['id']} on the media branch; marking it skipped.")
        spec = json.load(open(path)); spec["tiktok"] = {"status": "skipped", "message": "video not on the media branch"}
        json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2)
    else:
        print("Nothing due for TikTok has a video."); return
    user = pick_profile()
    caption = spec["caption"][:2200]
    print(f"Posting {spec['id']} to TikTok ({os.path.getsize('tiktok.mp4')/1e6:.1f} MB)")
    if DRY:
        print("DRY_RUN: would post with caption:\n" + caption); return
    sound = trending_sound(user, spec["id"])
    base = ["curl", "-sS", "--max-time", "600", "-H", f"Authorization: Apikey {KEY}",
            "-F", "video=@tiktok.mp4", "-F", f"user={user}", "-F", "platform[]=tiktok",
            "-F", f"title={caption}", "-F", f"tiktok_title={caption}",
            "-F", "privacy_level=PUBLIC_TO_EVERYONE", "-F", "is_aigc=true",  # AI voice and animation: label it
            "-F", f"cover_timestamp={spec.get('cover_offset_ms', 1000)}", "-F", "async_upload=true",
            "-F", f"external_id={spec['id']}"]
    # try the trending sound at volume 0, then 1 (in case 0 is refused), then no sound at all
    tries = ([0, 1] if sound else []) + [None]
    for vol in tries:
        extra = [] if vol is None else ["-F", f"tiktok_music_id={sound['id']}", "-F", f"tiktok_music_volume={vol}",
                                        "-F", "tiktok_original_sound_volume=100"]
        if vol is not None: print(f"Adding trending sound '{sound['title']}' by {sound['artist']} (#{sound['rank']}) at volume {vol}")
        out = subprocess.run(base + extra + [f"{API}/upload"], capture_output=True, text=True)
        try: resp = json.loads(out.stdout)
        except Exception: resp = {"success": False, "message": f"{out.stdout[:500]} {out.stderr[:300]}"}
        if resp.get("request_id") or resp.get("job_id") or resp.get("success") or vol is None: break
        print(f"::warning title=Sound refused::TikTok/Upload-Post refused the sound at volume {vol}: {json.dumps(resp)[:300]}. Retrying.")
    if vol is None: sound = None
    rid = resp.get("request_id") or resp.get("job_id")
    if not rid:
        res = resp.get("results")
        tk = res.get("tiktok") if isinstance(res, dict) else tiktok_result(resp)
        if resp.get("success") and tk and tk.get("success"):
            spec = json.load(open(path)); spec["tiktok"] = {"status": "posted", "url": tk.get("url", "")}
            if sound: spec["tiktok"]["sound"] = {**sound, "volume": vol}
            json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2); print("Posted to TikTok."); return
        fail(f"Upload-Post didn't accept the video: {json.dumps(resp)[:800]}")
    # record the submission straight away, so a later run can never post it twice
    spec = json.load(open(path))
    spec["tiktok"] = {"status": "submitted", "request_id": rid,
                      "submitted_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    if sound: spec["tiktok"]["sound"] = {**sound, "volume": vol}
    json.dump(spec, open(path, "w"), ensure_ascii=False, indent=2)
    print(f"Submitted to TikTok (request {rid}); waiting for TikTok to publish it")
    for _ in range(30):  # up to ~10 minutes; if still busy, the next run picks it up
        time.sleep(20)
        if resolve(path, spec): return
    print("TikTok is still processing; the next run will record the result.")


if __name__ == "__main__":
    main()
