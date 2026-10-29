"""Kinetic-type reel: no mascot, no cards. Huge words punch in one beat at a time, synced to the voice,
with real SaveSort screenshots as proof and a white flash as a pattern interrupt.
Usage (repo root): python3 content/kinetic.py ads/<id>.json out/<id> [--stills]
Spec: {"voice", "speed", "pitch", "beats": [{"kind": text|flash|crumb|shot, "vo", "chunks": [...], ...}]}
Chunk markup: *word* = yellow, !word! = red (and a screen shake).
"""
import json, os, re, subprocess, sys, zlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.io import wavfile
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "..", "engine")
sys.path.insert(0, ENG)
import g2p, tts, music  # noqa: E402

W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
INK, WHITE, YEL, RED, COBALT = (12, 12, 15), (250, 250, 247), (255, 222, 61), (255, 72, 72), (31, 60, 255)
BG = {"text": INK, "crumb": INK, "shot": INK, "flash": WHITE}
SAFE_L, SAFE_R = 90, W - 150          # nothing in the right 150px
_fonts = {}


def font(size, path=FONT):
    k = (size, path)
    if k not in _fonts: _fonts[k] = ImageFont.truetype(path, size)
    return _fonts[k]


def ease(p): p = min(1.0, max(0.0, p)); return 1 - (1 - p) ** 3


def parse(text):
    """'a *b* !c!' -> [(word, colour_key)]"""
    out = []
    for m in re.finditer(r"\*([^*]+)\*|!([^!]+)!|(\S+)", text):
        if m.group(1): out += [(w, "y") for w in m.group(1).split()]
        elif m.group(2): out += [(w, "r") for w in m.group(2).split()]
        else: out.append((m.group(3), "n"))
    return out


def rich(text, base, maxw, size=200, minsize=90, maxlines=3, align="center"):
    """Render marked-up text as a tight RGBA layer, shrinking to fit maxw."""
    words = parse(text)
    while True:
        f = font(size); sp = f.getlength(" ")
        lines, cur, cw = [], [], 0
        for w, c in words:
            ww = f.getlength(w)
            if cur and cw + sp + ww > maxw: lines.append((cur, cw)); cur, cw = [], 0
            cw = cw + (sp if cur else 0) + ww; cur.append((w, c, ww))
        if cur: lines.append((cur, cw))
        if (len(lines) <= maxlines and max(l[1] for l in lines) <= maxw) or size <= minsize: break
        size -= 8
    lh = int(size * 1.02); wd = int(max(l[1] for l in lines)) + 20
    im = Image.new("RGBA", (wd, lh * len(lines) + int(size * 0.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (ln, lw) in enumerate(lines):
        x = (wd - lw) / 2 if align == "center" else 0
        for w, c, ww in ln:
            col = {"y": YEL, "r": RED}.get(c, base)
            if c == "y" and base == INK: col = COBALT  # yellow is unreadable on the white flash
            d.text((x, i * lh), w, font=font(size), fill=col)
            x += ww + font(size).getlength(" ")
    return im


def place(frame, layer, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if scale != 1.0: layer = layer.resize((max(1, int(layer.width * scale)), max(1, int(layer.height * scale))), Image.BICUBIC)
    if rot: layer = layer.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = layer.getchannel("A").point(lambda v: int(v * alpha)); layer.putalpha(a)
    frame.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def rounded(img, r=44):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, fill=255)
    out = img.convert("RGBA"); out.putalpha(m); return out


def shadowed(img, blur=30, off=24):
    pad = blur * 2; s = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 170)); sh.putalpha(img.getchannel("A").point(lambda v: int(v * 0.65)))
    s.alpha_composite(sh, (pad, pad + off)); s = s.filter(ImageFilter.GaussianBlur(blur)); s.alpha_composite(img, (pad, pad)); return s


def build(spec_path, out_dir, stills=False):
    spec = json.load(open(spec_path)); os.makedirs(out_dir, exist_ok=True)
    beats = spec["beats"]; voice = spec.get("voice", "am_michael"); speed = spec.get("speed", 1.18)
    bad = []
    for b in beats:
        try: b["_ph"] = g2p.phonemize(b["vo"])
        except g2p.UnknownWords as e: bad.append(f'{b["vo"]!r}: {e}')
    if bad: print("UNKNOWN WORDS:\n  " + "\n  ".join(bad)); sys.exit(2)
    # 1. voice + timing: each chunk appears when its share of the line is spoken
    t = 0.0; vo_track = []; cuts, hits, ticks = [], [], []
    for b in beats:
        a = tts.speak(b.pop("_ph"), voice, b.get("speed", speed))
        if spec.get("pitch"): a = tts.pitch(a, spec["pitch"])
        vlen = len(a) / tts.SR; lead = 0.05
        dur = vlen + lead + b.get("tail", 0.12)
        wts = [len(re.sub(r"[*!]", "", c)) + 4 for c in b["chunks"]]; cum = np.concatenate([[0], np.cumsum(wts)]) / sum(wts)
        b["start"], b["dur"] = t, dur
        b["times"] = [t + lead + vlen * cum[i] * 0.97 for i in range(len(b["chunks"]))]
        vo_track.append((t + lead, a)); cuts.append(t)
        for i, c in enumerate(b["chunks"]):
            (hits if "!" in c or b.get("kind") == "flash" and i == 0 else ticks).append(b["times"][i])
        t += dur
    total = t
    # 2. sound: our synthesised effects only, ducked under the voice
    SR = music.SR
    bed = music.make(total, cuts, hits, ticks[::2], end_at=total, seed=zlib.crc32(spec["id"].encode()) % 1000, mode="sfx")
    vo = np.zeros(len(bed), np.float32)
    for st, a in vo_track:
        up = resample_poly(a, SR, tts.SR).astype(np.float32); i = int(st * SR); j = min(len(vo), i + len(up)); vo[i:j] += up[: j - i]
    vo = vo / (np.max(np.abs(vo)) + 1e-9) * 0.9
    envl = np.convolve(np.abs(vo), np.ones(2400) / 2400, mode="same"); duck = 1 - 0.6 * np.clip(envl / 0.04, 0, 1)
    mix = bed * (0.55 * duck)[:, None] + vo[:, None]; mix = np.tanh(mix * 1.1); mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
    wav = os.path.join(out_dir, "mix.wav"); wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    # 3. assets
    scr = os.path.join(ENG, "screens")
    shots = {}
    for b in beats:
        if b["kind"] == "shot":
            src = Image.open(os.path.join(scr, b["shot"])).convert("RGB")
            y0, y1 = b.get("crop", [0, 900]); im = src.crop((0, y0, src.width, y1))
            sc = 800 / im.width; im = im.resize((800, int(im.height * sc)), Image.LANCZOS)
            if b.get("box"):  # yellow highlight around a region (in source px)
                x, y, w, h = b["box"]; d = ImageDraw.Draw(im)
                d.rounded_rectangle(((x) * sc, (y - y0) * sc, (x + w) * sc, (y - y0 + h) * sc), 28, outline=YEL, width=12)
            b["_img"] = shadowed(rounded(im))
    zipcard = rich("saves.zip", INK, 600, size=64)
    zc = Image.new("RGBA", (zipcard.width + 80, zipcard.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(zc).rounded_rectangle((0, 0, zc.width - 1, zc.height - 1), 26, fill=YEL); zc.alpha_composite(zipcard, (40, 22))
    vign = Image.radial_gradient("L").resize((W, H)).point(lambda v: int(v * 0.55))
    rng = np.random.default_rng(3)
    layers = {}

    def chunk_layer(b, i):
        k = (id(b), i)
        if k not in layers:
            base = INK if b["kind"] == "flash" else WHITE
            maxw = SAFE_R - SAFE_L - 40
            size = 230 if b["kind"] in ("text", "flash") else 130
            layers[k] = rich(b["chunks"][i], base, maxw, size=size)
        return layers[k]

    tilts = {}

    def frame_at(tt):
        b = next((x for x in beats if x["start"] <= tt < x["start"] + x["dur"]), beats[-1])
        bg = COBALT if b.get("bg") == "cobalt" else BG[b["kind"]]
        fr = Image.new("RGBA", (W, H), bg + (255,))
        if b["kind"] != "flash": fr.paste((0, 0, 0, 255), (0, 0), Image.eval(vign, lambda v: v))
        lt = tt - b["start"]
        idx = max([i for i, s in enumerate(b["times"]) if s <= tt] or [0])
        since = tt - b["times"][idx]
        # shake on red words
        sx = sy = 0
        if "!" in b["chunks"][idx] and since < 0.3:
            amp = 16 * (1 - since / 0.3); sx, sy = rng.uniform(-amp, amp), rng.uniform(-amp, amp)
        if b.get("label"):
            lab = rich(b["label"], YEL, 900, size=44)
            place(fr, lab, W / 2 - 30, 300)
        if b["kind"] == "crumb":
            items = b.get("_items", b["chunks"]); offset = b.get("_offset", 0)
            shown = [it for i, it in enumerate(items) if i < offset or (i - offset) <= idx and tt >= b["times"][0]]
            y = 420
            for j, it in enumerate(shown):
                last = j == len(shown) - 1
                col = WHITE if last else (150, 150, 155)
                ly = rich(("→ " if j else "") + it, col, SAFE_R - SAFE_L - 60, size=78 if last else 60, maxlines=2)
                p = ease((tt - b["times"][j - offset]) / 0.18) if last and j >= offset else 1
                frame_x = SAFE_L + ly.width / 2 - 30 * (1 - p)
                place(fr, ly, frame_x + sx, y + ly.height / 2 + sy, alpha=p)
                y += ly.height + 18
        elif b["kind"] == "shot":
            p = ease(lt / 0.4); img = b["_img"]
            place(fr, img, W / 2 - 30 + sx, 1010 + 500 * (1 - p) + sy, rot=-3 + 1.5 * p)
            if b.get("zip"):  # a zip file drops into the drop zone
                zp = ease((lt - 0.45) / 0.45)
                if lt > 0.45: place(fr, zc, W / 2 - 30, 430 + 640 * zp, rot=8 * (1 - zp), alpha=min(1, (lt - 0.45) / 0.15))
            ly = chunk_layer(b, idx); pp = ease(since / 0.12)
            place(fr, ly, W / 2 - 30 + sx, 330 + sy, scale=1.15 - 0.15 * pp)
        else:
            ly = chunk_layer(b, idx); pp = ease(since / 0.12)
            if (id(b), idx) not in tilts: tilts[(id(b), idx)] = float(rng.uniform(-2.5, 2.5))
            place(fr, ly, W / 2 - 30 + sx, 860 + sy, scale=1.22 - 0.22 * pp, rot=tilts[(id(b), idx)] * (1 - pp) * 0.6)
        # progress bar
        ImageDraw.Draw(fr).rectangle((0, 0, int(W * tt / total), 12), fill=YEL if bg != YEL else INK)
        return fr.convert("RGB")

    # crumb beats can continue the previous list
    prev = None
    for b in beats:
        if b["kind"] == "crumb":
            if b.get("continue") and prev is not None:
                b["_items"] = prev["_items"] + b["chunks"]; b["_offset"] = len(prev["_items"])
                # earlier items are already on screen: align times so index math works
            else: b["_items"] = list(b["chunks"]); b["_offset"] = 0
            prev = b
    # 4. picture
    silent = os.path.join(out_dir, "silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", silent], stdin=subprocess.PIPE)
    sd = os.path.join(out_dir, "stills"); os.makedirs(sd, exist_ok=True) if stills else None
    n = int(total * FPS)
    for k in range(n):
        ff.stdin.write(frame_at(k / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    if stills:  # one still per beat, taken when its last chunk has landed
        for i, b in enumerate(beats):
            frame_at(min(b["start"] + b["dur"] - 0.05, b["times"][-1] + 0.3)).save(os.path.join(sd, f"scene-{i}.png"))
    reel = os.path.join(out_dir, "reel.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-ac", "2", "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", "48000", "-shortest", "-use_editlist", "0", "-movflags", "+faststart", reel], check=True)
    os.remove(silent); os.remove(wav)
    print(f"built {reel} ({total:.1f}s)")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], "--stills" in sys.argv)
