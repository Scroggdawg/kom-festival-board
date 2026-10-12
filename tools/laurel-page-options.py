#!/usr/bin/env python3
"""Mock up page-2 laurel arrangements with the title, rule, photo and label locked where they are in Canva (2026-10-11).
Usage: venv/bin/python tools/laurel-page-options.py OUTDIR. Prints each laurel ink box (x, y, w, h px on the 1728x2304 page)."""
import sys
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1]; D = "press/assets/derived/laurels"
W, H = 1728, 2304; G = (11, 8, 6); F = "press/assets/derived/fonts/libre-baskerville/LibreBaskerville-Regular.ttf"
def trim(p): im = Image.open(p).convert("RGBA"); return im.crop(im.split()[-1].getbbox())
S = {k: trim(f"{D}/{f}") for k, f in [("ABFF", "ABFF-2026-official-selection-white.png"), ("MVAAFF", "MVAAFF-2026-official-selection-white.png"),
     ("SCAD", "SCAD-2026-official-selection-white.png"), ("AFI", "AFI-FEST-conservatory-showcase-white-x4.png"), ("RBM", "RBM-2026-official-selection-white.png")]}
WIN = trim(f"{D}/BEST-2026-winner_gold.png")
MIN_H = 187; MAX_WIN = 1306
still = Image.open(f"{D}/still-1.1.13-feather22.jpg").convert("RGB")
still = still.resize((int(still.width * 860 / still.height), 860), Image.LANCZOS); x0 = (still.width - W) // 2; still = still.crop((x0, 0, x0 + W, 860))
def tracked(dr, t, y, size, span, col):
    font = ImageFont.truetype(F, size); adv = span / len(t); x = (W - span) / 2 + adv / 2
    for ch in t: w = dr.textlength(ch, font=font); dr.text((x - w / 2, y), ch, fill=col, font=font); x += adv
def base():
    img = Image.new("RGBA", (W, H), G + (255,)); dr = ImageDraw.Draw(img)
    tracked(dr, "AWARDS & SELECTIONS", 249, 53, 1460, (236, 230, 216)); dr.line([(706, 339), (1021, 339)], fill=(140, 120, 80), width=2)
    img.paste(still, (0, 429)); tracked(dr, "KILLER OF MEN", 1314, 22, 300, (150, 140, 125)); return img
def sized(it):
    if it[0] == "WIN": im = WIN; w = it[2]; return im, int(w), int(im.height * w / im.width)
    im = S[it[0]]; h = it[1]; return im, int(im.width * h / im.height), int(h)
def render(rows, row_gap):
    built = []
    for items, gap in rows:
        r = [sized(it) for it in items]
        for im, w, h in r:
            assert im is WIN or h >= MIN_H; assert im is not WIN or w < MAX_WIN
        built.append((r, gap, sum(w for _, w, _ in r) + gap * (len(r) - 1), max(h for _, _, h in r)))
    total = sum(b[3] for b in built) + row_gap * (len(built) - 1)
    top, bottom = 1338, 2304 - 150
    assert total <= bottom - top - 40, f"group too tall: {total}"
    y = top + (bottom - top - total) // 2 + 10; img = base(); geo = []
    for r, gap, rw, rh in built:
        assert rw <= W - 80, f"row too wide: {rw}"
        x = (W - rw) / 2
        for im, w, h in r:
            yy = int(y + (rh - h) / 2); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lay.paste(im.resize((w, h), Image.LANCZOS), (int(x), yy)); img.alpha_composite(lay)
            geo.append((int(x), yy, w, h)); x += w + gap
        y += rh + row_gap
    return img.convert("RGB"), total, geo
FIVE = lambda h, g: ([("ABFF", h), ("MVAAFF", h), ("SCAD", h), ("AFI", h), ("RBM", h * 1.08)], g)
OPTS = {
 "1  five across, winner below": ([FIVE(187, 28), ([("WIN", None, 980)], 0)], 70),
 "2  five across, larger winner below": ([FIVE(187, 28), ([("WIN", None, 1220)], 0)], 60),
 "3  winner first, five across below": ([([("WIN", None, 1120)], 0), FIVE(187, 28)], 70),
 "4  three over two, winner below": ([([("ABFF", 200), ("MVAAFF", 200), ("SCAD", 200)], 70), ([("AFI", 200), ("RBM", 216)], 80), ([("WIN", None, 800)], 0)], 36),
 "5  winner first, then three over two": ([([("WIN", None, 860)], 0), ([("ABFF", 190), ("MVAAFF", 190), ("SCAD", 190)], 70), ([("AFI", 190), ("RBM", 205)], 80)], 36),
 "6  three across; AFI, winner, Reel Black Men": ([([("ABFF", 220), ("MVAAFF", 220), ("SCAD", 220)], 80), ([("AFI", 200), ("WIN", None, 800), ("RBM", 216)], 60)], 70),
 "7  three, the winner, two": ([([("ABFF", 187), ("MVAAFF", 187), ("SCAD", 187)], 70), ([("WIN", None, 900)], 0), ([("AFI", 187), ("RBM", 202)], 80)], 36),
}
tiles = []
for name, (rows, gap) in OPTS.items():
    img, total, geo = render(rows, gap); k = name.split()[0]; img.save(f"{OUT}/option-{k}.png", optimize=True); tiles.append((name, img)); print(name, "| group", total, "| ink boxes", geo)
tw, th, pad, lab, cols = 560, 747, 24, 44, 4
sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad, 2 * (th + lab) + 3 * pad), (30, 28, 26)); dr = ImageDraw.Draw(sheet); font = ImageFont.truetype(F, 19)
for i, (name, img) in enumerate(tiles):
    r, c = divmod(i, cols); x = pad + c * (tw + pad); y = pad + r * (th + lab + pad)
    dr.text((x, y + 8), name, fill=(230, 224, 210), font=font); sheet.paste(img.resize((tw, th), Image.LANCZOS), (x, y + lab))
dr.text((pad + 3 * (tw + pad), pad + (th + lab + pad) + 60), "Title, rule, photo and label stay where\nthey are in Canva now. Only the laurels move.\n\nSelections: never smaller than option D's\nsmall ones. Winner: always under F's.\nAll five selections matched by height.", fill=(200, 194, 180), font=font, spacing=8)
sheet.save(f"{OUT}/contact-sheet-options.jpg", quality=88)
