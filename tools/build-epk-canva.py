#!/usr/bin/env python3
"""Emit the KILLER OF MEN press kit as Canva operations: the data contract the Canva app
(canva/kom-epk-builder) replays into an 18 x 24 in design, plus the flattened images it
places.

    <venv>/bin/python tools/build-epk-canva.py [--no-images] [--face libre|baskerville]

Writes
    canva/ops/epk-canva.json                 the contract (schema 1, see canva/README.md)
    press/assets/derived/canva/pNN-eMM.jpg   one flattened image per image placement

It does NOT lay pages out. tools/build-epk-kit.py does, once. This tool replays that
layout through tools/build-epk-ai.py's recording canvas (the same replay the Illustrator
project uses) and translates the recorded operations into Canva terms:

  * y measured DOWN from the page top, in pt of the 1296 x 1728 page; the app scales by
    the design's real pixel width, read at runtime
  * point text (a tracked heading or label) -> a "line": one richtext that must not wrap
  * area text (running copy) -> one "paragraph" richtext PER PARAGRAPH, each at the top
    the kit gave it, with a width; Canva wraps it. (As one richtext, every blank line
    between paragraphs became a full empty line, 0.4 of a lead taller than the kit's gap:
    six of them on the statement page, 2026-09-11.)
  * a rule -> a filled rectangle of the rule's weight
  * an image -> a derivative JPEG already cover-cropped to its box, with any ghost
    opacity and scrim baked in over the page ground, so the app places it opaque at x,y,w,h
  * a link rectangle -> attached to the line whose baseline it covers, as [start,end)
    offsets into that line's text

Derivatives are served by GitHub Pages once pushed (the repo is public), which is what
Canva's upload() needs: a public HTTPS URL that does not redirect. The masters in
press/assets are never modified.
"""
import datetime, importlib.util, json, os, re, subprocess, sys

from PIL import Image
from reportlab.lib.utils import simpleSplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS_OUT = os.path.join(ROOT, "canva", "ops", "epk-canva.json")
DERIVED = os.path.join(ROOT, "press", "assets", "derived", "canva")
PAGES_URL = "https://scroggdawg.github.io/kom-festival-board"
MAX_LONG_EDGE = 2400          # Canva renders at screen px; PDF Print upsamples past this anyway
JPEG_Q = 84


LIBRE_DIR = os.path.join(ROOT, "press", "assets", "derived", "fonts", "libre-baskerville")
FACE = sys.argv[sys.argv.index("--face") + 1] if "--face" in sys.argv else "libre"
if FACE not in ("libre", "baskerville"):
    sys.exit(f"--face must be libre or baskerville, not {FACE!r}")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def register_face(face):
    """Canva draws Libre Baskerville (an app cannot use an uploaded font), so the contract
    is MEASURED in it: every fit(), wrap, width and anchor the kit computes goes through
    reportlab's registered Bask faces, and the kit registers macOS Baskerville under those
    names at import. reportlab keeps the first registration of a name, so registering the
    Libre files first wins. Regular -> Bask; Bold -> Bask-SB (the weight the app falls back
    to for semibold) and Bask-B. The PDF and the .ai keep Baskerville. Laid out in
    Baskerville, Libre's wider glyphs reflowed the statement off the page foot, ate the cast
    page's gaps and put every handle on its lockup (Luke's notes, 2026-09-11)."""
    if face != "libre":
        return
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for name, fn in (("Bask", "LibreBaskerville-Regular.ttf"), ("Bask-SB", "LibreBaskerville-Bold.ttf"),
                     ("Bask-B", "LibreBaskerville-Bold.ttf")):
        path = os.path.join(LIBRE_DIR, fn)
        if not os.path.exists(path):
            sys.exit(f"missing {path}: see press/assets/derived/fonts/libre-baskerville/README.md")
        pdfmetrics.registerFont(TTFont(name, path))


register_face(FACE)
ai = _load("ai", os.path.join(ROOT, "tools", "build-epk-ai.py"))
kit, card = ai.kit, ai.card
W, H = ai.W, ai.H

FONT_KEY = {"Baskerville": "Bask", "Baskerville-SemiBold": "Bask-SB", "Baskerville-Bold": "Bask-B"}
FONTS = {
    "Bask":    {"family": "Baskerville", "weight": "normal",   "fallback_family": "Libre Baskerville", "fallback_weight": "normal"},
    "Bask-SB": {"family": "Baskerville", "weight": "semibold", "fallback_family": "Libre Baskerville", "fallback_weight": "bold"},
    "Bask-B":  {"family": "Baskerville", "weight": "bold",     "fallback_family": "Libre Baskerville", "fallback_weight": "bold"},
}
ASCENT = 0.95                 # baseline to richtext box top, in em; tuned on the pilot page
# A line's box is LINE_SLACK times its measure plus LINE_PAD pt, so Canva's own composer
# (kerning, rounding) never wraps it. Measured in Libre the slack is a margin; measured in
# Baskerville it had to cover Libre's wider glyphs as well (63 of 70 lines wrapped without it).
LINE_SLACK = 1.10 if FACE == "libre" else 1.35
LINE_PAD = 24.0


def hexcolor(rgb):
    return "#%02x%02x%02x" % tuple(int(v) for v in rgb)


def rel_url(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    return f"{PAGES_URL}/{rel}"


def flatten_image(op, scrim, out_path, write):
    """The image as the page will show it: cover-cropped to its box, ghost opacity and
    scrim baked over the ground, sized for Canva. Returns (w_px, h_px)."""
    x, top, w, h = op["x"], op["top"], op["w"], op["h"]
    scale_px = min(MAX_LONG_EDGE / max(w, h), 4.0)
    tw, th = max(1, round(w * scale_px)), max(1, round(h * scale_px))
    if not write:
        return tw, th
    im = Image.open(op["file"]).convert("RGB")
    iw, ih = im.size
    r = op["region"]
    rx0, ry0, rx1, ry1 = r[0] * iw, r[1] * ih, r[2] * iw, r[3] * ih
    rw, rh = rx1 - rx0, ry1 - ry0
    if op.get("fit") == "contain":
        s = min(w / rw, h / rh)
    else:
        s = max(w / rw, h / rh)
    cw, ch = w / s, h / s                                   # crop size in image px
    fx, fy = op["focus"]
    cx = rx0 + (rw - cw) * fx
    cy = ry0 + (rh - ch) * fy
    crop = im.crop((int(round(cx)), int(round(cy)), int(round(cx + cw)), int(round(cy + ch))))
    crop = crop.resize((tw, th), Image.LANCZOS)
    if op.get("grade") == "mono":                            # the kit's value-only grade
        crop = kit.grade_mono_pixels(crop)
    ground = Image.new("RGB", (tw, th), tuple(kit_ground_rgb()))
    alpha = float(op.get("opacity", 1.0))
    out = Image.blend(ground, crop, alpha) if alpha < 1.0 else crop
    if scrim is not None:
        veil = Image.new("RGB", (tw, th), tuple(int(v) for v in scrim["fill"]))
        out = Image.blend(out, veil, float(scrim["opacity"]))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    out.save(out_path, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    return tw, th


def kit_ground_rgb():
    return ai.rgb(kit.GROUND)


def convert(o, write_images=True):
    """Recorded operations -> the contract."""
    pages = {}
    for op in o.ops:
        pages.setdefault(op["p"], []).append(op)
    links_by_page = {}
    for lk in o.links:
        links_by_page.setdefault(lk["p"], []).append(lk)

    out_pages = []
    for p in sorted(pages):
        ops = pages[p]
        elements = []
        background = hexcolor(kit_ground_rgb())
        i = 0
        img_n = 0
        while i < len(ops):
            op = ops[i]
            if op["op"] == "rect":
                full = op["x"] <= 0.01 and op["w"] >= W - 0.01 and op["h"] >= H - 0.01
                if full and "opacity" not in op:
                    background = hexcolor(op["fill"])          # the page ground
                elif full and "opacity" in op:
                    pass                                         # a scrim without a picture under it: nothing to bake
                else:
                    elements.append({"type": "rule", "x": round(op["x"], 2), "y": round(H - op["top"], 2),
                                     "w": round(op["w"], 2), "h": round(op["h"], 2), "color": hexcolor(op["fill"])})
                i += 1
                continue
            if op["op"] == "image":
                scrim = None
                nxt = ops[i + 1] if i + 1 < len(ops) else None
                if nxt and nxt["op"] == "rect" and "opacity" in nxt and abs(nxt["w"] - op["w"]) < 1 and abs(nxt["h"] - op["h"]) < 1:
                    scrim = nxt
                    i += 1
                img_n += 1
                name = f"p{p:02d}-e{img_n:02d}.jpg"
                path = os.path.join(DERIVED, name)
                tw, th = flatten_image(op, scrim, path, write_images)
                elements.append({"type": "image", "url": rel_url(path), "file": os.path.relpath(path, ROOT),
                                 "px": [tw, th], "x": round(op["x"], 2), "y": round(H - op["top"], 2),
                                 "w": round(op["w"], 2), "h": round(op["h"], 2),
                                 "alt": os.path.basename(op["file"]).rsplit(".", 1)[0]})
                i += 1
                continue
            if op["op"] == "rule":
                x1, y1, x2, y2 = op["x1"], op["y1"], op["x2"], op["y2"]
                elements.append({"type": "rule", "x": round(min(x1, x2), 2), "y": round(H - max(y1, y2) - op["w"] / 2, 2),
                                 "w": round(abs(x2 - x1), 2), "h": round(op["w"], 2), "color": hexcolor(op["stroke"])})
                i += 1
                continue
            if op["op"] == "area":
                # One element per paragraph, each at the top the kit's para() gave it: the
                # first line's box top, then n lines of lead and the kit's gap per paragraph.
                # "lines" is the wrap the kit measured in the contract's face; the app's read
                # back flags a paragraph Canva set longer.
                size, lead, gap = op["size"], op["lead"], op["gap"]
                rl_font = {v: k for k, v in ai.FONT.items()}[op["font"]]
                top = op["top"]
                text = op["text"].replace("\r", "\n")
                for ptxt in [q for q in re.split(r"\n\s*\n", text.strip()) if q.strip()]:
                    ptxt = " ".join(ptxt.split())
                    n = len(simpleSplit(ptxt, rl_font, size, op["w"]))
                    elements.append({"type": "text", "kind": "paragraph", "text": ptxt, "lines": n,
                                     "font": FONT_KEY[op["font"]], "size_pt": round(size, 2), "leading_pt": round(lead, 2),
                                     "tracking_pt": 0.0, "color": hexcolor(op["fill"]),
                                     "align": {"left": "start", "center": "center", "right": "end"}[op["align"]],
                                     "x": round(op["x"], 2), "y": round(H - top, 2), "w": round(op["w"], 2), "links": []})
                    top -= n * lead + gap
                i += 1
                continue
            if op["op"] == "point":
                size = op["size"]
                track_pt = op["track"] / 1000.0 * size
                width = ai._measure.stringWidth(op["text"], {v: k for k, v in ai.FONT.items()}[op["font"]], size) \
                    + track_pt * max(len(op["text"]) - 1, 0)
                baseline_from_top = H - op["y"]
                # The box is generous and anchored on the line's own alignment edge: a right-
                # aligned line keeps its right edge (page 3's spine) and grows leftward if the
                # substitute face is wider; a centred line stays centred; a left one grows right.
                # The 2026-09-11 pilot wrapped 63 of page 3's lines with the old measured box.
                align = op.get("align", "left")
                ax = op.get("ax", op["x"])
                box_w = width * LINE_SLACK + LINE_PAD
                if align == "right":
                    bx, calign = ax - box_w, "end"
                elif align == "center":
                    bx, calign = ax - box_w / 2, "center"
                else:
                    bx, calign = op["x"], "start"
                elements.append({"type": "text", "kind": "line", "text": op["text"], "font": FONT_KEY[op["font"]],
                                 "size_pt": round(size, 2), "leading_pt": round(size * 1.2, 2),
                                 "tracking_pt": round(track_pt, 3), "color": hexcolor(op["fill"]), "align": calign,
                                 "x": round(bx, 2), "y": round(baseline_from_top - size * ASCENT, 2),
                                 "w": round(box_w, 2), "_baseline": baseline_from_top, "links": [],
                                 "_left": op["x"], "_right": op["x"] + width, "_width": width,
                                 "_align": align, "_ax": ax})
                i += 1
                continue
            i += 1

        # Two-tone rows: a key and a value drawn as two abutting runs on one baseline become
        # ONE line with two colour runs, anchored on the value's edge. As two boxes, a wider
        # substitute face slid the value under the key's tail (pilot round 2, 2026-09-11).
        merged, i = [], 0
        while i < len(elements):
            a = elements[i]
            b = elements[i + 1] if i + 1 < len(elements) else None
            if (b is not None and a["type"] == "text" and b["type"] == "text"
                    and a["kind"] == "line" and b["kind"] == "line"
                    and abs(a["_baseline"] - b["_baseline"]) < 0.5 and a["font"] == b["font"]
                    and abs(a["size_pt"] - b["size_pt"]) < 0.05 and abs(a["tracking_pt"] - b["tracking_pt"]) < 0.01):
                left, right = (a, b) if a["_left"] <= b["_left"] else (b, a)
                if abs(left["_right"] - right["_left"]) < 2.0:
                    text = left["text"] + right["text"]
                    width = left["_width"] + right["_width"]
                    box_w = width * LINE_SLACK + LINE_PAD
                    if right["_align"] == "right":
                        bx, calign, ax = right["_ax"] - box_w, "end", right["_ax"]
                    elif left["_align"] == "left":
                        bx, calign, ax = left["_left"], "start", left["_left"]
                    else:
                        mid = (left["_left"] + right["_right"]) / 2
                        bx, calign, ax = mid - box_w / 2, "center", mid
                    m = dict(right)
                    m.update({"text": text, "color": right["color"], "align": calign, "x": round(bx, 2),
                              "w": round(box_w, 2), "links": [], "_left": left["_left"], "_right": right["_right"],
                              "_width": width, "_align": calign, "_ax": ax,
                              "runs": [{"start": 0, "end": len(left["text"]), "color": left["color"]},
                                       {"start": len(left["text"]), "end": len(text), "color": right["color"]}]})
                    merged.append(m)
                    i += 2
                    continue
            merged.append(a)
            i += 1
        elements = merged

        # links: attach each recorded rectangle to the line whose baseline it covers
        unattached = []
        for lk in links_by_page.get(p, []):
            x0, y0, x1, y1 = lk["rect"]                          # y up
            top_from_top, bot_from_top = H - y1, H - y0
            hit = None
            for e in elements:
                if e["type"] == "text" and e["kind"] == "line":
                    b = e["_baseline"]
                    if top_from_top - 2 <= b <= bot_from_top + 2 and e["x"] + e["w"] >= x0 - 1 and e["x"] <= x1 + 1:
                        hit = e
                        break
            if hit is None:
                unattached.append(lk)
            else:
                hit["links"].append({"url": lk["url"], "start": 0, "end": len(hit["text"])})
        for e in elements:
            for k in ("_baseline", "_left", "_right", "_width", "_align", "_ax"):
                e.pop(k, None)
        out_pages.append({"n": p, "name": ai.ARTBOARDS[p - 1], "background": background,
                          "count": len(elements), "elements": elements,
                          "unattached_links": [lk["url"] for lk in unattached]})
    return out_pages


def main():
    write_images = "--no-images" not in sys.argv
    o = ai.record()
    pages = convert(o, write_images)
    d = card.load()
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except Exception:
        sha = ""
    doc = {"schema": 1, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "source": {"kit_commit": sha, "epk_rev": d.get("rev")},
           "measured_face": ("Libre Baskerville 2.005 (OFL; press/assets/derived/fonts/libre-baskerville)"
                             if FACE == "libre" else "Baskerville (macOS Supplemental)"),
           "page": {"width_pt": W, "height_pt": H}, "fonts": FONTS, "pages": pages}
    os.makedirs(os.path.dirname(OPS_OUT), exist_ok=True)
    json.dump(doc, open(OPS_OUT, "w"), indent=1, ensure_ascii=False)
    n_el = sum(p["count"] for p in pages)
    n_img = sum(1 for p in pages for e in p["elements"] if e["type"] == "image")
    n_links = sum(len(e["links"]) for p in pages for e in p["elements"] if e["type"] == "text")
    n_un = sum(len(p["unattached_links"]) for p in pages)
    n_para = sum(1 for p in pages for e in p["elements"] if e["type"] == "text" and e["kind"] == "paragraph")
    print(f"wrote {os.path.relpath(OPS_OUT, ROOT)}: {len(pages)} pages, {n_el} elements, {n_img} images, "
          f"{n_para} paragraphs, {n_links} links attached, {n_un} unattached; epk rev {d.get('rev')}, kit {sha}; "
          f"measured in {doc['measured_face']}")
    if write_images:
        total = sum(os.path.getsize(os.path.join(DERIVED, f)) for f in os.listdir(DERIVED) if f.endswith(".jpg"))
        print(f"derived images in {os.path.relpath(DERIVED, ROOT)}: {total/1e6:.1f} MB")
    if n_un:
        sys.exit("some links could not be attached to a text line; see unattached_links")


if __name__ == "__main__":
    main()
