#!/usr/bin/env python3
"""Build the KILLER OF MEN credit cards as a PDF, from press/epk.json.

    <venv>/bin/python tools/build-credit-card.py [--medium|--large] [--transparent] [--png]
                                                 [--headings] [--label-gold] [--crew-size 16|17|18]
                                                 [--press] [--still SECTION=N,ALPHA,ANCHOR]
                                                 [--ground-only] [--out FILE] [--no-gate]

    --medium        type at 1.30x, stacked and centred. The readable middle.
    --large         type at 1.75x, stacked and centred. For projection.
                    Both enlarged sizes STACK role over name and paginate with a CONTINUED
                    tag; the four-column CREW form and the half-page hero composition of
                    the 1x card only fit at 1x (role room 290 x 1.3 per pair is already
                    1560 pt against 1200 usable). Every enlarged page uses the CREW
                    backdrop (still 1.1.27 at 0.45, anchor 0.50) because stacked type
                    spans the full width and runs over the figure. The three-column thanks
                    drops to two columns at --medium and one at --large; the extras and
                    thanks rows may break across pages (a '&'-wrapped entry never splits),
                    and the legal block is pushed down to sit 90 pt above the AFI slot on
                    the page that ends the stack when it would otherwise leave a hole.
    --transparent   draw no ground at all, so the pages keep their alpha
    --png           also render each page to press/assets/CREDITS at 200 dpi
    --headings      draw the 10.1 department names on CREW (default off: the reference
                    form separates departments by ONE blank line, a 2P gap; under
                    --headings the gap grows to one blank line plus the heading line)
    --label-gold    set the three wayfinding labels CAST / EXTRAS / THE FILMMAKERS WISH
                    TO THANK in DIM gold instead of cream (default off)
    --crew-size N   CREW body size 16, 17 or 18 pt (default 17, the measured ceiling of
                    the four-column form: at 18 fourteen role labels wrap)
    --press         drop rows whose name is exactly STILL UNKNOWN and print a notice
                    (default off: the gap stays visible, as the data reads)
    --still S=N,A,X override one page's still: S is CREDITS, CREW, THANKS or ENLARGED,
                    N the 1.1.N still number, A the alpha, X the horizontal anchor 0..1
                    (e.g. --still THANKS=25,0.35,0.50 renders the lantern-in-frame
                    alternate). GROUND_RECIPE is updated to match, so the replays follow.
                    The gate still runs; a variant that fails it is not a variant.
    --ground-only   draw only the grounds (the legibility gate's helper)
    --no-gate       skip the legibility gate (it needs pymupdf and numpy)
    --out FILE      write the PDF here instead of press/KillerOfMen_Credits*.pdf

A transparent PDF opened in Preview looks blank: the type is cream, and a viewer
paints white behind a page that carries none of its own. That is the format working,
not failing. Composite it over the footage, or use the PNGs.

Pages are the EPK's own size (1296 x 1728 pt, per press/epk-spec.md) so they drop
straight into the kit:

    CREDITS         the poster block stacked in the black left third (role and name at
                    one size, as the reference sets them), then CAST
    CREW            four columns (two role | name pairs) on one 28 pt slot grid; the
                    9.1 tail first; departments parted by one blank slot (2P = 56)
    THANKS + AFI    extras, thanks, PARTNER LOGOS slot, Avid, boilerplate, fellows,
                    copyright, AFI CONSERVATORY LOGO slot; the copyright sits 90 pt
                    above the slot (p3 grid 28: paragraph gaps 56, fellows 84, copyright 112)

Every letterspaced label keeps a tracking of at most ~0.13 em so pymupdf (and, by the
same heuristic, most viewers) still reads it as a word: CAST, EXTRAS, PARTNER LOGOS, AFI
CONSERVATORY LOGO and the --headings names must all be found by page.search_for(); the
gate asserts it. That is pymupdf's word-gap heuristic, a floor and not a proof for
Preview or Acrobat.

Nothing is retyped. Every name, paragraph and year is parsed out of press/epk.json
fields 9.1, 9.2, 10.1, 11.1 and 11.3 at build time. The only hardcoded strings are the
UI words CREDITS, CREW, CAST, CONTINUED and the two slot labels PARTNER LOGOS and
AFI CONSERVATORY LOGO. Structural rules replace names: the poster block is 9.1 through
the first row whose role starts 'executive producer'; the rows after it open CREW; the
lead cast pair is the first 9.2 row; extras are the 9.2 row whose role is 'Extras';
the fellows split at ', AFI '.

Data gaps print as the data reads: 'SOUND DESIGNER | STILL UNKNOWN' at the top of CREW,
SOUND as two lines, 'JORDAN UWHUBETINE' in the fellows beside 'JORDAN BETINE' on the
credit pages, and '(c) COPYRIGHT MMXXV'. Nothing is sorted or deduplicated.

The full-bleed still, its opacity and horizontal anchor are the page's only picture
treatment: no scrim, no gradient (GROUND_RECIPE). Backdrops are derived at build time
in unletterbox() from press/assets/STILLS, which is never modified.

Two logo positions are reserved as labelled hairline slots. No AFI Conservatory logo
and no partner logo file exists on this machine; nothing is drawn in their place.

API used by tools/build-epk-kit.py and the two Illustrator replays: one_col_pages,
two_col_pages, page_thanks, build, load, field, pairs, condense, Sz, tracked, ground,
unletterbox and the constants W, H, M, CREAM, DIM, GROUND, RULE. All text goes through
tracked(), every rule through c.line, every backdrop through ground().
"""
import io, json, math, os, re, sys, tempfile

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
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
pdfmetrics.registerFont(TTFont("Bask-B", BASK, subfontIndex=1))
pdfmetrics.registerFont(TTFont("Bask-SB", BASK, subfontIndex=4))

CREAM = colors.HexColor("#efe6d6")
DIM = colors.HexColor("#b9a88c")
GROUND = colors.HexColor("#0b0806")
RULE = colors.HexColor("#6b5942")
WHITE = colors.HexColor("#ffffff")      # the reference's type colour; unused, one-constant swap

M = 74.0            # the EPK kit reads this for its own pages 1-8; the card's extents are below
M2 = 48.0           # CREW side margins (usable x 48..1248)

# ---------- ground: one still per page, drawn once, no scrim ----------
BACKDROP_MAX_PX = 1920          # native width of the stills; no upscaling occurs
BACKDROP_JPEG_Q = 90
P2_ALPHA = 0.60                 # drop to 0.50 for a lit-room projection; floor 0.45
P2_ALPHA_ENLARGED = 0.45        # --medium / --large: centred stacked type runs over the
                                # figure's head, which 0.60 leaves at p95 67-75 (gate limit 65)
P1 = (29, 1.0, 0.20)            # (still 1.1.N, alpha, horizontal anchor 0..1)
P2 = (27, P2_ALPHA, 0.50)
P2E = (27, P2_ALPHA_ENLARGED, 0.50)
P3 = (25, 0.45, 0.70)   # verify round 2: 0.50 put the lantern under the middle thanks column; 0.70 keeps it in the margin, 0.45 nearer the guide's brightness, gate 49.7 / limit 75
GROUND_RECIPE = {
    "ground": "#0b0806",
    "fit": "cover to page height; the page-shaped crop starts at x = (still_w * scale - W) * anchor; "
           "drawn once into the full page box (0, 0, W, H) with setFillAlpha(alpha)",
    "scrim": None,
    "gradient": None,
    "pages": {"CREDITS": {"still": P1[0], "alpha": P1[1], "anchor": P1[2]},
              "CREW": {"still": P2[0], "alpha": P2[1], "anchor": P2[2]},
              "THANKS": {"still": P3[0], "alpha": P3[1], "anchor": P3[2]}},
    "enlarged": {"still": P2E[0], "alpha": P2E[1], "anchor": P2E[2],
                 "note": "at s > 1.05 every page uses this, the CREW still at the enlarged alpha"},
    "overflow": "every overflow page of a section repeats its section's still",
    "backdrop_max_px": BACKDROP_MAX_PX,
    "backdrop_jpeg_q": BACKDROP_JPEG_Q,
}
BACKDROP_CACHE = os.path.join(tempfile.gettempdir(), "kom-card-backdrops")

# ---------- the type table at 1x (points) ----------
# size -> (role_room, pitch). Pitch ~1.65x: with the department gap at its true 2P (one
# blank slot) the 91-slot list on 17/26 stopped at baseline 1346, two-thirds down a page
# the reference fills to 1537; 17/28 ends at 1408 / 1436. The enlarged stacked column
# keeps its own 26s grid (Sz.crew_pitch) so its pagination does not move.
CREW_SIZES = {16: (260.0, 26.0), 17: (290.0, 28.0), 18: (275.0, 29.0)}
CREW_PITCH_STACKED = 26.0
HEAD_TRACK = 2.2                # --headings tracking: 0.13 em keeps the name one searchable word
BOILER_MEASURE = 1148.0         # the boilerplate's measure, x 74..1222 (inside the kit's 74 pt margin)

DRAW_TEXT = True                # False while the gate builds its ground-only twin
CONDENSED = []                  # every string condense() actually shrank
PAGES = []                      # section name per page drawn, for the gate
WORDS = []                      # (page index, word, centre x, baseline from top, size) of every
                                # UI word drawn, for the gate's positional search_for assert
SECTIONS = ("CREDITS", "CREW", "THANKS", "ENLARGED")


class Opts:
    """The flags. build(c, z, opts) reads them; Sz carries a copy for the page functions."""
    def __init__(self, headings=False, label_gold=False, crew_size=17, press=False,
                 ground_only=False, transparent=False, stills=None, proof_slug=False):
        self.headings, self.label_gold, self.crew_size = headings, label_gold, int(crew_size)
        self.press, self.ground_only, self.transparent = press, ground_only, transparent
        self.proof_slug = proof_slug            # the kit: a PROOF mark on CREW for what --press dropped
        self.stills = dict(stills or {})        # section -> (still n, alpha, anchor) overrides
        if self.crew_size not in CREW_SIZES:
            sys.exit(f"--crew-size must be one of {sorted(CREW_SIZES)}")
        for sec, tup in self.stills.items():
            if sec not in SECTIONS or len(tup) != 3 or not 0 <= tup[1] <= 1 or not 0 <= tup[2] <= 1:
                sys.exit(f"--still: expected SECTION=N,ALPHA,ANCHOR with SECTION in {SECTIONS}, "
                         f"ALPHA and ANCHOR in 0..1; got {sec}={tup}")

    @classmethod
    def from_argv(cls, argv):
        cs = int(argv[argv.index("--crew-size") + 1]) if "--crew-size" in argv else 17
        stills = {}
        for i, a in enumerate(argv):
            if a == "--still" and i + 1 < len(argv):
                sec, _, rest = argv[i + 1].partition("=")
                try:
                    n, alpha, anchor = rest.split(",")
                    stills[sec.upper()] = (int(n), float(alpha), float(anchor))
                except ValueError:
                    sys.exit(f"--still: cannot parse {argv[i + 1]!r}; want SECTION=N,ALPHA,ANCHOR")
        return cls("--headings" in argv, "--label-gold" in argv, cs, "--press" in argv,
                   "--ground-only" in argv, "--transparent" in argv, stills)


class Sz:
    """Every measurement derives from the scale, so one number moves the whole card."""
    def __init__(self, s, opts=None):
        self.s = s
        self.opts = opts or Opts()
        self.stacked = s > 1.05
        ts = min(s, 1.25)                       # titles never eat the column
        bs = min(s, 1.30)                       # boilerplate on its fixed 1160 measure
        # p1. Poster roles and names share ONE size, as the reference sets them (its
        # 'WRITTEN & DIRECTED BY' and 'RANA ROY' both measure cap ~18-19); the role's
        # slightly wider tracking is the only distinction besides position.
        self.title1 = ("Bask-B", 56 * ts, 2.0, CREAM)     # one size with CREW (2026-09-11)
        self.poster_role = ("Bask-B", 26 * s, 1.6, CREAM)
        self.poster_name = ("Bask-B", 26 * s, 1.2, CREAM)
        self.poster_pitch = 36 * s
        self.cast_label = ("Bask-B", 22 * s, 3.0, CREAM)
        self.lead_role = ("Bask-B", 30 * s, 1.4, CREAM)
        self.lead_name = ("Bask-B", 30 * s, 1.4, CREAM)
        self.cast_role = ("Bask-B", 20 * s, 1.3, CREAM)     # one tracking for both halves
        self.cast_name = ("Bask-B", 20 * s, 1.3, CREAM)     # of a cast row, as the reference
        self.cast_pitch = 28 * s
        # p2
        room, pitch = CREW_SIZES[self.opts.crew_size]
        self.title2 = ("Bask-B", 56 * ts, 2.0, CREAM)
        self.crew = ("Bask-B", self.opts.crew_size * s, 1.0, CREAM)
        self.crew_head = ("Bask-B", self.opts.crew_size * s, HEAD_TRACK, CREAM)
        self.crew_pitch = (CREW_PITCH_STACKED if self.stacked else pitch) * s
        self.role_room = room
        # p3. Letterspaced labels stay under ~0.13 em so they remain searchable words.
        self.body3 = ("Bask-B", 20 * s, 1.0, CREAM)
        self.boiler3 = ("Bask-B", 20 * bs, 1.0, CREAM)
        self.pitch3 = 28 * s
        self.boiler_pitch = 28 * bs
        self.extras_label = ("Bask-B", 18 * s, 2.3, CREAM)
        self.thanks_head = ("Bask-B", 26 * s, 2.0, CREAM)
        self.slot_partner = ("Bask", 13, 1.6, DIM)         # slots reserve real asset sizes:
        self.slot_afi = ("Bask", 11, 1.4, DIM)             # they do not scale
        self.continued = ("Bask", 12 * s, 1.5 * s, DIM)
        # legacy attributes the EPK kit reads for its own pages 1-8 (values unchanged)
        self.title = 40.0 * s
        self.role = 14.2 * s
        self.name = 15.6 * s
        self.lead = 21.0 * s
        self.track_t = 6.0 * s
        self.track_r = 1.35 * s
        self.track_n = 0.95 * s
        self.boiler = 11.4 * max(s * 0.8, 1.0)
        self.boiler_lead = 17.0 * max(s * 0.8, 1.0)

    def gold(self, st):
        """A wayfinding label: DIM under --label-gold, cream otherwise."""
        return (st[0], st[1], st[2], DIM) if self.opts.label_gold else st


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
    which is what keeps the fields' trailing caveats off the card. An upper-case line
    under 40 characters is a department heading: (None, 'CAMERA')."""
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


def split_at_ep(rows):
    """The poster block is 9.1 through the FIRST row whose role starts 'executive
    producer'; the rows after it open CREW. A rule on the field's order, never a name."""
    for i, (role, _) in enumerate(rows):
        if role and role.lower().startswith("executive producer"):
            return rows[:i + 1], rows[i + 1:]
    return rows, []


PRESS_DROPPED = []              # roles --press dropped, for the kit's PROOF mark on CREW


def press_filter(rows, opts):
    """--press drops rows whose name is exactly STILL UNKNOWN, audibly. Never silent."""
    if not opts.press:
        return rows
    kept = []
    for e in rows:
        if e[0] and [n.upper() for n in e[1]] == ["STILL UNKNOWN"]:
            print(f"--press: dropping '{e[0]} | {e[1][0]}'")
            if e[0] not in PRESS_DROPPED:
                PRESS_DROPPED.append(e[0])
            continue
        kept.append(e)
    return kept


def thanks_list(d):
    """(heading, [entries]) from 11.1: the first line is the heading as written; the
    name lines follow until the first prose line (ends with a period) or upper-case note."""
    lines = [l.strip() for l in field(d, "11.1").split("\n")]
    lines = [l for l in lines if l]
    heading, names = lines[0], []
    for line in lines[1:]:
        if line.endswith(".") or line.isupper():
            break
        names += [n.strip() for n in re.split(r"\s+·\s+", line) if n.strip()]
    return heading, names


def fellows_list(d):
    """[(name, 'AFI ... Fellow')] from 11.3, split at ', AFI ' at draw time."""
    out = []
    for l in field(d, "11.3").split("\n"):
        l = l.strip()
        if re.match(r"^[^|,]+, AFI .+ Fellow$", l):
            name, _, title = l.partition(", AFI ")
            out.append((name.strip(), "AFI " + title.strip()))
    return out


def boilerplate(d):
    """The four quoted items of 11.3 in field order, the two copyright lines, and a
    check that the '[AFI Conservatory logo]' marker follows. Quotes are extracted only
    between the BOILERPLATE line and the copyright line: the rest of the field quotes
    a typo and two names."""
    lines = [l.rstrip() for l in field(d, "11.3").split("\n")]
    ib = next(i for i, l in enumerate(lines) if l.strip().startswith("BOILERPLATE"))
    ic = next(i for i, l in enumerate(lines) if l.strip().startswith("©"))
    between = " ".join(l.strip() for l in lines[ib + 1:ic])
    items = [" ".join(q.split()) for q in re.findall(r'"([^"]+)"', between)]
    assert len(items) == 4, f"11.3: expected four quoted boilerplate items, found {len(items)}"
    copy = [lines[ic].strip(), lines[ic + 1].strip()]
    assert copy[1] and not copy[1].startswith("["), f"11.3: no line after the copyright line"
    assert lines[ic + 2].strip() == "[AFI Conservatory logo]", \
        f"11.3: expected '[AFI Conservatory logo]' after the copyright lines, got {lines[ic + 2]!r}"
    return items, copy


# ---------- drawing primitives ----------
def tracked(c, x, y, s, font, size, track, fill, align="left"):
    """Letterspacing lives on the text object, not the canvas. The only text primitive."""
    w = c.stringWidth(s, font, size) + track * max(len(s) - 1, 0)
    if not DRAW_TEXT:
        return w
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


def width(c, s, st):
    return c.stringWidth(s, st[0], st[1]) + st[2] * max(len(s) - 1, 0)


def put(c, x, ytop, s, st, align="left"):
    """Draw s with style st at a baseline measured from the TOP edge."""
    return tracked(c, x, H - ytop, s, st[0], st[1], st[2], st[3], align)


def ui_word(s, x, ytop, w, st, align="center"):
    """Note a UI word for the gate: where it was drawn, so search_for must hit THERE
    (a heading like SOUND also occurs inside credits elsewhere on the page)."""
    cx = x if align == "center" else x + w / 2.0 if align == "left" else x - w / 2.0
    WORDS.append((len(PAGES) - 1, s, cx, ytop, st[1]))


def hairline(c, x1, y1, x2, y2):
    """A slot edge: c.line only, never a stroked rect (the Illustrator replay records
    fill-only rects). Coordinates from the top edge."""
    if not DRAW_TEXT:
        return
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(x1, H - y1, x2, H - y2)


def condense(c, text, font, size, track, room):
    """Shrink a label until it fits its room. Clipping a name is not an option, and
    silently running past the margin is how the first --large render broke. At 1x the
    build asserts this was never needed; the enlarged modes may use it."""
    s0, t0 = size, track
    while size > 6 and c.stringWidth(text, font, size) + track * max(len(text) - 1, 0) > room:
        size -= 0.4
        track = max(track - 0.03, 0)
    if size != s0:
        CONDENSED.append((text, s0, size))
    return size, track


def unletterbox(path, anchor=0.5, save_to=None):
    """The stills carry their black bars in the pixels, so the picture rows are found
    and cropped out (detected, not hardcoded). The page-shaped crop is then taken at
    the horizontal anchor (0 = left edge of the frame, 1 = right), saved as a JPEG and
    returned as an ImageReader that carries, for the Illustrator replays:
        .path       the SOURCE still in press/assets/STILLS (never modified)
        .region     fractions (x0, y0, x1, y1) of the source that are shown
        .size       the source's pixel size
        ._kom_path  the derived JPEG on disk
    Drawn into the full page box (0, 0, W, H) it is a cover crop of the frame."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    src_w, src_h = im.size
    g = im.convert("L")
    rows = [y for y in range(src_h) if g.crop((0, y, src_w, y + 1)).getextrema()[1] > 8]
    r0, r1 = (rows[0], rows[-1] + 1) if rows and (rows[0] > 2 or rows[-1] < src_h - 3) else (0, src_h)
    im = im.crop((0, r0, src_w, r1))
    if im.width > BACKDROP_MAX_PX:
        im.thumbnail((BACKDROP_MAX_PX, BACKDROP_MAX_PX), Image.LANCZOS)
    f = im.width / src_w                        # 1.0 today: the stills are 1920 wide
    iw, ih = im.size
    sc = max(W / iw, H / ih)
    sw, sh = W / sc, H / sc                     # the shown region, in derived pixels
    x0 = (iw - sw) * anchor
    y0 = (ih - sh) * 0.5
    box = (int(round(x0)), int(round(y0)), int(round(x0 + sw)), int(round(y0 + sh)))
    crop = im.crop(box)
    if save_to is None:
        os.makedirs(BACKDROP_CACHE, exist_ok=True)
        st = os.stat(path)
        save_to = os.path.join(BACKDROP_CACHE, "%s_a%.3f_%d_q%d_%d_%d.jpg" % (
            os.path.splitext(os.path.basename(path))[0], anchor, BACKDROP_MAX_PX,
            BACKDROP_JPEG_Q, st.st_size, int(st.st_mtime)))
    if not os.path.exists(save_to):
        crop.save(save_to, "JPEG", quality=BACKDROP_JPEG_Q, optimize=True)
    img = ImageReader(save_to)
    img.path = os.path.abspath(path)
    img.region = (box[0] / f / src_w, (r0 + box[1] / f) / src_h,
                  box[2] / f / src_w, (r0 + box[3] / f) / src_h)
    img.size = (src_w, src_h)
    img._kom_path = save_to
    return img


_LEGACY_NOTICED = set()


def with_recipe(still, recipe):
    """What a page draws behind itself. A (path, alpha, anchor) tuple is used as given.
    A BARE PATH is a legacy iterator (the EPK kit's credit_pages still yields the bright
    frames it picked for the old 0.16-under-0.55 ghost recipe): drawn at this design's
    alpha those frames swallow the type, so the page draws its own recipe's still
    instead and says so once. To override a page's still, pass the tuple."""
    if still is None or isinstance(still, tuple):
        return still
    own = pick_still(recipe[0])
    if still not in _LEGACY_NOTICED:
        _LEGACY_NOTICED.add(still)
        print(f"  ground: caller passed a bare still path ({os.path.basename(still)}); the "
              f"redesigned page draws its own 1.1.{recipe[0]} at alpha {recipe[1]} anchor "
              f"{recipe[2]} instead. Pass (path, alpha, anchor) to override.")
    return (own, recipe[1], recipe[2]) if own else None


def pick_still(n):
    """press/assets/STILLS/...1.1.<n>.png, or None when the folder is absent."""
    if not os.path.isdir(BG):
        return None
    for st in sorted(os.listdir(BG)):
        if st.endswith(f"1.1.{n}.png"):
            return os.path.join(BG, st)
    return None


def ground(c, still=None, transparent=False):
    """The ground rect, then the still ONCE at its alpha and anchor. No scrim, no
    gradient. transparent=True draws nothing, so the page keeps its alpha. `still` is
    None, a path, or (path, alpha, anchor)."""
    if transparent:
        return
    c.setFillColor(GROUND)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    if still is None:
        return
    if isinstance(still, tuple):
        path, alpha, anchor = still
    else:
        path, alpha, anchor = still, 1.0, 0.5
    if not path or not os.path.exists(path):
        return
    img = unletterbox(path, anchor=anchor)
    c.saveState()
    c.setFillAlpha(alpha)
    c.drawImage(img, 0, 0, W, H, mask="auto")
    c.restoreState()


# ---------- wrapping guards (uniform size first; condense() is the last resort) ----------
def amp_wrap(c, text, st, measure):
    """A line wider than its measure breaks before its LAST ' & ' so line two begins
    '& ' (the reference's 'VALERIE, PHYLLIS, ROGER,' / '& MARION IVEY'); a line with no
    ' & ' breaks at its last space."""
    if width(c, text, st) <= measure:
        return [text]
    i = text.rfind(" & ")
    if i > 0:
        return [text[:i], "& " + text[i + 3:]]
    j = text.rfind(" ")
    if j > 0:
        return [text[:j], text[j + 1:]]
    return [text]


def role_wrap(c, label, st, room):
    """A CREW role label wider than its room breaks at the word boundary that minimises
    the longer line. Returns one or two lines."""
    if width(c, label, st) <= room:
        return [label]
    words = label.split()
    best = None
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        m = max(width(c, a, st), width(c, b, st))
        if best is None or m < best[0]:
            best = (m, [a, b])
    return best[1] if best else [label]


def greedy_wrap(c, text, st, measure):
    """Words packed by tracked width; for the boilerplate. A last line under three
    words narrows the measure a notch (1160 -> 1120 -> 1080) rather than leaving one
    word alone, as long as that costs no extra line."""
    def pack(m):
        lines, cur = [], ""
        for w in text.split():
            t = (cur + " " + w).strip()
            if cur and width(c, t, st) > m:
                lines.append(cur)
                cur = w
            else:
                cur = t
        if cur:
            lines.append(cur)
        return lines
    first = pack(measure)
    for m in (measure, measure - 40, measure - 80):
        lines = pack(m)
        if len(lines) == len(first) and len(lines[-1].split()) >= 3:
            return lines
    return first


def step_down(c, block, st, floor=16.0):
    """BLOCK STEP-DOWN: if any (text, room) in block still exceeds its room, the whole
    block drops 1 pt uniformly (floor 16) and the build says which entry forced it."""
    font, size, track, fill = st
    s0, why = size, None
    while size > floor:
        over = [t for t, room in block if width(c, t, (font, size, track, fill)) > room]
        if not over:
            break
        why = why or over[0]
        size -= 1.0
    if size != s0:
        print(f"  step-down: '{why}' does not fit its column; block {s0:.0f} -> {size:.0f} pt")
    return (font, size, track, fill)


# ---------- the line engine (pages 1 and 3, and every enlarged page) ----------
# a line is (segments, pitch_after); a segment is ("text", s, style, x, align) or
# ("rule", x1, x2); a block is (gap_before, lines, keep_with_next)
def paginate(blocks, top, bottom):
    """Blocks are atomic. A gap is dropped at the top of a page. A keep_with_next block
    (a heading, or a column row that begins a two-line entry) moves with the block after
    it; a run of them moves together. `top` is one number, or (first page, later pages)
    so a CONTINUED tag has room above the later pages' first line."""
    top1, topn = top if isinstance(top, tuple) else (top, top)
    pages, cur, y = [], [], top1

    def height(lines):
        return sum(p for _, p in lines[:-1])
    for gap, lines, keep in blocks:
        if cur:
            y += gap
        if cur and y + height(lines) > bottom:
            carried = []
            while cur and cur[-1][2]:                   # an orphaned heading / open entry
                carried.insert(0, cur.pop())
            if not cur:                                 # the page held only keep blocks
                cur, carried = carried, []
            pages.append(cur)
            cur, y = [], topn
            for _, hl, hk in carried:
                cur.append((y, hl, hk))
                y += sum(p for _, p in hl)
        cur.append((y, lines, keep))
        y += sum(p for _, p in lines)
    if cur:
        pages.append(cur)
    return pages


def draw_page_lines(c, page):
    for y0, lines, _ in page:
        y = y0
        for segs, pitch in lines:
            for seg in segs:
                if seg[0] == "text":
                    _, s, st, x, align, ui = seg
                    w = put(c, x, y, s, st, align)
                    if ui:
                        ui_word(s, x, y, w, st, align)
                elif seg[0] == "rule":
                    _, x1, x2 = seg
                    hairline(c, x1, y, x2, y)
            y += pitch


def T(s, st, x, align="left", ui=False):
    """A text segment. ui=True marks a hardcoded UI word or a wayfinding label whose
    searchability the gate asserts."""
    return ("text", s, st, x, align, ui)


def continued(c, z, y):
    w = put(c, W / 2, y, "CONTINUED", z.continued, "center")
    ui_word("CONTINUED", W / 2, y, w, z.continued)


# ---------- page 1: CREDITS ----------
P1_TITLE_Y, P1_X, P1_MEASURE, P1_FIRST = 134.0, 340.0, 560.0, 200.0
P1_AXIS, P1_GUTTER, P1_MAX_X, P1_BOTTOM = 370.0, 24.0, 800.0, 1624.0


def one_col_pages(c, title, groups, z, stills, transparent):
    """The CREDITS page: the poster block (9.1 through the executive producers) stacked
    and centred on x=340, then the cast pairs under the CAST label. `title` is the label
    over the cast pairs (the kit passes 'C A S T'; spaces are collapsed). `groups` is a
    list of entry-lists: the group holding a row whose role starts 'executive producer'
    is the key-credits group (its rows after that one belong to CREW and are not drawn
    here); the other groups' rows are the cast, except an 'Extras' row, which page_thanks
    draws. Enlarged: centred on the page, cast stacked role over name, paginated."""
    label = title.replace(" ", "")
    poster, cast = [], []
    for g in groups:
        if any(r and r.lower().startswith("executive producer") for r, _ in g):
            poster, _ = split_at_ep([e for e in g if e[0]])
        else:
            cast += [e for e in g if e[0] and e[0].lower() != "extras"]
    poster = press_filter(poster, z.opts)
    s = z.s
    cx = W / 2 if z.stacked else P1_X
    measure = 1100.0 if z.stacked else P1_MEASURE
    blocks = []
    # the poster block: role, then one line per name, one blank pitch between blocks
    for i, (role, names) in enumerate(poster):
        lines = [([T(role.upper(), z.poster_role, cx, "center")], z.poster_pitch)]
        for n in names:
            for ln in amp_wrap(c, n.upper(), z.poster_name, measure):
                if width(c, ln, z.poster_name) > measure:
                    print(f"  WARNING p1: '{ln}' exceeds the {measure:.0f} measure")
                lines.append(([T(ln, z.poster_name, cx, "center")], z.poster_pitch))
        blocks.append((z.poster_pitch, lines, False))
    # the CAST label, 84 below the last poster line at 1x
    blocks.append((84 * s - z.poster_pitch, [([T(label, z.gold(z.cast_label), cx, "center", ui=True)],
                                             64 * s)], True))
    for i, (role, names) in enumerate(cast):
        r_st, n_st = (z.lead_role, z.lead_name) if i == 0 else (z.cast_role, z.cast_name)
        if z.stacked:
            pitch = z.cast_pitch * (1.5 if i == 0 else 1.0)    # the lead's 1.5x type
            lines = [([T(role.upper(), r_st, cx, "center")], pitch)]
            lines += [([T(n.upper(), n_st, cx, "center")], pitch) for n in names]
            blocks.append((z.cast_pitch if i else 0, lines, False))
        else:
            segs = [T(role.upper(), r_st, P1_AXIS, "right")]
            segs.append(T(" · ".join(names).upper(), n_st, P1_AXIS + P1_GUTTER, "left"))
            blocks.append((0, [(segs, 36.0 if i == 0 else z.cast_pitch)], False))
    top = P1_FIRST if not z.stacked else P1_TITLE_Y * min(s, 1.25) + 66 * s
    pages = paginate(blocks, top, P1_BOTTOM)
    if not z.stacked:
        assert len(pages) == 1, f"CREDITS overflowed one page at 1x ({len(pages)})"
    ty = P1_TITLE_Y * min(s, 1.25)
    for i, page in enumerate(pages):
        ground(c, with_recipe(next(stills), P2E if z.stacked else P1), transparent)
        PAGES.append("CREDITS")
        w = put(c, cx, ty, "CREDITS", z.title1, "center")
        ui_word("CREDITS", cx, ty, w, z.title1)
        if i:
            continued(c, z, ty + 30 * s)
        draw_page_lines(c, page)
        c.showPage()
    last = pages[-1][-1][0] + sum(p for _, p in pages[-1][-1][1][:-1])
    print(f"CREDITS: {len(poster)} poster rows, {len(cast)} cast rows, "
          f"{len(pages)} page(s), last baseline {last:.0f}")


# ---------- page 2: CREW ----------
P2_TITLE_Y, P2_FIRST, G, PG = 117.0, 176.0, 24.0, 22.0


def crew_sequence(c, entries, z):
    """entries -> [('entry', role_lines, name_lines) | ('gap', heading)] with the
    department headings converted to gaps: one blank slot (baseline to baseline 2P, the
    reference's one blank line), or one blank slot plus the heading line under
    --headings. A wrapped role keeps its name on the first line; names never wrap."""
    st = z.crew
    seq = []
    for role, names in entries:
        if role is None:
            seq.append(("gap", names))
            continue
        seq.append(("entry", role_wrap(c, role.upper(), st, z.role_room),
                    [n.upper() for n in names]))
    return seq


def slots(item, headings=False):
    """Grid slots an item occupies: a gap is ONE blank slot (2P baseline to baseline),
    two under --headings when it carries a heading (blank, then the heading line)."""
    if item[0] == "gap":
        return 2 if headings and item[1] else 1
    if item[0] == "head":
        return 1
    return max(len(item[1]), len(item[2]))


def balance_slots(seq, headings):
    """Split by slot count: the left column takes items until adding half the next one
    would pass total/2. Trailing gaps leave the left column; a leading gap on the right
    is dropped (its heading survives as a one-slot line under --headings)."""
    h = [slots(i, headings) for i in seq]
    total = sum(h)
    left, run = [], 0
    for i, item in enumerate(seq):
        if run + h[i] / 2 > total / 2:
            break
        left.append(item)
        run += h[i]
    right = seq[len(left):]
    while left and left[-1][0] == "gap":
        right.insert(0, left.pop())
    while right and right[0][0] == "gap":
        g = right.pop(0)
        if headings and g[1]:
            right.insert(0, ("head", g[1]))
            break
    return left, right


def two_col_pages(c, title, entries, z, stills, transparent):
    """The CREW page: two role | name pairs on one slot grid, departments separated by
    one blank slot (2P = 56 at 17 pt, the reference's one blank line), headings only
    under --headings (then blank + heading line). If `entries` begins with a
    department heading (the kit passes 10.1 alone) the 9.1 rows after the executive
    producers are fetched and put first, as the reference opens with UPM / 1st AD /
    2nd AD. Enlarged: one centred stacked column, paginated: entries are role over
    name with one blank pitch between entries and two between departments."""
    title = title.replace(" ", "")
    if entries and entries[0][0] is None:
        _, tail = split_at_ep(pairs(field(load(), "9.1")))
        entries = tail + list(entries)
    # A row that is an exact role-and-names copy of an earlier row is printed once, on both
    # paths (the kit's fetch above and the card's pre-joined list), audibly; nothing is
    # sorted or deduplicated by inference (taste pass 2026-09-11, C10.3 as amended).
    seen, once = [], []
    for e in entries:
        k = (e[0], list(e[1])) if e[0] else None
        if k is not None and k in seen:
            print(f"  CREW: '{e[0]} | {' · '.join(e[1])}' listed twice in the data; printed once")
            continue
        if k is not None:
            seen.append(k)
        once.append(e)
    entries = press_filter(once, z.opts)
    s, opts = z.s, z.opts
    ty = P2_TITLE_Y * min(s, 1.25)

    if z.stacked:
        P = z.crew_pitch
        blocks, prev_head = [], False
        for role, names in entries:
            if role is None:
                if opts.headings:
                    blocks.append((2 * P, [([T(names, z.crew_head, W / 2, "center", ui=True)], P)], True))
                    prev_head = True
                else:
                    prev_head = "gap"
                continue
            gap = 0 if prev_head is True else 2 * P if prev_head == "gap" else P
            lines = [([T(role.upper(), z.crew, W / 2, "center")], P)]
            for n in names:
                u = n.upper()
                sz, tr = condense(c, u, z.crew[0], z.crew[1], z.crew[2], W - 2 * M)
                lines.append(([T(u, (z.crew[0], sz, tr, z.crew[3]), W / 2, "center")], P))
            blocks.append((gap, lines, False))
            prev_head = False
        pages = paginate(blocks, ty + 66 * s, P1_BOTTOM)
        for i, page in enumerate(pages):
            ground(c, with_recipe(next(stills), P2E), transparent)
            PAGES.append("CREW")
            w = put(c, W / 2, ty, title, z.title2, "center")
            ui_word(title, W / 2, ty, w, z.title2)
            if i:
                continued(c, z, ty + 30 * s)
            draw_page_lines(c, page)
            c.showPage()
        print(f"CREW: {len(pages)} page(s) stacked at {z.crew[1]:.1f} pt")
        return

    # 1x: the four-column form, with a fallback cascade if the assembly cannot fit
    cascade = [(opts.crew_size, z.role_room, z.crew_pitch), (opts.crew_size, 275.0, z.crew_pitch),
               (16, 260.0, 24.0)]
    for size, room, P in cascade:
        z.crew = ("Bask-B", float(size), 1.0, CREAM)
        z.crew_head = ("Bask-B", float(size), HEAD_TRACK, CREAM)
        z.role_room, z.crew_pitch = room, P
        seq = crew_sequence(c, entries, z)
        left, right = balance_slots(seq, opts.headings)
        nameW = []
        for col in (left, right):
            nameW.append(max([width(c, n, z.crew) for it in col if it[0] == "entry" for n in it[2]] or [0]))
        axis_L = M2 + room
        names_L = axis_L + G
        pair_R = names_L + nameW[0] + PG
        axis_R = pair_R + room
        names_R = axis_R + G
        right_edge = names_R + nameW[1]
        wraps = [it[1] for it in seq if it[0] == "entry" and len(it[1]) > 1]
        if right_edge <= W - M2:
            break
        print(f"  CREW: right edge {right_edge:.0f} > {W - M2:.0f} at {size} pt / room {room:.0f}; cascading")
    else:
        sys.exit(f"CREW: the four-column assembly does not fit even at 16 pt / room 260 ({right_edge:.0f})")
    shift = (W - M2 - right_edge) / 2
    axis_L, names_L, axis_R, names_R = (v + shift for v in (axis_L, names_L, axis_R, names_R))
    nL, nR = sum(slots(i, opts.headings) for i in left), sum(slots(i, opts.headings) for i in right)
    ngap = sum(1 for i in seq if i[0] == "gap")
    print(f"CREW: {z.crew[1]:.0f} pt on pitch {P:.0f} (department gap {2 * P:.0f} = 2P"
          f"{', heading in the second slot' if opts.headings else ''}), role room {room:.0f}; "
          f"{len(wraps)} wrapped roles: " + "; ".join(" | ".join(w) for w in wraps))
    print(f"      slots L {nL} / R {nR} (total {nL + nR}, {ngap} gaps); names widest L {nameW[0]:.0f} R {nameW[1]:.0f}; "
          f"axes L {axis_L:.0f}/{names_L:.0f} R {axis_R:.0f}/{names_R:.0f}; right edge {right_edge + shift:.0f}")
    print(f"      columns end at baselines {P2_FIRST + (nL - 1) * P:.0f} / {P2_FIRST + (nR - 1) * P:.0f}")
    assert P2_FIRST + (max(nL, nR) - 1) * P <= 1658, "CREW column runs past the foot"

    # the same-row clearance check: a left name against the right pair's role ink
    def rows(col, axis, names_x):
        out = {}
        k = 0
        for it in col:
            if it[0] == "gap":
                if opts.headings and it[1]:
                    out[k + 1] = [("head", it[1])]     # blank slot, then the heading
                k += slots(it, opts.headings)
            elif it[0] == "head":
                out[k] = [("head", it[1])]
                k += 1
            else:
                for j, rl in enumerate(it[1]):
                    out.setdefault(k + j, []).append(("role", rl))
                for j, nm in enumerate(it[2]):
                    out.setdefault(k + j, []).append(("name", nm))
                k += slots(it, opts.headings)
        return out
    L, R = rows(left, axis_L, names_L), rows(right, axis_R, names_R)
    for k, segs in L.items():
        ln = [s_ for kind, s_ in segs if kind == "name"]
        rr = [s_ for kind, s_ in R.get(k, []) if kind == "role"]
        if ln and rr:
            l_edge = names_L + width(c, ln[0], z.crew)
            r_ink = axis_R - width(c, rr[0], z.crew)
            if l_edge + 16 > r_ink:
                sys.exit(f"CREW: '{ln[0]}' ({l_edge:.0f}) collides with '{rr[0]}' ({r_ink:.0f}) on row {k}")

    ground(c, with_recipe(next(stills), P2), transparent)
    PAGES.append("CREW")
    w = put(c, W / 2, ty, title, z.title2, "center")
    ui_word(title, W / 2, ty, w, z.title2)
    for col, axis, names_x in ((L, axis_L, names_L), (R, axis_R, names_R)):
        for k, segs in col.items():
            y = P2_FIRST + k * P
            for kind, s_ in segs:
                if kind == "role":
                    put(c, axis, y, s_, z.crew, "right")
                elif kind == "name":
                    # a data gap keeps its slot but reads as a query, in the card's own
                    # not-yet colour (the slot labels, the CONTINUED tag) (C10.2)
                    st = (z.crew[0], z.crew[1], z.crew[2], DIM) if s_.upper() == "STILL UNKNOWN" else z.crew
                    put(c, names_x, y, s_, st, "left")
                else:
                    w = put(c, axis + G / 2, y, s_, z.crew_head, "center")
                    ui_word(s_, axis + G / 2, y, w, z.crew_head)
    if opts.proof_slug and PRESS_DROPPED:
        # provenance is data, never copy: the dropped row surfaces as the kit's one proof
        # class (9.5 pt DIM on the 33 pt mark line), as on pages 2, 5 and 7
        tracked(c, W / 2, M * 0.45, "PROOF — " + " · ".join(f"{r.upper()} NOT YET NAMED" for r in PRESS_DROPPED),
                "Bask", 9.5, 1.4, DIM, "center")
    c.showPage()


# ---------- page 3: THANKS + AFI ----------
P3_LABEL_Y, P3_BOTTOM = 96.0, 1560.0
COLS3 = ((400.0, "right", 340.0), (648.0, "center", 480.0), (896.0, "left", 340.0))
COLS2 = ((628.0, "right", 560.0), (668.0, "left", 560.0))
COLS1 = ((648.0, "center", 1100.0),)
BAND_X = (90.0, 1206.0)
AFI_BOX = (538.0, 1602.0, 758.0, 1658.0)        # x0, y0, x1, y1 from the top; 220 x 56
AFI_GAP = 90.0                                  # air between the copyright baseline and the slot
AFI_SLACK = 200.0                               # more than this above the slot pushes the legal block down


def columns_for(z):
    return COLS3 if not z.stacked else COLS2 if z.s <= 1.5 else COLS1


def fill_columns(items, ncol):
    """items: [(lines)] -> column lists, filled sequentially by LINE count toward
    ceil(total/ncol); an item is never split across columns."""
    total = sum(len(i) for i in items)
    target = math.ceil(total / ncol)
    cols, cur, run = [], [], 0
    for it in items:
        if len(cols) < ncol - 1 and cur and run + len(it) > target:
            cols.append(cur)
            cur, run = [], 0
        cur.append(it)
        run += len(it)
    cols.append(cur)
    while len(cols) < ncol:
        cols.append([])
    return cols


def column_block(c, items, cols, st, pitch, gap_before):
    """Mirrored columns of one-or-two-line items on a shared pitch, returned as ONE
    BLOCK PER ROW so the enlarged modes may break the columns across pages; a row that
    begins a two-line entry in any column is keep-with-next, so a '&'-wrapped entry
    never splits. Steps the block down if an item that cannot wrap exceeds its room."""
    filled = fill_columns(items, len(cols))
    checks = []
    for col, (x, align, room) in zip(filled, cols):
        for it in col:
            for ln in it:
                checks.append((ln, room))
    st = step_down(c, checks, st)
    flats = [[(ln, j < len(it) - 1) for it in col for j, ln in enumerate(it)] for col in filled]
    depth = max([len(f) for f in flats] or [0])
    blocks = []
    for r in range(depth):
        segs, keep = [], False
        for flat, (x, align, room) in zip(flats, cols):
            if r < len(flat):
                segs.append(T(flat[r][0], st, x, align))
                keep = keep or flat[r][1]
        blocks.append((gap_before if r == 0 else 0, [(segs, pitch)], keep))
    return blocks


def page_thanks(c, d, z, stills, transparent):
    """Extras band, thanks, PARTNER LOGOS slot, Avid, boilerplate, fellows, copyright,
    AFI CONSERVATORY LOGO slot: the reference's p11 order with our extras in its
    overflow position. Everything from d (9.2, 11.1, 11.3)."""
    s = z.s
    cols = columns_for(z)
    pitch = z.pitch3
    extras = [e for e in pairs(field(d, "9.2")) if e[0] and e[0].lower() == "extras"]
    heading, thanks = thanks_list(d)
    fellows = fellows_list(d)
    items, copy = boilerplate(d)
    blocks = []
    # (1) the extras band: the label keeps with the first row; rows may break across
    # pages in the enlarged modes only (at 1x the page asserts it holds everything)
    if extras:
        role, names = extras[0]
        blocks.append((0, [([T(role.upper(), z.gold(z.extras_label), W / 2, "center", ui=True)], 40 * s)], True))
        blocks += column_block(c, [[n.upper()] for n in names], cols, z.body3, pitch, 0)
    # (2) the heading as 11.1 writes it, (3) the thanks in data order, '&'-wrapped
    blocks.append((76 * s - pitch, [([T(heading.upper(), z.gold(z.thanks_head), W / 2, "center", ui=True)],
                                    56 * s)], True))
    wrap_at = 350.0 if len(cols) == 3 else cols[0][2]
    entries = [amp_wrap(c, n.upper(), z.body3, wrap_at) for n in thanks]
    blocks += column_block(c, entries, cols, z.body3, pitch, 0)
    nwrap = sum(1 for e in entries if len(e) > 1)
    # (4)-(8): one atomic block from the PARTNER LOGOS band to the copyright, so they
    # always share a page with each other and with the AFI slot. On the 28 grid:
    # paragraph gaps 56 (2P), boilerplate -> fellows 84 (3P), fellows -> copyright
    # 112 (4P); the copyright then sits AFI_GAP above the slot at 1x.
    bp = z.boiler_pitch
    # The PARTNER LOGOS band is drawn only when 11.2 holds logos to place; an empty field
    # earns no 148 pt of rules on the end card (C10.4). The AFI box below is unconditional.
    tail = []
    if field(d, "11.2").strip():
        tail = [([("rule",) + BAND_X], 49.0),
                ([T("PARTNER LOGOS", z.slot_partner, W / 2, "center", ui=True)], 41.0),
                ([("rule",) + BAND_X], 58 * min(s, 1.3))]
    tail.append(([T(items[3].upper(), z.boiler3, W / 2, "center")], 56 * min(s, 1.3)))
    for k, para in enumerate(items[:3]):
        ls = greedy_wrap(c, para.upper(), z.boiler3, BOILER_MEASURE)
        for j, ln in enumerate(ls):
            tail.append(([T(ln, z.boiler3, W / 2, "center")],
                         bp if j < len(ls) - 1 else (56 * min(s, 1.3) if k < 2 else 84 * s)))
    gutter = 16 * s
    fst = step_down(c, [(n.upper(), W / 2 - gutter - M) for n, _ in fellows]
                    + [(t.upper(), W / 2 - gutter - M) for _, t in fellows], z.body3)
    for j, (name, ttl) in enumerate(fellows):
        tail.append(([T(name.upper(), fst, W / 2 - gutter, "right"),
                      T(ttl.upper(), fst, W / 2 + gutter, "left")],
                     pitch if j < len(fellows) - 1 else 112 * s))
    tail.append(([T(copy[0].upper(), z.body3, W / 2, "center")], pitch))
    tail.append(([T(copy[1].upper(), z.body3, W / 2, "center")], pitch))
    blocks.append((60 * s - pitch, tail, False))
    # later pages of an enlarged stack open lower, under a CONTINUED tag at baseline 40
    top = P3_LABEL_Y if not z.stacked else (P3_LABEL_Y, P3_LABEL_Y + 30 * s)
    pages = paginate(blocks, top, P3_BOTTOM)
    if not z.stacked:
        assert len(pages) == 1, f"THANKS overflowed one page at 1x ({len(pages)})"
    # the AFI slot is a foot anchor: if the legal block ends more than AFI_SLACK above
    # it (an enlarged stack whose last page holds the block alone), the block moves
    # down so the copyright sits AFI_GAP above the slot, as the reference's stack runs
    # continuous to its mark
    y0, tl, _ = pages[-1][-1]
    copyright_y = y0 + sum(p for _, p in tl[:-1])
    slack = AFI_BOX[1] - copyright_y
    if slack > AFI_SLACK:
        pages[-1][-1] = (y0 + slack - AFI_GAP, tl, False)
        print(f"  THANKS: legal block pushed down {slack - AFI_GAP:.0f} so the copyright sits "
              f"{AFI_GAP:.0f} above the AFI slot (it ended {slack:.0f} above it)")
    for i, page in enumerate(pages):
        ground(c, with_recipe(next(stills), P2E if z.stacked else P3), transparent)
        PAGES.append("THANKS")
        is_last = i == len(pages) - 1
        if i and not (is_last and len(page) == 1):
            continued(c, z, 40.0)
        draw_page_lines(c, page)
        if is_last:
            x0, y0, x1, y1 = AFI_BOX
            hairline(c, x0, y0, x1, y0)
            hairline(c, x0, y1, x1, y1)
            hairline(c, x0, y0, x0, y1)
            hairline(c, x1, y0, x1, y1)
            w = put(c, (x0 + x1) / 2, y0 + 32, "AFI CONSERVATORY LOGO", z.slot_afi, "center")
            ui_word("AFI CONSERVATORY LOGO", (x0 + x1) / 2, y0 + 32, w, z.slot_afi)
        c.showPage()
    last = pages[-1][-1][0] + sum(p for _, p in pages[-1][-1][1][:-1])
    print(f"THANKS: {len(extras[0][1]) if extras else 0} extras, {len(thanks)} thanks entries "
          f"({nwrap} '&'-wrapped), {len(fellows)} fellows, {len(pages)} page(s); "
          f"copyright baseline {last:.0f}, AFI slot at {AFI_BOX[1]:.0f}..{AFI_BOX[3]:.0f}")


# ---------- the whole card ----------
def build(c, z, opts=None):
    """Draw every page of the card on canvas c (a reportlab canvas or a recorder that
    mimics its primitives). The one entry point both builders and the Illustrator replay
    call."""
    if opts is not None:
        z.opts = opts
    opts = z.opts
    del PAGES[:]
    del CONDENSED[:]
    del WORDS[:]
    d = load()

    # the per-page recipes, with any --still override written into GROUND_RECIPE too
    recipes = {"CREDITS": P1, "CREW": P2, "THANKS": P3, "ENLARGED": P2E}
    for sec, tup in opts.stills.items():
        recipes[sec] = tup
        entry = {"still": tup[0], "alpha": tup[1], "anchor": tup[2]}
        if sec == "ENLARGED":
            GROUND_RECIPE["enlarged"].update(entry)
        else:
            GROUND_RECIPE["pages"][sec] = entry
        print(f"  --still {sec}: 1.1.{tup[0]} at alpha {tup[1]} anchor {tup[2]} (override)")

    def stills_for(sec):
        n, alpha, anchor = recipes["ENLARGED"] if z.stacked else recipes[sec]
        path = pick_still(n)
        while True:
            yield (path, alpha, anchor) if path else None

    key = pairs(field(d, "9.1"))
    billed = pairs(field(d, "9.2"))
    crew = pairs(field(d, "10.1"))
    poster, tail = split_at_ep(key)
    cast = [e for e in billed if e[0] and e[0].lower() != "extras"]
    one_col_pages(c, "CAST", [cast, poster], z, stills_for("CREDITS"), opts.transparent)
    two_col_pages(c, "CREW", tail + crew, z, stills_for("CREW"), opts.transparent)
    page_thanks(c, d, z, stills_for("THANKS"), opts.transparent)
    return list(PAGES)


# ---------- the legibility gate ----------
GATE_P95 = {"CREDITS": 60, "CREW": 65, "THANKS": 75}


GATE_WINDOW = 300.0             # pt: a wide span is judged by its worst 300 pt window, not its mean


def gate(pdf, pdf_ground, sections, z, words=(), dpi=200):
    """Measure the ground under every span. FAIL if a cream span's window mean > 85 (a
    span wider than GATE_WINDOW is judged by the worst GATE_WINDOW-wide window slid
    across it), a page's p95 over its cream spans exceeds its threshold, or a DIM
    span's mean > 30. Structural asserts ride along, including that every UI word in
    `words` [(page index, word)] is found by page.search_for() on its page, i.e. the
    letterspacing left it a word. Returns a report string; exits non-zero on failure."""
    import numpy as np
    import pymupdf
    doc, gnd = pymupdf.open(pdf), pymupdf.open(pdf_ground)
    assert len(doc) == len(gnd), "gate: page counts differ"
    k = dpi / 72.0
    wpx = int(GATE_WINDOW * k)
    fails, lines = [], []
    cream_hex, dim_hex = 0xefe6d6, 0xb9a88c
    chars, max_x1, max_base = 0, 0.0, 0.0
    for pi, (page, gp) in enumerate(zip(doc, gnd)):
        pm = gp.get_pixmap(dpi=dpi, alpha=False)
        arr = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width, pm.n)[:, :, :3]
        lum = (0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2])
        worst, worst_s, union = 0.0, "", []
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    txt = sp["text"]
                    if not txt.strip():
                        continue
                    chars += len(txt)
                    x0, y0, x1, y1 = sp["bbox"]
                    max_x1 = max(max_x1, x1)
                    max_base = max(max_base, sp["origin"][1])
                    if not z.stacked and pi == 0 and x1 > P1_MAX_X + 0.5:
                        fails.append(f"p1: '{txt}' reaches x={x1:.0f} > {P1_MAX_X:.0f}")
                    if x1 > 1246:
                        fails.append(f"p{pi + 1}: '{txt}' reaches x={x1:.0f} > 1246")
                    if sp["origin"][1] > 1658:
                        fails.append(f"p{pi + 1}: '{txt}' baseline {sp['origin'][1]:.0f} > 1658")
                    px0, py0 = int((x0 - 2) * k), int((y0 - 2) * k)
                    px1, py1 = int(math.ceil((x1 + 2) * k)), int(math.ceil((y1 + 2) * k))
                    win = lum[max(py0, 0):py1, max(px0, 0):px1]
                    if win.size == 0:
                        continue
                    if win.shape[1] > wpx:              # slide a GATE_WINDOW across a wide span
                        cs = np.concatenate([[0.0], np.cumsum(win.mean(axis=0))])
                        mean = float(((cs[wpx:] - cs[:-wpx]) / wpx).max())
                    else:
                        mean = float(win.mean())
                    if sp["color"] == dim_hex:
                        if mean > 30:
                            fails.append(f"p{pi + 1}: DIM '{txt}' on a bed of {mean:.0f} > 30")
                    else:
                        union.append(win.ravel())
                        if mean > worst:
                            worst, worst_s = mean, txt
                        if mean > 85:
                            fails.append(f"p{pi + 1}: '{txt}' window mean {mean:.0f} > 85")
        sec = sections[pi] if pi < len(sections) else "CREW"
        thr = 65 if z.stacked else GATE_P95[sec]
        p95 = float(np.percentile(np.concatenate(union), 95)) if union else 0.0
        if p95 > thr:
            fails.append(f"p{pi + 1} ({sec}): p95 {p95:.0f} > {thr}")
        lines.append(f"  p{pi + 1} {sec:7s} worst window {worst:5.1f} ('{worst_s}')  p95 {p95:5.1f} (limit {thr})")
    found, seen = 0, set()
    for pi, word, cx, yb, size in words:
        key = (pi, word, round(cx), round(yb))
        if key in seen:
            continue
        seen.add(key)
        py = yb - 0.3 * size                        # a point inside the caps, from the top
        hits = doc[pi].search_for(word) if pi < len(doc) else []
        if any(r.x0 - 1 <= cx <= r.x1 + 1 and r.y0 - 1 <= py <= r.y1 + 1 for r in hits):
            found += 1
        else:
            fails.append(f"p{pi + 1}: '{word}' at ({cx:.0f}, {yb:.0f}) is not searchable as a "
                         f"word there (letterspacing too wide)")
    lines.append(f"  {found}/{len(seen)} UI words searchable where drawn: "
                 + ", ".join(sorted({w for _, w, _, _, _ in words})))
    lines.append(f"  {chars} selectable characters; max span right edge {max_x1:.0f}; "
                 f"lowest baseline {max_base:.0f}; condense() shrank {len(CONDENSED)} string(s)")
    if not z.stacked:
        if len(doc) != 3:
            fails.append(f"{len(doc)} pages at 1x, expected 3")
        if CONDENSED:
            fails.append("condense() touched at 1x: " + "; ".join(t for t, _, _ in CONDENSED))
    elif CONDENSED:
        lines.append("  condensed: " + "; ".join(f"{t} {a:.1f}->{b:.1f}" for t, a, b in CONDENSED))
    report = "\n".join(lines)
    if fails:
        sys.exit("LEGIBILITY GATE FAILED\n" + report + "\n" + "\n".join("  FAIL " + f for f in fails))
    return report


def main():
    global DRAW_TEXT
    argv = sys.argv
    large, medium = "--large" in argv, "--medium" in argv
    opts = Opts.from_argv(argv)
    z = Sz(1.75 if large else 1.30 if medium else 1.0, opts)
    out = OUT
    if large:
        out = out.replace(".pdf", "_large.pdf")
    elif medium:
        out = out.replace(".pdf", "_medium.pdf")
    if opts.transparent:
        out = out.replace(".pdf", "_transparent.pdf")
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]

    DRAW_TEXT = not opts.ground_only
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("Killer of Men — Credits")
    sections = build(c, z, opts)
    words = list(WORDS)
    c.save()
    print(f"wrote {out}  ({os.path.getsize(out) / 1e6:.2f} MB, {len(sections)} pages)")

    if not opts.ground_only and not opts.transparent and "--no-gate" not in argv:
        DRAW_TEXT = False
        gpath = os.path.join(tempfile.gettempdir(), "kom-card-ground-only.pdf")
        gc = canvas.Canvas(gpath, pagesize=(W, H))
        build(gc, Sz(z.s, opts), opts)
        gc.save()
        DRAW_TEXT = True
        print("legibility gate:\n" + gate(out, gpath, sections, z, words))

    if "--png" in argv:
        import pymupdf
        outdir = os.path.join(ROOT, "press", "assets", "CREDITS")
        os.makedirs(outdir, exist_ok=True)
        doc = pymupdf.open(out)
        tag = ("_large" if large else "_medium" if medium else "") + \
              ("_transparent" if opts.transparent else "")
        for i, page in enumerate(doc):
            f = os.path.join(outdir, f"KillerOfMen_Credits_p{i + 1}{tag}.png")
            page.get_pixmap(dpi=200, alpha=opts.transparent).save(f)
            print(f"  {os.path.basename(f)}")


if __name__ == "__main__":
    main()
