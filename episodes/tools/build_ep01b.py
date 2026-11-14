"""Builds episodes/ep01b.json (Ep 1: The Gym Bro's Saves) from the beat list below.
Timing follows the voice lines (public/ep01b/vo/durations.json), so re-recording a line re-times the edit."""
import json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(HERE, "public/ep01b/vo/durations.json")))
C = lambda n: f"ep01b/clips/raw_{n}.mp4"
TEXT = {
 "v01": "You saved *900* reels.", "v02": "You watched *four.*",
 "v03": "I sorted *156* in seconds. But first, I nearly got *fired.*",
 "v05": "New client.", "v06": "4,317 gym reels. Leg day? *Zero.*", "v07": "*ZERO?!*",
 "v08": "Sorted by *Friday.* Or you're *fired.*", "v09": "I don't judge. I sort. Then I *judge.*",
 "v10": "Fine. By *hand.*", "v13": "I'm *cooked.*", "v14": "Wait. The export *ZIP!*",
 "v15": "Drop it in. Nothing gets *uploaded.* Done.", "v17a": "It's Thursday.", "v17b": "I'm early. *Locked in.*",
 "v18": "One leg day in there. *One.*", "v19": "Send this to the mate with *4,000* gym saves and chicken legs.",
 "v21": "Sorted. Now go *do one.*",
}
shots, voices, sfx, mute = [], [], [], []
t = 0.0
def shot(dur, **k):
    global t
    k.setdefault("camera", "push")
    shots.append(dict(n=len(shots) + 1, start=round(t, 2), end=round(t + dur, 2), **k)); t += dur
def vo(i, at=0.05):
    voices.append(dict(src=f"ep01b/vo/{i}.wav", at=round(t + at, 2), dur=D[i], text=TEXT[i]))
def fx(k, at=0.0, v=0.7): sfx.append(dict(k=k, at=round(t + at, 2), v=v))

# 1-2 hook: dark, cool, phone-lit
vo("v01"); fx("hook"); shot(D["v01"] + 0.15, src=C("a"), **{"from": 1.0}, tint="cool")
vo("v02"); fx("irony"); shot(D["v02"] + 0.2, src=C("a"), **{"from": 3.8}, camera="crash", tint="cool")
# 3 real screen, open loop
vo("v03", 0.1); fx("scroll", 0.2); shot(D["v03"] + 0.2, kind="screen", screen=dict(src="ep01b/screens/report-all.png", y0=0, y1=120), camera="none", tag="REAL SCREEN · OUR SAMPLE REPORT")
# 4 title
fx("hit"); shot(0.9, kind="title", text="EP 1", sub="THE GYM BRO'S SAVES", camera="crash")
# 5-8 stakes
vo("v05"); fx("drop"); shot(D["v05"] + 0.15, src=C("b"), **{"from": 0.0}, camera="shake", tint="cool")
vo("v06"); shot(2.2, src=C("b"), **{"from": 1.3}, card="4,317 gym reels", cardLabel="CLIENT'S SAVED TAB", tint="cool")
fx("tap"); shot(D["v06"] - 2.2 + 0.1, src=C("b"), **{"from": 3.0}, card="Leg day: 0", cardLabel="CLIENT'S SAVED TAB", camera="crash", tint="cool")
vo("v07"); fx("mood-shocked"); shot(0.85, src=C("b"), **{"from": 3.9}, camera="crash", tint="red")
vo("v08"); fx("riser", 0.6); shot(D["v08"] + 0.15, src=C("b"), **{"from": 0.2}, tint="red")
# 9-12 he tries by hand
vo("v09"); fx("stamp", 0.35); shot(D["v09"] + 0.15, src=C("c"), **{"from": 0.0}, tint="warm")
vo("v10"); fx("scroll"); shot(D["v10"] + 0.15, src=C("d"), **{"from": 0.0}, camera="pan")
for st, fr in (("skip", 1.3), ("watch", 2.4), ("watch", 3.5)):
    fx("stamp", 0.05); shot(0.5, src=C("d"), **{"from": fr}, stamp=st, camera="crash")
fx("tap"); shot(0.7, kind="title", text="THURSDAY", sub="11:58 PM", camera="crash")
# 13-14 low point, then the toy car
mute.append([t, t + 1.5]); vo("v13", 0.35); fx("mood-sad"); shot(1.5, src=C("e"), **{"from": 2.9}, camera="tilt", tint="cool")
vo("v14", 0.3); fx("whip"[:0] or "cut"); fx("mood-shocked", 0.35); shot(D["v14"] + 0.45, src=C("f"), **{"from": 0.2}, camera="whip", big="EXPORT.ZIP")
# 15 twist: real screen
vo("v15", 0.1); fx("drop", 0.3); shot(1.2, kind="screen", screen=dict(src="ep01b/screens/drop.png", y0=170, y1=200), camera="none", tag="REAL SCREEN · SAVESORTAI.COM")
shot(D["v15"] - 1.1 + 0.2, kind="screen", screen=dict(src="ep01b/screens/report-all.png", y0=0, y1=30), camera="crash", tag="REAL SCREEN · OUR SAMPLE REPORT")
# 16 win montage, gold
fx("payoff"); fx("hit")
for i, fr in enumerate((0.3, 1.5, 2.7, 3.9)):
    fx("stamp", 0.02); shot(0.35, src=C("g"), **{"from": fr}, camera="crash", tint="gold", **({"stamp": "do"} if i == 3 else {}))
# 17 the Algorithm is stunned
vo("v17a"); shot(D["v17a"] + 0.1, src=C("c"), **{"from": 2.4}, tint="warm")
vo("v17b"); fx("mood-smug"); shot(D["v17b"] + 0.15, src=C("c"), **{"from": 3.6}, camera="crash", tint="gold")
vo("v18"); fx("payoff"); shot(D["v18"] + 0.15, src=C("g"), **{"from": 4.2}, card="1 leg day reel", cardLabel="CLIENT'S DO IT LIST", tint="gold")
# 18-21 send ask, rehook, outro
vo("v19"); fx("hook"); shot(D["v19"] + 0.15, src=C("h"), **{"from": 0.0}, tint="warm")
fx("hit"); shot(0.9, kind="title", text="FOLLOW FOR EP 2", sub="SORTY VS YOUR RECIPE SAVES", camera="crash")
vo("v21"); fx("payoff", 0.9); shot(D["v21"] + 0.25, src=C("h"), **{"from": 2.6}, tint="warm")
end = dict(start=round(t, 2), end=round(t + 1.5, 2), line="Sorted. *Now go do one.*", url="savesortai.com", sub="free · link in bio")
spec = dict(id="ep01b", title="Ep 1: The Gym Bro's Saves", fps=30, music=dict(src="ep01b/sound.wav", volume=0.6, duck=0.2),
            hits=[], shots=shots, end=end, voices=voices, sfxAt=sfx, musicMute=mute, aiTag="AI voice")
json.dump(spec, open(os.path.join(HERE, "ep01b.json"), "w"), indent=1)
print("length", end["end"], "shots", len(shots))
