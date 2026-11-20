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


# Landscape design for the film frames: Instagram's widest feed shape, 1.91:1, keeps the frames at
# full sharpness (a 1528 px wide crop shown at 1080). The laurel ceiling there is 113 px.
LANDSCAPE = [
    ("A elder looking up",   "press/social/cta-2027/source/still-7.webp", None,       (386, 0, 1916, 801),     "tl"),
    ("B Mace firelight",     "press/social/cta-2027/source/still-4.webp", (140, 940), (0, 140, 1528, 940),     "tr"),
    ("C elder firelight",    "press/social/cta-2027/source/still-8.webp", (140, 940), (200, 140, 1728, 940),   "tl"),
    ("D Mace at the cabin",  "press/social/cta-2027/source/still-5.webp", (140, 940), (0, 140, 1528, 940),     "tl"),
    ("E the burial",         "press/social/cta-2027/source/still-6.webp", (140, 940), (193, 140, 1721, 940),   "tl"),
    ("F elder under the oak","press/social/cta-2027/source/still-3.webp", (140, 940), (386, 140, 1914, 940),   "tl"),
]


def build(frames, PW, PH, LH, out, card):
    LW = round(LH * lw0 / lh0)
    M = round(56 * PH / 1350) if PH < PW else 56

    def laurel_xy(corner):
        x = {"l": M, "r": PW - LW - M, "c": (PW - LW) / 2}[corner[1]]
        y = M if corner[0] == "t" else PH - LH - M
        return x, y

    pages = []
    for k, (name, src, rows, box, corner) in enumerate(frames, start=1):
        im = Image.open(src).convert("RGB")
        top = 0
        if rows:
            top = rows[0]
            im = im.crop((0, rows[0], im.width, rows[1]))
        s = PW / (box[2] - box[0])               # page px per source px
        k2 = min(1.0, 2 * s)                      # host at up to 2x the page's need
        hosted = im.resize((round(im.width * k2), round(im.height * k2)), Image.LANCZOS) if k2 < 1 else im
        f = f"{OUT}/{name.split()[0]}.jpg"
        if not os.path.exists(f) or hosted.size != Image.open(f).size:
            hosted.save(f, quality=90, subsampling=0)
        lx, ly = laurel_xy(corner)
        pages.append({"n": k, "name": f"CTA · {name}", "background": "#000000", "count": 2, "elements": [
            {"type": "image", "url": BASE + f, "file": f, "px": list(hosted.size),
             "x": round(-box[0] * s, 1), "y": round(-(box[1] - top) * s, 1),
             "w": round(im.width * s, 1), "h": round(im.height * s, 1), "alt": f"Killer of Men, {name}"},
            {"type": "image", "url": BASE + LAUREL, "file": LAUREL, "px": [lw0, lh0],
             "x": round(lx, 1), "y": round(ly, 1), "w": LW, "h": LH, "alt": "College Television Awards 2027 nominee laurel"},
        ]})
        print(f"{name:26s} {PW}x{PH}  image {hosted.size[0]}x{hosted.size[1]}  laurel {LW}x{LH} ({LH/PH:.3f} of page, max 0.200) at {lx:.0f},{ly:.0f}")
    if card:   # the laurel alone on black
        pages.append({"n": len(pages) + 1, "name": "CTA · Z laurel alone", "background": "#000000", "count": 1, "elements": [
            {"type": "image", "url": BASE + LAUREL, "file": LAUREL, "px": [lw0, lh0],
             "x": (PW - 760) / 2, "y": round((PH - 760 * lh0 / lw0) / 2, 1), "w": 760, "h": round(760 * lh0 / lw0, 1),
             "alt": "College Television Awards 2027 nominee laurel"}]})
    doc = {"schema": 1, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "source": {"kit_commit": "cta-2027", "epk_rev": 0},
           "page": {"width_pt": PW, "height_pt": PH}, "fonts": {}, "pages": pages}
    json.dump(doc, open(out, "w"), indent=1)
    print(f"{len(pages)} pages -> {out}")


# Crops and laurel spots come from the composition pass (tools/cta-compose.py -> layout.json).
LAYOUT = json.load(open("press/social/cta-2027/layout.json"))
for c in ("white", "black"):
    dst = f"press/assets/derived/laurels/CTA-2027-nominee-{c}.png"
    if not os.path.exists(dst):
        Image.open(f"press/laurels/cta-2027/Found_CTA27_Laurel-Nominee_{c.title()}.png").save(dst, optimize=True)


def build_from_layout(shape, PW, PH, out, card):
    frames = {f[0].split()[0]: f for f in FRAMES}
    pages = []
    for k, spec in LAYOUT[shape].items():
        name, src, rows, _, _ = frames[k]
        im = Image.open(src).convert("RGB")
        top = 0
        if rows:
            top = rows[0]
            im = im.crop((0, rows[0], im.width, rows[1]))
        x0, y0, x1, y1 = spec["crop"]
        s = PW / (x1 - x0)
        k2 = min(1.0, 2 * s)
        hosted = im.resize((round(im.width * k2), round(im.height * k2)), Image.LANCZOS) if k2 < 1 else im
        f = f"{OUT}/{k}.jpg"
        if not os.path.exists(f) or Image.open(f).size != hosted.size:
            hosted.save(f, quality=90, subsampling=0)
        L = spec["laurel"]
        lp = f"press/assets/derived/laurels/CTA-2027-nominee-{L['colour']}.png"
        pages.append({"n": len(pages) + 1, "name": f"CTA · {name}", "background": "#000000", "count": 2, "elements": [
            {"type": "image", "url": BASE + f, "file": f, "px": list(hosted.size),
             "x": round(-x0 * s, 1), "y": round(-(y0 - top) * s, 1),
             "w": round(im.width * s, 1), "h": round(im.height * s, 1), "alt": f"Killer of Men, {name}"},
            {"type": "image", "url": BASE + lp, "file": lp, "px": [lw0, lh0],
             "x": L["x"], "y": L["y"], "w": L["w"], "h": L["h"], "alt": "College Television Awards 2027 nominee laurel"},
        ]})
        print(f"{shape:9s} {k}  laurel {L['colour']} {L['w']:.0f}x{L['h']} ({L['h']/PH:.3f} of page, max 0.200)")
    if card:
        pages.append({"n": len(pages) + 1, "name": "CTA · Z laurel alone", "background": "#000000", "count": 1, "elements": [
            {"type": "image", "url": BASE + LAUREL, "file": LAUREL, "px": [lw0, lh0],
             "x": (PW - 760) / 2, "y": round((PH - 760 * lh0 / lw0) / 2, 1), "w": 760, "h": round(760 * lh0 / lw0, 1),
             "alt": "College Television Awards 2027 nominee laurel"}]})
    doc = {"schema": 1, "generated": datetime.datetime.now().isoformat(timespec="seconds") + f"-{shape}",
           "source": {"kit_commit": "cta-2027-composed", "epk_rev": 1},
           "page": {"width_pt": PW, "height_pt": PH}, "fonts": {}, "pages": pages}
    json.dump(doc, open(out, "w"), indent=1)
    print(f"{len(pages)} pages -> {out}")


build_from_layout("portrait", 1080, 1350, "canva/ops/cta-2027-canva.json", True)
build_from_layout("landscape", 1080, 566, "canva/ops/cta-2027-landscape-canva.json", False)
