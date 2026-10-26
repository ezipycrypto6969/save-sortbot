"""Five more long SaveSort ads (45-60s) in the style of ad-j: real footage of the SaveSort site sorting a real
Instagram export, packed with checkable info from those saves, and a bit of Sorty humour.
Facts come from the verified breakdowns (prices in USD, rounded, "about" where they vary).
Run from the repo root: python3 content/ads_v5.py
"""
import json, os

END = lambda vo, line="Sort your saves.\n*Free.*": {"type": "end", "line": line, "pill": "Link in bio →", "vo": vo,
                                                     "mascot": {"pos": "tr", "mood": "happy"}}
PL = lambda mood="happy": {"pos": "pl", "mood": mood}
TR = lambda mood="happy": {"pos": "tr", "mood": mood}
STATS = {"x": 30, "y": 118, "w": 720, "h": 420}
CHIP = {"go": (250, 1728), "warn": (128, 1808), "gate": (370, 1808)}
TOP = 1650
META = json.load(open("engine/screens/meta.json"))


def chip(k, label, vo, mood="happy", payoff=False):
    shot = {"go": "report-go.png", "warn": "report-warn.png", "gate": "report-gate.png"}[k]
    s = {"type": "screen", "label": label, "segs": [{"shot": "report-all.png", "from": TOP}, {"shot": shot, "from": TOP, "to": 3200, "t0": 0.3, "t1": 0.95}],
         "taps": [{"at": 0.18, "x": CHIP[k][0], "y": CHIP[k][1]}], "mascot": PL(mood), "vo": vo}
    if payoff: s["payoff"] = True
    return s


def topic(key, label, vo, mood="happy"):
    tap = META["topics"][key]["tap"]
    return {"type": "screen", "label": label, "segs": [{"shot": "report-all.png", "from": 500}, {"shot": f"topic-{key}.png", "from": TOP, "to": 3200, "t0": 0.35, "t1": 0.95}],
            "taps": [{"at": 0.2, "x": tap["x"], "y": tap["y"]}], "mascot": PL(mood), "vo": vo}


def stats(label, vo, mood="shocked"):
    return {"type": "screen", "label": label, "segs": [{"shot": "report-all.png", "from": 0}], "highlights": [dict(STATS, at=0.15)],
            "zoom": {"at": 0.12, "s": 1.1, "x": 390, "y": 330}, "mascot": PL(mood), "vo": vo}


def drop(vo, label="DROP THE ZIP IN"):
    return {"type": "screen", "label": label, "segs": [{"shot": "drop.png", "from": 560}], "drop": {"at": 0.25, "x": 390, "y": 1180}, "mascot": PL("happy"), "vo": vo}


def react(quote, verdict, color, mood, vo, payoff=False):
    s = {"type": "react", "quote": quote, "mood": mood, "verdict": verdict, "verdictColor": color, "vo": vo}
    if payoff: s["payoff"] = True
    return s


ADS = {
 "ad-n-ai-hustles": {"fx": {"hook": "WAIT FOR THE LAST ONE"}, "scenes": [
   {"type": "hook", "lines": ["My saves said I'd be", "*rich by Tuesday.*"], "mascot": {"pos": "bl", "mood": "smug"},
    "vo": "My saved reels promised I'd be rich by Tuesday. It's Wednesday."},
   {"type": "talk", "text": "So I let SaveSort\n*fact check them.*", "mood": "suspicious", "vo": "So I dropped them into SaveSort to see which AI hustles are real."},
   topic("AI", "TAP AI & TOOLS", "Tap AI and tools. 33 saves. Let's check four of them.", "smug"),
   react("Build an AI receptionist and sell it to local businesses", "WORTH DOING", "go", "happy",
         "AI receptionist? Real. Tools like Vapi run about 30 cents a minute all in. Test it hard before you sell it."),
   react("A free AI agent that finds you clients", "WORTH DOING", "go", "shocked",
         "A free AI that finds clients? Real and open source. It runs on Claude Pro, 20 dollars a month. You approve every email."),
   react("Build any app with one prompt", "BE CAREFUL", "warn", "suspicious",
         "Any app in one prompt? Half true. Lovable's free plan gives you 5 credits a day. Big apps eat them fast."),
   react("Run 100 AI agents at once", "BE CAREFUL", "warn", "smug",
         "100 agents at once? You'll hit your limit before lunch. 3 to 5 is the useful number.", payoff=True),
   {"type": "talk", "text": "2 real. 2 hype.\n*Still not rich.*", "mood": "sad", "vo": "Two real, two hype. Still not rich. But now I know where to start."},
   END("Tap the link in bio and fact check your saves free.")]},

 "ad-o-free-tools": {"fx": {"hook": "#1 IS COMPLETELY FREE"}, "scenes": [
   {"type": "hook", "lines": ["Stop paying", "for *free stuff.*"], "mascot": {"pos": "bl", "mood": "shocked"},
    "vo": "Half my saved reels were trying to sell me things that are free."},
   drop("I dropped my saves into SaveSort. It runs on your phone. Nothing gets uploaded."),
   chip("go", "TAP WORTH DOING", "Tap worth doing. Turns out a lot of the good stuff costs nothing.", "happy"),
   {"type": "count", "n": 4, "label": "Spy on any brand's ads:\n*Meta Ad Library*", "mascot": TR("smug"),
    "vo": "Number 4. Paying for an ad spy tool? Meta's Ad Library shows every active ad. Free."},
   {"type": "count", "n": 3, "label": "Rank on Google Maps:\n*Business Profile*", "mascot": TR("happy"),
    "vo": "Number 3. Google Business Profile is free. Fill every field, post photos weekly, reply to every review."},
   {"type": "count", "n": 2, "label": "A free *offline*\nsurvival computer", "mascot": TR("shocked"),
    "vo": "Number 2. A free, open source offline computer. Offline Wikipedia, maps and a local AI. No internet needed."},
   {"type": "count", "n": 1, "label": "Learn cyber security:\n*free tier first*", "mascot": TR("happy"), "payoff": True,
    "vo": "Number 1. Want to learn cyber security? Try Hack Me has a free tier. Start with Linux and networking."},
   {"type": "talk", "text": "My wallet\n*thanks me.*", "mood": "smug", "vo": "My wallet would like to thank SaveSort personally."},
   END("Tap the link in bio and find your free stuff.")]},

 "ad-p-boring-business": {"fx": {"hook": "WAIT FOR #1"}, "scenes": [
   {"type": "hook", "lines": ["Skip the", "*AI startup.*"], "mascot": {"pos": "bl", "mood": "smug"},
    "vo": "Skip the AI startup. My saves had better ideas. They're just boring."},
   topic("BIZ", "TAP SIDE HUSTLES", "SaveSort sorted my business and side hustle saves. Here's what held up.", "happy"),
   {"type": "count", "n": 3, "label": "Gutters & high windows\n*nobody wants to do*", "mascot": TR("smug"),
    "vo": "Number 3. Gutter and window cleaning. One reel says homeowners pay 250 to 300 dollars to skip it. Get insured, respect ladders."},
   {"type": "count", "n": 2, "label": "Pressure washing:\n*one job, whole street*", "mascot": TR("happy"),
    "vo": "Number 2. Pressure washing. Do one house well and the neighbours notice. Check local rules on runoff."},
   {"type": "count", "n": 1, "label": "An AI receptionist\n*for trades*", "mascot": TR("shocked"), "payoff": True,
    "vo": "Number 1. Plumbers and electricians miss calls on the job. An AI receptionist answers every call and books the work."},
   {"type": "steps", "heading": "The boring secret", "items": ["Inspection sheet", "Job checklist", "Final quality check", "Every single job"],
    "vo": "The secret that keeps them running? Written systems. An inspection sheet, a checklist, and a final check on every job."},
   chip("go", "THE REST: WORTH DOING", "SaveSort found 30 saves like this worth doing. All in one list.", "happy"),
   {"type": "talk", "text": "Boring?\n*Yes. Paying? Often.*", "mood": "smug", "vo": "Boring? Yes. Glamorous? No. Paying? Often."},
   END("Tap the link in bio and sort your saves free.")]},

 "ad-q-comment-guide": {"fx": {"hook": "THE LAST ONE IS THE WORST"}, "scenes": [
   {"type": "talk", "text": "22 of my saves\nwanted a *comment.*", "mood": "shocked", "vo": "22 of my saved reels wouldn't tell me anything unless I commented."},
   drop("So I dropped my saves into SaveSort."),
   chip("gate", "TAP GATED GUIDES", "Tap gated guides, and there they all are. Let's open a few.", "suspicious"),
   react("Comment PHONE and I'll send the setup", "GATED GUIDE", "gate", "smug",
         "Comment phone? It connects Claude Code to an AI phone service, so it rings you. Free plan, then about 9 cents a minute."),
   react("Comment DESIGN for my 3 skills", "GATED GUIDE", "gate", "happy",
         "Comment design? Three design skills for Claude. Free, and public anyway."),
   react("Comment SCALE to grow your business", "NO DETAILS", "gate", "sad",
         "Comment scale? No tip at all. Just a sales call waiting to happen.", payoff=True),
   {"type": "talk", "text": "Plot twist:\n*it was free.*", "mood": "smug", "vo": "Plot twist. Most of it was free all along. No comment needed."},
   {"type": "checks", "heading": "Before you comment", "label": "30 SECOND CHECK", "items": ["Steps in the caption?", "Search the tool's name", "Is it free already?", "Then decide"], "lastWarn": False,
    "vo": "Before you comment, check the caption, search the tool's name, see if it's free. Then decide."},
   END("Tap the link in bio and find your gated guides.")]},

 "ad-r-ai-myths": {"fx": {"hook": "#4 IS THE BIGGEST LIE"}, "scenes": [
   {"type": "hook", "lines": ["My saves taught me", "*fake AI features.*"], "mascot": {"pos": "bl", "mood": "suspicious"},
    "vo": "My saved reels taught me AI features that don't exist."},
   stats("MY 156 SAVES", "SaveSort read all 156 of my saves. 10 got flagged be careful. Here are four.", "suspicious"),
   react("Claude has a secret Founder Thinking Mode", "BE CAREFUL", "warn", "smug",
         "Founder thinking mode? Not a real feature. It's a prompt wearing a costume."),
   react("Turn on ADHD Executive Function Mode", "BE CAREFUL", "warn", "suspicious",
         "Not a feature either. The prompts are good though. Just call them prompts."),
   react("Run 100 subagents at once", "BE CAREFUL", "warn", "shocked",
         "100 agents? You'll hit your usage limit before lunch. 3 to 5 is plenty."),
   react("Make $1M in 90 days with AI", "BE CAREFUL", "warn", "sad",
         "A million in 90 days? If that worked, they wouldn't be selling the course.", payoff=True),
   chip("warn", "TAP BE CAREFUL", "SaveSort puts all of these in one list, so you skip them.", "suspicious"),
   {"type": "talk", "text": "No secret modes.\nJust *good prompts.*", "mood": "happy", "vo": "No secret modes. Just good prompts, and actually doing the thing."},
   END("Tap the link in bio and check your saves free.")]},
}

os.makedirs("ads", exist_ok=True)
for aid, ad in ADS.items():
    spec = {"id": aid, "format": "ad", "status": "draft", "voice": "am_onyx*0.55+am_puck*0.45", "pitch": 1.5, "speed": 1.22, "music": "sfx",
            "fx": ad["fx"], "scenes": ad["scenes"], "caption": ""}
    json.dump(spec, open(f"ads/{aid}.json", "w"), ensure_ascii=False, indent=2)
print(len(ADS), "long ads written")
