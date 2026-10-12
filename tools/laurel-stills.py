#!/usr/bin/env python3
"""Festival laurels on 2.39:1 frames from press/assets/STILLS, placed by hand into each frame's clean area.

Each frame below has a box (x0, y0, x1, y1, px on the 1920x803 picture) drawn round its negative space,
chosen by eye from a gridded sheet of the frame. The laurel, trimmed to its ink, is fitted inside the box
(8% padding, capped at a share of the frame height) and centred in it. White or gold on dark frames, black
where the box is light. White marks get a faint blurred shadow so leaves hold on textured ground.

B.E.S.T. comes in two shapes: the wide winner laurel (wreath + WINNER + awards) for wide boxes, and a
stacked build (wreath over the awards) for tall boxes.

Usage: venv/bin/python tools/laurel-stills.py
Writes press/assets/derived/laurel-stills/<FEST>/KOM-<FEST>-still-1.1.N.jpg (1920x803) and a contact sheet."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = "press/assets/derived/laurels"; OUT = "press/assets/derived/laurel-stills"
STILL = lambda n: f"press/assets/STILLS/Still 2026-09-08 210640_1.1.{n}.png"
TOP, BOT = 138, 941

def trim(p):
    im = Image.open(p).convert("RGBA"); return im.crop(im.split()[-1].getbbox())

def stacked(p):
    """Wreath (ink columns up to 1819) over the award text (from 2014); every text line centred under it."""
    import numpy as np
    im = Image.open(p).convert("RGBA")
    wreath = im.crop((0, 0, 1900, im.height)); wreath = wreath.crop(wreath.split()[-1].getbbox())
    text = im.crop((1950, 0, im.width, im.height)); text = text.crop(text.split()[-1].getbbox())
    rows = np.array(text.split()[-1]).max(axis=1) > 0; lines = []; start = None
    for y, on in enumerate(list(rows) + [False]):
        if on and start is None: start = y
        if not on and start is not None: lines.append((start, y)); start = None
    parts = []
    for a, b in lines:
        ln = text.crop((0, a, text.width, b)); ln = ln.crop(ln.split()[-1].getbbox()); parts.append((a, ln))
    W = max(wreath.width, max(ln.width for _, ln in parts)); gap = int(wreath.height * 0.10)
    H = wreath.height + gap + (lines[-1][1] - lines[0][0])
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0)); out.paste(wreath, ((W - wreath.width) // 2, 0))
    for a, ln in parts: out.paste(ln, ((W - ln.width) // 2, wreath.height + gap + a - lines[0][0]))
    return out

L = {
  "SCAD":  {"light": trim(f"{D}/SCAD-2026-official-selection-white.png"), "dark": trim(f"{D}/SCAD-2026-official-selection-black.png")},
  "AFI-FEST": {"light": trim(f"{D}/AFI-FEST-conservatory-showcase-white-x4.png"), "dark": trim(f"{D}/AFI-FEST-conservatory-showcase-black-x4.png")},
  "REEL-BLACK-MEN": {"light": trim(f"{D}/RBM-2026-official-selection-white.png"), "dark": trim(f"{D}/RBM-2026-official-selection-black.png")},
  "BEST-wide": {"light": trim(f"{D}/BEST-2026-winner_gold.png"), "dark": trim(f"{D}/BEST-2026-winner_black.png")},
  "BEST-stack": {"light": stacked(f"{D}/BEST-2026-winner_gold.png"), "dark": stacked(f"{D}/BEST-2026-winner_black.png")},
}
# Clean areas, by eye (x0, y0, x1, y1) on the 1920x803 picture, and what is there.
BOX = {
  2:  ((50, 150, 600, 660), "left third: the dark beside the bound hands"),
  17: ((1470, 40, 1890, 330), "top right: soft tree bokeh past the cabin roof"),
  18: ((70, 110, 860, 700), "left half: the dark cabin wall behind the Elder"),
  22: ((960, 40, 1850, 275), "top right: dark above the hand and the shrine"),
  23: ((1240, 40, 1890, 430), "top right: the dark wall past Mace's face"),
  25: ((1080, 60, 1870, 410), "upper right: night, away from the lantern"),
  31: ((40, 70, 470, 760), "left quarter: black beside the face"),
  32: ((40, 70, 450, 760), "left quarter: black beside the face"),
  33: ((1330, 60, 1880, 520), "right: the dark blue past the head wrap"),
  36: ((1320, 40, 1880, 330), "top right: the dark barn wall"),
  37: ((1330, 40, 1880, 430), "top right: dark beyond the head wrap"),
  41: ((40, 40, 640, 330), "top left: pale leaf bokeh above the Elder (black laurel)"),
}
DARK_ON = {41}           # boxes too light for white marks
PLAN = {
  "SCAD":           [(18, "SCAD"), (22, "SCAD"), (31, "SCAD"), (17, "SCAD"), (41, "SCAD"), (33, "SCAD")],
  "AFI-FEST":       [(25, "AFI-FEST"), (37, "AFI-FEST"), (2, "AFI-FEST"), (23, "AFI-FEST"), (32, "AFI-FEST"), (36, "AFI-FEST")],
  "REEL-BLACK-MEN": [(23, "REEL-BLACK-MEN"), (18, "REEL-BLACK-MEN"), (22, "REEL-BLACK-MEN"), (41, "REEL-BLACK-MEN"), (2, "REEL-BLACK-MEN"), (37, "REEL-BLACK-MEN")],
  "BEST":           [(25, "BEST-wide"), (22, "BEST-wide"), (31, "BEST-stack"), (18, "BEST-stack"), (37, "BEST-stack"), (33, "BEST-stack")],
}
MAXH = {"SCAD": 0.27, "AFI-FEST": 0.30, "REEL-BLACK-MEN": 0.33, "BEST-wide": 0.36, "BEST-stack": 0.62}

def place(fr, lau, box, maxh, light):
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0; pw, ph = bw * 0.84, bh * 0.84
    s = min(pw / lau.width, ph / lau.height, maxh * fr.height / lau.height)
    w, h = int(lau.width * s), int(lau.height * s); l = lau.resize((w, h), Image.LANCZOS)
    x, y = x0 + (bw - w) // 2, y0 + (bh - h) // 2
    base = fr.convert("RGBA")
    if light:
        sh = Image.new("RGBA", fr.size, (0, 0, 0, 0)); a = l.split()[-1].point(lambda v: int(v * 0.45))
        sh.paste(Image.new("RGBA", (w, h), (0, 0, 0, 255)), (x, y + max(2, h // 120)), a)
        base = Image.alpha_composite(base, sh.filter(ImageFilter.GaussianBlur(max(3, h // 60))))
    layer = Image.new("RGBA", fr.size, (0, 0, 0, 0)); layer.paste(l, (x, y))
    return Image.alpha_composite(base, layer).convert("RGB"), (x, y, w, h)

def main():
    sheets = {}
    for fest, items in PLAN.items():
        os.makedirs(f"{OUT}/{fest}", exist_ok=True)
        for old in os.listdir(f"{OUT}/{fest}"): os.remove(f"{OUT}/{fest}/{old}")
        tiles = []
        for n, key in items:
            fr = Image.open(STILL(n)).convert("RGB").crop((0, TOP, 1920, BOT))
            light = n not in DARK_ON
            out, geo = place(fr, L[key]["light" if light else "dark"], BOX[n][0], MAXH[key], light)
            out.save(f"{OUT}/{fest}/KOM-{fest}-still-1.1.{n}.jpg", quality=92, subsampling=0)
            tiles.append((n, out)); print(fest, f"1.1.{n}", key, "light" if light else "dark", geo, "-", BOX[n][1])
        sheets[fest] = tiles
    tw = 480; th = int(tw * 803 / 1920); pad = 14; lab = 34
    sheet = Image.new("RGB", (6 * tw + 7 * pad, 4 * (th + lab) + 5 * pad), (24, 22, 20)); dr = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("press/assets/derived/fonts/libre-baskerville/LibreBaskerville-Regular.ttf", 19)
    for r, (fest, tiles) in enumerate(sheets.items()):
        y0 = pad + r * (th + lab + pad); dr.text((pad, y0 + 6), fest, fill=(230, 224, 210), font=font)
        for c, (n, t) in enumerate(tiles):
            x = pad + c * (tw + pad); sheet.paste(t.resize((tw, th), Image.LANCZOS), (x, y0 + lab))
            dr.text((x + tw - 60, y0 + 6), f"1.1.{n}", fill=(150, 140, 125), font=font)
    sheet.save(f"{OUT}/contact-sheet-laurel-stills.jpg", quality=88)

if __name__ == "__main__":
    main()
