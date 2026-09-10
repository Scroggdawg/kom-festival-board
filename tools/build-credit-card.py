#!/usr/bin/env python3
"""Build the KILLER OF MEN credit cards as a PDF, from press/epk.json.

    <venv>/bin/python tools/build-credit-card.py [--transparent] [--png] [--out FILE]

    --transparent   draw no ground at all, so the pages keep their alpha
    --png           also render each page to press/assets/CREDITS at 200 dpi

A transparent PDF opened in Preview looks blank: the type is cream, and a viewer
paints white behind a page that carries none of its own. That is the format working,
not failing. Composite it over the footage, or use the PNGs.

Three pages at the EPK's own page size (1296 x 1728 pt, per press/epk-spec.md) so they
drop straight into the kit as pages 9-11:

    1  CAST            billed cast, then extras
    2  CREW            two columns, role right, name left  -- the reference layout
    3  THANKS + AFI    thank-yous, fellows, the required boilerplate

Nothing is retyped. Every name is parsed out of press/epk.json fields 9.1, 9.2, 10.1,
11.1 and 11.3, which were themselves transcribed from the End Titles tab of
2513 KOM Credits 11-5-SDnotes.xlsx. Change a name with epk.py and rebuild; the card
cannot drift from the worksheet because it has no copy of its own.

A trailing prose note in a field (the caveats about TBD sound, blank positions and the
Uwhubetine/Betine mismatch) is deliberately NOT drawn -- parsing stops at the first line
that is not "role | name". Those caveats stay in the worksheet where they belong.
"""
import json, os, re, sys

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "press", "epk.json")
OUT = os.path.join(ROOT, "press", "KillerOfMen_Credits.pdf")
BG = os.path.join(ROOT, "press", "assets", "STILLS")

W, H = 1296.0, 1728.0                      # the EPK page, per epk-spec.md
BASK = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
pdfmetrics.registerFont(TTFont("Bask", BASK, subfontIndex=0))
pdfmetrics.registerFont(TTFont("Bask-SB", BASK, subfontIndex=4))

CREAM = colors.HexColor("#efe6d6")         # the film's own cream, off the poster
DIM = colors.HexColor("#b9a88c")           # role labels sit back from the names
GROUND = colors.HexColor("#0b0806")
RULE = colors.HexColor("#6b5942")

M = 74.0                                   # page margin
TITLE = 40.0
ROLE = 14.2
NAME = 15.6
LEAD = 21.0                                # line to line, within a block
GAP = 15.0                                 # between role blocks
TRACK_T = 6.0                              # letterspacing: title
TRACK_R = 1.35                             # roles
TRACK_N = 0.95                             # names


# ---------- reading the worksheet ----------
def load():
    return json.load(open(SRC, encoding="utf-8"))


def field(d, n):
    for s in d["sections"]:
        for f in s["fields"]:
            if f["n"] == n:
                return f["value"]
    raise KeyError(n)


def pairs(text, stop_at_prose=True):
    """(role, [names]) out of 'Role | Name' lines. A line with no pipe ends the run,
    which is what keeps the fields' trailing caveats off the card."""
    out = []
    for line in text.split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        if "|" not in line:
            if line.isupper() and len(line) < 40:      # a department heading
                out.append((None, line.strip()))
                continue
            if stop_at_prose:
                break
            continue
        role, _, name = line.partition("|")
        role, name = role.strip(), name.strip()
        if not name:                                    # an empty slot: not drawn
            continue
        names = [n.strip() for n in re.split(r"\s+·\s+", name) if n.strip()]
        out.append((role, names))
    return out


# ---------- drawing ----------
def tracked(c, x, y, s, font, size, track, fill, align="left"):
    """Letterspacing lives on the text object, not the canvas."""
    w = c.stringWidth(s, font, size) + track * max(len(s) - 1, 0)
    if align == "right":
        x -= w
    elif align == "center":
        x -= w / 2.0
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setFillColor(fill)
    t.setCharSpace(track)
    t.textOut(s)
    c.drawText(t)
    return w


def unletterbox(path):
    """The stills carry their black bars in the pixels. Drawn as a background those bars
    show up as a hard horizontal edge across the page, so the picture area is found and
    cropped out first. Detected, not hardcoded, so any still can be used."""
    from PIL import Image
    import io
    im = Image.open(path).convert("RGB")
    g = im.convert("L")
    w, h = g.size
    rows = [y for y in range(h) if g.crop((0, y, w, y + 1)).getextrema()[1] > 8]
    if rows and (rows[0] > 2 or rows[-1] < h - 3):
        im = im.crop((0, rows[0], w, rows[-1] + 1))
    buf = io.BytesIO()
    im.save(buf, "PNG")
    buf.seek(0)
    return ImageReader(buf)


def ground(c, still=None, transparent=False):
    """transparent=True draws nothing at all, so the page keeps its alpha and the
    cards can be laid over footage, a still, or a page in a layout app."""
    if transparent:
        return
    c.setFillColor(GROUND)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    if still and os.path.exists(still):
        try:
            c.saveState()
            c.setFillAlpha(0.16)
            img = unletterbox(still)
            iw, ih = img.getSize()
            sc = max(W / iw, H / ih)
            c.drawImage(img, (W - iw * sc) / 2, (H - ih * sc) / 2,
                        iw * sc, ih * sc, mask="auto")
            c.restoreState()
        except Exception:
            pass
    c.saveState()                                        # settle the ground back down
    c.setFillColor(GROUND)
    c.setFillAlpha(0.55)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.restoreState()


def heading(c, text, y):
    tracked(c, W / 2, y, text, "Bask", TITLE, TRACK_T, CREAM, "center")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(W / 2 - 118, y - 22, W / 2 + 118, y - 22)
    return y - 62


def block_height(entries, lead=None, gap=None):
    lead, gap = lead or LEAD, gap or GAP
    h = 0.0
    for role, names in entries:
        h += (lead + gap) if role is None else lead * len(names) + gap
    return h


def fit(natural, available, lo=1.0, hi=1.62):
    """One factor on leading and gap so a page fills its column rather than stopping
    two thirds down. Clamped: a short page opens up, it never becomes a poster."""
    if natural <= 0:
        return 1.0
    return max(lo, min(hi, available / natural))


def draw_column(c, entries, x_role, x_name, y, lead=None, gap=None):
    """Roles right-aligned to x_role, names left-aligned from x_name."""
    lead, gap = lead or LEAD, gap or GAP
    for role, names in entries:
        if role is None:                                  # department heading
            y -= 6
            tracked(c, x_name, y, names, "Bask-SB", ROLE, TRACK_R + 0.7, RULE)
            y -= lead + gap - 6
            continue
        tracked(c, x_role, y, role.upper(), "Bask", ROLE, TRACK_R, DIM, "right")
        for i, n in enumerate(names):
            tracked(c, x_name, y - i * lead, n.upper(), "Bask", NAME, TRACK_N, CREAM)
        y -= lead * len(names) + gap
    return y


def split_columns(entries):
    """Balance by drawn height, and never orphan a department heading at a column foot."""
    total = block_height(entries)
    _ = total
    left, right, run = [], [], 0.0
    for i, e in enumerate(entries):
        h = LEAD + GAP if e[0] is None else LEAD * len(e[1]) + GAP
        if run + h / 2 <= total / 2 and not right:
            left.append(e)
            run += h
        else:
            right.append(e)
    while left and left[-1][0] is None:                   # heading stranded at the foot
        right.insert(0, left.pop())
    return left, right


def page_cast(c, d, still, transparent=False):
    ground(c, still, transparent)
    y0 = heading(c, "C A S T", H - M - 46)
    billed = pairs(field(d, "9.2"))
    cast = [e for e in billed if e[0] and e[0].lower() != "extras"]
    extras = [e for e in billed if e[0] and e[0].lower() == "extras"]
    key = [e for e in pairs(field(d, "9.1"))
           if e[0] and "unknown" not in " ".join(e[1]).lower()]
    SEP1, SEP2 = 56.0, 30.0
    natural = (block_height(cast) + SEP1 + block_height(key)
               + (SEP2 + block_height(extras) if extras else 0))
    f = fit(natural, y0 - M)
    lead, gap = LEAD * f, GAP * f
    x_role, x_name = W / 2 - 26, W / 2 + 26
    y = draw_column(c, cast, x_role, x_name, y0, lead, gap)
    y -= SEP1 * f * 0.45
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(W / 2 - 90, y + 10, W / 2 + 90, y + 10)
    y -= SEP1 * f * 0.55
    y = draw_column(c, key, x_role, x_name, y, lead, gap)
    if extras:
        y -= SEP2 * f
        draw_column(c, extras, x_role, x_name, y, lead, gap)
    c.showPage()


def page_crew(c, d, still, transparent=False):
    ground(c, still, transparent)
    y0 = heading(c, "C R E W", H - M - 46)
    entries = pairs(field(d, "10.1"))
    left, right = split_columns(entries)
    f = fit(max(block_height(left), block_height(right)), y0 - M)
    lead, gap = LEAD * f, GAP * f
    colw = (W - 2 * M - 56) / 2
    lx = M + colw * 0.52
    rx = M + colw + 56 + colw * 0.52
    draw_column(c, left, lx, lx + 18, y0, lead, gap)
    draw_column(c, right, rx, rx + 18, y0, lead, gap)
    c.showPage()


def wrapped(c, text, x, y, width, font, size, lead, fill, track=0.0, align="center"):
    from reportlab.lib.utils import simpleSplit
    c.setFont(font, size)
    for line in simpleSplit(text, font, size, width):
        tracked(c, x, y, line, font, size, track, fill, align)
        y -= lead
    return y


def page_thanks(c, d, still, transparent=False):
    ground(c, still, transparent)
    y0 = heading(c, "T H A N K S", H - M - 46)
    raw = field(d, "11.1")
    names = []
    for line in raw.split("\n")[1:]:
        if not line.strip():
            continue
        if line.strip().isupper() or line.startswith(("Thirty", "PADMA", "AFI")):
            break
        names += [n.strip() for n in re.split(r"\s+·\s+", line.strip()) if n.strip()]
    fellows = [l.strip() for l in field(d, "11.3").split("\n")
               if re.match(r"^[A-Z][^|]*, AFI .* Fellow$", l.strip())]
    BOILER = [
        "PRODUCED AT THE AFI CONSERVATORY IN PARTIAL FULFILLMENT OF THE "
        "REQUIREMENTS FOR THE MASTER OF FINE ARTS DEGREE OR CERTIFICATE OF COMPLETION.",
        "THIS MOTION PICTURE IS THE PROPERTY OF THE AMERICAN FILM INSTITUTE AND IS "
        "PROTECTED UNDER THE COPYRIGHT LAWS OF THE UNITED STATES AND OTHER COUNTRIES.",
        "THE CHARACTERS AND EVENTS DEPICTED IN THIS MOTION PICTURE ARE FICTITIOUS. "
        "ANY SIMILARITY TO ACTUAL PERSONS, LIVING OR DEAD, IS PURELY COINCIDENTAL.",
    ]
    # the fixed furniture at the foot does not stretch; only the two name lists do
    foot = 34 + len(fellows) * LEAD + 34 + len(BOILER) * (2 * 17 + 16) + 10 + LEAD + 40
    f = fit(46 + len(names) * LEAD, y0 - M - foot, hi=1.45)
    lead = LEAD * f
    tracked(c, W / 2, y0, "THE FILMMAKERS WISH TO THANK", "Bask", ROLE, TRACK_R + 1.0, DIM, "center")
    y = y0 - 46 * f
    for n in names:
        tracked(c, W / 2, y, n.upper(), "Bask", NAME, TRACK_N, CREAM, "center")
        y -= lead
    y -= 40
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(W / 2 - 118, y + 14, W / 2 + 118, y + 14)
    y -= 30
    for fl in fellows:
        tracked(c, W / 2, y, fl.upper(), "Bask", ROLE + 0.4, TRACK_N, CREAM, "center")
        y -= LEAD
    y -= 34
    for para in BOILER:
        y = wrapped(c, para, W / 2, y, W - 2 * M - 180, "Bask", 11.4, 17, DIM, 0.6) - 16
    y -= 10
    tracked(c, W / 2, y, "© MMXXV   AMERICAN FILM INSTITUTE", "Bask", ROLE, TRACK_R, CREAM, "center")
    c.showPage()


def main():
    transparent = "--transparent" in sys.argv
    out = OUT if not transparent else OUT.replace(".pdf", "_transparent.pdf")
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    d = load()
    stills = sorted(f for f in os.listdir(BG) if f.endswith(".png")) if os.path.isdir(BG) else []

    def pick(n):
        want = f"1.1.{n}.png"
        for st in stills:
            if st.endswith(want):
                return os.path.join(BG, st)
        return None

    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("Killer of Men — Credits")
    page_cast(c, d, pick(31), transparent)
    page_crew(c, d, pick(35), transparent)
    page_thanks(c, d, pick(41), transparent)
    c.save()
    print(f"wrote {out}")

    if "--png" in sys.argv:
        import pymupdf
        dpi = 200
        names = ["1_Cast", "2_Crew", "3_Thanks"]
        outdir = os.path.join(ROOT, "press", "assets", "CREDITS")
        os.makedirs(outdir, exist_ok=True)
        doc = pymupdf.open(out)
        for i, page in enumerate(doc):
            suffix = "_transparent" if transparent else ""
            f = os.path.join(outdir, f"KillerOfMen_Credits_{names[i]}{suffix}.png")
            page.get_pixmap(dpi=dpi, alpha=transparent).save(f)
            print(f"  {os.path.basename(f)}")


if __name__ == "__main__":
    main()
