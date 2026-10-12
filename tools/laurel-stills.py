#!/usr/bin/env python3
"""Composite a festival laurel onto 2.39:1 frames from press/assets/STILLS.

Usage: venv/bin/python tools/laurel-stills.py [still numbers...]   (default: 5 13 14 17 35 41)
Writes press/assets/derived/laurel-stills/<FEST>/KOM-<FEST>-still-1.1.N.jpg (1920x803) and a contact sheet.
The laurel sits top-centre (6% down, ~22% of the frame height, like a festival's own social still);
the light or dark version is chosen by the mean luminance under it (dark marks only above 140/255)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageStat
D = "press/assets/derived/laurels"; OUT = "press/assets/derived/laurel-stills"
STILL = lambda n: f"press/assets/STILLS/Still 2026-09-08 210640_1.1.{n}.png"
TOP, BOT = 138, 941   # the picture rows inside the 1920x1080 letterboxed export
def rgba(p): return Image.open(p).convert("RGBA")
FESTS = {
  "SCAD":           {"light": f"{D}/SCAD-2026-official-selection-white.png", "dark": f"{D}/SCAD-2026-official-selection-black.png", "h": 0.22},
  "AFI-FEST":       {"light": f"{D}/AFI-FEST-conservatory-showcase-white-x4.png", "dark": f"{D}/AFI-FEST-conservatory-showcase-black-x4.png", "h": 0.22},
  "REEL-BLACK-MEN": {"light": f"{D}/RBM-2026-official-selection-white.png", "dark": f"{D}/RBM-2026-official-selection-black.png", "h": 0.26},
  "BEST":           {"light": f"{D}/BEST-2026-winner_gold.png", "dark": f"{D}/BEST-2026-winner_black.png", "h": 0.25},
}
def main(stills):
    sheets = {}
    for fest, cfg in FESTS.items():
        os.makedirs(f"{OUT}/{fest}", exist_ok=True); tiles = []
        for n in stills:
            fr = Image.open(STILL(n)).convert("RGB"); fr = fr.crop((0, TOP, fr.width, BOT)); W, H = fr.size
            lh = int(H * cfg["h"]); probe = rgba(cfg["light"]); lw = int(probe.width * lh / probe.height)
            x, y = (W - lw) // 2, int(H * 0.06); gx, gy = int(lw * .08), int(lh * .08)
            lum = ImageStat.Stat(fr.crop((max(0, x-gx), max(0, y-gy), min(W, x+lw+gx), min(H, y+lh+gy))).convert("L")).mean[0]
            lau = rgba(cfg["dark" if lum > 140 else "light"]); lw = int(lau.width * lh / lau.height); x = (W - lw) // 2
            layer = Image.new("RGBA", fr.size, (0, 0, 0, 0)); layer.paste(lau.resize((lw, lh), Image.LANCZOS), (x, y))
            out = Image.alpha_composite(fr.convert("RGBA"), layer).convert("RGB")
            out.save(f"{OUT}/{fest}/KOM-{fest}-still-1.1.{n}.jpg", quality=92, subsampling=0); tiles.append(out)
            print(fest, n, f"lum {lum:.0f}", "dark" if lum > 140 else "light", f"{lw}x{lh}")
        sheets[fest] = tiles
    tw = 480; th = int(tw * 803 / 1920); pad = 14; lab = 34; n = len(stills)
    sheet = Image.new("RGB", (n*tw + (n+1)*pad, 4*(th+lab) + 5*pad), (24, 22, 20)); dr = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("press/assets/derived/fonts/libre-baskerville/LibreBaskerville-Regular.ttf", 20)
    for r, (fest, tiles) in enumerate(sheets.items()):
        y0 = pad + r*(th+lab+pad); dr.text((pad, y0 + 4), f"{fest}   (stills 1.1.{', 1.1.'.join(map(str, stills))})", fill=(230, 224, 210), font=font)
        for c, t in enumerate(tiles): sheet.paste(t.resize((tw, th), Image.LANCZOS), (pad + c*(tw+pad), y0 + lab))
    sheet.save(f"{OUT}/contact-sheet-laurel-stills.jpg", quality=88)
if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or [5, 13, 14, 17, 35, 41])
