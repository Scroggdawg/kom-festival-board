#!/usr/bin/env python3
"""Composition and laurel-placement pass for the CTA nominee posts (Luke, 2026-11-19).

Crop: for each image and each Instagram shape, search every crop window of that shape and score it on
the rule of thirds (eyes on the upper third line, on the third that leaves room in the direction the
subject looks), on keeping the subject box whole, and on resolution (a tighter crop costs pixels).

Laurel: search positions inside the chosen crop, off the subject box, near an edge, and measure the
picture under the laurel's footprint. White laurel only on ground that is dark AND even; black laurel
only on ground that is light AND even (Luke: "white on dark and dark on light"; not half bright, half
dark). Height is fixed per shape and stays under the toolkit's 1/5 ceiling.

Writes press/social/cta-2027/layout.json (read by tools/build-cta-canva.py) and preview sheets.
"""
import json
import numpy as np
from PIL import Image, ImageDraw

SRC = "press/social/cta-2027/source/"
BTS = "press/assets/BTS/"
# key: source, picture rows (letterbox) or None, eyes (x, y), gaze (-1 left, 0 frontal, +1 right),
#      subject box that must stay whole and stay clear of the laurel (x0, y0, x1, y1), all in source px
IMAGES = {
    "A": (SRC + "still-7.webp", None,       (1350, 160),  0, (960, 0, 1580, 610)),
    "B": (SRC + "still-4.webp", (140, 940), (930, 415),  +1, (780, 170, 1120, 880)),
    "C": (SRC + "still-8.webp", (140, 940), (980, 520),  -1, (780, 160, 1400, 940)),
    "D": (SRC + "still-5.webp", (140, 940), (500, 355),  -1, (440, 190, 950, 940)),
    "E": (SRC + "still-6.webp", (140, 940), (1140, 400),  0, (950, 270, 1400, 940)),
    "F": (SRC + "still-3.webp", (140, 940), (840, 330),  +1, (560, 170, 1030, 940)),
    "G": (BTS + "KOM_Stage-1.jpg", None,    (2750, 1300), 0, (1300, 350, 3950, 7008)),
    "H": (BTS + "KOM_Stage-12.jpg", None,   (2400, 1700), -1, (1200, 1100, 4400, 7008)),
    "I": (BTS + "KOM_Stage-9.jpg", None,    (3550, 1500), 0, (500, 1000, 4672, 6000)),
    "J": (BTS + "KOM_Stage-4.jpg", None,    (3700, 1100), +1, (1700, 600, 4600, 4439)),
    "K": (BTS + "KOM_Stage-5.jpg", None,    (2900, 1800), +1, (900, 700, 4600, 4400)),
}
SHAPES = {"portrait": (1080, 1350, 230), "landscape": (1080, 566, 108)}
LAUREL_RATIO = 1980 / 1295
LANDSCAPE_KEYS = "ABCDEF"


def load(key):
    path, rows, eyes, gaze, box = IMAGES[key]
    im = Image.open(path).convert("RGB")
    top = 0
    if rows:
        top = rows[0]
        im = im.crop((0, rows[0], im.width, rows[1]))
    sh = lambda p: (p[0], p[1] - top)
    eyes = sh(eyes)
    box = (box[0], max(0, box[1] - top), box[2], min(im.height, box[3] - top))
    return im, top, eyes, gaze, box


def best_crop(im, eyes, gaze, box, aspect, film):
    W, H = im.size
    hmax = min(H, W / aspect)
    best = None
    for z in np.linspace(1.0, 0.7, 16):                     # zoom: crop height as a share of the largest
        ch = hmax * z
        cw = ch * aspect
        for x0 in np.linspace(0, W - cw, 60):
            for y0 in np.linspace(0, H - ch, 30) if H - ch > 1 else [0.0]:
                ex, ey = (eyes[0] - x0) / cw, (eyes[1] - y0) / ch
                if not (0.05 < ex < 0.95 and 0.05 < ey < 0.95):
                    continue
                tx = {+1: [1 / 3], -1: [2 / 3], 0: [1 / 3, 2 / 3, 0.5]}[gaze]
                dx = min(abs(ex - t) for t in tx)
                dy = abs(ey - 1 / 3)
                # share of the subject box cut off
                ix = max(0, min(box[2], x0 + cw) - max(box[0], x0))
                iy = max(0, min(box[3], y0 + ch) - max(box[1], y0))
                cut = 1 - (ix * iy) / ((box[2] - box[0]) * (box[3] - box[1]))
                zoom_cost = (1 - z) * (2.0 if film else 0.6)
                s = dx * 1.6 + dy * 1.0 + cut * 2.5 + zoom_cost
                if best is None or s < best[0]:
                    best = (s, (x0, y0, x0 + cw, y0 + ch), ex, ey, cut, z)
    return best


def best_laurel(im, crop, box, page):
    PW, PH, LH = page
    LW = LH * LAUREL_RATIO
    s = PW / (crop[2] - crop[0])                             # page px per source px
    lum = np.asarray(im.convert("L"), dtype=np.float32) / 255
    m = 0.04 * PW
    cands = []
    for lx in np.arange(m, PW - LW - m + 1, 10):
        for ly in np.arange(m, PH - LH - m + 1, 10):
            sx0, sy0 = crop[0] + lx / s, crop[1] + ly / s
            sx1, sy1 = sx0 + LW / s, sy0 + LH / s
            pad = 0.03 * (box[2] - box[0])
            ox = max(0, min(sx1, box[2] + pad) - max(sx0, box[0] - pad))
            oy = max(0, min(sy1, box[3] + pad) - max(sy0, box[1] - pad))
            over = ox * oy / ((sx1 - sx0) * (sy1 - sy0))        # share of the laurel over the subject
            r = lum[int(sy0):int(sy1), int(sx0):int(sx1)]
            mean, std = float(r.mean()), float(r.std())
            p90, p10 = float(np.percentile(r, 95)), float(np.percentile(r, 5))
            edge = min(lx, PW - LW - lx, ly, PH - LH - ly) / PW     # distance to nearest edge
            for colour in ("white", "black"):
                # contrast: the laurel against the lightest (white) or darkest (black) part of the ground
                if colour == "white":
                    bad = max(0, p90 - 0.32) * 3 + mean
                else:
                    bad = max(0, 0.68 - p10) * 3 + (1 - mean)
                cands.append((bad + std * 2.5 + edge * 0.8 + over * 20, colour, lx, ly, mean, std, p10, p90))
    cands.sort()
    return cands[0], LW, LH


def run(only=None):
    import os
    layout = json.load(open("press/social/cta-2027/layout.json")) if only and os.path.exists("press/social/cta-2027/layout.json") else {}
    sheets = {}
    for shape, page in SHAPES.items():
        keys = LANDSCAPE_KEYS if shape == "landscape" else list(IMAGES)
        tiles = []
        for k in keys:
            if only and k not in only:
                continue
            im, top, eyes, gaze, box = load(k)
            film = IMAGES[k][1] is not None or k == "A"
            sc, crop, ex, ey, cut, z = best_crop(im, eyes, gaze, box, page[0] / page[1], film)
            (score, colour, lx, ly, mean, std, p10, p90), LW, LH = best_laurel(im, crop, box, page)
            layout.setdefault(shape, {})[k] = {
                "crop": [round(v, 1) for v in (crop[0], crop[1] + top, crop[2], crop[3] + top)],
                "laurel": {"colour": colour, "x": round(float(lx), 1), "y": round(float(ly), 1),
                           "w": round(LW, 1), "h": LH},
                "check": {"eyes_at": [round(ex, 3), round(ey, 3)], "subject_cut": round(cut, 3), "zoom": round(float(z), 2),
                          "ground_mean": round(mean, 3), "ground_std": round(std, 3), "ground_p5_p95": [round(p10, 3), round(p90, 3)],
                          "laurel_height_share": round(LH / page[1], 3)}}
            print(f"{shape:9s} {k}  eyes at ({ex:.2f},{ey:.2f}) cut {cut:.2f} zoom {z:.2f}  laurel {colour} at ({lx:.0f},{ly:.0f}) "
                  f"ground mean {mean:.2f} std {std:.2f} p5-p95 {p10:.2f}-{p90:.2f}")
            # preview tile
            t = im.crop(tuple(int(v) for v in crop)).resize(page[:2], Image.LANCZOS)
            lau = Image.open(f"press/laurels/cta-2027/Found_CTA27_Laurel-Nominee_{colour.title()}.png").resize((round(LW), LH), Image.LANCZOS)
            t.paste(lau, (round(float(lx)), round(float(ly))), lau)
            tiles.append((k, t))
        sheets[shape] = tiles
    json.dump(layout, open("press/social/cta-2027/layout.json", "w"), indent=1)
    if only:
        return
    for shape, tiles in sheets.items():
        tw = 300 if shape == "portrait" else 520
        th = round(tw * tiles[0][1].height / tiles[0][1].width)
        cols = 6 if shape == "portrait" else 3
        rows = (len(tiles) + cols - 1) // cols
        S = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 30) + 10), (40, 40, 40))
        d = ImageDraw.Draw(S)
        for i, (k, t) in enumerate(tiles):
            x, y = 10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 30)
            S.paste(t.resize((tw, th)), (x, y))
            d.text((x, y + th + 6), k, fill=(230, 230, 230))
        S.save(f"press/social/cta-2027/compose-{shape}.jpg", quality=88)


if __name__ == "__main__":
    import sys
    run(sys.argv[1] if len(sys.argv) > 1 else None)   # e.g. "A" recomputes A only and merges into layout.json
