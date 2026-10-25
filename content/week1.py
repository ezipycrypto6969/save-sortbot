"""Writes week one's queue files (26 Oct – 1 Nov 2026). Run from the repo root: python3 content/week1.py"""
import json, os

END = {"type": "end", "line": "Sort your saves.\n*Free.*", "pill": "Link in bio →", "vo": "Tap the link in bio and sort yours now.", "mascot": {"pos": "tr", "mood": "happy"}}
SIGN = "\n\nFound in my own saved reels and sorted by SaveSort. Sort yours free, link in bio."

posts = [
 ("2026-10-26", 2, "reveal-156", "reveal",
  "I saved 156 reels. I watched none of them again. 💀" "\n\nSo I sorted them:\n✅ 24 actually worth doing\n🤷 61 said nothing without the video\n⚠️ 7 were hype or straight-up scams" + SIGN + "\n\n#savedreels #productivity #aitools #sidehustle",
  [{"type": "hook", "lines": ["I saved", "*156 reels.*"], "vo": "I saved a hundred and fifty six reels."},
   {"type": "hook", "lines": ["Watched again:", "*zero.*"], "slow": True, "grey": True, "vo": "Watched them again? Zero."},
   {"type": "stat", "value": 24, "label": "actually worth doing", "color": "go", "vo": "Twenty four were actually useful. Past me had taste."},
   {"type": "quote", "quote": "Claude has a secret Founder Thinking Mode", "note": "That feature doesn't exist. It's a prompt dressed up as a secret.", "stamp": "BE CAREFUL", "stampColor": "warn", "vo": "A secret Claude mode? Mate. No."},
   END]),
 ("2026-10-27", 1, "harvey-sales-agent", "breakdown",
  "\"Comment HARVEY for the repo\" 🙄 It's free and public. Here's what it is.\n\nHarvey is an open-source sales agent that runs on Claude Code on your own computer:\n1. Finds local businesses\n2. Checks their website and scores them\n3. Writes a personal cold email\n4. Waits for YOU to approve every send\n\nRuns on your Claude plan, no API bill. Cold email has rules in most countries: use business addresses, say who you are, include an unsubscribe link." + SIGN + "\n\n#claudeai #aiagents #sidehustle #coldemail",
  [{"type": "quote", "quote": "Comment HARVEY and I'll send you the repo", "note": "It's free and public on GitHub.", "stamp": "GATED GUIDE", "stampColor": "gate", "vo": "This reel wanted a comment for a free GitHub link. Here it is."},
   {"type": "title", "text": "A free AI agent\nthat finds\n*clients.*", "vo": "Harvey. A free AI sales agent that runs on your own computer."},
   {"type": "checks", "heading": "What it does", "label": "HARVEY · OPEN SOURCE", "items": ["Finds local businesses", "Scores each one", "Writes the cold email", "You approve every send"], "lastWarn": True, "vo": "It finds businesses, scores them, writes the email, and waits for you to approve it."},
   {"type": "title", "text": "You approve\n*every email.*", "bg": "ink", "vo": "And nothing sends until you approve it."},
   END]),
 ("2026-10-27", 2, "adhd-mode-myth", "scam-watch",
  "There is no \"ADHD Executive Function Mode\" in Claude. 🚫\n\nBut the prompts in that reel actually work:\n1. Break a task into steps under 1 minute, give me only the first\n2. Act as my body double and check in every 10 minutes\n3. Turn this boring task into a quest with a reward" + SIGN + "\n\n#adhd #productivity #claudeai #aitips",
  [{"type": "quote", "quote": "BREAKING: Claude has an ADHD Executive Function Mode", "stamp": "BE CAREFUL", "stampColor": "warn", "vo": "Breaking news. Claude does not have an ADHD mode."},
   {"type": "title", "text": "It's just a\n*prompt.*", "vo": "It's just a prompt. But honestly? A good one."},
   {"type": "steps", "heading": "Prompts that work", "items": ["Break it into one minute steps", "Give me only the first step", "Check in every ten minutes", "Make the boring task a quest"], "vo": "Ask for tiny steps. Just the first one. Check ins every ten minutes. Make it a quest."},
   END]),
 ("2026-10-28", 1, "ai-receptionist", "breakdown",
  "Tradies miss calls on the tools. Every missed call is a missed job. 📞\n\nThe side hustle: build an AI receptionist that answers 24/7 and books jobs.\n1. Pick one niche: tradies, dentists, salons, mechanics\n2. Collect their hours, services and FAQs\n3. Build it in Vapi or Retell\n4. Demo it with THEIR business details\n5. Free trial, then setup fee + monthly\n\nTell callers it's an AI and check call-recording rules." + SIGN + "\n\n#sidehustle #aiagents #smallbusiness #tradies",
  [{"type": "quote", "quote": "Comment VOICE for the free guide", "stamp": "GATED GUIDE", "stampColor": "gate", "vo": "Another reel hiding the guide. Fine. I'll do it."},
   {"type": "title", "text": "Sell an AI\n*receptionist.*", "vo": "The side hustle. An AI that answers the phone for tradies."},
   {"type": "steps", "heading": "How to start", "items": ["Pick one niche", "Collect their FAQs", "Build it in Vapi", "Demo it with their details"], "vo": "Pick one niche. Collect their questions. Build it in Vapi. Demo it with their own business."},
   {"type": "title", "text": "Setup fee.\n*Then monthly.*", "bg": "ink", "vo": "Charge a setup fee, then monthly. Tell callers it's an AI."},
   END]),
 ("2026-10-28", 2, "meta-ad-library", "tool",
  "Stop paying for ad spy tools. Meta gives you this for free. 🔍\n\nMeta Ad Library shows every ad running on Facebook and Instagram.\n1. Search a competitor or keyword\n2. Pick your country\n3. Look for ads running for months: brands keep paying for what works\n4. Copy the idea, never the ad itself" + SIGN + "\n\n#metaads #marketing #smallbusiness #facebookads",
  [{"type": "quote", "quote": "Comment TIER for a tool to spy on any brand's ads", "stamp": "GATED GUIDE", "stampColor": "gate", "vo": "This reel sells a paid spy tool. Meta made a free one."},
   {"type": "title", "text": "Meta\n*Ad Library.*", "vo": "It's called the Meta Ad Library. It's free."},
   {"type": "steps", "heading": "How to use it", "items": ["Search a competitor", "Pick your country", "Find ads running for months", "Copy the idea, not the ad"], "vo": "Search a competitor. Find the ads that have run for months. They work."},
   END]),
 ("2026-10-29", 1, "how-savesort-works", "product",
  "Your saved reels, sorted in 30 seconds ⏱️\n\n1. Instagram → Settings → Accounts Center → Download your information\n2. Tick only \"Saved\" and download\n3. Drop the zip into SaveSort\n4. Get one list: sorted by topic, what's worth doing, what's hype, what's hiding a guide\n\nFree, and it runs in your browser. Nothing gets uploaded." + SIGN + "\n\n#savedreels #productivity #instagramtips #aitools",
  [{"type": "talk", "text": "Your saved reels\nare a *mess.*", "mood": "shocked", "vo": "Your saved reels are a mess. Let's fix that in 30 seconds."},
   {"type": "steps", "heading": "How it works", "items": ["Download your Instagram data", "Tick only \"Saved\"", "Drop the zip into SaveSort", "Get your sorted list"], "vo": "Download your Instagram data. Tick saved. Drop the zip into SaveSort. Done."},
   {"type": "checks", "heading": "You instantly see", "label": "YOUR SAVESORT LIST", "items": ["Every save, by topic", "What's worth doing", "What's just hype", "What's hiding a guide"], "lastWarn": True, "vo": "Every save sorted by topic. What's worth doing, what's hype, and what's hiding a guide."},
   {"type": "talk", "text": "Free. *Private.*\nNothing gets uploaded.", "mood": "smug", "vo": "It's free, and it runs right in your browser."},
   END]),
 ("2026-10-29", 2, "home-services", "breakdown",
  "Everyone wants an AI startup. Meanwhile homeowners will happily pay someone to clean gutters and wash high windows. 🪜\n\nThe playbook:\n1. Pick one service\n2. Register your business and get public liability insurance\n3. Set up your Google Business Profile\n4. On every job: door hangers on the street, a yard sign, and ask for a review\n\nWorking at heights is dangerous. Follow your local safety rules." + SIGN + "\n\n#homeservices #sidehustle #perth #smallbusiness",
  [{"type": "hook", "lines": ["Skip the", "*AI startup.*"], "vo": "Skip the AI startup."},
   {"type": "title", "text": "Clean\n*gutters.*", "vo": "Homeowners will pay you to clean gutters. Seriously."},
   {"type": "steps", "heading": "The playbook", "items": ["Pick one service", "Register and get insured", "Set up Google Maps", "Door hangers on every job"], "vo": "Pick one service. Register and get insured. Get on Google Maps. Hit the whole street."},
   {"type": "title", "text": "One job.\n*Whole street.*", "bg": "ink", "vo": "One job turns into the whole street."},
   END]),
 ("2026-10-30", 1, "data-cleanup", "tool",
  "A saved reel said someone used AI to scrub their personal data off the internet in a weekend. Here's the free version. 🧹\n\n1. Check your email on haveibeenpwned.com and change breached passwords\n2. Find old accounts and how to delete them on justdeleteme.xyz\n3. Use Google's \"Results about you\" to remove your phone and address from search\n4. Ask Claude to draft the deletion requests\n\nPrivacy laws in many countries give you the right to see and delete your data." + SIGN + "\n\n#privacy #cybersecurity #aitools #onlinesafety",
  [{"type": "quote", "quote": "He used AI to clean his data off the internet in one weekend", "vo": "Someone cleaned their data off the internet in a weekend. Here's how."},
   {"type": "checks", "heading": "Free tools", "label": "PRIVACY CLEANUP", "items": ["Have I Been Pwned", "Just Delete Me", "Results about you", "Claude drafts the emails"], "vo": "Check your breaches. Delete old accounts. Remove your address from Google."},
   {"type": "title", "text": "Change breached\n*passwords.*", "bg": "ink", "vo": "And change every breached password today."},
   END]),
 ("2026-10-30", 2, "clone-any-store", "scam-watch",
  "\"This AI can clone any ecom store in minutes.\" 🚩\n\nCopying another brand's design, photos or product text can breach copyright and trademark law. Fast way to get your store shut down.\n\nUse AI to build YOUR store faster: your own name, your own photos, your own words." + SIGN + "\n\n#ecommerce #shopify #dropshipping #aitools",
  [{"type": "quote", "quote": "This AI can clone any ecom store in minutes", "stamp": "BE CAREFUL", "stampColor": "warn", "vo": "Clone any store in minutes? Sure. Then enjoy the copyright letter."},
   {"type": "title", "text": "Copying a brand\n= *trouble.*", "bg": "ink", "vo": "Copying their design and photos can breach copyright."},
   {"type": "steps", "heading": "Do this instead", "items": ["Your own brand name", "Your own photos", "Your own product copy", "AI to build it faster"], "vo": "Use AI to build your own brand faster. Not someone else's."},
   END]),
 ("2026-10-31", 1, "save-time-money", "product",
  "You saved it to \"do it later\". Later never came. 😅\n\nOnly 24 of my 156 saved reels were worth my time. SaveSort finds those, flags the hype before you waste money on it, and gives you one clear list.\n\nLess scrolling. More doing." + SIGN + "\n\n#productivity #savedreels #sidehustle #timemanagement",
  [{"type": "hook", "lines": ["You saved it", "to *do it later.*"], "mascot": {"pos": "bl", "mood": "sad"}, "vo": "You saved it to do it later. Later never came."},
   {"type": "stat", "value": 24, "label": "of my 156 saves were\n*worth my time*", "color": "go", "mascot": {"pos": "tr", "mood": "shocked"}, "vo": "Only 24 of my 156 saves were worth my time."},
   {"type": "react", "quote": "Make $1000 a day dropshipping", "mood": "suspicious", "verdict": "HYPE", "verdictColor": "warn", "vo": "SaveSort flags hype like this, before you waste money on it."},
   {"type": "talk", "text": "Less scrolling.\n*More doing.*", "mood": "happy", "vo": "Less scrolling. More doing. Feels lighter already."},
   END]),
 ("2026-10-31", 2, "gated-guides", "reveal",
  "22 of my 156 saved reels hid the actual info behind \"comment GUIDE\" or \"DM me\". 🙄\n\nSaveSort flags those and works out what they were hinting at, so you get the guide without the DM funnel." + SIGN + "\n\n#savedreels #instagramtips #productivity",
  [{"type": "hook", "lines": ["Comment *GUIDE*", "for the guide."], "vo": "Comment guide for the guide."},
   {"type": "stat", "value": 22, "label": "of my saves did this", "color": "warn", "vo": "Twenty two of my saved reels did this."},
   {"type": "title", "text": "We find the\n*actual guide.*", "vo": "So SaveSort finds the actual guide. No comment needed."},
   END]),
 ("2026-11-01", 1, "simple-offer", "breakdown",
  "Your offer is too complicated. Fix it with one sentence: ✍️\n\n\"I'll [result] for [who] in [time] for [price].\"\n\nThen add a guarantee that removes the risk, and give ONE next step. Cut everything else." + SIGN + "\n\n#marketing #smallbusiness #sales #copywriting",
  [{"type": "hook", "lines": ["Your offer is", "*too complicated.*"], "vo": "Your offer is too complicated."},
   {"type": "title", "text": "I'll get *[result]*\nfor *[who]*\nin *[time]*.", "vo": "Write it in one sentence. What, for who, how fast, how much."},
   {"type": "steps", "heading": "Then", "items": ["Add a guarantee", "Give one next step", "Cut everything else"], "vo": "Add a guarantee. Give one next step. Cut everything else."},
   END]),
 ("2026-11-01", 2, "offline-computer", "tool",
  "A saved reel: \"someone open sourced a computer that works when the internet goes down.\" It's real. 🛰️\n\nProject N.O.M.A.D. is free and open source:\n• Offline Wikipedia\n• A local AI assistant\n• Offline maps\n• Khan Academy courses\n\nRuns on an old PC or mini PC. Storage is the main cost." + SIGN + "\n\n#opensource #tech #offline #prepping",
  [{"type": "quote", "quote": "A computer that works when the internet goes down", "vo": "A computer that works when the whole internet goes down? It's real."},
   {"type": "checks", "heading": "What's on it", "label": "PROJECT NOMAD · FREE", "items": ["Offline Wikipedia", "A local AI assistant", "Offline maps", "Free courses"], "vo": "Offline Wikipedia, a local AI, maps and courses. Free."},
   {"type": "title", "text": "Old PC.\n*New life.*", "vo": "Put it on an old computer. Storage is the only real cost."},
   END]),
]

def restyle(s):
    """Quotes with a stamp become Sorty reactions; stat/count scenes get Sorty top-right."""
    s = dict(s)
    if s["type"] == "quote" and s.get("stamp"):
        mood = "smug" if s.get("stampColor") == "gate" else "suspicious"
        s = {"type": "react", "quote": s["quote"], "label": s.get("label", "SAVED REEL SAYS"), "mood": mood,
             "verdict": s["stamp"], "verdictColor": s.get("stampColor", "warn"), "vo": s["vo"]}
    elif s["type"] in ("stat", "count") and "mascot" not in s:
        s["mascot"] = {"pos": "tr", "mood": "happy" if s.get("color", "go") == "go" else "shocked"}
    return s


os.makedirs("queue", exist_ok=True)
for date, slot, slug, fmt, caption, scenes in posts:
    pid = f"{date}-{slot}-{slug}"
    scenes = [restyle(s) for s in scenes]
    spec = {"id": pid, "post_at": f"{date}T{'12:30' if slot == 1 else '19:30'}:00+08:00", "format": fmt, "status": "queued",
            "voice": "af_heart", "speed": 1.22, "music": "sfx", "caption": caption, "scenes": scenes}
    json.dump(spec, open(f"queue/{pid}.json", "w"), ensure_ascii=False, indent=2)
print(len(posts), "queue files written")
