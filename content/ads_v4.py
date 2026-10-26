"""Three longer SaveSort ads (45-65s) built around REAL footage of the SaveSort site sorting a real
Instagram export (156 saves). Numbers on screen and in the voiceover match the actual report:
156 read, 30 worth doing, 65 need the video, 10 be careful, 22 gated guides.
Only claims what the free sorter does today. Run from the repo root: python3 content/ads_v4.py
"""
import json, os

END = lambda vo, line="Sort your saves.\n*Free.*": {"type": "end", "line": line, "pill": "Link in bio →", "vo": vo,
                                                     "mascot": {"pos": "tr", "mood": "happy"}}
PL = lambda mood="happy": {"pos": "pl", "mood": mood}
STATS = {"x": 30, "y": 118, "w": 720, "h": 420}
CHIP = {"go": (250, 1728), "warn": (128, 1808), "gate": (370, 1808)}
TOP = 1650  # report scroll position where the filter chips sit near the top of the phone

ADS = {
 # 1. The demo: watch it sort 156 real saves, then the 3 best finds
 "ad-j-watch-it-sort": {"fx": {"hook": "WAIT FOR #1"}, "scenes": [
   {"type": "hook", "lines": ["156 saved reels.", "*0* actually used."], "mascot": {"pos": "bl", "mood": "sad"},
    "vo": "I had 156 saved reels. I'd used exactly none of them."},
   {"type": "talk", "text": "So I dropped them\ninto *SaveSort.*", "mood": "smug", "vo": "So I dropped them into SaveSort. Watch this."},
   {"type": "screen", "label": "DROP THE ZIP IN", "segs": [{"shot": "drop.png", "from": 560}], "drop": {"at": 0.25, "x": 390, "y": 1180},
    "mascot": PL("happy"), "vo": "Drop in the file Instagram sends you. It runs on your phone. Nothing gets uploaded."},
   {"type": "screen", "label": "2 SECONDS LATER", "segs": [{"shot": "report-all.png", "from": 0}], "highlights": [dict(STATS, at=0.15)],
    "zoom": {"at": 0.12, "s": 1.1, "x": 390, "y": 330}, "mascot": PL("shocked"),
    "vo": "Two seconds later. 156 saves read. 30 worth doing. 65 need the video. And 10? Be careful."},
   {"type": "screen", "label": "SORTED BY TOPIC", "segs": [{"shot": "report-all.png", "from": 520, "to": 1500, "t0": 0.1, "t1": 0.95}], "mascot": PL("happy"),
    "vo": "Every save sorted by topic. AI tools, marketing, side hustles, money."},
   {"type": "screen", "label": "TAP WORTH DOING", "segs": [{"shot": "report-all.png", "from": TOP}, {"shot": "report-go.png", "from": TOP, "to": 3400, "t0": 0.35, "t1": 0.95}],
    "taps": [{"at": 0.22, "x": CHIP["go"][0], "y": CHIP["go"][1]}], "mascot": PL("smug"),
    "vo": "Tap worth doing, and there's your short list. The stuff you can actually use."},
   {"type": "count", "n": 3, "label": "See any brand's ads\n*free:* Meta Ad Library", "mascot": {"pos": "tr", "mood": "happy"},
    "vo": "Number 3. See every ad a brand is running, free, in the Meta Ad Library."},
   {"type": "count", "n": 2, "label": "Rank on Google Maps:\n*reply to every review*", "mascot": {"pos": "tr", "mood": "smug"},
    "vo": "Number 2. Rank on Google Maps. Pick a specific category, post real photos, reply to every review."},
   {"type": "count", "n": 1, "label": "A *free* AI agent\nthat finds clients", "mascot": {"pos": "tr", "mood": "shocked"}, "payoff": True,
    "vo": "Number 1. A free, open source AI agent that finds you clients. And you approve every email."},
   {"type": "screen", "label": "AND THE 10 TO SKIP", "segs": [{"shot": "report-all.png", "from": TOP}, {"shot": "report-warn.png", "from": TOP, "to": 3000, "t0": 0.3, "t1": 0.95}],
    "taps": [{"at": 0.18, "x": CHIP["warn"][0], "y": CHIP["warn"][1]}], "mascot": PL("suspicious"),
    "vo": "And be careful? That's the hype pile. Big money promises. Secret AI modes. Skip them."},
   {"type": "talk", "text": "Less scrolling.\n*More doing.*", "mood": "happy", "vo": "Less scrolling. More doing. Your saves, finally useful."},
   END("Tap the link in bio and sort yours free.")]},

 # 2. The full tutorial: exactly how to get your saved reels out of Instagram and sorted
 "ad-k-full-tutorial": {"fx": {"hook": "SAVE THIS FOR LATER"}, "scenes": [
   {"type": "talk", "text": "Your saved reels\nare *useless.*", "mood": "suspicious", "vo": "Your saved reels are useless. Unless you do this."},
   {"type": "hook", "lines": ["156 saves.", "*0* ever opened."], "slow": True, "mascot": {"pos": "bl", "mood": "sad"},
    "vo": "I had 156 saved reels and never opened one again. Here's the fix, step by step."},
   {"type": "path", "label": "STEP 1 · IN INSTAGRAM", "screens": [
      {"title": "Settings and activity", "rows": ["Accounts Center", "Saved", "Archive", "Your activity"], "pick": 0},
      {"crumb": "Accounts Center", "title": "Account settings", "rows": ["Password and security", "Personal details", "Your information and permissions", "Ad preferences"], "pick": 2},
      {"crumb": "Your information and permissions", "title": "Your information", "rows": ["Access your information", "Export your information", "Search history"], "pick": 1}],
    "mascot": PL("happy"), "vo": "In Instagram, open settings. Accounts Center. Your information and permissions. Then export your information."},
   {"type": "path", "label": "STEP 2 · ONLY TICK SAVED", "screens": [
      {"crumb": "Export your information", "title": "Create export", "rows": ["Export to device", "Transfer to destination"], "pick": 0},
      {"crumb": "Customize information", "title": "Your Instagram activity", "rows": ["Saved", "Likes", "Comments", "Messages"], "ticks": True, "on": [0]},
      {"crumb": "Export to device", "title": "Confirm your export", "rows": ["Date range: All time", "Format: HTML", "Start export"], "btn": 2, "pick": 2}],
    "mascot": PL("smug"), "vo": "Create export. Export to device. Customize, and tick only saved. Pick HTML, then start export."},
   {"type": "talk", "text": "Instagram *emails you*\nwhen it's ready.", "mood": "happy", "vo": "Instagram emails you when it's ready. Download the zip."},
   {"type": "screen", "label": "STEP 3 · DROP IT IN SAVESORT", "segs": [{"shot": "drop.png", "from": 560}], "drop": {"at": 0.3, "x": 390, "y": 1180},
    "mascot": PL("happy"), "vo": "Now open SaveSort and drop the zip in. Don't even unzip it."},
   {"type": "screen", "label": "YOUR SAVES, SORTED", "segs": [{"shot": "report-all.png", "from": 0}, {"shot": "report-all.png", "from": 0, "to": 1100, "t0": 0.55, "t1": 0.98}],
    "highlights": [dict(STATS, at=0.1, until=0.5)], "mascot": PL("shocked"),
    "vo": "Done. Mine read 156 saves and sorted every one by topic."},
   {"type": "screen", "label": "THE GOOD STUFF", "segs": [{"shot": "report-all.png", "from": TOP}, {"shot": "report-go.png", "from": TOP, "to": 3000, "t0": 0.3, "t1": 0.95}],
    "taps": [{"at": 0.18, "x": CHIP["go"][0], "y": CHIP["go"][1]}], "mascot": PL("happy"),
    "vo": "Worth doing shows the 30 you can actually act on."},
   {"type": "screen", "label": "THE HIDDEN GUIDES", "segs": [{"shot": "report-all.png", "from": TOP}, {"shot": "report-gate.png", "from": TOP, "to": 3000, "t0": 0.3, "t1": 0.95}],
    "taps": [{"at": 0.18, "x": CHIP["gate"][0], "y": CHIP["gate"][1]}], "mascot": PL("suspicious"), "payoff": True,
    "vo": "And gated guides finds the 22 that hid the info behind comment GUIDE."},
   {"type": "react", "quote": "Comment GUIDE and I'll DM you the steps", "mood": "smug", "verdict": "GATED GUIDE", "verdictColor": "gate",
    "vo": "Like this one. The steps were never in the reel. Now you know which ones to skip."},
   {"type": "checks", "heading": "What you get", "label": "YOUR SAVESORT REPORT", "items": ["Every save, by topic", "What's worth doing", "What's just hype", "Free, nothing uploaded"], "lastWarn": False,
    "vo": "Every save by topic. What's worth doing. What's hype. Free, and nothing gets uploaded."},
   END("Save this, then tap the link in bio.")]},

 # 3. Scam-watch: the saved reels that lied, and how SaveSort flags them
 "ad-m-saves-that-lied": {"fx": {"hook": "10 OF MY SAVES WERE HYPE"}, "scenes": [
   {"type": "talk", "text": "Your saved tab is\n*lying to you.*", "mood": "shocked", "vo": "Your saved tab is lying to you. Let me show you."},
   {"type": "react", "quote": "Make $1000 a day dropshipping", "mood": "suspicious", "verdict": "BE CAREFUL", "verdictColor": "warn",
    "vo": "A thousand a day? That's the best case. Most new stores make way less."},
   {"type": "react", "quote": "Claude has a secret Founder Thinking Mode", "mood": "shocked", "verdict": "BE CAREFUL", "verdictColor": "warn",
    "vo": "A secret AI mode? It doesn't exist. It's just a prompt."},
   {"type": "react", "quote": "Comment GUIDE and I'll DM you the steps", "mood": "smug", "verdict": "GATED GUIDE", "verdictColor": "gate",
    "vo": "Comment guide? The steps were never in the reel."},
   {"type": "talk", "text": "So how many\nof *yours* lie?", "mood": "suspicious", "vo": "So how many of your saves are like this? I checked mine."},
   {"type": "screen", "label": "MY REAL SAVES", "segs": [{"shot": "report-all.png", "from": 0}], "highlights": [dict(STATS, at=0.2)],
    "zoom": {"at": 0.15, "s": 1.1, "x": 390, "y": 330}, "mascot": PL("shocked"),
    "vo": "156 saves. 10 flagged be careful. Only 30 actually worth doing."},
   {"type": "screen", "label": "TAP BE CAREFUL", "segs": [{"shot": "report-all.png", "from": TOP}, {"shot": "report-warn.png", "from": TOP, "to": 3200, "t0": 0.3, "t1": 0.95}],
    "taps": [{"at": 0.18, "x": CHIP["warn"][0], "y": CHIP["warn"][1]}], "mascot": PL("suspicious"),
    "vo": "Tap be careful, and every hype reel is in one list."},
   {"type": "screen", "label": "TAP GATED GUIDES", "segs": [{"shot": "report-all.png", "from": TOP}, {"shot": "report-gate.png", "from": TOP, "to": 3200, "t0": 0.3, "t1": 0.95}],
    "taps": [{"at": 0.18, "x": CHIP["gate"][0], "y": CHIP["gate"][1]}], "mascot": PL("smug"), "payoff": True,
    "vo": "Gated guides shows the 22 that wanted a comment before the info."},
   {"type": "checks", "heading": "Save money too", "label": "BEFORE YOU BUY THE COURSE", "items": ["Check the claim", "Look for real steps", "Skip the hype", "Do the 30 that work"], "lastWarn": False,
    "vo": "Check the claim. Look for real steps. Skip the hype. Do the ones that work."},
   {"type": "talk", "text": "Sorts in *seconds.*\nIt's free.", "mood": "happy", "vo": "It sorts in seconds, it's free, and it runs on your phone."},
   END("Tap the link in bio and check yours now.")]},
}

os.makedirs("ads", exist_ok=True)
for aid, ad in ADS.items():
    spec = {"id": aid, "format": "ad", "status": "draft", "voice": "af_heart", "speed": 1.22, "music": "sfx",
            "fx": ad["fx"], "scenes": ad["scenes"], "caption": ""}
    json.dump(spec, open(f"ads/{aid}.json", "w"), ensure_ascii=False, indent=2)
print(len(ADS), "long ads written")
