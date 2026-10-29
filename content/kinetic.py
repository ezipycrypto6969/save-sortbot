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
BG = {"text": INK, "crumb": INK, "shot": INK, "reel": INK, "flash": WHITE}
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


GHOST_BODY = (246, 246, 252)


def ghost_img(mood="happy", mouth=0.0, scale=1.0):
    """The ghost of your saved tab: a soft white ghost whose mouth follows the voice."""
    S = 2; w, h = 300 * S, 340 * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, top, r, bot = w // 2, 40 * S, 120 * S, 300 * S
    d.ellipse((cx - r, top, cx + r, top + 2 * r), fill=GHOST_BODY)
    d.rectangle((cx - r, top + r, cx + r, bot), fill=GHOST_BODY)
    bw = 2 * r / 4
    for k in range(4):  # wavy hem
        x0 = cx - r + k * bw
        d.ellipse((x0, bot - bw / 2, x0 + bw, bot + bw / 2), fill=GHOST_BODY if k % 2 == 0 else (0, 0, 0, 0))
    for k in (1, 3):
        x0 = cx - r + k * bw; d.pieslice((x0, bot - bw / 2, x0 + bw, bot + bw / 2), 180, 360, fill=(0, 0, 0, 0))
    ey = top + 110 * S; ex = 46 * S; K = (20, 20, 28)
    for sgn in (-1, 1):
        x = cx + sgn * ex
        if mood == "happy":
            d.arc((x - 22 * S, ey - 18 * S, x + 22 * S, ey + 22 * S), 200, 340, fill=K, width=9 * S)
        elif mood == "shocked":
            d.ellipse((x - 24 * S, ey - 34 * S, x + 24 * S, ey + 34 * S), fill=K); d.ellipse((x - 8 * S, ey - 22 * S, x + 6 * S, ey - 8 * S), fill="white")
        else:
            d.ellipse((x - 17 * S, ey - 26 * S, x + 17 * S, ey + 26 * S), fill=K); d.ellipse((x - 6 * S, ey - 18 * S, x + 4 * S, ey - 8 * S), fill="white")
            if mood == "smug": d.rectangle((x - 20 * S, ey - 30 * S, x + 20 * S, ey - 2 * S), fill=GHOST_BODY); d.line((x - 20 * S, ey - 2 * S, x + 20 * S, ey - 2 * S), fill=K, width=6 * S)
            if mood == "sad": d.line((x - 20 * S, ey - 36 * S - sgn * 8 * S, x + 20 * S, ey - 36 * S + sgn * 8 * S), fill=K, width=6 * S)
    for sgn in (-1, 1):  # cheeks
        x = cx + sgn * 82 * S; d.ellipse((x - 16 * S, ey + 26 * S, x + 16 * S, ey + 44 * S), fill=(255, 170, 190))
    my = ey + 62 * S; mw = (16 + 26 * mouth) * S; mh = (6 + 46 * mouth) * S
    if mouth < 0.08 and mood in ("happy", "smug"):
        d.arc((cx - 22 * S, my - 22 * S, cx + 22 * S, my + 10 * S), 20, 160, fill=K, width=7 * S)
    else:
        d.ellipse((cx - mw, my - mh / 2, cx + mw, my + mh / 2), fill=K)
    im = im.resize((int(w / S * scale), int(h / S * scale)), Image.LANCZOS)
    return shadowed(im, blur=18, off=14)


def tile_wall(seed=5):
    """A dim wall of saved-reel tiles that scrolls behind the words."""
    rng = np.random.default_rng(seed)
    labels = ["gym plan", "pasta", "side hustle", "AI tool", "comment GUIDE", "$1000/day", "morning routine", "cold email", "secret mode",
              "budget hack", "Google Maps", "study hack", "dropshipping", "breathwork", "tax news", "prompt pack", "watch later", "SEO tip"]
    cols, tw, th, gap = 3, 330, 470, 24
    rows = 9; wall = Image.new("RGB", (W, rows * (th + gap)), INK); d = ImageDraw.Draw(wall)
    pal = [(255, 120, 90), (90, 140, 255), (255, 200, 80), (120, 220, 170), (200, 120, 255), (255, 110, 170), (90, 200, 240)]
    for r_ in range(rows):
        for c in range(cols):
            x = 18 + c * (tw + gap); y = r_ * (th + gap) + (c % 2) * 120 - 60
            col = pal[rng.integers(len(pal))]; col2 = tuple(int(v * 0.45) for v in col)
            tile = Image.new("RGB", (tw, th), col)
            g = Image.linear_gradient("L").resize((tw, th)); tile = Image.composite(Image.new("RGB", (tw, th), col2), tile, g)
            td = ImageDraw.Draw(tile); td.text((22, th - 76), labels[rng.integers(len(labels))], font=font(36), fill="white")
            td.polygon([(tw - 58, 22), (tw - 26, 22), (tw - 26, 70), (tw - 42, 58), (tw - 58, 70)], fill="white")
            m = Image.new("L", (tw, th), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, tw - 1, th - 1), 30, fill=255)
            wall.paste(tile, (x, y), m)
    wall = wall.filter(ImageFilter.GaussianBlur(3))
    return Image.blend(wall, Image.new("RGB", wall.size, INK), 0.8)


def fake_reel(caption, label="SAVED REEL · PARAPHRASED"):
    """A made-up reel (no real creator, handle blurred) showing a claim from a saved reel."""
    w, h = 560, 960
    im = Image.new("RGB", (w, h)); g = Image.linear_gradient("L").resize((w, h))
    im = Image.composite(Image.new("RGB", (w, h), (40, 20, 70)), Image.new("RGB", (w, h), (255, 140, 60)), g)
    d = ImageDraw.Draw(im)
    d.ellipse((w / 2 - 260, 640, w / 2 + 260, 1120), fill=(25, 15, 35))         # shoulders
    d.ellipse((w / 2 - 95, 440, w / 2 + 95, 650), fill=(25, 15, 35))            # head
    d.rounded_rectangle((w / 2 - 80, 510, w / 2 + 80, 556), 18, fill=(5, 5, 8))  # sunglasses
    cap = rich(caption, WHITE, w - 80, size=60, maxlines=4)
    stroke = Image.new("RGBA", (cap.width + 40, cap.height + 30), (0, 0, 0, 140))
    m = Image.new("L", stroke.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, stroke.width - 1, stroke.height - 1), 20, fill=140); stroke.putalpha(m)
    base = im.convert("RGBA"); base.alpha_composite(stroke, ((w - stroke.width) // 2, 150)); base.alpha_composite(cap, ((w - cap.width) // 2, 165))
    d = ImageDraw.Draw(base)
    d.ellipse((28, h - 150, 84, h - 94), fill=(230, 230, 235))
    blur = Image.new("RGBA", (200, 26), (230, 230, 235, 255)).filter(ImageFilter.GaussianBlur(6)); base.alpha_composite(blur, (98, h - 136))
    d.rounded_rectangle((28, h - 70, w - 140, h - 54), 8, fill=(200, 200, 205)); d.rounded_rectangle((28, h - 44, w - 220, h - 30), 7, fill=(160, 160, 168))
    ix = w - 62
    d.ellipse((ix - 22, h - 360, ix, h - 338), outline="white", width=6); d.ellipse((ix - 4, h - 360, ix + 18, h - 338), outline="white", width=6)
    d.polygon([(ix - 22, h - 346), (ix + 18, h - 346), (ix - 2, h - 318)], outline="white", width=6)
    d.rounded_rectangle((ix - 22, h - 280, ix + 20, h - 244), 14, outline="white", width=6)
    d.polygon([(ix - 22, h - 200), (ix + 22, h - 216), (ix + 6, h - 172)], outline="white", width=6)
    lab = rich(label, YEL, w, size=26, minsize=26); chip = Image.new("RGBA", (lab.width + 24, lab.height + 10), (0, 0, 0, 200))
    chip.alpha_composite(lab, (12, 8)); base.alpha_composite(chip, (24, 26))
    return rounded(base, 40)


def stamp_img(text, color=RED):
    t = rich(text, color, 900, size=92); s = Image.new("RGBA", (t.width + 70, t.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((4, 4, s.width - 5, s.height - 5), 26, outline=color, width=14); s.alpha_composite(t, (35, 18))
    return s


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
        if b.get("stamp"): b["stampAt"] = b["times"][-1] + 0.25; hits.append(b["stampAt"])
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
    hop = SR // FPS; nfr = len(vo) // hop + 1
    rms = np.array([np.sqrt(np.mean(vo[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(vo) else 0 for i in range(nfr)])
    ref = np.percentile(rms[rms > 0.005], 90) if np.any(rms > 0.005) else 1.0
    mouth = np.convolve(np.clip((rms - 0.008) / ref, 0, 1) ** 0.7, [0.25, 0.5, 0.25], mode="same")
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
    for b in beats:
        if b["kind"] == "reel": b["_img"] = shadowed(fake_reel(b["caption"]))
        if b.get("stamp"): b["_stamp"] = stamp_img(b["stamp"], RED if b.get("stampColor", "red") == "red" else YEL)
    wall = tile_wall(); gcache = {}

    def ghost(mood, m, sc):
        k = (mood, round(m * 5), sc)
        if k not in gcache: gcache[k] = ghost_img(mood, round(m * 5) / 5, sc)
        return gcache[k]
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
            if isinstance(b.get("ghost"), dict) and b["ghost"].get("big"): size = 170
            layers[k] = rich(b["chunks"][i], base, maxw, size=size)
        return layers[k]

    tilts = {}

    def frame_at(tt):
        b = next((x for x in beats if x["start"] <= tt < x["start"] + x["dur"]), beats[-1])
        bg = COBALT if b.get("bg") == "cobalt" else BG[b["kind"]]
        fr = Image.new("RGBA", (W, H), bg + (255,))
        if bg == INK:
            off = int(tt * 70) % (wall.height - H); fr.paste(wall.crop((0, off, W, off + H)), (0, 0))
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
        elif b["kind"] == "reel":
            p = ease(lt / 0.35)
            place(fr, b["_img"], W / 2 - 30 + sx, 1000 + 520 * (1 - p) + sy, rot=4 - 2 * p)
            ly = chunk_layer(b, idx); pp = ease(since / 0.12)
            place(fr, ly, W / 2 - 30 + sx, 330 + sy, scale=1.15 - 0.15 * pp)
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
            ty = 560 if isinstance(b.get("ghost"), dict) and b["ghost"].get("big") else 860
            place(fr, ly, W / 2 - 30 + sx, ty + sy, scale=1.22 - 0.22 * pp, rot=tilts[(id(b), idx)] * (1 - pp) * 0.6)
        if b.get("_stamp") and tt >= b["stampAt"]:
            q = ease((tt - b["stampAt"]) / 0.14)
            place(fr, b["_stamp"], W / 2 - 30, 1080, scale=2.2 - 1.2 * q, rot=-12, alpha=min(1, 0.3 + q))
        g = b.get("ghost")
        if g:
            g = {"mood": g} if isinstance(g, str) else g
            big = g.get("big"); sc = 1.5 if big else 0.85
            m = float(mouth[min(len(mouth) - 1, int(tt * FPS))])
            gi = ghost(g.get("mood", "happy"), m, sc)
            gp = ease(lt / 0.3) if b.get("_gin") else 1
            gx = W / 2 - 30 if big else 230; gy = 1270 if big else 1360
            place(fr, gi, gx, gy + 14 * np.sin(tt * 3.9) + 200 * (1 - gp), rot=4 * np.sin(tt * 2.1))
        # progress bar
        ImageDraw.Draw(fr).rectangle((0, 0, int(W * tt / total), 12), fill=YEL if bg != YEL else INK)
        out = fr.convert("RGB")
        recent = [h_ for h_ in hits if 0 <= tt - h_ < 0.22]
        if recent:  # camera punch on every hit
            z = 1 + 0.045 * (1 - (tt - recent[-1]) / 0.22)
            big = out.resize((int(W * z), int(H * z)), Image.BILINEAR); x0 = (big.width - W) // 2; y0 = (big.height - H) // 2
            out = big.crop((x0, y0, x0 + W, y0 + H))
        return out

    for i, b in enumerate(beats):  # the ghost slides in only when he wasn't on screen already
        big = lambda x: isinstance(x.get("ghost"), dict) and bool(x["ghost"].get("big"))
        b["_gin"] = i > 0 and bool(b.get("ghost")) and (not beats[i - 1].get("ghost") or big(b) != big(beats[i - 1]))
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
