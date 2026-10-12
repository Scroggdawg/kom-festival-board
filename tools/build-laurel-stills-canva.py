#!/usr/bin/env python3
"""Ops file for a separate Canva design: every still x each festival laurel, one page each, the still
full-bleed and the laurel as its own movable element (Luke, 2026-10-11: "every still with each logo,
then I'm going to go in and move them around").

Writes press/assets/derived/canva-laurel-stills/still-1.1.N.jpg (1920x803, the 2.39:1 picture of each
export), press/assets/derived/laurels/BEST-2026-winner_*_stacked.png, and canva/ops/laurel-stills-canva.json
(schema 1, page 1920 x 803 "pt", so s = 1 on a 1920 x 803 px design). Built by the kom-epk-builder app
with the ops URL set to https://scroggdawg.github.io/kom-festival-board/canva/ops/laurel-stills-canva.json.

Starting positions: the hand-drawn clean-area boxes from tools/laurel-stills.py where a frame has one;
otherwise the calmest of nine candidate spots (lowest luminance spread, avoiding the frame centre).
Light marks on dark ground, dark marks where the spot is light."""
import importlib.util, json, os, datetime
import numpy as np
from PIL import Image
spec = importlib.util.spec_from_file_location("ls", "tools/laurel-stills.py"); ls = importlib.util.module_from_spec(spec); spec.loader.exec_module(ls)
BASE = "https://scroggdawg.github.io/kom-festival-board/"
D = "press/assets/derived/laurels"; SD = "press/assets/derived/canva-laurel-stills"; os.makedirs(SD, exist_ok=True)
for c in ("gold", "black"):
    p = f"{D}/BEST-2026-winner_{c}_stacked.png"
    if not os.path.exists(p): ls.stacked(f"{D}/BEST-2026-winner_{c}.png").save(p, optimize=True)
FILES = {
  "SCAD": (f"{D}/SCAD-2026-official-selection-white.png", f"{D}/SCAD-2026-official-selection-black.png", 0.24),
  "AFI FEST": (f"{D}/AFI-FEST-conservatory-showcase-white-x4.png", f"{D}/AFI-FEST-conservatory-showcase-black-x4.png", 0.27),
  "REEL BLACK MEN": (f"{D}/RBM-2026-official-selection-white.png", f"{D}/RBM-2026-official-selection-black.png", 0.30),
  "B.E.S.T.": (f"{D}/BEST-2026-winner_gold.png", f"{D}/BEST-2026-winner_black.png", 0.30),
  "B.E.S.T. stacked": (f"{D}/BEST-2026-winner_gold_stacked.png", f"{D}/BEST-2026-winner_black_stacked.png", 0.55),
}
def info(p):
    im = Image.open(p).convert("RGBA"); return im.size, im.split()[-1].getbbox()
FW, FH = 1920, 803
STILLS = [n for n in range(1, 42) if n != 26]   # 1.1.26 repeats 1.1.25
def frame(n):
    f = f"{SD}/still-1.1.{n}.jpg"
    if not os.path.exists(f):
        Image.open(ls.STILL(n)).convert("RGB").crop((0, ls.TOP, FW, ls.BOT)).save(f, quality=90, subsampling=0)
    return f
def ink_box(fest, n, lum_img):
    """(ink x, y, w, h) and whether the spot is light."""
    light_p, dark_p, maxh = FILES[fest]; (pw, ph), (bx0, by0, bx1, by1) = info(light_p); iw, ih = bx1 - bx0, by1 - by0
    if n in ls.BOX:
        x0, y0, x1, y1 = ls.BOX[n][0]; s = min((x1 - x0) * .84 / iw, (y1 - y0) * .84 / ih, maxh * FH / ih)
        w, h = iw * s, ih * s; x, y = x0 + (x1 - x0 - w) / 2, y0 + (y1 - y0 - h) / 2
    else:
        s = maxh * FH / ih; w, h = iw * s, ih * s; m = 60; best = None
        for cx in (m, (FW - w) / 2, FW - m - w):
            for cy in (m, (FH - h) / 2, FH - m - h):
                if cx == (FW - w) / 2 and cy == (FH - h) / 2: continue
                reg = lum_img[int(cy):int(cy + h), int(cx):int(cx + w)]
                score = reg.std() + 0.15 * abs(reg.mean() - (20 if reg.mean() < 128 else 235))
                if best is None or score < best[0]: best = (score, cx, cy)
        _, x, y = best
    reg = lum_img[int(y):int(y + h), int(x):int(x + w)]
    return (x, y, w, h), reg.mean() > 140 or n in ls.DARK_ON
pages = []; k = 0
for fest in ("SCAD", "AFI FEST", "REEL BLACK MEN", "B.E.S.T."):
    for n in STILLS:
        f = frame(n); lum = np.asarray(Image.open(f).convert("L"), dtype=float)
        key = fest
        if fest == "B.E.S.T." and n in ls.BOX:
            x0, y0, x1, y1 = ls.BOX[n][0]
            if (x1 - x0) / (y1 - y0) < 2.2: key = "B.E.S.T. stacked"
        (x, y, w, h), is_light = ink_box(key, n, lum)
        p = FILES[key][1 if is_light else 0]; (pw, ph), (bx0, by0, bx1, by1) = info(p)
        sc = w / (bx1 - bx0)                       # element = whole PNG, scaled so its ink lands on the box
        k += 1
        pages.append({"n": k, "name": f"{fest} · 1.1.{n}", "background": "#0b0806", "count": 2, "elements": [
            {"type": "image", "url": BASE + f, "file": f, "px": [FW, FH], "x": 0, "y": 0, "w": FW, "h": FH, "alt": f"Killer of Men still 1.1.{n}"},
            {"type": "image", "url": BASE + p, "file": p, "px": [pw, ph], "x": round(x - bx0 * sc, 1), "y": round(y - by0 * sc, 1),
             "w": round(pw * sc, 1), "h": round(ph * sc, 1), "alt": f"{fest} 2026 laurel"}]})
doc = {"schema": 1, "generated": datetime.datetime.now().isoformat(timespec="seconds"), "source": {"kit_commit": "laurel-stills", "epk_rev": 0},
       "page": {"width_pt": FW, "height_pt": FH}, "fonts": {}, "pages": pages}
json.dump(doc, open("canva/ops/laurel-stills-canva.json", "w"), indent=1)
print(len(pages), "pages;", sum(1 for p in pages if "black" in p["elements"][1]["file"]), "with dark marks")
