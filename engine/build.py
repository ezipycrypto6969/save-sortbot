"""Build one reel from a JSON spec.

  python3 engine/build.py queue/<id>.json out/<id> [--stills]

Writes reel.mp4 (1080x1920, voice + music), cover.jpg, captions.srt and timeline.json.
Each scene's length is stretched to fit its voiceover line, so scripts never get cut off.
Exits with code 2 and lists the words if a voiceover line has words the dictionary doesn't know.
"""
import json, os, subprocess, sys, zlib
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g2p, tts, music  # noqa: E402

MIN = {"hook": 1.3, "quote": 1.8, "title": 1.2, "steps": 2.4, "stat": 1.6, "checks": 2.0, "count": 1.1, "talk": 1.3, "react": 2.0, "end": 1.6, "screen": 2.6, "path": 3.0}


def caption_chunks(lines, max_words=3):
    """Word-by-word caption timing: spread each line's words over its spoken time by length, 1-3 words per chunk."""
    out = []
    for a, b, text in lines:
        words = text.replace("\n", " ").split()
        if not words: continue
        weights = [len(w.strip(".,!?")) + 2 for w in words]; total = sum(weights); t = a
        timed = []
        for w, wt in zip(words, weights):
            d = (b - a) * wt / total; timed.append({"w": w, "t0": round(t, 3), "t1": round(t + d, 3)}); t += d
        chunk = []
        for i, w in enumerate(timed):
            chunk.append(w)
            if len(chunk) == max_words or w["w"][-1] in ".,!?" or i == len(timed) - 1:
                out.append({"t0": chunk[0]["t0"], "t1": chunk[-1]["t1"], "words": chunk}); chunk = []
    for i in range(len(out) - 1):  # hold each chunk until the next one starts (no flicker in short gaps)
        if out[i + 1]["t0"] - out[i]["t1"] < 0.35: out[i]["t1"] = out[i + 1]["t0"]
    return out


def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main(spec_path, out_dir, stills=False):
    spec = json.load(open(spec_path))
    os.makedirs(out_dir, exist_ok=True)
    voice = spec.get("voice", "af_heart")
    # 1. phonemes for every line first, so unknown words are reported all at once
    bad = []
    for sc in spec["scenes"]:
        if sc.get("vo"):
            try: sc["_ph"] = g2p.phonemize(sc["vo"])
            except g2p.UnknownWords as e: bad.append(f'{sc["vo"]!r}: {e}')
    if bad:
        print("UNKNOWN WORDS — rephrase these lines or add the words to models/custom.json:\n  " + "\n  ".join(bad))
        sys.exit(2)
    # 2. speech + timeline
    t = 0.0; lines = []; cuts = []; hits = []; ticks = []
    vo_track = []
    for sc in spec["scenes"]:
        audio = tts.speak(sc["_ph"], voice, sc.get("speed", spec.get("speed", 1.2))) if sc.get("vo") else np.zeros(0, np.float32)
        if len(audio) and spec.get("pitch"): audio = tts.pitch(audio, spec["pitch"])
        vlen = len(audio) / tts.SR
        lead = 0.06  # fast pace: voice starts almost on the cut, short tail
        dur = max(sc.get("min", MIN[sc["type"]]), vlen + lead + 0.14)
        sc["start"], sc["end"] = round(t, 3), round(t + dur, 3)
        cuts.append(t)
        if sc.get("vo"):
            vo_track.append((t + lead, audio)); lines.append((t + lead, t + lead + vlen, sc["vo"]))
        if sc["type"] == "quote" and sc.get("stamp"):
            sc["stampAt"] = round(min(dur - 0.4, sc.get("stampAt", max(0.6, vlen * 0.55))), 3); hits.append(t + sc["stampAt"])
        if sc["type"] == "hook": hits.append(t + 0.12 + 0.38 * (len(sc["lines"]) - 1))
        if sc["type"] == "count": hits.append(t)
        if sc["type"] == "screen": ticks += [t + a["at"] * dur for a in sc.get("taps", [])]; hits += [t + sc["drop"]["at"] * dur + 0.7] if sc.get("drop") else []
        if sc["type"] == "path": ticks += [t + (k + 0.62) * dur / len(sc["screens"]) for k in range(len(sc["screens"]))]
        if sc["type"] == "react" and sc.get("verdict"):
            sc["verdictAt"] = round(min(dur - 0.4, sc.get("verdictAt", max(0.7, vlen * 0.6))), 3); hits.append(t + sc["verdictAt"])
        if sc.get("payoff") and "hookUntil" not in spec.get("fx", {}): spec.setdefault("fx", {})["hookUntil"] = round(t, 3)
        if sc["type"] == "stat": ticks += [t + 0.1 + k * (1.0 / 20) for k in range(20)]
        if sc["type"] in ("steps", "checks"):
            n = len(sc["items"]); span = max(0.6, (vlen if vlen else dur) - 0.3)
            sc["itemTimes"] = [round(t + 0.35 + k * span / n, 3) for k in range(n)]; ticks += sc["itemTimes"]
        t += dur
        sc.pop("_ph", None)
    total = round(t, 3)
    if total > 90: print(f"warning: reel is {total:.1f}s; aim for 15–60s")
    fx = spec.get("fx", {})
    if "hookUntil" not in fx: fx["hookUntil"] = spec["scenes"][-1]["start"]  # banner disappears at the end card
    tl = {"dur": total, "scenes": spec["scenes"], "fx": fx, "caps": caption_chunks(lines), "mascot": spec.get("mascot", True)}
    # 3. sound: voice track first (the mascot lip-syncs to it), then music ducked under it
    SR = music.SR
    bed = music.make(total, cuts, hits, ticks, end_at=spec["scenes"][-1]["start"], seed=zlib.crc32(spec.get("id", "").encode()) % 1000, mode=spec.get("music", "sfx"))
    vo = np.zeros(len(bed), np.float32)
    for start, a in vo_track:
        up = resample_poly(a, SR, tts.SR).astype(np.float32); i = int(start * SR); j = min(len(vo), i + len(up))
        vo[i:j] += up[: j - i]
    if np.max(np.abs(vo)) > 0: vo = vo / np.max(np.abs(vo)) * 0.9
    # lip-sync: how open the mascot's mouth is on each video frame (30 fps), from the voice loudness
    hop = SR // 30; n = int(np.ceil(len(vo) / hop))
    rms = np.array([np.sqrt(np.mean(vo[i * hop:(i + 1) * hop] ** 2)) if (i + 1) * hop <= len(vo) else 0.0 for i in range(n)])
    ref = np.percentile(rms[rms > 0.005], 90) if np.any(rms > 0.005) else 1.0
    mouth = np.clip((rms - 0.008) / max(ref, 1e-4), 0, 1) ** 0.7
    mouth = np.convolve(mouth, [0.25, 0.5, 0.25], mode="same")
    tl["mouth"] = [round(float(v), 2) for v in mouth]
    json.dump(tl, open(os.path.join(out_dir, "timeline.json"), "w"), ensure_ascii=False)
    # 4. picture
    sd = os.path.join(out_dir, "stills") if stills else ""
    if sd: os.makedirs(sd, exist_ok=True)
    silent = os.path.join(out_dir, "silent.mp4")
    subprocess.run(["node", os.path.join(HERE, "render.js"), os.path.join(out_dir, "timeline.json"), silent] + ([sd] if sd else []), check=True)
    envl = np.convolve(np.abs(vo), np.ones(2400) / 2400, mode="same")
    duck = 1 - 0.68 * np.clip(envl / 0.04, 0, 1)
    duck = np.convolve(duck, np.ones(4800) / 4800, mode="same")
    mix = bed * (0.5 * duck)[:, None] + vo[:, None] * 1.0
    mix = np.tanh(mix * 1.1); mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
    wav = os.path.join(out_dir, "mix.wav")
    wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    reel = os.path.join(out_dir, "reel.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", "48000", "-shortest",
                    "-use_editlist", "0", "-movflags", "+faststart", reel], check=True)
    cover_t = spec["scenes"][1]["start"] + 0.9 if len(spec["scenes"]) > 1 else 1.0
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(cover_t), "-i", silent, "-frames:v", "1", "-q:v", "3", os.path.join(out_dir, "cover.jpg")], check=True)
    with open(os.path.join(out_dir, "captions.srt"), "w") as f:
        for k, (a, b, text) in enumerate(lines, 1):
            f.write(f"{k}\n{srt_time(a)} --> {srt_time(b)}\n{text}\n\n")
    for tmp in (silent, wav): os.remove(tmp)
    json.dump({"id": spec.get("id"), "duration": total, "caption": spec.get("caption", ""), "cover_offset_ms": int(cover_t * 1000)},
              open(os.path.join(out_dir, "meta.json"), "w"), ensure_ascii=False, indent=1)
    raw = json.load(open(spec_path))  # record render facts on the queue item for the poster
    raw.update(cover_offset_ms=int(cover_t * 1000), duration=total)
    json.dump(raw, open(spec_path, "w"), ensure_ascii=False, indent=2)
    print(f"built {reel} ({total:.1f}s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--stills" in sys.argv)
