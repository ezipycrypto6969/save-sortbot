"""Three longer (35-45s) SaveSort ads starring Sorty, the mascot. Written to ads/. Real numbers only:
156 saved, 24 worth doing, 61 caption-only (39%), 7 hype/scams, 22 gated guides.
Run from the repo root: python3 content/ads_mascot.py
"""
import json, os

END = lambda vo, line="Sort your saves.\n*Free.*": {"type": "end", "line": line, "pill": "Link in bio →", "vo": vo,
                                                     "mascot": {"pos": "tr", "mood": "happy"}}

ADS = {
 "ad-l1-meet-sorty": {"fx": {"hook": "WAIT FOR THE ONE THAT LIED"}, "scenes": [
   {"type": "talk", "text": "Help.\nI live in your\n*saved tab.*", "mood": "shocked", "vo": "Help. I live in your saved tab."},
   {"type": "hook", "lines": ["156 reels saved.", "*Zero* opened."], "slow": True, "mascot": {"pos": "bl", "mood": "sad"},
    "vo": "You saved 156 reels. You opened zero of them."},
   {"type": "talk", "text": "So I read\n*every single one.*", "mood": "smug", "vo": "So I read every single one. Yes. Even the gym ones."},
   {"type": "stat", "value": 24, "label": "were actually\n*worth doing*", "color": "go", "mascot": {"pos": "tr", "mood": "happy"},
    "vo": "24 were actually worth doing."},
   {"type": "react", "quote": "Claude has a secret Founder Thinking Mode", "mood": "suspicious", "verdict": "BE CAREFUL", "verdictColor": "warn", "payoff": True,
    "vo": "And this one? That mode doesn't exist. I checked."},
   {"type": "react", "quote": "Comment GUIDE and I'll DM you", "mood": "smug", "verdict": "GATED GUIDE", "verdictColor": "gate",
    "vo": "This one hid the guide behind a DM. I found it anyway."},
   {"type": "checks", "heading": "For the good ones", "label": "EVERY BREAKDOWN", "items": ["The real tool", "The steps", "The cost", "The catch"], "lastWarn": True,
    "vo": "For the good ones, I write the real tool, the steps, the cost, and the catch."},
   {"type": "talk", "text": "I'm *Sorty.*\nI sort your saves.", "mood": "happy", "wave": True, "vo": "I'm Sorty. I sort your saves, so you can actually do them."},
   END("Try it free. Link in bio.")]},
 "ad-l2-sorty-rates": {"fx": {"hook": "2 OF THESE ARE ACTUALLY GOOD"}, "scenes": [
   {"type": "talk", "text": "Let's rate your\n*saved reels.*", "mood": "smug", "vo": "Okay. Let's rate some saved reels."},
   {"type": "react", "quote": "Make $1000 a day dropshipping", "mood": "shocked", "verdict": "BE CAREFUL", "verdictColor": "warn",
    "vo": "A thousand a day? That's a best case. Plenty of stores lose money."},
   {"type": "react", "quote": "Someone built a free AI agent that finds you clients", "mood": "happy", "verdict": "WORTH DOING", "verdictColor": "go",
    "vo": "A free AI that finds clients? Real. It's on GitHub, and you approve every email."},
   {"type": "react", "quote": "Help sellers skip agent fees and take a cut", "mood": "suspicious", "verdict": "BE CAREFUL", "verdictColor": "warn",
    "vo": "Skip agent fees and take a cut? In WA, that needs a licence."},
   {"type": "react", "quote": "this is the trick", "mood": "sad", "verdict": "NO DETAILS", "verdictColor": "gate",
    "vo": "This is the trick. That's the whole caption. Thanks, I guess."},
   {"type": "react", "quote": "Rank higher on Google Maps", "mood": "happy", "verdict": "WORTH DOING", "verdictColor": "go", "payoff": True,
    "vo": "Rank higher on Google Maps? Real. Pick a specific category, post real photos, reply to reviews."},
   {"type": "talk", "text": "Want me to\n*rate yours?*", "mood": "happy", "wave": True, "vo": "Want me to rate yours? I'll sort every save you've got."},
   END("SaveSort. Free. Link in bio.")]},
 "ad-l3-sorty-rules": {"fx": {"hook": "RULE 3 SAVES YOU MONEY"}, "scenes": [
   {"type": "talk", "text": "3 rules before\nyou *save a reel.*", "mood": "smug", "vo": "Three rules before you save another reel."},
   {"type": "count", "n": 1, "label": "No steps in the caption?\n*Saving won't help.*", "mascot": {"pos": "tr", "mood": "suspicious"},
    "vo": "One. If the caption has no steps, saving it won't help you."},
   {"type": "count", "n": 2, "label": "\"Comment GUIDE\"?\nIt's often *free elsewhere.*", "mascot": {"pos": "tr", "mood": "smug"},
    "vo": "Two. Comment guide? The info is often out there, free."},
   {"type": "count", "n": 3, "label": "Big money claim?\n*Red flag.*", "mascot": {"pos": "tr", "mood": "shocked"}, "payoff": True,
    "vo": "Three. A big money claim? That's a red flag, not a plan."},
   {"type": "stat", "value": 7, "label": "of my 156 saves\nwere *hype or scams*", "color": "warn", "mascot": {"pos": "tr", "mood": "sad"},
    "vo": "Seven of my 156 saves were hype or scams."},
   {"type": "talk", "text": "Or let me\n*check them for you.*", "mood": "happy", "vo": "Or, let me check them for you. I sort, flag, and break down every save."},
   END("Sort your saves free. Link in bio.")]},
}

os.makedirs("ads", exist_ok=True)
for aid, ad in ADS.items():
    spec = {"id": aid, "format": "ad", "status": "draft", "voice": "af_heart", "speed": 1.1, "fx": ad["fx"], "scenes": ad["scenes"], "caption": ""}
    json.dump(spec, open(f"ads/{aid}.json", "w"), ensure_ascii=False, indent=2)
print(len(ADS), "mascot ads written")
