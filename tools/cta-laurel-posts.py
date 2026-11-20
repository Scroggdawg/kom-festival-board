"""Instagram candidates for the 46th College Television Awards nomination.

Laurel rules (press/social/cta-2027-rules.md): supplied file only, scaled
proportionally, height <= 1/5 of the image, inside the picture, touching no
text or logo. Every output is checked and the numbers printed.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "press/social/cta-2027/source"
OUT = ROOT / "press/social/cta-2027/candidates"
LAUREL = {c: ROOT / f"press/laurels/cta-2027/Found_CTA27_Laurel-Nominee_{c.title()}.png"
          for c in ("white", "black")}
PORTRAIT, LANDSCAPE = (1080, 1350), (1080, 566)
MARGIN = 56

# name: still, crop box in source px (x0, y0, x1, y1), canvas, laurel colour,
# corner, laurel height as a fraction of canvas height
CANDIDATES = {
    "A_elder-looking-up":   ("still-7", (386, 0, 1916, 801),    LANDSCAPE, "white", "tl", 0.19),
    "B_mace-firelight":     ("still-4", (500, 140, 1140, 940),   PORTRAIT,  "white", "tr", 0.17),
    "C_elder-firelight":    ("still-8", (560, 140, 1200, 940),   PORTRAIT,  "white", "bl", 0.17),
    "D_mace-cabin":         ("still-5", (200, 140, 840, 940),    PORTRAIT,  "white", "tl", 0.17),
    "E_funeral-wide":       ("still-6", (193, 140, 1720, 940),   LANDSCAPE, "white", "tl", 0.19),
    "F_elder-under-oak":    ("still-3", (386, 140, 1913, 940),   LANDSCAPE, "white", "tl", 0.19),
    # Jedidiah Woods' stage portraits, full-resolution files from press/assets/BTS
    "G_two-men-smoke":      ("BTS/KOM_Stage-1",  (0, 300, 4672, 6140),    PORTRAIT, "white", "tl", 0.17),
    "H_bw-motion":          ("BTS/KOM_Stage-12", (0, 400, 4672, 6240),    PORTRAIT, "white", "tl", 0.17),
    "I_kente-motion":       ("BTS/KOM_Stage-9",  (0, 0, 4672, 5840),      PORTRAIT, "white", "tl", 0.17),
    "J_kente-portrait":     ("BTS/KOM_Stage-4",  (1800, 0, 5351, 4439),   PORTRAIT, "white", "tr", 0.17),
    "K_fight-motion":       ("BTS/KOM_Stage-5",  (1635, 0, 5373, 4672),   PORTRAIT, "white", "tc", 0.17),
}


def place(name, still, box, canvas, colour, corner, frac):
    path = (ROOT / "press/assets" / f"{still}.jpg") if still.startswith("BTS/") else SRC / f"{still}.webp"
    img = Image.open(path).convert("RGB").crop(box)
    img = img.resize(canvas, Image.LANCZOS)
    lau = Image.open(LAUREL[colour])
    h = round(canvas[1] * frac)
    w = round(h * lau.width / lau.height)
    lau = lau.resize((w, h), Image.LANCZOS)
    m = round(MARGIN * canvas[0] / 1080)
    x = {"l": m, "r": canvas[0] - w - m, "c": (canvas[0] - w) // 2}[corner[1]]
    y = m if corner[0] == "t" else canvas[1] - h - m
    img.paste(lau, (x, y), lau)
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / f"{name}.jpg", quality=95)
    ratio_in = Image.open(LAUREL[colour]).width / Image.open(LAUREL[colour]).height
    print(f"{name}: {canvas[0]}x{canvas[1]}  laurel {w}x{h} at ({x},{y})  "
          f"height {h / canvas[1]:.3f} of image (max 0.200)  "
          f"ratio {w / h:.3f} vs supplied {ratio_in:.3f}  "
          f"{'PASS' if h / canvas[1] <= 0.2 and abs(w / h - ratio_in) < 0.005 else 'FAIL'}")


def laurel_alone():
    """Carousel card: the white laurel on plain black, as the toolkit shows."""
    img = Image.new("RGB", PORTRAIT, (0, 0, 0))
    lau = Image.open(LAUREL["white"])
    w = 760
    lau = lau.resize((w, round(w * lau.height / lau.width)), Image.LANCZOS)
    img.paste(lau, ((PORTRAIT[0] - lau.width) // 2, (PORTRAIT[1] - lau.height) // 2), lau)
    img.save(OUT / "Z_laurel-alone-black.jpg", quality=95)
    print(f"Z_laurel-alone-black: 1080x1350, laurel {lau.width}x{lau.height}")


if __name__ == "__main__":
    for name, spec in CANDIDATES.items():
        place(name, *spec)
    laurel_alone()
