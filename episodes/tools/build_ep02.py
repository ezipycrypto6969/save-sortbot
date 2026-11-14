"""Builds episodes/ep02.json (Ep 2: The 10K Bet). Timing follows the voice lines in public/ep02/vo/durations.json."""
import json, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(HERE, "public/ep02/vo/durations.json")))
C = lambda n: f"ep02/clips/c{n:02d}.mp4"
TEXT = {
 "k1": "I'll watch it *later.*", "k2": "Later. Later. *Later.*", "k3": "I've watched... *some.*", "k4": "*Deal.*",
 "k5": "Gym. Recipe. Gym. *Gym.*", "k6": "I haven't gone back to a *single one.*", "k7": "Ten grand and I'll *tell you.*",
 "k8": "Wait. Who *are you?*", "b1": "*67,000* saves? You've watched none of them.", "b2": "Ten grand says you can't sort them in *24 hours.*",
 "b3": "Tick *tock.*", "b4": "No way. How?! *Tell me how!*", "s1": "You *done?*", "s2": "Give me the *zip.*", "s3": "I'm *Sorty.*",
 "s4": "Sorted. Now go *do one.*",
}
shots, voices, sfx, mute = [], [], [], []
t = 0.0
def shot(dur, **k):
    global t
    k.setdefault("camera", "drift")
    shots.append(dict(n=len(shots) + 1, start=round(t, 2), end=round(t + dur, 2), **k)); t += dur
def vo(i, at=0.05):
    voices.append(dict(src=f"ep02/vo/{i}.wav", at=round(t + at, 2), dur=D[i], text=TEXT[i]))
def fx(k, at=0.0, v=0.4): sfx.append(dict(k=k, at=round(t + at, 2), v=v))
LAP = dict(x=257, y=809, w=570, h=353)

# 1 hook: 2am, "I'll watch it later" (Sorty already hiding on the couch)
vo("k1", 0.25); fx("tap", 1.5, 0.3); shot(2.0, src=C(1), **{"from": 0.2}, top="SPOT SORTY BEFORE HE TALKS")
# 2 time-lapse, one shot
vo("k2", 0.2); fx("riser", 0.4, 0.3); shot(2.6, src=C(2), **{"from": 0.0}, rate=1.7)
# 3 the number (3 days later)
fx("scroll", 0.0, 0.3); shot(1.7, src=C(1), **{"from": 3.0}, ticker=dict(label="SAVED REELS", **{"from": 2140, "to": 67569}, sub="3 DAYS LATER"), fade=0.25)
# 4 Brad finds out
vo("b1", 0.1); shot(D["b1"] + 0.25, src=C(3), **{"from": 0.0}, rate=0.95)
vo("k3", 0.05); shot(D["k3"] + 0.15, src=C(3), **{"from": 3.2}, rate=0.6)
# 5 the bet
vo("b2", 0.05); fx("drop", 0.4, 0.35); shot(D["b2"] + 0.2, src=C(4), **{"from": 0.0})
vo("k4", 0.25); fx("hit", 0.25, 0.35); shot(1.2, src=C(4), **{"from": 3.6}, ticker=dict(label="TIME LEFT", **{"from": 86400, "to": 86400}, clock=True))
# 6 the struggle, getting faster
vo("k5", 0.1); shot(2.3, src=C(5), **{"from": 0.0}, rate=1.3, ticker=dict(label="TIME LEFT", **{"from": 86399, "to": 11520}, clock=True))
shot(D["k5"] - 2.3 + 0.35, src=C(6), **{"from": 2.6}, ticker=dict(label="TIME LEFT", **{"from": 11520, "to": 3600}, clock=True))
# 7 rock bottom (quiet)
mute.append([t, t + D["k6"] + D["b3"] + 0.9])
vo("k6", 0.3); shot(D["k6"] + 0.4, src=C(7), **{"from": 0.0}, ticker=dict(label="TIME LEFT", **{"from": 599, "to": 590}, clock=True))
vo("b3", 0.05); fx("tap", 0.1, 0.25); fx("tap", 0.55, 0.25); shot(D["b3"] + 0.4, src=C(7), **{"from": 3.0})
# 8 Sorty speaks for the first time
vo("s1", 0.45); fx("mood-suspicious", 0.2, 0.35); shot(1.5, src=C(8), **{"from": 1.0}, camera="push")
# 9 the twist: the real SaveSort screen, inside the laptop
vo("s2", 0.1); fx("drop", 1.0, 0.4)
shot(1.6, src=C(9), **{"from": 0.0}, camera="flat", laptop=dict(LAP, src="ep02/screens/drop.png", y0=290, y1=300, label="REAL SAVESORT SCREEN"))
fx("payoff", 0.0, 0.35); shot(2.9, src=C(9), **{"from": 1.6}, camera="flat", laptop=dict(LAP, src="ep02/screens/report-all.png", y0=0, y1=20, label="OUR SAMPLE REPORT"))
# 10 timer freezes: SORTED
fx("hit", 0.0, 0.45); shot(1.2, src=C(9), **{"from": 4.5}, rate=0.5, camera="flat", ticker=dict(label="SORTED", **{"from": 1, "to": 1}, clock=True, sub="WITH 1 SECOND LEFT"))
# 11 sore loser
vo("b4", 0.05); shot(D["b4"] + 0.15, src=C(10), **{"from": 0.0})
vo("k7", 0.05); fx("mood-smug", 0.0, 0.3); shot(D["k7"] + 0.2, src=C(10), **{"from": 2.9}, rate=0.9, camera="push")
# 12 who are you?
vo("k8", 0.6); fx("payoff", 0.0, 0.3); shot(D["k8"] + 0.7, src=C(11), **{"from": 0.0})
vo("s3", 0.15); shot(D["s3"] + 0.45, src=C(11), **{"from": 4.0}, camera="push")
# 13 outro
vo("s4", 0.1); fx("payoff", 1.0, 0.35); shot(D["s4"] + 0.3, src="ep02/clips/outro.mp4", **{"from": 2.6})
end = dict(start=round(t, 2), end=round(t + 1.4, 2), line="Sorted. *Now go do one.*", url="savesortai.com", sub="free · link in bio")
spec = dict(id="ep02", title="Ep 2: The 10K Bet", fps=30, music=dict(src="ep02/sound.wav", volume=0.45, duck=0.14),
            hits=[], shots=shots, end=end, voices=voices, sfxAt=sfx, musicMute=mute, aiTag="AI voices")
json.dump(spec, open(os.path.join(HERE, "ep02.json"), "w"), indent=1)
print("length", end["end"], "shots", len(shots))
