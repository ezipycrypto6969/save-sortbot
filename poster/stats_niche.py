"""Daily stats for the niche accounts (gym, kitchen, hype check, ...), from Upload-Post's post analytics.

Saves Instagram and TikTok numbers into each posted item under "stats" and writes accounts/summary.md:
one table per account plus a format comparison (slideshow vs reel), for the analyst and the marketing council.
Needs secret UPLOAD_POST_API_KEY. Items are judged once they are 3 days old (marked ✓).
"""
import datetime as dt, glob, json, os, statistics, urllib.parse, urllib.request

KEY = "".join(os.environ.get("UPLOAD_POST_API_KEY", "").split())
NOW = dt.datetime.now(dt.timezone.utc)
WINDOW, SETTLED = dt.timedelta(days=28), dt.timedelta(days=3)
KEEP = {"views": "views", "likes": "likes", "comments": "comments", "shares": "shares", "favorites": "saved", "saved": "saved",
        "saves": "saved", "reach": "reach", "new_followers": "new_followers", "profile_views": "profile_views",
        "average_time_watched": "avg_watch_s", "full_video_watched_rate": "full_watch_rate"}


def metrics(rid, platform):
    url = f"https://api.upload-post.com/api/uploadposts/post-analytics/{urllib.parse.quote(rid)}?platform={platform}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": f"Apikey {KEY}"}), timeout=60) as r:
            d = json.loads(r.read() or b"{}")
    except Exception as e:
        print(f"::warning title=Niche stats::{platform} {rid}: {str(e)[:200]}"); return {}
    m = ((d.get("platforms") or {}).get(platform) or {}).get("post_metrics") or {}
    return {v: m[k] for k, v in KEEP.items() if k in m and m[k] is not None}


def when(s): return dt.datetime.fromisoformat((s.get("posted_at") or s["post_at"]).replace("Z", "+00:00"))


def main():
    items = [(p, json.load(open(p))) for p in sorted(glob.glob("accounts/*/queue/*.json"))]
    if KEY:
        for p, s in items:
            rid = (s.get("upload") or {}).get("request_id")
            if s.get("status") != "posted" or not rid or NOW - when(s) > WINDOW: continue
            st = s.get("stats") or {}
            for plat in (s["upload"].get("platforms") or ["instagram", "tiktok"]):
                st[plat] = metrics(rid, plat) or st.get(plat, {})
            st["total_views"] = sum((st.get(k) or {}).get("views", 0) or 0 for k in ("instagram", "tiktok"))
            st["total_engagement"] = sum(sum((st.get(k) or {}).get(m, 0) or 0 for m in ("likes", "comments", "shares", "saved")) for k in ("instagram", "tiktok"))
            st["new_followers"] = sum((st.get(k) or {}).get("new_followers", 0) or 0 for k in ("instagram", "tiktok"))
            st["updated"] = NOW.isoformat(timespec="seconds"); s["stats"] = st
            json.dump(s, open(p, "w"), ensure_ascii=False, indent=2)
        items = [(p, json.load(open(p))) for p in sorted(glob.glob("accounts/*/queue/*.json"))]
    out = [f"# Niche account performance (updated {NOW.astimezone(dt.timezone(dt.timedelta(hours=8))):%a %d %b %Y %H:%M} Perth)", "",
           "Views and engagement summed across Instagram and TikTok. Engagement = likes + comments + shares + saves. ✓ = 3+ days old.", ""]
    accts = sorted({p.split("/")[1] for p, _ in items})
    fmt_rows = {}
    for a in accts:
        rows = []
        for p, s in items:
            if not p.startswith(f"accounts/{a}/") or s.get("status") != "posted" or not s.get("stats"): continue
            st = s["stats"]; v = st.get("total_views", 0); e = st.get("total_engagement", 0)
            settled = NOW - when(s) >= SETTLED
            rows.append((v, f"| {'✓' if settled else ''} | {(s.get('caption') or '').split(chr(10))[0][:55]} | {s.get('format','reel')} | {s.get('style','')} | "
                            f"{s.get('hook_type','')} | {v:,} | {(st.get('instagram') or {}).get('views','-')} | {(st.get('tiktok') or {}).get('views','-')} | "
                            f"{e / v if v else 0:.1%} | {st.get('new_followers', 0)} | {s['id']} |"))
            if settled: fmt_rows.setdefault((a, s.get("format", "reel")), []).append((v, e / v if v else 0))
        out += [f"## {a}", ""]
        if not rows: out += ["(nothing posted yet)", ""]; continue
        out += ["| ✓ | Post | Format | Style | Hook | Views | IG | TikTok | Eng. rate | New followers | Queue file |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        out += [r for _, r in sorted(rows, reverse=True)] + [""]
    out += ["## Format comparison (judged posts only)", "", "| Account | Format | Posts | Median views | Median engagement rate |", "|---|---|---|---|---|"]
    for (a, f), rs in sorted(fmt_rows.items()):
        out.append(f"| {a} | {f} | {len(rs)} | {statistics.median(r[0] for r in rs):,.0f} | {statistics.median(r[1] for r in rs):.1%} |")
    if not fmt_rows: out.append("| (nothing old enough yet) | | | | |")
    open("accounts/summary.md", "w").write("\n".join(out) + "\n")
    print("Wrote accounts/summary.md")


if __name__ == "__main__":
    main()
