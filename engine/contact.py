"""Contact sheet of every scene still for the given out/ dirs: python3 engine/contact.py out.png out/<id> ..."""
import sys, glob
from PIL import Image, ImageDraw
rows = []
for d in sys.argv[2:]:
    fs = sorted(glob.glob(d + "/stills/scene-*.png"), key=lambda f: int(f.split("-")[-1][:-4]))
    rows.append([Image.open(f).resize((216, 384)) for f in fs])
w = max(len(r) for r in rows) * 224; s = Image.new("RGB", (w, 392 * len(rows)), "white")
for y, r in enumerate(rows):
    for x, im in enumerate(r): s.paste(im, (x * 224, y * 392))
s.save(sys.argv[1]); print("ok")
