"""Three SaveSort ads for a global audience: how it works, time & money, how it feels.
Only claims what the free sorter does today (sort by topic, flag worth doing / hype / gated guides, runs in the browser).
No music beat (effects only), faster voice, clear call to action. Real numbers: 156 saved, 24 worth doing.
Run from the repo root: python3 content/ads_v3.py
"""
import json, os

CTA = lambda vo, line="Sort your saves.\n*Free.*": {"type": "end", "line": line, "pill": "Link in bio →", "vo": vo,
                                                     "mascot": {"pos": "tr", "mood": "happy"}}

ADS = {
 "ad-g-how-it-works": {"fx": {"hook": "THE 30-SECOND FIX"}, "scenes": [
   {"type": "talk", "text": "Your saved reels\nare a *mess.*", "mood": "shocked", "vo": "Your saved reels are a mess. Let's fix that in 30 seconds."},
   {"type": "steps", "heading": "How it works", "items": ["Download your Instagram data", "Tick only \"Saved\"", "Drop the zip into SaveSort", "Get your sorted list"],
    "vo": "Download your Instagram data. Tick saved. Drop the zip into SaveSort. Done."},
   {"type": "checks", "heading": "You instantly see", "label": "YOUR SAVESORT LIST", "items": ["Every save, by topic", "What's worth doing", "What's just hype", "What's hiding a guide"], "lastWarn": True,
    "vo": "Every save sorted by topic. What's worth doing, what's just hype, and what's hiding a guide."},
   {"type": "talk", "text": "Free. *Private.*\nNothing gets uploaded.", "mood": "smug", "vo": "It's free, and it runs right in your browser. Nothing gets uploaded."},
   {"type": "talk", "text": "Your saves.\n*Finally useful.*", "mood": "happy", "wave": True, "payoff": True, "vo": "Your saves, finally useful."},
   CTA("Tap the link in bio and sort yours now.")]},
 "ad-h-time-money": {"fx": {"hook": "STOP WASTING YOUR SAVES"}, "scenes": [
   {"type": "hook", "lines": ["You saved it", "to *do it later.*"], "mascot": {"pos": "bl", "mood": "sad"}, "vo": "You saved it to do it later. Later never came."},
   {"type": "talk", "text": "Hours of scrolling.\n*Nothing done.*", "mood": "sad", "vo": "Hours of scrolling. Nothing actually done."},
   {"type": "stat", "value": 24, "label": "of my 156 saves were\n*worth my time*", "color": "go", "mascot": {"pos": "tr", "mood": "shocked"},
    "vo": "Only 24 of my 156 saves were worth my time."},
   {"type": "react", "quote": "Make $1000 a day dropshipping", "mood": "suspicious", "verdict": "HYPE", "verdictColor": "warn",
    "vo": "SaveSort flags hype like this, before you waste money on it."},
   {"type": "checks", "heading": "Save time and money", "label": "SAVESORT", "items": ["Skip the hype", "Find what's worth doing", "Stop rewatching", "Focus your time"],
    "vo": "Skip the hype. Find what's worth doing. Stop rewatching. Focus your time."},
   {"type": "talk", "text": "Feel *in control*\nof your feed.", "mood": "happy", "payoff": True, "vo": "And finally feel in control of your feed."},
   CTA("Try SaveSort free. Link in bio.")]},
 "ad-i-how-it-feels": {"fx": {"hook": "FROM 156 SAVES TO 1 LIST"}, "scenes": [
   {"type": "talk", "text": "That feeling when\nyour saved tab is *full*", "mood": "sad", "vo": "That feeling when your saved tab is full, and you've done none of it."},
   {"type": "hook", "lines": ["156 saves.", "*0 done.*"], "slow": True, "grey": True, "mascot": {"pos": "bl", "mood": "sad"}, "vo": "156 saves. Zero done."},
   {"type": "talk", "text": "Now imagine\n*one clear list.*", "mood": "happy", "vo": "Now imagine one clear list of what's actually worth doing."},
   {"type": "steps", "heading": "SaveSort gives you", "items": ["Your best saves first", "Hype flagged", "Sorted by topic", "All in one place"], "payoff": True,
    "vo": "Your best saves first. Hype flagged. Everything sorted, in one place."},
   {"type": "talk", "text": "Less scrolling.\n*More doing.*", "mood": "smug", "vo": "Less scrolling. More doing. It feels so much lighter."},
   CTA("Sort your saves free. Link in bio.")]},
}

os.makedirs("ads", exist_ok=True)
for aid, ad in ADS.items():
    spec = {"id": aid, "format": "ad", "status": "draft", "voice": "af_heart", "speed": 1.22, "music": "sfx",
            "fx": ad["fx"], "scenes": ad["scenes"], "caption": ""}
    json.dump(spec, open(f"ads/{aid}.json", "w"), ensure_ascii=False, indent=2)
print(len(ADS), "ads written")
