"""Original cartoon characters for kinetic reels. Each one is drawn from simple shapes, with a face whose mood
and mouth (0 = closed, 1 = wide open) change per frame. Usage: char_img("brain", "shocked", 0.6, scale=1.0)
Characters: ghost, tombstone, brain, phone, goldfish, potato."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 2  # draw at 2x, then downscale for smooth edges
K = (20, 20, 28)
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"


def face(d, cx, ey, mood, mouth, skin, ex=46, eye=1.0, blush=(255, 170, 190)):
    """Eyes at height ey, mouth below. Sizes are in 1x units."""
    e = lambda v: v * S * eye
    for sgn in (-1, 1):
        x = cx + sgn * ex * S
        if mood == "happy":
            d.arc((x - e(22), ey - e(18), x + e(22), ey + e(22)), 200, 340, fill=K, width=int(e(9)))
        elif mood == "shocked":
            d.ellipse((x - e(24), ey - e(34), x + e(24), ey + e(34)), fill=K); d.ellipse((x - e(8), ey - e(22), x + e(6), ey - e(8)), fill="white")
        else:
            d.ellipse((x - e(17), ey - e(26), x + e(17), ey + e(26)), fill=K); d.ellipse((x - e(6), ey - e(18), x + e(4), ey - e(8)), fill="white")
            if mood == "smug":
                d.rectangle((x - e(20), ey - e(30), x + e(20), ey - e(2)), fill=skin); d.line((x - e(20), ey - e(2), x + e(20), ey - e(2)), fill=K, width=int(e(6)))
            if mood == "sad":
                d.line((x - e(20), ey - e(36) - sgn * e(8), x + e(20), ey - e(36) + sgn * e(8)), fill=K, width=int(e(6)))
    if blush:
        for sgn in (-1, 1):
            x = cx + sgn * (ex + 36) * S * eye; d.ellipse((x - e(16), ey + e(26), x + e(16), ey + e(44)), fill=blush)
    my = ey + e(62); mw = e(16 + 26 * mouth); mh = e(6 + 46 * mouth)
    if mouth < 0.08 and mood in ("happy", "smug"):
        d.arc((cx - e(22), my - e(22), cx + e(22), my + e(10)), 20, 160, fill=K, width=int(e(7)))
    elif mouth < 0.08 and mood == "sad":
        d.arc((cx - e(22), my - e(4), cx + e(22), my + e(28)), 200, 340, fill=K, width=int(e(7)))
    else:
        d.ellipse((cx - mw, my - mh / 2, cx + mw, my + mh / 2), fill=K)


def _ghost(d, w, h, mood, mouth):
    body = (246, 246, 252); cx, top, r, bot = w // 2, 40 * S, 120 * S, 300 * S
    d.ellipse((cx - r, top, cx + r, top + 2 * r), fill=body); d.rectangle((cx - r, top + r, cx + r, bot), fill=body)
    bw = 2 * r / 4
    for k in range(0, 4, 2): x0 = cx - r + k * bw; d.ellipse((x0, bot - bw / 2, x0 + bw, bot + bw / 2), fill=body)
    face(d, cx, top + 110 * S, mood, mouth, body)


def _tombstone(d, w, h, mood, mouth):
    stone, dark = (168, 172, 186), (120, 124, 138); cx = w // 2
    d.rounded_rectangle((cx - 120 * S, 30 * S, cx + 120 * S, 320 * S), 110 * S, fill=stone)
    d.rectangle((cx - 120 * S, 200 * S, cx + 120 * S, 320 * S), fill=stone)
    d.text((cx, 78 * S), "RIP", font=ImageFont.truetype(FONT, 46 * S), fill=dark, anchor="mm")
    d.line((cx + 60 * S, 120 * S, cx + 84 * S, 170 * S, cx + 70 * S, 200 * S), fill=dark, width=4 * S)  # crack
    for k in range(9):  # grass
        x = cx - 140 * S + k * 35 * S; d.polygon([(x, 330 * S), (x + 14 * S, 296 * S), (x + 28 * S, 330 * S)], fill=(70, 170, 90))
    face(d, cx, 160 * S, mood, mouth, stone, ex=40, eye=0.85, blush=None)


def _brain(d, w, h, mood, mouth):
    pink, fold = (255, 150, 180), (220, 100, 140); cx = w // 2
    d.ellipse((cx - 140 * S, 40 * S, cx + 140 * S, 270 * S), fill=pink)
    for k, (x0, y0) in enumerate([(-110, 70), (-40, 52), (30, 58), (-90, 130), (60, 120)]):
        d.arc((cx + x0 * S, y0 * S, cx + (x0 + 70) * S, (y0 + 50) * S), 180, 360, fill=fold, width=6 * S)
    d.rounded_rectangle((cx - 26 * S, 250 * S, cx + 26 * S, 320 * S), 20 * S, fill=fold)  # stem
    face(d, cx, 175 * S, mood, mouth, pink, ex=44, eye=0.85, blush=(255, 110, 150))


def _phone(d, w, h, mood, mouth):
    case, scr = (35, 35, 45), (150, 210, 255); cx = w // 2
    d.rounded_rectangle((cx - 105 * S, 20 * S, cx + 105 * S, 330 * S), 34 * S, fill=case)
    d.rounded_rectangle((cx - 92 * S, 34 * S, cx + 92 * S, 316 * S), 26 * S, fill=scr)
    d.rounded_rectangle((cx - 30 * S, 44 * S, cx + 30 * S, 58 * S), 7 * S, fill=case)  # notch
    d.line((cx + 30 * S, 34 * S, cx + 10 * S, 90 * S, cx + 46 * S, 120 * S, cx + 30 * S, 160 * S), fill=(255, 255, 255), width=3 * S)  # crack
    d.rectangle((cx + 52 * S, 70 * S, cx + 80 * S, 84 * S), outline=K, width=2 * S); d.rectangle((cx + 54 * S, 72 * S, cx + 60 * S, 82 * S), fill=(255, 72, 72))  # low battery
    face(d, cx, 170 * S, mood, mouth, scr, ex=38, eye=0.8, blush=None)


def _goldfish(d, w, h, mood, mouth):
    orange, fin = (255, 140, 40), (255, 190, 90); cx = w // 2 + 40 * S
    d.polygon([(cx - 100 * S, 175 * S), (cx - 175 * S, 95 * S), (cx - 165 * S, 255 * S)], fill=fin)  # tail
    d.ellipse((cx - 120 * S, 75 * S, cx + 100 * S, 275 * S), fill=orange)
    d.polygon([(cx - 30 * S, 85 * S), (cx + 20 * S, 35 * S), (cx + 40 * S, 95 * S)], fill=fin)  # top fin
    for (bx, by, r) in [(70, 40, 12), (86, 6, 8), (64, -22, 6)]:
        d.ellipse((cx + (bx - r) * S, (by - r + 10) * S, cx + (bx + r) * S, (by + r + 10) * S), outline=(190, 230, 255), width=3 * S)
    face(d, cx - 5 * S, 160 * S, mood, mouth, orange, ex=38, eye=0.8, blush=(255, 110, 90))


def _potato(d, w, h, mood, mouth):
    tan, spot = (200, 150, 95), (165, 115, 70); cx = w // 2
    d.ellipse((cx - 130 * S, 40 * S, cx + 125 * S, 320 * S), fill=tan)
    d.ellipse((cx - 110 * S, 30 * S, cx + 40 * S, 150 * S), fill=tan)
    for (x, y, r) in [(-90, 90, 8), (70, 80, 7), (-60, 270, 9), (80, 250, 6), (10, 60, 5)]:
        d.ellipse((cx + (x - r) * S, (y - r) * S, cx + (x + r) * S, (y + r) * S), fill=spot)
    face(d, cx, 170 * S, mood, mouth, tan, ex=42, eye=0.85, blush=(240, 130, 110))


BODIES = {"ghost": _ghost, "tombstone": _tombstone, "brain": _brain, "phone": _phone, "goldfish": _goldfish, "potato": _potato}


def char_img(kind="ghost", mood="happy", mouth=0.0, scale=1.0):
    w, h = 300 * S, 340 * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); BODIES[kind](ImageDraw.Draw(im), w, h, mood, mouth)
    im = im.resize((int(w / S * scale), int(h / S * scale)), Image.LANCZOS)
    pad = 36; s = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 170)); sh.putalpha(im.getchannel("A").point(lambda v: int(v * 0.6)))
    s.alpha_composite(sh, (pad, pad + 14)); s = s.filter(ImageFilter.GaussianBlur(18)); s.alpha_composite(im, (pad, pad))
    return s


if __name__ == "__main__":  # preview sheet: python3 content/characters.py out.png
    import sys
    moods = ["happy", "shocked", "sad", "smug", "suspicious"]
    sheet = Image.new("RGB", (len(moods) * 360, len(BODIES) * 420), (12, 12, 15))
    for r, k in enumerate(BODIES):
        for c, m in enumerate(moods):
            sheet.paste(char_img(k, m, 0.5 if c % 2 else 0.0), (c * 360, r * 420), char_img(k, m, 0.5 if c % 2 else 0.0))
    sheet.save(sys.argv[1])
