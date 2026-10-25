"""Writes six SaveSort ads (not queued for posting) into ads/. Each tests a different hook style.
Numbers are the founder's real saves: 156 saved, 24 worth doing, 61 caption-only (39%), 7 hype/scams, 22 gated guides.
Run from the repo root: python3 content/ads_v2.py && for f in ads/*.json; do python3 engine/build.py $f out/$(basename $f .json) --stills; done
"""
import json, os

END = lambda vo, line="Sort your saves.\n*Free.*": {"type": "end", "line": line, "pill": "Link in bio →", "vo": vo}

ADS = {
 "ad-a-callout": {"fx": {"hook": "CHECK YOUR SAVED TAB"}, "scenes": [
   {"type": "hook", "lines": ["Stop scrolling", "if you have *100+ saves.*"], "vo": "Stop scrolling if you've got over 100 saved reels."},
   {"type": "title", "text": "You'll never\nwatch them *again.*", "bg": "ink", "vo": "Be honest. You're never watching them again."},
   {"type": "stat", "value": 24, "label": "of my 156 were\n*worth doing*", "color": "go", "vo": "Out of my 156, only 24 were worth doing."},
   {"type": "checks", "heading": "So I built this", "label": "SAVESORT", "items": ["Sorts every save", "Writes the steps", "Flags the scams", "Free to try"], "vo": "It sorts them, writes the steps, and flags the scams."},
   END("Sort yours free. Link in bio.")]},
 "ad-b-countdown": {"fx": {"hook": "#1 IS ILLEGAL IN WA"}, "scenes": [
   {"type": "hook", "lines": ["3 saved reels", "that *lied to me.*"], "vo": "Three saved reels that lied to me. Number one is illegal."},
   {"type": "count", "n": 3, "label": "A *secret* Claude mode", "vo": "Three. A secret Claude mode. It doesn't exist."},
   {"type": "count", "n": 2, "label": "Clone any store\n*in minutes*", "vo": "Two. Clone any store in minutes. Enjoy the copyright letter."},
   {"type": "count", "n": 1, "label": "Skip agent fees,\n*take a cut*", "payoff": True, "vo": "One. Help sellers skip agent fees. In WA, that needs a licence."},
   END("SaveSort flags these for you. Link in bio.", "Spot the scams.\n*Free.*")]},
 "ad-c-pov": {"fx": {"hook": "POV"}, "scenes": [
   {"type": "hook", "lines": ["POV: you finally", "open your *saved reels*"], "vo": "P O V. You finally open your saved reels."},
   {"type": "quote", "quote": "this is the trick", "label": "SAVED REEL SAYS", "note": "That's the whole caption.", "stamp": "NO DETAILS", "stampColor": "gate", "vo": "This is the trick. That's it. That's the whole caption."},
   {"type": "quote", "quote": "Comment GUIDE and I'll DM you", "label": "SAVED REEL SAYS", "stamp": "GATED GUIDE", "stampColor": "gate", "vo": "Comment guide for the guide. Of course."},
   {"type": "stat", "value": 39, "suffix": "%", "label": "of my saves said\n*nothing*", "color": "warn", "vo": "39 percent of my saves said nothing at all."},
   END("SaveSort finds the ones worth doing. Link in bio.")]},
 "ad-d-contrarian": {"fx": {}, "scenes": [
   {"type": "hook", "lines": ["Don't comment", "*GUIDE.*"], "vo": "Don't comment guide."},
   {"type": "title", "text": "22 of my saves\nhid the *guide.*", "vo": "22 of my saved reels hid the guide behind a DM."},
   {"type": "checks", "heading": "We find it for you", "label": "EVERY BREAKDOWN", "items": ["The real tool", "The real steps", "The real cost", "The catch"], "lastWarn": True, "vo": "SaveSort finds the real tool, the steps, the cost, and the catch."},
   END("No comment needed. Link in bio.", "Skip the DM.\n*Free.*")]},
 "ad-e-guess": {"fx": {"hook": "GUESS BEFORE IT SHOWS"}, "scenes": [
   {"type": "hook", "lines": ["I saved *156 reels.*", "Guess how many..."], "vo": "I saved 156 reels. Guess how many were actually worth doing."},
   {"type": "title", "text": "Lock in\nyour *guess.*", "bg": "ink", "vo": "Lock in your guess. Comment it."},
   {"type": "stat", "value": 24, "label": "were worth doing", "color": "go", "payoff": True, "vo": "24. That's it."},
   {"type": "quote", "quote": "Claude has a secret Founder Thinking Mode", "stamp": "BE CAREFUL", "stampColor": "warn", "vo": "And seven were straight up hype."},
   END("Sort yours free. Link in bio.")]},
 "ad-f-lying": {"fx": {"hook": "WAIT FOR THE $1000/DAY ONE"}, "scenes": [
   {"type": "hook", "lines": ["Your saved tab", "is *lying to you.*"], "vo": "Your saved tab is lying to you."},
   {"type": "stat", "value": 7, "label": "of mine were\n*hype or scams*", "color": "warn", "vo": "Seven of mine were hype, or straight up scams."},
   {"type": "quote", "quote": "Make $1000 a day dropshipping", "label": "SAVED REEL SAYS", "note": "That's a best case. Plenty of stores lose money on ads.", "stamp": "BE CAREFUL", "stampColor": "warn", "payoff": True, "vo": "A thousand a day? Best case. Plenty of stores lose money."},
   {"type": "steps", "heading": "SaveSort tells you", "items": ["What's real", "What it costs", "What to skip"], "vo": "SaveSort tells you what's real, what it costs, and what to skip."},
   END("Check yours free. Link in bio.", "Check your saves.\n*Free.*")]},
}

os.makedirs("ads", exist_ok=True)
for aid, ad in ADS.items():
    spec = {"id": aid, "format": "ad", "status": "draft", "voice": "af_heart", "speed": 1.12, "fx": ad["fx"], "scenes": ad["scenes"],
            "caption": ""}
    json.dump(spec, open(f"ads/{aid}.json", "w"), ensure_ascii=False, indent=2)
print(len(ADS), "ads written")
