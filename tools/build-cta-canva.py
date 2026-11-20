#!/usr/bin/env python3
"""Ops file for a Canva design of the 46th College Television Awards nominee posts: one 1080 x 1350
Instagram page per image, the image as one element and the CTA laurel as its own movable element
(Luke, 2026-11-19: "make them in Canva so that I can adjust where the laurel goes").

The image element is larger than the page, so the frame can be slid as well. Starting positions follow
tools/cta-laurel-posts.py. The laurel starts at 230 px tall; the toolkit's ceiling is 1/5 of the image,
270 px on this page. Built by the kom-epk-builder app with the ops URL
https://scroggdawg.github.io/kom-festival-board/canva/ops/cta-2027-canva.json.

Writes press/assets/derived/canva-cta-2027/*.jpg, press/assets/derived/laurels/CTA-2027-nominee-white.png
and canva/ops/cta-2027-canva.json."""
import json, os, datetime
from PIL import Image

BASE = "https://scroggdawg.github.io/kom-festival-board/"
OUT = "press/assets/derived/canva-cta-2027"
LAUREL_SRC = "press/laurels/cta-2027/Found_CTA27_Laurel-Nominee_White.png"
LAUREL = "press/assets/derived/laurels/CTA-2027-nominee-white.png"
PW, PH = 1080, 1350
LH = 230                                  # laurel height; max 270 (1/5 of 1350)
M = 56                                    # margin
os.makedirs(OUT, exist_ok=True)
if not os.path.exists(LAUREL):
    Image.open(LAUREL_SRC).save(LAUREL, optimize=True)
lw0, lh0 = Image.open(LAUREL).size
LW = round(LH * lw0 / lh0)

# name, source, picture rows to keep (top, bottom) or None, visible box in source px (x0, y0, x1, y1), laurel corner
FRAMES = [
    ("A elder looking up",   "press/social/cta-2027/source/still-7.webp", None,       (910, 0, 1551, 801),     "bl"),
    ("B Mace firelight",     "press/social/cta-2027/source/still-4.webp", (140, 940), (500, 140, 1140, 940),   "tr"),
    ("C elder firelight",    "press/social/cta-2027/source/still-8.webp", (140, 940), (560, 140, 1200, 940),   "bl"),
    ("D Mace at the cabin",  "press/social/cta-2027/source/still-5.webp", (140, 940), (200, 140, 840, 940),    "tl"),
    ("E the burial",         "press/social/cta-2027/source/still-6.webp", (140, 940), (800, 140, 1440, 940),   "bl"),
    ("F elder under the oak","press/social/cta-2027/source/still-3.webp", (140, 940), (380, 140, 1020, 940),   "tl"),
    ("G two men in smoke",   "press/assets/BTS/KOM_Stage-1.jpg",          None,       (0, 300, 4672, 6140),    "tl"),
    ("H black-and-white motion", "press/assets/BTS/KOM_Stage-12.jpg",     None,       (0, 400, 4672, 6240),    "tl"),
    ("I kente in motion",    "press/assets/BTS/KOM_Stage-9.jpg",          None,       (0, 0, 4672, 5840),      "tl"),
    ("J kente portrait",     "press/assets/BTS/KOM_Stage-4.jpg",          None,       (1800, 0, 5351, 4439),   "tr"),
    ("K fight in motion",    "press/assets/BTS/KOM_Stage-5.jpg",          None,       (1635, 0, 5373, 4672),   "tc"),
]


def laurel_xy(corner):
    x = {"l": M, "r": PW - LW - M, "c": (PW - LW) / 2}[corner[1]]
    y = M if corner[0] == "t" else PH - LH - M
    return x, y


pages = []
for k, (name, src, rows, box, corner) in enumerate(FRAMES, start=1):
    im = Image.open(src).convert("RGB")
    top = 0
    if rows:
        top = rows[0]
        im = im.crop((0, rows[0], im.width, rows[1]))
    s = PW / (box[2] - box[0])               # page px per source px
    k2 = min(1.0, 2 * s)                      # host at up to 2x the page's need
    hosted = im.resize((round(im.width * k2), round(im.height * k2)), Image.LANCZOS) if k2 < 1 else im
    slug = name.split()[0]
    f = f"{OUT}/{slug}.jpg"
    hosted.save(f, quality=90, subsampling=0)
    lx, ly = laurel_xy(corner)
    pages.append({"n": k, "name": f"CTA · {name}", "background": "#000000", "count": 2, "elements": [
        {"type": "image", "url": BASE + f, "file": f, "px": list(hosted.size),
         "x": round(-box[0] * s, 1), "y": round(-(box[1] - top) * s, 1),
         "w": round(im.width * s, 1), "h": round(im.height * s, 1), "alt": f"Killer of Men, {name}"},
        {"type": "image", "url": BASE + LAUREL, "file": LAUREL, "px": [lw0, lh0],
         "x": round(lx, 1), "y": round(ly, 1), "w": LW, "h": LH, "alt": "College Television Awards 2027 nominee laurel"},
    ]})
    print(f"{name:26s} image {hosted.size[0]}x{hosted.size[1]} placed {pages[-1]['elements'][0]['w']:.0f}x{pages[-1]['elements'][0]['h']:.0f}  laurel {LW}x{LH} ({LH/PH:.3f} of page) at {lx:.0f},{ly:.0f}")

# the laurel alone on black
pages.append({"n": len(pages) + 1, "name": "CTA · Z laurel alone", "background": "#000000", "count": 1, "elements": [
    {"type": "image", "url": BASE + LAUREL, "file": LAUREL, "px": [lw0, lh0],
     "x": (PW - 760) / 2, "y": round((PH - 760 * lh0 / lw0) / 2, 1), "w": 760, "h": round(760 * lh0 / lw0, 1),
     "alt": "College Television Awards 2027 nominee laurel"}]})

doc = {"schema": 1, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
       "source": {"kit_commit": "cta-2027", "epk_rev": 0},
       "page": {"width_pt": PW, "height_pt": PH}, "fonts": {}, "pages": pages}
json.dump(doc, open("canva/ops/cta-2027-canva.json", "w"), indent=1)
print(f"{len(pages)} pages -> canva/ops/cta-2027-canva.json")
