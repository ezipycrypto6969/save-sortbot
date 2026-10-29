"""Collects views and engagement for every posted reel from Instagram, YouTube and TikTok (via Upload-Post),
saves them in each queue file under "stats", and writes stats/summary.md for the Sunday content run.

Runs daily in GitHub Actions (.github/workflows/stats.yml). Every platform is optional: if its keys are missing,
or an API refuses a metric, it is skipped and the rest still work.
Usage: python3 poster/stats.py            fetch stats, update queue files, write the summary
       python3 poster/stats.py --summary  only rebuild stats/summary.md from the saved stats (no API calls)
"""
import datetime as dt, glob, json, os, statistics, sys, urllib.parse, urllib.request

NOW = dt.datetime.now(dt.timezone.utc)
WINDOW = dt.timedelta(days=28)   # keep refreshing stats for posts up to 4 weeks old
SETTLED = dt.timedelta(days=3)   # a reel is judged only after 3 days

IG_TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
YT = {k: "".join(os.environ.get(k, "").split()) for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")}
UP_KEY = "".join(os.environ.get("UPLOAD_POST_API_KEY", "").split())
HIDE = [s for s in (IG_TOKEN, YT["YT_CLIENT_SECRET"], YT["YT_REFRESH_TOKEN"], UP_KEY) if s]


def warn(msg):
    for s in HIDE: msg = msg.replace(s, "***")
    print(f"::warning title=Stats::{msg}")


def http(method, url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"{}")


def safe(fn, label):
    try: return fn()
    except urllib.error.HTTPError as e: warn(f"{label}: HTTP {e.code} {e.read().decode(errors='replace')[:300]}")
    except Exception as e: warn(f"{label}: {e}")
    return None


def ig_stats(media_id):
    base = f"https://graph.instagram.com/v21.0/{media_id}"
    q = urllib.parse.urlencode({"metric": "views,reach,likes,comments,shares,saved,ig_reels_avg_watch_time", "access_token": IG_TOKEN})
    try:
        data = http("GET", f"{base}/insights?{q}").get("data", [])
        out = {m["name"]: (m.get("values") or [{}])[0].get("value", m.get("total_value", {}).get("value")) for m in data}
        if "ig_reels_avg_watch_time" in out and out["ig_reels_avg_watch_time"] is not None:
            out["avg_watch_s"] = round(out.pop("ig_reels_avg_watch_time") / 1000, 1)
        return {k: v for k, v in out.items() if v is not None}
    except urllib.error.HTTPError:
        # token may lack the insights permission: fall back to public counters
        q = urllib.parse.urlencode({"fields": "like_count,comments_count", "access_token": IG_TOKEN})
        d = safe(lambda: http("GET", f"{base}?{q}"), f"Instagram {media_id}") or {}
        return {k: v for k, v in {"likes": d.get("like_count"), "comments": d.get("comments_count")}.items() if v is not None}


def yt_token():
    body = urllib.parse.urlencode({"client_id": YT["YT_CLIENT_ID"], "client_secret": YT["YT_CLIENT_SECRET"],
                                   "refresh_token": YT["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return http("POST", "https://oauth2.googleapis.com/token", body,
                {"Content-Type": "application/x-www-form-urlencoded"})["access_token"]


def yt_stats(ids, token):
    out = {}
    for i in range(0, len(ids), 50):
        q = urllib.parse.urlencode({"part": "statistics", "id": ",".join(ids[i:i + 50])})
        d = safe(lambda: http("GET", f"https://www.googleapis.com/youtube/v3/videos?{q}", headers={"Authorization": f"Bearer {token}"}), "YouTube") or {}
        for v in d.get("items", []):
            s = v.get("statistics", {})
            out[v["id"]] = {k2: int(s[k1]) for k1, k2 in (("viewCount", "views"), ("likeCount", "likes"), ("commentCount", "comments")) if k1 in s}
    return out


def tt_stats(request_id):
    url = f"https://api.upload-post.com/api/uploadposts/post-analytics/{urllib.parse.quote(request_id)}?platform=tiktok"
    d = safe(lambda: http("GET", url, headers={"Authorization": f"Apikey {UP_KEY}"}), f"TikTok {request_id}") or {}
    m = ((d.get("platforms") or {}).get("tiktok") or {}).get("post_metrics") or {}
    keep = {"views": "views", "likes": "likes", "comments": "comments", "shares": "shares", "favorites": "saved",
            "new_followers": "new_followers", "profile_views": "profile_views", "average_time_watched": "avg_watch_s",
            "full_video_watched_rate": "full_watch_rate"}
    return {v: m[k] for k, v in keep.items() if k in m}


def posted_at(spec):
    t = spec.get("posted_at") or spec.get("post_at")
    return dt.datetime.fromisoformat(t.replace("Z", "+00:00"))


def style_of(spec):
    return spec.get("style") or ("funny-ad" if spec.get("format") == "ad" else "base")


def totals(st):
    plats = [st.get(p) or {} for p in ("instagram", "youtube", "tiktok")]
    views = sum(p.get("views", 0) or 0 for p in plats)
    eng = sum((p.get("likes", 0) or 0) + (p.get("comments", 0) or 0) + (p.get("shares", 0) or 0) + (p.get("saved", 0) or 0) for p in plats)
    return views, eng


def fetch(specs):
    yt_tok = safe(yt_token, "YouTube login") if all(YT.values()) else None
    yt_ids = [s["youtube"]["video_id"] for _, s in specs if (s.get("youtube") or {}).get("video_id")]
    yt = yt_stats(yt_ids, yt_tok) if yt_tok and yt_ids else {}
    for path, s in specs:
        st = s.get("stats") or {}
        if IG_TOKEN and s.get("media_id"): st["instagram"] = ig_stats(s["media_id"]) or st.get("instagram", {})
        vid = (s.get("youtube") or {}).get("video_id")
        if vid in yt: st["youtube"] = yt[vid]
        rid = (s.get("tiktok") or {}).get("request_id")
        if UP_KEY and rid: st["tiktok"] = tt_stats(rid) or st.get("tiktok", {})
        st["total_views"], st["total_engagement"] = totals(st)
        st["updated"] = NOW.isoformat(timespec="seconds")
        s["stats"] = st
        json.dump(s, open(path, "w"), ensure_ascii=False, indent=2)
    print(f"Updated stats for {len(specs)} posted reels.")


def summary(all_specs):
    rows = []
    for _, s in all_specs:
        if s.get("status") != "posted" or not s.get("stats"): continue
        st = s["stats"]; v = st.get("total_views", 0); e = st.get("total_engagement", 0)
        age = NOW - posted_at(s)
        rows.append(dict(id=s["id"], title=(s.get("yt_title") or s.get("caption", "").split("\n")[0])[:60], style=style_of(s),
                         hook=s.get("hook_type", ""), views=v, eng=e, rate=(e / v if v else 0), settled=age >= SETTLED,
                         ig=(st.get("instagram") or {}).get("views", "-"), yt=(st.get("youtube") or {}).get("views", "-"),
                         tt=(st.get("tiktok") or {}).get("views", "-"), days=age.days))
    rows.sort(key=lambda r: r["views"], reverse=True)
    lines = [f"# Reel performance (updated {NOW.astimezone(dt.timezone(dt.timedelta(hours=8))):%a %d %b %Y %H:%M} Perth)", "",
             "Views and engagement are summed across Instagram, YouTube and TikTok. Engagement = likes + comments + shares + saves.",
             f"Only reels at least {SETTLED.days} days old count towards style results (marked ✓).", "", "## By style", "",
             "| Style | Judged reels | Median views | Median engagement rate | Best reel |", "|---|---|---|---|---|"]
    by = {}
    for r in rows:
        if r["settled"]: by.setdefault(r["style"], []).append(r)
    for style, rs in sorted(by.items(), key=lambda kv: -statistics.median([r["views"] for r in kv[1]])):
        lines.append(f"| {style} | {len(rs)} | {statistics.median([r['views'] for r in rs]):,.0f} | "
                     f"{statistics.median([r['rate'] for r in rs]):.1%} | {rs[0]['title']} |")
    if not by: lines.append("| (no reels old enough yet) | | | | |")
    lines += ["", "## Every posted reel (most views first)", "",
              "| ✓ | Reel | Style | Hook | Days | Views | IG | YT | TikTok | Eng. rate | Queue file |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {'✓' if r['settled'] else ''} | {r['title']} | {r['style']} | {r['hook']} | {r['days']} | {r['views']:,} | "
                     f"{r['ig']} | {r['yt']} | {r['tt']} | {r['rate']:.1%} | {r['id']} |")
    os.makedirs("stats", exist_ok=True)
    open("stats/summary.md", "w").write("\n".join(lines) + "\n")
    print("Wrote stats/summary.md")


def main():
    all_specs = [(p, json.load(open(p))) for p in sorted(glob.glob("queue/*.json"))]
    if "--summary" not in sys.argv:
        recent = [(p, s) for p, s in all_specs if s.get("status") == "posted" and NOW - posted_at(s) <= WINDOW]
        fetch(recent)
        all_specs = [(p, json.load(open(p))) for p in sorted(glob.glob("queue/*.json"))]
    summary(all_specs)


if __name__ == "__main__":
    main()
