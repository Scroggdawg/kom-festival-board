#!/usr/bin/env python3
"""Build the KILLER OF MEN credit cards as a PDF, from press/epk.json.

    <venv>/bin/python tools/build-credit-card.py [--medium|--large] [--transparent] [--png]

    --medium        type at 1.30x, stacked and centred. The readable middle.
    --large         type at 1.75x, stacked and centred. For projection.

    Both enlarged sizes STACK role over name instead of setting them side by side.
    The two-column reference layout only fits at 1x: a crew column leaves 284pt for
    the label and the longest one already needs 388pt at 1x. Enlarging it clips names
    off the page edge, which the first attempt at --large did.
                    Pages are FLOWED, not crammed: each carries its heading.
    --transparent   draw no ground at all, so the pages keep their alpha
    --png           also render each page to press/assets/CREDITS at 200 dpi

A transparent PDF opened in Preview looks blank: the type is cream, and a viewer
paints white behind a page that carries none of its own. That is the format working,
not failing. Composite it over the footage, or use the PNGs.

Pages are the EPK's own size (1296 x 1728 pt, per press/epk-spec.md) so they drop
straight into the kit:

    CAST            billed cast, key credits, extras
    CREW            two columns, role right, name left  -- the reference layout
    THANKS + AFI    thank-yous, fellows, the required boilerplate

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
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "press", "epk.json")
OUT = os.path.join(ROOT, "press", "KillerOfMen_Credits.pdf")
BG = os.path.join(ROOT, "press", "assets", "STILLS")

W, H = 1296.0, 1728.0
BASK = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
pdfmetrics.registerFont(TTFont("Bask", BASK, subfontIndex=0))
pdfmetrics.registerFont(TTFont("Bask-SB", BASK, subfontIndex=4))

CREAM = colors.HexColor("#efe6d6")
DIM = colors.HexColor("#b9a88c")
GROUND = colors.HexColor("#0b0806")
RULE = colors.HexColor("#6b5942")

M = 74.0
S = 1.0                                    # type scale; --large raises it


class Sz:
    """Every measurement derives from the scale, so one number moves the whole card."""
    def __init__(self, s):
        self.s = s
        self.title = 40.0 * s
        self.role = 14.2 * s
        self.name = 15.6 * s
        self.lead = 21.0 * s
        self.gap = 15.0 * s
        self.track_t = 6.0 * s
        self.track_r = 1.35 * s
        self.track_n = 0.95 * s
        self.boiler = 11.4 * max(s * 0.8, 1.0)
        self.boiler_lead = 17.0 * max(s * 0.8, 1.0)
        # Two columns only survive at 1x, and only just. A crew column is 546pt wide
        # and leaves 284pt for the label, while "Department head makeup and SFX makeup"
        # is 388pt at 1x already — it works today because it lands beside empty space,
        # which is luck, not design. Any enlargement STACKS role over name, centred,
        # the way an end crawl does. That is also what lets the names get properly big.
        self.stacked = s > 1.05
        if self.stacked:
            self.role *= 0.72                      # the label steps back; the name leads


# ---------- reading the worksheet ----------
def load():
    return json.load(open(SRC, encoding="utf-8"))


def field(d, n):
    for sec in d["sections"]:
        for f in sec["fields"]:
            if f["n"] == n:
                return f["value"]
    raise KeyError(n)


def pairs(text):
    """(role, [names]) out of 'Role | Name' lines. A line with no pipe ends the run,
    which is what keeps the fields' trailing caveats off the card."""
    out = []
    for line in text.split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        if "|" not in line:
            if line.isupper() and len(line) < 40:
                out.append((None, line.strip()))
                continue
            break
        role, _, name = line.partition("|")
        role, name = role.strip(), name.strip()
        if not name:
            continue
        names = [n.strip() for n in re.split(r"\s+·\s+", name) if n.strip()]
        out.append((role, names))
    return out


# ---------- drawing primitives ----------
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
    """The stills carry their black bars in the pixels. Drawn as a background those
    bars show as a hard horizontal edge, so the picture area is found and cropped out.
    Detected, not hardcoded, so any still works."""
    from PIL import Image
    import io
    im = Image.open(path).convert("RGB")
    g = im.convert("L")
    w, h = g.size
    rows = [y for y in range(h) if g.crop((0, y, w, y + 1)).getextrema()[1] > 8]
    if rows and (rows[0] > 2 or rows[-1] < h - 3):
        im = im.crop((0, rows[0], w, rows[-1] + 1))
    # The backdrop sits at 16% under a 55% scrim; it does not need six megapixels, and
    # at full size ten pages of it made a 35 MB PDF. This is the card's own artwork,
    # not a delivered asset — the stills themselves are untouched in press/assets.
    im.thumbnail((1600, 1600), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True)   # lossless is wasted at 16% opacity
    buf.seek(0)
    return ImageReader(buf)


def ground(c, still=None, transparent=False):
    """transparent=True draws nothing, so the page keeps its alpha."""
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
    c.saveState()
    c.setFillColor(GROUND)
    c.setFillAlpha(0.55)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.restoreState()


def heading(c, text, y, z, cont=False):
    tracked(c, W / 2, y, text, "Bask", z.title, z.track_t, CREAM, "center")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    half = 118 * z.s
    c.line(W / 2 - half, y - 22 * z.s, W / 2 + half, y - 22 * z.s)
    y -= 62 * z.s
    if cont:
        tracked(c, W / 2, y + 18 * z.s, "CONTINUED", "Bask", z.role * 0.8,
                z.track_r, RULE, "center")
    return y


# ---------- flow: the part that makes --large possible ----------
def label_lines(role, z):
    """A long role label wraps onto extra lines at full size instead of shrinking
    (side-by-side layout only). z.label_room is the width the column gives labels."""
    room = getattr(z, "label_room", None)
    if z.stacked or not room:
        return [role.upper()]
    lab = role.upper()
    if pdfmetrics.stringWidth(lab, "Bask", z.role) + z.track_r * max(len(lab) - 1, 0) <= room:
        return [lab]
    return simpleSplit(lab, "Bask", z.role, room - z.track_r * max(len(lab) - 1, 0) / 2)


def item_h(e, z):
    if e[0] is None:
        return z.lead + z.gap
    n = len(e[1]) + (1 if z.stacked else 0)        # stacked spends a line on the role
    n = max(n, len(label_lines(e[0], z)))          # a wrapped label can be the tall side
    return z.lead * n + z.gap * (1.35 if z.stacked else 1.0)


def flow(entries, col_h, z):
    """Break the list into columns that fit col_h. A department heading is never left
    at the foot of a column with nothing under it — it moves to the next column."""
    cols, cur, run = [], [], 0.0
    for e in entries:
        h = item_h(e, z)
        if cur and run + h > col_h:
            while cur and cur[-1][0] is None:
                e_moved = cur.pop()
                run -= item_h(e_moved, z)
                cols.append(cur) if False else None
                cur_tail = [e_moved]
                break
            else:
                cur_tail = []
            cols.append(cur)
            cur, run = cur_tail, sum(item_h(x, z) for x in cur_tail)
        cur.append(e)
        run += h
    if cur:
        cols.append(cur)
    return cols


def balance(cols, z, col_h=None):
    """When everything fits on one page, split it evenly instead of filling column one
    to the brim and leaving column two short. The split falls on a department heading
    when one fits, so neither column opens mid-department (F22); otherwise the old
    nearest-to-half split stands."""
    if len(cols) != 2:
        return cols
    flat = cols[0] + cols[1]
    h = [item_h(e, z) for e in flat]
    total = sum(h)
    if col_h:
        best, best_diff = None, None
        for i in range(1, len(flat)):
            if flat[i][0] is not None:                      # only at a heading
                continue
            lh, rh = sum(h[:i]), sum(h[i:])
            if lh > col_h or rh > col_h:
                continue
            if best is None or abs(lh - rh) < best_diff:
                best, best_diff = i, abs(lh - rh)
        if best is not None:
            return [flat[:best], flat[best:]]
    left, run = [], 0.0
    for i, e in enumerate(flat):
        if run + h[i] / 2 > total / 2:
            break
        left.append(e)
        run += h[i]
    right = flat[len(left):]
    while left and left[-1][0] is None:
        right.insert(0, left.pop())
    return [left, right]


def condense(c, text, font, size, track, room):
    """Shrink a label until it fits its room. Clipping a name is not an option, and
    silently running past the margin is how the first --large render broke."""
    while size > 6 and c.stringWidth(text, font, size) + track * max(len(text) - 1, 0) > room:
        size -= 0.4
        track = max(track - 0.03, 0)
    return size, track


def draw_col(c, entries, x_role, x_name, y, z, left_bound=M):
    """Side by side at normal size; stacked and centred on the page at large size."""
    for role, names in entries:
        if role is None:                                        # department heading
            y -= 6 * z.s
            if z.stacked:
                tracked(c, W / 2, y, names, "Bask-SB", z.role * 1.1,
                        z.track_r + 0.7 * z.s, RULE, "center")
            else:
                sz, tr = condense(c, names, "Bask-SB", z.role,
                                  z.track_r + 0.7 * z.s, W - M - x_name)
                tracked(c, x_name, y, names, "Bask-SB", sz, tr, RULE)
            y -= z.lead + z.gap - 6 * z.s
            continue
        if z.stacked:
            tracked(c, W / 2, y, role.upper(), "Bask", z.role,
                    z.track_r + 0.6 * z.s, DIM, "center")
            y -= z.lead
            for n in names:
                tracked(c, W / 2, y, n.upper(), "Bask", z.name, z.track_n, CREAM, "center")
                y -= z.lead
            y -= z.gap * 1.35
            continue
        # A label too long for its room wraps at full size (F17); only names condense.
        lines = label_lines(role, z)
        for i, lab in enumerate(lines):
            tracked(c, x_role, y - i * z.lead, lab, "Bask", z.role, z.track_r, DIM, "right")
        for i, n in enumerate(names):
            u = n.upper()
            ns, nt = condense(c, u, "Bask", z.name, z.track_n, W - M - x_name)
            tracked(c, x_name, y - i * z.lead, u, "Bask", ns, nt, CREAM)
        y -= z.lead * max(len(names), len(lines)) + z.gap
    return y


# ---------- pages ----------
def two_col_pages(c, title, entries, z, stills, transparent):
    y_probe = H - M - 46 * z.s
    col_h = (y_probe - 62 * z.s) - M
    colw = (W - 2 * M - 56) / 2
    lx = M + colw * 0.52
    rx = M + colw + 56 + colw * 0.52
    z.label_room = colw * 0.52                     # what a label may take before wrapping
    cols = flow(entries, col_h, z)
    if len(cols) == 2:
        cols = balance(cols, z, col_h)
    for p in range(0, len(cols), 2):
        ground(c, next(stills), transparent)
        y0 = heading(c, title, y_probe, z, cont=(p > 0))
        draw_col(c, cols[p], lx, lx + 18 * z.s, y0, z, M)
        if p + 1 < len(cols):
            draw_col(c, cols[p + 1], rx, rx + 18 * z.s, y0, z, M + colw + 56)
        c.showPage()


def one_col_pages(c, title, groups, z, stills, transparent):
    """groups: list of entry-lists, drawn with a rule between them. Centred column."""
    y_probe = H - M - 46 * z.s
    col_h = (y_probe - 62 * z.s) - M
    z.label_room = W / 2 - 26 * z.s - M
    seq = []
    for gi, g in enumerate(groups):
        if gi:
            seq.append(("__RULE__", None))
        seq += g
    pages, cur, run = [], [], 0.0
    for e in seq:
        h = 46 * z.s if e[0] == "__RULE__" else item_h(e, z)
        if cur and run + h > col_h:
            pages.append(cur)
            cur, run = [], 0.0
            if e[0] == "__RULE__":
                continue
        cur.append(e)
        run += h
    if cur:
        pages.append(cur)
    x_role, x_name = W / 2 - 26 * z.s, W / 2 + 26 * z.s
    for i, page in enumerate(pages):
        ground(c, next(stills), transparent)
        y = heading(c, title, y_probe, z, cont=(i > 0))
        for e in page:
            if e[0] == "__RULE__":
                y -= 20 * z.s
                c.setStrokeColor(RULE)
                c.setLineWidth(0.5)
                c.line(W / 2 - 90 * z.s, y + 10, W / 2 + 90 * z.s, y + 10)
                y -= 26 * z.s
                continue
            y = draw_col(c, [e], x_role, x_name, y, z)
        c.showPage()


def page_thanks(c, d, z, stills, transparent):
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
    y_probe = H - M - 46 * z.s
    # Boilerplate sets on a 540 pt measure (F11): two lines a paragraph, 10-12 words on
    # the last; a last line under three words widens the measure a notch instead.
    def split_boiler(para):
        for width in (540, 520):
            lines = simpleSplit(para, "Bask", z.boiler, width * max(z.s * 0.8, 1.0))
            if len(lines[-1].split()) >= 3:
                return lines
        return lines
    boiler_lines = [split_boiler(p) for p in BOILER]
    legal_h = sum(len(l) * z.boiler_lead for l in boiler_lines) + 12 * (len(BOILER) - 1)
    foot = (34 * z.s + len(fellows) * z.lead + 34 * z.s + legal_h + 10 + z.lead + 40 * z.s)
    avail = (y_probe - 62 * z.s) - M

    # names first, over as many pages as they need; the AFI card lands on the last one
    per = max(1, int((avail - 46 * z.s) // z.lead))
    chunks = [names[i:i + per] for i in range(0, len(names), per)] or [[]]
    if len(chunks) == 1 and 46 * z.s + len(names) * z.lead > avail - foot:
        room = max(1, int((avail - 46 * z.s - foot) // z.lead))
        chunks = [names[:room], names[room:]]

    for i, chunk in enumerate(chunks):
        ground(c, next(stills), transparent)
        y = heading(c, "T H A N K S", y_probe, z, cont=(i > 0))
        if len(chunks) == 1:
            # One page: the names and fellows sit centred between the title and the
            # legal block anchored at the foot, so the seam is two zones, not one hole.
            block = (46 * z.s + len(chunk) * z.lead + 40 * z.s + 30 * z.s
                     + len(fellows) * z.lead)
            legal_top = M + 18 + 10 + z.lead + legal_h
            spare = (y - legal_top) - block
            y -= max(0.0, spare / 2 - 40 * z.s)
        if i == 0:
            tracked(c, W / 2, y, "THE FILMMAKERS WISH TO THANK", "Bask",
                    z.role * 1.1, z.track_r + 1.0 * z.s, DIM, "center")   # the label class
            y -= 46 * z.s
        for n in chunk:
            tracked(c, W / 2, y, n.upper(), "Bask", z.name, z.track_n, CREAM, "center")
            y -= z.lead
        if i == len(chunks) - 1:
            y -= 40 * z.s
            c.setStrokeColor(RULE)
            c.setLineWidth(0.5)
            c.line(W / 2 - 90 * z.s, y + 14, W / 2 + 90 * z.s, y + 14)   # a divider, not a title rule
            y -= 30 * z.s
            for fl in fellows:
                tracked(c, W / 2, y, fl.upper(), "Bask", z.role + 0.4 * z.s,
                        z.track_n, CREAM, "center")
                y -= z.lead
            # The legal block anchors from the foot: the © line on the kit's footer
            # baseline, the three paragraphs stacked above it. The ghost holds the seam.
            y_c = M + 18
            y = y_c + 10 + z.lead + legal_h
            for lines in boiler_lines:
                for line in lines:
                    tracked(c, W / 2, y, line, "Bask", z.boiler, 0.6, DIM, "center")
                    y -= z.boiler_lead
                y -= 12
            tracked(c, W / 2, y_c, "© MMXXV   AMERICAN FILM INSTITUTE", "Bask",
                    z.role, z.track_r, CREAM, "center")
        c.showPage()


def main():
    large = "--large" in sys.argv
    medium = "--medium" in sys.argv
    transparent = "--transparent" in sys.argv
    z = Sz(1.75 if large else 1.30 if medium else 1.0)
    out = OUT
    if large:
        out = out.replace(".pdf", "_large.pdf")
    elif medium:
        out = out.replace(".pdf", "_medium.pdf")
    if transparent:
        out = out.replace(".pdf", "_transparent.pdf")
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]

    d = load()
    pool = sorted(f for f in os.listdir(BG) if f.endswith(".png")) if os.path.isdir(BG) else []

    def pick(n):
        for st in pool:
            if st.endswith(f"1.1.{n}.png"):
                return os.path.join(BG, st)
        return None

    def stills_for(nums):
        while True:
            for n in nums:
                yield pick(n)

    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("Killer of Men — Credits")

    billed = pairs(field(d, "9.2"))
    cast = [e for e in billed if e[0] and e[0].lower() != "extras"]
    extras = [e for e in billed if e[0] and e[0].lower() == "extras"]
    key = [e for e in pairs(field(d, "9.1"))
           if e[0] and "unknown" not in " ".join(e[1]).lower()]
    one_col_pages(c, "C A S T", [cast, key] + ([extras] if extras else []),
                  z, stills_for([31, 27, 38]), transparent)
    crew = pairs(field(d, "10.1"))
    if z.stacked:
        one_col_pages(c, "C R E W", [crew], z, stills_for([35, 3, 19]), transparent)
    else:
        two_col_pages(c, "C R E W", crew, z, stills_for([35, 3, 19]), transparent)
    page_thanks(c, d, z, stills_for([41, 13]), transparent)
    c.save()
    print(f"wrote {out}")

    if "--png" in sys.argv:
        import pymupdf
        outdir = os.path.join(ROOT, "press", "assets", "CREDITS")
        os.makedirs(outdir, exist_ok=True)
        doc = pymupdf.open(out)
        tag = ("_large" if large else "_medium" if medium else "") + \
              ("_transparent" if transparent else "")
        for i, page in enumerate(doc):
            f = os.path.join(outdir, f"KillerOfMen_Credits_p{i+1}{tag}.png")
            page.get_pixmap(dpi=200, alpha=transparent).save(f)
            print(f"  {os.path.basename(f)}")


if __name__ == "__main__":
    main()
