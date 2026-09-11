#!/usr/bin/env python3
"""Check and preview the Canva contract (canva/ops/epk-canva.json) before it is built.

    <venv>/bin/python tools/check-canva-contract.py [--render DIR]

Measures every text element in the face the contract was measured in (Libre Baskerville
from press/assets/derived/fonts/libre-baskerville) and reports, per page:
  * two lines on one baseline whose extents overlap (a handle on its lockup)
  * a paragraph whose last line ends below the foot margin
  * the gap after each paragraph before the next text element
With --render it also draws each page to DIR/pNN.png with PIL, one px per pt, in the
same face: a preview of what Canva should show, not what it does show (the app's read
back is the check for that).
"""
import json, os, sys

from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS = os.path.join(ROOT, "canva", "ops", "epk-canva.json")
LIBRE = os.path.join(ROOT, "press", "assets", "derived", "fonts", "libre-baskerville")
FILES = {"Bask": "LibreBaskerville-Regular.ttf", "Bask-SB": "LibreBaskerville-Bold.ttf", "Bask-B": "LibreBaskerville-Bold.ttf"}
ASCENT_LINE, ASCENT_PARA = 0.95, 0.78          # the emitter's baseline offsets
M = 74.0

for k, f in FILES.items():
    pdfmetrics.registerFont(TTFont("chk-" + k, os.path.join(LIBRE, f)))


def width(e, text=None):
    t = e["text"] if text is None else text
    return pdfmetrics.stringWidth(t, "chk-" + e["font"], e["size_pt"]) + e["tracking_pt"] * max(len(t) - 1, 0)


def extent(e):
    """(left, right, baseline) of a line element in page pt, y down."""
    w = width(e)
    if e["align"] == "end":
        left = e["x"] + e["w"] - w
    elif e["align"] == "center":
        left = e["x"] + (e["w"] - w) / 2
    else:
        left = e["x"]
    return left, left + w, e["y"] + e["size_pt"] * ASCENT_LINE


def check(doc):
    H = doc["page"]["height_pt"]
    problems = 0
    for p in doc["pages"]:
        lines = [e for e in p["elements"] if e["type"] == "text" and e["kind"] == "line"]
        paras = [e for e in p["elements"] if e["type"] == "text" and e["kind"] == "paragraph"]
        texts = [e for e in p["elements"] if e["type"] == "text"]
        for i, a in enumerate(lines):
            la, ra, ba = extent(a)
            for b in lines[i + 1:]:
                lb, rb, bb = extent(b)
                if abs(ba - bb) < 0.5 * min(a["size_pt"], b["size_pt"]) and min(ra, rb) - max(la, lb) > 1.0:
                    problems += 1
                    print(f"  p{p['n']:02d} OVERLAP on baseline {ba:.0f}: '{a['text'][:36]}' [{la:.0f}..{ra:.0f}] "
                          f"and '{b['text'][:36]}' [{lb:.0f}..{rb:.0f}] by {min(ra, rb) - max(la, lb):.1f} pt")
        for e in paras:
            bottom = e["y"] + e["lines"] * e["leading_pt"]
            below = [t for t in texts if t is not e and t["y"] >= bottom - 1 and abs(t["x"] - e["x"]) < e["w"]]
            nxt = min(below, key=lambda t: t["y"]) if below else None
            gap = f"gap to next text {nxt['y'] - bottom:6.1f} pt ('{nxt['text'][:24]}')" if nxt else "last text in its column"
            flag = ""
            if bottom > H - M:
                flag = "  <-- BELOW THE FOOT MARGIN" if bottom <= H else "  <-- OFF THE PAGE"
                problems += 1
            print(f"  p{p['n']:02d} paragraph {e['lines']:2} lines x {e['leading_pt']:5.2f} at {e['size_pt']:5.2f} pt, "
                  f"top {e['y']:7.1f} bottom {bottom:7.1f}; {gap}{flag}")
    return problems


def render(doc, out_dir):
    W, H = int(doc["page"]["width_pt"]), int(doc["page"]["height_pt"])
    os.makedirs(out_dir, exist_ok=True)
    fonts = {}

    def font(e):
        key = (e["font"], round(e["size_pt"], 2))
        if key not in fonts:
            fonts[key] = ImageFont.truetype(os.path.join(LIBRE, FILES[e["font"]]), size=max(1, round(e["size_pt"])))
        return fonts[key]

    def draw_line(d, e, text, left, baseline):
        f = font(e)
        if e["tracking_pt"] > 0.01:
            x = left
            for ch in text:
                d.text((x, baseline), ch, font=f, fill=e["color"], anchor="ls")
                x += pdfmetrics.stringWidth(ch, "chk-" + e["font"], e["size_pt"]) + e["tracking_pt"]
        else:
            d.text((left, baseline), text, font=f, fill=e["color"], anchor="ls")

    from reportlab.lib.utils import simpleSplit
    for p in doc["pages"]:
        im = Image.new("RGB", (W, H), p["background"])
        d = ImageDraw.Draw(im)
        for e in p["elements"]:
            if e["type"] == "image":
                src = os.path.join(ROOT, e["file"])
                if os.path.exists(src):
                    pic = Image.open(src).convert("RGB").resize((max(1, round(e["w"])), max(1, round(e["h"]))))
                    im.paste(pic, (round(e["x"]), round(e["y"])))
            elif e["type"] == "rule":
                d.rectangle([e["x"], e["y"], e["x"] + e["w"], e["y"] + max(e["h"], 1)], fill=e["color"])
            elif e["kind"] == "line":
                left, right, base = extent(e)
                if e.get("runs"):
                    x = left
                    for r in e["runs"]:
                        seg = e["text"][r["start"]:r["end"]]
                        draw_line(d, dict(e, color=r["color"]), seg, x, base)
                        x += width(e, seg) + (e["tracking_pt"] if seg else 0)
                else:
                    draw_line(d, e, e["text"], left, base)
            else:
                base = e["y"] + e["size_pt"] * ASCENT_PARA
                for ln in simpleSplit(e["text"], "chk-" + e["font"], e["size_pt"], e["w"]):
                    w = width(e, ln)
                    left = e["x"] + (e["w"] - w) if e["align"] == "end" else e["x"] + (e["w"] - w) / 2 if e["align"] == "center" else e["x"]
                    draw_line(d, e, ln, left, base)
                    base += e["leading_pt"]
        d.line([0, H - M, W, H - M], fill="#3a2f22", width=1)      # the foot margin, for the eye
        im.save(os.path.join(out_dir, f"p{p['n']:02d}.png"))
    print(f"rendered {len(doc['pages'])} pages to {out_dir}")


def main():
    doc = json.load(open(OPS))
    print(f"{os.path.relpath(OPS, ROOT)}: generated {doc['generated']}, measured in {doc.get('measured_face', '?')}")
    n = check(doc)
    print(f"{n} problem(s)")
    if "--render" in sys.argv:
        render(doc, sys.argv[sys.argv.index("--render") + 1])
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
