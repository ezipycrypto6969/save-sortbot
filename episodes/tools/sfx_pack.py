"""Export our own synthesised sound effects (engine/music.py, no samples) as a small pack for episodes.
Run: python3 episodes/tools/sfx_pack.py   -> episodes/public/sfx/<kind>-<n>.wav"""
import os, sys, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "engine"))
import music  # noqa: E402

OUT = os.path.join(ROOT, "episodes", "public", "sfx")
KINDS = ["cut", "stamp", "hook", "drop", "tap", "payoff", "scroll", "hit", "irony", "riser", "end",
         "mood:shocked", "mood:sad", "mood:smug", "mood:suspicious"]
os.makedirs(OUT, exist_ok=True)
for kind in KINDS:
    for n, seed in enumerate((3, 11, 29)):
        t = 1.2  # after the longest lead-in, so nothing is cut off
        mix = music.make(3.0, [0], [], [], 100, seed=seed, mode="sfx", events=[(t, kind)])
        mono = mix.mean(1)
        idx = np.nonzero(np.abs(mono) > 1e-3)[0]
        if len(idx) == 0:
            continue
        a, b = idx[0], min(len(mono), idx[-1] + 2400)
        clip = (mix[a:b] / (np.max(np.abs(mix[a:b])) + 1e-9) * 0.9 * 32767).astype(np.int16)
        name = f"{kind.replace(':', '-')}-{n + 1}.wav"
        with wave.open(os.path.join(OUT, name), "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(music.SR); w.writeframes(clip.tobytes())
print("\n".join(sorted(os.listdir(OUT))))
