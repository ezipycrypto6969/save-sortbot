"""Diabolical hook generator: spits out over-the-top (but true) opening lines about the saved-reels problem.

Every hook is a cold-open `title` scene: short on-screen text (with *marker*) + a spoken `vo` line of 9 words or fewer (about 1.5 s).
Numbers aimed at the viewer can be big (300, 500, 1,000); "I"/"my" lines only ever use the owner's real 156.
Skips hooks already used in the queue in the last 28 days and hooks marked [used ...] in content/hooks.md.

Usage (repo root):
  python3 content/hookgen.py                 # 25 fresh hooks, mixed families
  python3 content/hookgen.py --n 60 --seed 7 # more, different shuffle
  python3 content/hookgen.py --family funeral --n 10
  python3 content/hookgen.py --json          # machine-readable, ready to paste as a scene
  python3 content/hookgen.py --min-score 0   # include weak hooks (default keeps hookscore 60+, best first)
"""
import argparse, datetime as dt, glob, itertools, json, os, random, re, subprocess, sys

N = ["300", "500", "800", "1,000"]
THINGS = [  # (plural, singular, where you'd actually use it)
    ("gym routines", "gym routine", "gym"), ("recipes", "recipe", "kitchen"), ("side hustles", "side hustle", "bank account"),
    ("morning routines", "morning routine", "mornings"), ("study hacks", "study hack", "exams"),
    ("budget tips", "budget tip", "bank account"), ("skincare routines", "skincare routine", "bathroom"),
    ("date ideas", "date idea", "weekends"), ("cleaning hacks", "cleaning hack", "house"), ("AI tools", "AI tool", "laptop"),
]

T = {  # family -> list of (on-screen text, vo, needs) ; {n} viewer number, {p}/{s}/{w} thing plural/singular/where
    "funeral": [
        ("Time of death:\n*the day you hit save.*", "Time of death. The day you hit save.", ""),
        ("Rest in peace,\n*{n} saved {p}.*", "Rest in peace, {n} saved {p}.", "nt"),
        ("Breaking: {n} reels\n*missing.*", "Breaking news. {n} saved reels missing. Presumed forgotten.", "n"),
        ("Crime scene:\n*{n} victims.*", "Your saved tab is a crime scene. {n} victims.", "n"),
        ("{n} saves?\nYour tab is *haunted.*", "{n} saved reels? Your saved tab is haunted.", "n"),
    ],
    "warning": [
        ("Do not open\nyour *saved tab.*", "Do not open your saved tab. Seriously.", ""),
        ("Hit save again.\n*I dare you.*", "Hit save one more time. I dare you.", ""),
        ("Stop. Saving.\n*Reels.*", "Stop. Saving. Reels. Watch this first.", ""),
        ("This is your sign\nto *delete {n}.*", "This is your sign to delete {n} saved reels.", "n"),
        ("Warning: this reel\n*judges your saves.*", "Warning. This reel is about to judge your saves.", ""),
    ],
    "callout": [
        ("{n} saved {p}.\n*Done: 0.*", "{n} saved {p}? Done zero? Thought so.", "nt"),
        ("Your saves have more\n{p} than your *{w}.*", "Your saves have more {p} than your {w}.", "t"),
        ("Past {n} saves?\nThis is an *intervention.*", "Past {n} saves? This is an intervention.", "n"),
        ("Saving it isn't\n*doing it.*", "Saving it isn't doing it. Sorry.", ""),
        ("I broke\n*156 promises.*", "Every saved reel is a promise. I broke 156.", ""),
        ("Your future self\nis *furious.*", "Your future self is furious.", ""),
        ("Those {p}\nare *laughing at you.*", "Those {p} you saved are laughing at you.", "t"),
    ],
    "challenge": [
        ("Name 3 reels\nyou saved. *Go.*", "Name 3 reels you saved last month. I'll wait.", ""),
        ("Find one {s}\nin your saves. *10 seconds.*", "Find one {s} you saved. 10 seconds.", "t"),
        ("How many saves?\n*Don't lie.*", "How many saved reels have you got? Don't lie.", ""),
        ("Guess how many\nwere *worth it.*", "156 saves. Guess how many were worth it.", ""),
    ],
    "absurd": [
        ("Diagnosis:\n*chronic saver.*", "Diagnosis. Chronic reel saver. The cure is coming.", ""),
        ("Your saved tab just\n*filed for divorce.*", "Your saved tab just filed for divorce.", ""),
        ("Your saved tab\nneeds *a lawyer.*", "Your saved tab needs a lawyer.", ""),
        ("Confession: I'm a\n*reel hoarder.*", "Confession. I'm a reel hoarder. 156 saves.", ""),
        ("156 saves.\nWatched again: *0.*", "156 saved reels. Watched again? Zero.", ""),
        ("POV: you saved it\n*\"for later.\"*", "POV. You saved it for later. Two years ago.", ""),
    ],
}


def used_recently():
    seen = set()
    cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=28)
    for p in glob.glob("queue/*.json") + glob.glob("accounts/*/queue/*.json"):
        try:
            d = json.load(open(p))
            if dt.datetime.fromisoformat(d["post_at"]) >= cut and d.get("scenes"):
                seen.add(norm(d["scenes"][0].get("vo", "")))
        except Exception: pass
    if os.path.exists("content/hooks.md"):
        for line in open("content/hooks.md"):
            if "[used" in line:
                m = re.search(r'"([^"]+)"', line)
                if m: seen.add(norm(m.group(1)))
    return seen


def norm(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def generate(family=None, seed=None):
    out = []
    for fam, rows in T.items():
        if family and fam != family: continue
        for text, vo, needs in rows:
            ns = N if "n" in needs else [None]
            ts = THINGS if "t" in needs else [None]
            for n, t in itertools.product(ns, ts):
                f = dict(n=n or "", p=t[0] if t else "", s=t[1] if t else "", w=t[2] if t else "")
                out.append({"family": fam, "tid": text, "text": text.format(**f), "vo": vo.format(**f)})
    seen = used_recently()
    out = [h for h in out if norm(h["vo"]) not in seen and len(h["vo"].split()) <= 9
           and len(re.sub(r"[*\n]", " ", h["text"]).split()) <= 7]
    rnd = random.Random(seed)
    rnd.shuffle(out)
    # interleave families so the top of the list is varied
    by = {}
    for h in out: by.setdefault(h["family"], []).append(h)
    mixed = [h for grp in itertools.zip_longest(*by.values()) for h in grp if h]
    return mixed


def score(hooks):
    """Score each hook's vo with team/tools/hookscore.py (if present). Adds h["score"]."""
    tool = os.path.join("team", "tools", "hookscore.py")
    if not os.path.exists(tool) or not hooks: return hooks
    r = subprocess.run([sys.executable, tool, "--json", "-"], input="\n".join(h["vo"] for h in hooks),
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout); d = d if isinstance(d, list) else d.get("hooks", d)
        for h, x in zip(hooks, d): h["score"] = round(x["score"], 1)
    except Exception: pass
    return hooks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=25)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--family", choices=list(T))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-score", type=float, default=60, help="drop hooks hookscore rates below this (0 = keep all)")
    a = ap.parse_args()
    hooks = score(generate(a.family, a.seed))
    hooks = [h for h in hooks if h.get("score", 100) >= a.min_score]
    hooks.sort(key=lambda h: -h.get("score", 0))
    first, rest, seen = [], [], set()  # one version of each idea first, then the number/topic variants
    for h in hooks: (rest if h["tid"] in seen else first).append(h); seen.add(h["tid"])
    hooks = (first + rest)[:a.n]
    if a.json:
        print(json.dumps([{"type": "title", "text": h["text"], "vo": h["vo"], "bg": "paper", "clean": True,
                           "_hook_type": "crazy-" + h["family"], "_hook_score": h.get("score")} for h in hooks], ensure_ascii=False, indent=1))
    else:
        for i, h in enumerate(hooks, 1):
            print(f"{i:>2}. {h.get('score', '-'):>5} [{h['family']}] {h['text'].replace(chr(10), ' / ')}   ->  \"{h['vo']}\"")


if __name__ == "__main__":
    main()
