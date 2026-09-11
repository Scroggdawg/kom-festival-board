#!/usr/bin/env python3
"""Build the eleven-page KILLER OF MEN press kit as one PDF, from press/epk.json.

    <venv>/bin/python tools/build-epk-kit.py [--out FILE] [--png]

Page order follows press/epk-spec.md, which was modelled on a strong AFI thesis EPK:

     1  Poster                 full-bleed key art
     2  Logline + synopsis     hero still, then the two paragraphs
     3  The programmer page    specs, team, cast, rights, links, contact
     4  Director's statement   page 3's armature: figure left, flush-left column right
     5  Filmmaker bios         director, producer, cinematographer
     6  Filmmaker bios         production designer, editor
     7  Cast                   the cast column on the left edge, one figure ghosted right
     8  Behind the scenes      twelve set photographs, no captions
     9  Cast + key credits     )
    10  Crew                   ) drawn by tools/build-credit-card.py; stills per page and
    11  Thanks + AFI end card  ) press mode set from credit_pages()

Text is selectable on every page, and the links are real PDF link annotations. The
model kit (built in Canva, per its PDF metadata) has live text only on pages 2-4 and
pictures of text on 5-11; it does carry links (thirty, on pages 3, 5, 6 and 7), so
the earlier note here that it had none was wrong (corrected 2026-09-10).

Nothing is retyped. Every fact comes out of press/epk.json at build time, except two
paragraphs the worksheet does not hold yet: the logline is read from
press/logline-final-three.md (version A, the recommended one) and the synopsis from
press/synopsis-draft.md (version C, the recommended one). Both are DRAFTS awaiting
Jordan's pick. The moment 2.1 or 2.2 is filled in the worksheet, the worksheet wins.

Portraits on pages 5-6: five headshots, one per bio. PORTRAITS below is the mapping,
settled by checksum against the Drive's named copies (the director's, KOM Headshots-1,
found on the Drive 2026-09-11). Were PORTRAITS_CONFIRMED False the pages would carry a
small PROOF slug so the kit could not be mistaken for final.

Fonts, colours and measurements are the credit card's, so the kit reads as one object.
"""
import importlib.util, io, os, re, sys, datetime

from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESS = os.path.join(ROOT, "press")
ASSETS = os.path.join(PRESS, "assets")

# The credit card is imported, not copied, so pages 9-11 here ARE the card.
_spec = importlib.util.spec_from_file_location(
    "card", os.path.join(ROOT, "tools", "build-credit-card.py"))
card = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(card)

W, H = card.W, card.H
M = card.M
CREAM, DIM, GROUND, RULE = card.CREAM, card.DIM, card.GROUND, card.RULE
tracked, field, pairs = card.tracked, card.field, card.pairs
Z = card.Sz(1.0)

BODY = 15.6          # running text
BODY_LEAD = 24.5
SMALL = 12.4
SMALL_LEAD = 18.0
HEAD = 40.0          # page titles, letterspaced
SUB = 21.0           # person / section headings

STILL = lambda n: os.path.join(ASSETS, "STILLS", f"Still 2026-09-08 210640_1.1.{n}.png")
BTS = lambda name: os.path.join(ASSETS, "BTS", name)
POSTER = os.path.join(ASSETS, "POSTER", "KillerOfMen_Poster_2160x2700.jpg")
HEADSHOT = lambda n: os.path.join(ASSETS, "HEADSHOTS", f"KOM Headshots v3-{n}.jpg")
HEADSHOT_FILE = lambda name: os.path.join(ASSETS, "HEADSHOTS", name)

# ---- page 3: where the five links go. The press folder holds the five subfolders;
# per-subfolder share URLs live in the EPK LINKS doc and are not in the worksheet yet.
PRESS_FOLDER = "https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx"
LINKS = [("BTS", PRESS_FOLDER), ("STILLS", PRESS_FOLDER), ("POSTER", PRESS_FOLDER),
         ("TRAILER", PRESS_FOLDER), ("HEADSHOTS", PRESS_FOLDER)]

# ---- pages 5-6: portrait mapping. Per bio slot: a headshot number, a file name in
# HEADSHOTS, or None for no portrait. Settled Sep 9 by checksum against the named copies
# Luke put on the Drive (05 MARKETING/00 PRESS/HEADSHOTS): v3-1 You Wu, v3-2 Ruoxiao Li,
# v3-3 RJ Ragampudi, v3-4 Luke Scroggins.
PORTRAITS_CONFIRMED = True
# 5.1, the director: the fifth frame of the same session (Hasselblad X1D II 50C, 14 Sep
# 2024), KOM Headshots-1.jpg, found on the Drive 2026-09-11 and matched to the portrait
# Luke sent ("use the attached photo"); its Drive twin is Director_Jordan_Betine.jpg. It
# replaces the value-graded set photograph Day3-43 that stood in from the taste pass.
DIRECTOR_PORTRAIT_CONFIRMED = True
PORTRAITS = {"5.1": HEADSHOT_FILE("KOM Headshots-1.jpg"), "5.2": 2, "5.3": 4, "5.4": 3, "5.5": 1}
PORTRAIT_GRADE = {}                              # key -> "mono": a set photograph graded to sit with the studio heads
PORTRAIT_FOCUS = {}                              # default (0.5, 0.40)
PORTRAIT_ZOOM = {}                               # crop only; masters untouched
# Ruoxiao Li's head fills ~28% of her box against ~40% for the other three; the fix is one
# entry each, PORTRAIT_FOCUS["5.2"] = (0.5, 0.42) and PORTRAIT_ZOOM["5.2"] = 1.25, and it
# re-crops a delivered headshot, so it ships only on Luke's yes (sexy-pass question 2).
BIO_GAP = 66.0                                   # between bio blocks, both pages
# Instagram / IMDb per filmmaker come from field 5.7 at build time (Luke, Sep 10):
# "Role | Name | @handle | https://www.imdb.com/name/nmNNN/", one line each. Matched to
# a bio slot by the role word; handles are shown exactly as typed.
ROLE_TO_BIO = {"director": "5.1", "producer": "5.2", "cinematographer": "5.3",
               "production designer": "5.4", "editor": "5.5"}


def person_links(d):
    """key -> [(label, url), ...] from field 5.7; empty when the field is."""
    out = {}
    for line in field(d, "5.7").split("\n"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
        key = ROLE_TO_BIO.get(parts[0].lower())
        if not key:
            continue
        handle, imdb = parts[2], parts[3]
        links = []
        if handle.startswith("@"):
            links.append((handle, f"https://www.instagram.com/{handle[1:]}/"))
        if imdb.startswith("http"):
            links.append(("IMDB", imdb))
        out[key] = links
    return out

PORTRAIT_H = 396.0                              # every portrait, every page
PORTRAIT_W = round(PORTRAIT_H * 0.84)           # 333

BIOS = [  # field, heading role, name
    ("5.1", "WRITER-DIRECTOR", "JORDAN BETINE"),
    ("5.2", "PRODUCER", "RUOXIAO LI"),
    ("5.3", "CINEMATOGRAPHER", "LUKE SCROGGINS"),
    ("5.4", "PRODUCTION DESIGNER", 'RAJARAJESHWARI "RJ" RAGAMPUDI'),
    ("5.5", "EDITOR", "YOU WU"),
]

# ---- page 8: ten set photographs on a held thirds grid, with one size break: the crew
# photograph runs the full width on the last row. Cells are (file, relative width).
# Row heights + 3 gaps + the 74 pt credit strip sum to exactly 1728.
# Rows read as the shoot did: the farm by day, the barn and the fight, the soundstage and
# the burial, then the unit. An optional third element is the cover focus (taste pass
# 2026-09-11, P8-A/B/C: -149 and Soundstage-32 read as nothing at cell size; -84 opens
# with the barn yard, the truck, the dolly and six crew, render-checked at cell size).
MOSAIC = [
    (399, [("KOM_Day3_TheFarm-84.jpg", 432, (0.45, 0.5)), ("KOM_Day3_TheFarm-59.jpg", 432),
           ("KOM_Day3_TheFarm-152.jpg", 432)]),
    (399, [("KOM_Day3_TheFarm-194.jpg", 432), ("KOM_Day3_TheFarm-185.jpg", 432),
           ("KOM_Day3_TheFarm-220.jpg", 432)]),
    (399, [("KOM_Day4_Soundstage-76.jpg", 432, (0.5, 0.62)), ("KOM_Day4_Soundstage-81.jpg", 432),
           ("KOM_Day4_Soundstage-93.jpg", 432)]),
    (439, [("KOM_Day3_TheFarm-237.jpg", 1296)]),
]
GAP = 6.0
STRIP = M                                       # the credit strip is the page's own margin


# ---------- text the worksheet does not hold yet ----------
def quoted_block(path, heading_prefix):
    """The '> ' blockquote under the first '## <prefix>' heading in a markdown file."""
    lines = open(path, encoding="utf-8").read().split("\n")
    out, on, started = [], False, False
    for ln in lines:
        if ln.startswith("## "):
            if started:
                break
            on = ln[3:].strip().startswith(heading_prefix)
            continue
        if not on:
            continue
        if ln.startswith(">"):
            started = True
            out.append(ln[1:].strip())
        elif started and ln.strip() == "":
            out.append("")
        elif started:
            break
    text = "\n".join(out).strip()
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return re.sub(r"\n{2,}", "\n\n", text)


def logline(d):
    v = field(d, "2.1").strip()
    if v:
        return v, False
    return quoted_block(os.path.join(PRESS, "logline-final-three.md"), "A"), True


def synopsis(d):
    v = field(d, "2.2").strip()
    if v:
        return v, False
    return quoted_block(os.path.join(PRESS, "synopsis-draft.md"), "C"), True


# ---------- images ----------
def load_rgb(path, maxpx=1800):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im.thumbnail((maxpx, maxpx), Image.LANCZOS)
    return im


def unletterbox(im):
    g = im.convert("L")
    w, h = g.size
    rows = [y for y in range(h) if g.crop((0, y, w, y + 1)).getextrema()[1] > 8]
    if rows and (rows[0] > 2 or rows[-1] < h - 3):
        im = im.crop((0, rows[0], w, rows[-1] + 1))
    return im


def reader(im, q=84):
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    buf.seek(0)
    return ImageReader(buf)


def cover(c, im, x, y, w, h, alpha=1.0, focus=(0.5, 0.5), q=84, zoom=1.0):
    """Draw im to fill the box, cropping. focus is where in the image to keep; zoom > 1
    crops tighter around it (the master is never resampled on disk)."""
    iw, ih = im.size
    sc = max(w / iw, h / ih) * zoom
    cw, ch = w / sc, h / sc
    cx = (iw - cw) * focus[0]
    cy = (ih - ch) * focus[1]
    crop = im.crop((int(cx), int(cy), int(cx + cw), int(cy + ch)))
    c.saveState()
    if alpha < 1.0:
        c.setFillAlpha(alpha)
    c.drawImage(reader(crop, q), x, y, w, h)
    c.restoreState()


def grade_mono_pixels(im, target_l=20.0):
    """Value-only grade for a set photograph that stands beside the studio headshots:
    grayscale, gamma 1.9, a GROUND-to-CREAM ramp (no hue the palette does not own), then
    brightness to a mean L near the headshots'. Draw time only; the master is untouched."""
    from PIL import ImageEnhance, ImageStat
    g = ImageOps.grayscale(im).point(lambda v: int(255 * (v / 255) ** 1.9))
    t = ImageOps.colorize(g, black=(11, 8, 6), white=(239, 230, 214))
    mean = ImageStat.Stat(t.convert("L")).mean[0]
    return ImageEnhance.Brightness(t).enhance(target_l / mean) if mean > 0 else t


def mono(im, target_l=20.0):
    """The primitive the page calls; the replays (build-epk-ai.py) patch this one to mark
    the image `grade = "mono"` instead, and the Canva emitter grades its derivative with
    grade_mono_pixels(). Illustrator links the master ungraded."""
    return grade_mono_pixels(im, target_l)


GHOST_ALPHA, GHOST_SCRIM = 0.48, 0.32   # the ghost family (pages 3, 4, 7): Luke, 2026-09-11,
                                        # from four rendered strengths; was 0.22 / 0.50


def ground(c, still_n=None, alpha=0.16, scrim=0.55, focus=(0.5, 0.5)):
    """The page ground, with a still ghosted under a scrim when still_n is given. The
    ghost family draws at GHOST_ALPHA / GHOST_SCRIM (page 3's Elder measures face L 24,
    left third L 29; the type's ground stays under L 30). The old 0.16 / 0.55 defaults
    remain for any caller that asks for them."""
    c.setFillColor(GROUND)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    if still_n is not None:
        im = unletterbox(load_rgb(STILL(still_n), 1600))
        cover(c, im, 0, 0, W, H, alpha=alpha, focus=focus, q=78)
        c.saveState()
        c.setFillColor(GROUND)
        c.setFillAlpha(scrim)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.restoreState()


# ---------- type ----------
def title(c, text, y, align="center", x=None):
    """Letterspaced page title with the card's short rule under it."""
    spaced = " ".join(text)
    if align == "center":
        tracked(c, W / 2, y, spaced, "Bask", HEAD, Z.track_t, CREAM, "center")
        c.setStrokeColor(RULE); c.setLineWidth(0.7)
        c.line(W / 2 - 118, y - 22, W / 2 + 118, y - 22)
    else:
        tracked(c, x, y, spaced, "Bask", HEAD, Z.track_t, CREAM, align)
        c.setStrokeColor(RULE); c.setLineWidth(0.7)
        if align == "right":
            c.line(x - 236, y - 22, x, y - 22)
        else:
            c.line(x, y - 22, x + 236, y - 22)
    return y - 62


LABEL_TRACK = Z.track_r + 1.0                   # one label class across pages 2, 7 and 11


def label(c, x, y, text, align="left", color=DIM):
    """Section label: 15.6 pt Baskerville caps, tracked 2.35, DIM. Pass plain words."""
    tracked(c, x, y, text.upper(), "Bask", BODY, LABEL_TRACK, color, align)


def para(c, text, x, y, width, size=BODY, lead=BODY_LEAD, color=CREAM, align="left",
         font="Bask", gap=None):
    """Wrap and draw paragraphs separated by blank lines. Returns the y below."""
    gap = lead * 0.6 if gap is None else gap
    for p in [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]:
        p = " ".join(p.split())
        for line in simpleSplit(p, font, size, width):
            lw = c.stringWidth(line, font, size)
            lx = x + (width - lw) / 2 if align == "center" else \
                x + width - lw if align == "right" else x
            # A text object with its own zero letterspacing: the headings' tracking
            # otherwise leaks into running text and the wrap no longer matches.
            t = c.beginText(lx, y)
            t.setFont(font, size)
            t.setFillColor(color)
            t.setCharSpace(0)
            t.textOut(line)
            c.drawText(t)
            y -= lead
        y -= gap
    return y + gap


def text_width(c, s, font, size, track):
    return c.stringWidth(s, font, size) + track * max(len(s) - 1, 0)


def para_height(text, width, size=BODY, lead=BODY_LEAD, font="Bask", gap=None):
    gap = lead * 0.6 if gap is None else gap
    h = 0
    ps = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    for p in ps:
        h += len(simpleSplit(" ".join(p.split()), font, size, width)) * lead + gap
    return h - gap if ps else 0


def fit(text, width, height, size=BODY, lead=BODY_LEAD, font="Bask"):
    """Step the size down until the text fits the box. Overflow is never allowed."""
    while size > 9 and para_height(text, width, size, lead, font) > height:
        size -= 0.3
        lead = size * (BODY_LEAD / BODY)
    return size, lead


def link(c, url, x, y, w, h):
    c.linkURL(url, (x, y, x + w, y + h), relative=0, thickness=0)


def proof_slug(c, text):
    """The one mark whose job is to be read, so DIM (8.6:1), not RULE (3:1)."""
    tracked(c, W / 2, M * 0.45, text, "Bask", 9.5, 1.4, DIM, "center")


# ---------- pages ----------
def page_poster(c):
    """The key art whole, fitted to the page width; the sliver above and below is
    the kit's own ground. Nothing of the poster is cropped."""
    ground(c)
    im = load_rgb(POSTER, 2200)
    iw, ih = im.size
    sc = min(W / iw, H / ih)
    dw, dh = iw * sc, ih * sc
    c.drawImage(reader(im, 90), (W - dw) / 2, (H - dh) / 2, dw, dh)
    c.showPage()


def page_logline(c, d):
    ground(c)
    # 720 pt keeps 76% of the frame's width from its left edge, so the owner watching from
    # the doorway stays in the picture; at 860 centred the crop kept 63% and lost him, and
    # what remained was a physique shot, not the story. 700 is the floor (P2-1).
    hero_h = 720.0
    im = unletterbox(load_rgb(STILL(5), 2000))
    cover(c, im, 0, H - hero_h, W, hero_h, focus=(0.0, 0.5), q=88)
    lg, lg_draft = logline(d)
    sy, sy_draft = synopsis(d)
    x, w = M, 820.0                                # the page margin; 80-94 characters a line
    # The block is placed, not hung: the spare in the band under the hero splits 3:5 above
    # and below, the proportion the page already had, so a change of hero height never
    # leaves the copy as remainder (P2-2).
    lg_h = para_height(lg, w, 26.0, 40.0)
    band = H - hero_h - M
    sz, ld = fit(sy, w, band - (BODY + 52 + lg_h + 48 + 52) - 44, 22.0, 34.5)
    block = BODY + 52 + lg_h + 48 + 52 + para_height(sy, w, sz, ld)
    y = H - hero_h - 0.375 * max(band - block, 0) - BODY
    label(c, x, y, "LOGLINE")
    y -= 52
    y = para(c, lg, x, y, w, 26.0, 40.0)
    y -= 48
    label(c, x, y, "SYNOPSIS")
    y -= 52
    room = y - M - 44
    size, lead = fit(sy, w, room, 22.0, 34.5)
    para(c, sy, x, y, w, size, lead)
    if lg_draft or sy_draft:
        proof_slug(c, "PROOF — LOGLINE A AND SYNOPSIS C ARE DRAFTS, NOT YET CHOSEN")
    c.showPage()


COL_SIZE, COL_STEP = 19.0, 28.0                 # the programmer page's one type size and step


def programmer_rows(d):
    """The page as data first, so the column's type size can be settled before a line
    is drawn: ('kv', key, value) · ('head', title) · ('cast', role, actor)."""
    rows = []
    srt = field(d, "3.7")
    srt_langs = "English" if srt.lower().startswith("english only") else ""
    kv = lambda k, v: rows.append(("kv", k, v))
    kv("Genre", field(d, "3.1")); kv("Country", field(d, "3.2"))
    kv("Shooting location", field(d, "3.3")); kv("Production year", field(d, "3.4"))
    kv("Completion year", field(d, "3.5"))
    kv("Language", field(d, "3.6").strip() + (f"  (.srt available: {srt_langs})" if srt_langs else ""))
    kv("Duration", field(d, "3.8")); kv("Aspect ratio", field(d, "3.9"))
    kv("Frame rate", field(d, "3.10")); kv("Shooting format", field(d, "3.11"))
    if field(d, "3.12").strip():
        kv("Exhibition format", field(d, "3.12").strip())
    if field(d, "3.13").strip():
        kv("Sound", field(d, "3.13").strip().replace("Stereo 5.1", "5.1, stereo"))
    rows.append(("head", "THE TEAM"))
    for role, names in pairs(field(d, "3.14")):
        if role:
            kv({"Director": "Written & directed by"}.get(role, role), " · ".join(names))
    rows.append(("head", "CAST"))
    for role, names in pairs(field(d, "3.15")):
        if role and "coordinator" not in role.lower():
            rows.append(("cast", role, " · ".join(names)))
    rows.append(("head", "RIGHTS"))
    kv("Rights holder", field(d, "3.16"))
    contact = field(d, "3.17").strip()
    if contact:
        name, _, email = contact.partition("·")
        kv("Contact", name.strip())
        if email.strip():
            rows.append(("kv", "Email", email.strip(), "mailto:" + email.strip()))
    return rows


def page_programmer(c, d):
    ground(c, 41, alpha=GHOST_ALPHA, scrim=GHOST_SCRIM)
    xr = W - M                      # everything right-aligned to this edge
    y = title(c, "KILLER OF MEN", H - M - 30, align="right", x=xr)
    rows = programmer_rows(d)

    # One size for the whole column. If any line would have to condense below 18 pt to
    # fit, the column steps down together rather than letting one line differ.
    room = W - 2 * M - 300
    size, step = COL_SIZE, COL_STEP
    for r in rows:
        if r[0] == "kv":
            s, _ = card.condense(c, f"{r[1]}: {r[2]}".upper(), "Bask", size, Z.track_n, room)
            if s < 18.0:
                size, step = 18.0, 27.0
                break

    def two_tone(key, value):
        """Key in DIM, value in CREAM, one baseline, one right edge (F05)."""
        nonlocal y
        line = f"{key}{value}".upper()
        s, tr = card.condense(c, line, "Bask", size, Z.track_n, room)
        wv = tracked(c, xr, y, value.upper(), "Bask", s, tr, CREAM, "right")
        tracked(c, xr - wv, y, key.upper(), "Bask", s, tr, DIM, "right")
        base = y
        y -= step
        return base

    for r in rows:
        if r[0] == "head":
            y -= 34
            tracked(c, xr, y, r[1], "Bask-SB", 24.0, 2.2, CREAM, "right")
            y -= 34
        elif r[0] == "kv":
            base = two_tone(f"{r[1]}: ", r[2])
            if len(r) > 3:                                  # a live mailto under the value
                link(c, r[3], xr - 520, base - 6, 520, size + 6)
        elif r[0] == "cast":
            two_tone(f"{r[1]}  |  ", r[2])

    y -= 34
    tracked(c, xr, y, "LINKS", "Bask-SB", 24.0, 2.2, CREAM, "right")
    y -= 34
    for name, url in LINKS:
        wtxt = tracked(c, xr, y, name, "Bask", size, Z.track_n, CREAM, "right")
        c.setStrokeColor(DIM); c.setLineWidth(0.5)
        c.line(xr - wtxt, y - 6, xr, y - 6)
        link(c, url, xr - wtxt - 8, y - 8, wtxt + 16, step)
        y -= step

    # footer: email · website · instagram · imdb, all live, all underlined (F06).
    # The production email is field 3.20 (Luke, Sep 10); absent, the row is skipped.
    def optional(n):
        try:
            return field(d, n).strip()
        except KeyError:
            return ""
    email = optional("3.20")
    items = [(email.upper(), "mailto:" + email) if email else ("", ""),
             ("WWW.KILLEROFMEN.COM", field(d, "1.3")),
             ("INSTAGRAM  @KILLEROFMENMOVIE", field(d, "3.18")),
             ("IMDB", field(d, "3.19"))]
    items = [it for it in items if it[1].strip()]
    yy = M + 24 + (len(items) - 1) * step
    for text, url in items:
        if not url.strip():
            continue
        wtxt = tracked(c, xr, yy, text, "Bask", size, Z.track_n, CREAM, "right")
        c.setStrokeColor(DIM); c.setLineWidth(0.5)
        c.line(xr - wtxt, yy - 6, xr, yy - 6)
        link(c, url.strip(), xr - wtxt - 8, yy - 8, wtxt + 16, step)
        yy -= step
    c.showPage()


def page_statement(c, d):
    # Page 3's armature: the figure in the left third, one alignment edge at xr = 1222.
    # focus 0.83 stands Mace's back whole in the left third of the crop of still 10; the
    # owner leaves the frame and his hand on the shoulder enters from the edge (Luke's
    # call, handoff-113). 0.62 kept both silhouettes and ran the column across both (P4-02).
    ground(c, 10, alpha=GHOST_ALPHA, scrim=GHOST_SCRIM, focus=(0.83, 0.5))
    xr = W - M
    y = title(c, "DIRECTOR'S STATEMENT", H - M - 30, align="right", x=xr)
    # Single newlines in 4.1 are the director's own paragraph turns; para() would fold them
    # into one seventeen-line block, so they are promoted to paragraph breaks (P4-03).
    text = re.sub(r"\n+", "\n\n", field(d, "4.1").strip())
    x, w = xr - 686, 686.0                          # 536..1222, 25 pt clear of the figure
    top = y - 44
    room = top - (M + 76) - 56                      # the signature lives inside the box
    size, lead = fit(text, w, room, 23.0, 36.5)     # fit() steps down until it fits
    y_end = para(c, text, x, top, w, size, lead)
    tracked(c, x, y_end - 56, "JORDAN BETINE, WRITER-DIRECTOR", "Bask", Z.role + 1,
            Z.track_r + 1.0, DIM)                 # closes the letter, on the column's edge
    c.showPage()


def portrait_src(key):
    """(path, graded): a headshot by number or by path; PORTRAIT_GRADE marks a set
    photograph that mono() grades to sit beside the studio headshots."""
    pn = PORTRAITS.get(key)
    if pn is None:
        return None, False
    return (pn if isinstance(pn, str) else HEADSHOT(pn)), PORTRAIT_GRADE.get(key) == "mono"


def bio_block(c, key, role, name, y, side, height, port_h=None):
    """Heading, portrait on one side, text on the other. Returns the y below. `port_h`
    overrides the portrait height (the five-on-one test page); width keeps the 0.84 aspect."""
    src, graded = portrait_src(key)
    has_img = src is not None and os.path.exists(src)
    head_text = f"{role}  |  {name}"
    # Page 3's law on a bio block: one text edge, the image in the opposite third. The
    # lockup, its handles and the prose all sit on M; only the portrait alternates sides
    # (taste pass 2026-09-11, C06 as amended). Handles in the label class with page 3's
    # 0.5 pt DIM underline, each a live link (C07).
    tracked(c, M, y, head_text, "Bask-SB", SUB, 2.2, CREAM)
    links = person_links(c._d).get(key, [])
    hw = text_width(c, head_text, "Bask-SB", SUB, 2.2)
    gap = 28
    c.setStrokeColor(DIM); c.setLineWidth(0.5)
    px = M + hw + gap
    for lab, url in links:
        wd = tracked(c, px, y, lab, "Bask", BODY, LABEL_TRACK, DIM)
        c.line(px, y - 6, px + wd, y - 6)
        link(c, url, px - 4, y - 8, wd + 8, BODY + 12)
        px += wd + gap
    y -= 40
    img_h = PORTRAIT_H if port_h is None else port_h
    img_w = PORTRAIT_W if port_h is None else round(port_h * 0.84)
    text_w = W - 2 * M - img_w - 48                 # the measure every bio shares
    text = field(c._d, key)
    size, lead = fit(text, text_w, img_h - 4, 19.0, 30.0)
    if has_img:
        im = load_rgb(src, 1200)
        if graded:
            im = mono(im)
        ix = M if side == "left" else W - M - img_w
        cover(c, im, ix, y - img_h, img_w, img_h, focus=PORTRAIT_FOCUS.get(key, (0.5, 0.40)),
              q=86, zoom=PORTRAIT_ZOOM.get(key, 1.0))
        tx = M + img_w + 48 if side == "left" else M
        para(c, text, tx, y - lead * 0.85, text_w, size, lead)
        return y - img_h
    # No portrait: the text keeps the shared measure under its own heading and the
    # block is only as tall as the words, so no empty slot is reserved (F01 fallback).
    para(c, text, M, y - lead * 0.85, text_w, size, lead)
    return y - para_height(text, text_w, size, lead) - lead


def bio_height(d, key, port_h=None):
    """What bio_block() will use, so the page can distribute its spare evenly."""
    src, _ = portrait_src(key)
    img_h = PORTRAIT_H if port_h is None else port_h
    img_w = PORTRAIT_W if port_h is None else round(port_h * 0.84)
    if src is not None and os.path.exists(src):
        return 40 + img_h
    text_w = W - 2 * M - img_w - 48
    size, lead = fit(field(d, key), text_w, img_h - 4, 19.0, 30.0)
    return 40 + para_height(field(d, key), text_w, size, lead) + lead


def page_bios(c, d, items, first, offset=0):
    """Portrait sides alternate by a running index across the spread (offset), so the page
    turn never meets two left-hand portraits. The titled page anchors its first block under
    the title and its last on the foot margin, like page 3's footer; the untitled page
    carries its blocks as one group with the same gap, set a little above centre
    (taste pass 2026-09-11, P5-02, P6-01, P56-01; replaces F08's even split)."""
    c._d = d
    ground(c)
    y = H - M - 30
    heights = [bio_height(d, key) for key, _, _ in items]
    if first:
        y = title(c, "FILMMAKERS", y)
        y -= 48
        between = (y - M - sum(heights)) / max(len(items) - 1, 1)
    else:
        between = BIO_GAP
        group = sum(heights) + between * (len(items) - 1)
        y -= 0.45 * max((y - M) - group, 0)
    for i, (key, role, name) in enumerate(items):
        y = bio_block(c, key, role, name, y, "left" if (offset + i) % 2 == 0 else "right",
                      heights[i])
        y -= between
    if not PORTRAITS_CONFIRMED:
        proof_slug(c, "PROOF — PORTRAITS NOT YET ASSIGNED TO NAMES")
    elif first and not DIRECTOR_PORTRAIT_CONFIRMED and PORTRAIT_GRADE.get("5.1") == "mono":
        proof_slug(c, "PROOF — THE DIRECTOR'S PORTRAIT IS A SET PHOTOGRAPH, IDENTITY TO CONFIRM")
    c.showPage()


BIO_GAP_SINGLE = 30.0


def page_bios_single(c, d, items, offset=0):
    """Test page (Luke, 2026-09-11: "a test page where all 5 filmmakers fit on a single
    page"). Pages 5-6's law unchanged: one text edge, the lockup and its handles and the
    prose on M, only the portrait alternating sides; the portrait height is what one page
    allows after the title, five headings and four gaps, the last block on the foot margin,
    and fit() sets each bio in the box beside its portrait. Not wired into main(); rendered
    by tools/build-epk-variants.py."""
    c._d = d
    ground(c)
    y = title(c, "FILMMAKERS", H - M - 30)
    y -= 48
    port_h = float(int((y - M - 40 * len(items) - BIO_GAP_SINGLE * (len(items) - 1)) / len(items)))
    heights = [bio_height(d, key, port_h) for key, _, _ in items]
    between = (y - M - sum(heights)) / max(len(items) - 1, 1)
    sizes = []
    for i, (key, role, name) in enumerate(items):
        text_w = W - 2 * M - round(port_h * 0.84) - 48
        sizes.append(fit(field(d, key), text_w, port_h - 4, 19.0, 30.0)[0])
        y = bio_block(c, key, role, name, y, "left" if (offset + i) % 2 == 0 else "right",
                      heights[i], port_h)
        y -= between
    print(f"five-on-one: portrait {port_h:.0f} x {round(port_h * 0.84)} pt (pages 5-6: {PORTRAIT_H:.0f} x {PORTRAIT_W}), "
          f"gap {between:.0f}, bio sizes " + ", ".join(f"{s:.1f}" for s in sizes))
    c.showPage()


# ---- page 7: the page-3 form, mirrored. The cast column on the left edge, one figure
# ghosted in the right third. Still 1.1.17 (Mace at the cabin, daylight) at focus 0.12
# puts his face in the upper right looking into the column, the Elder's gesture on page 3.
# The pass's other candidate, 1.1.15 at 0.48 (his figure at the oak), loses the head in
# the page-shaped crop; Luke rules (handoff-113). No hero: still 40 over the lead's lockup
# read as the lead's face, and it is Kojo's. Taste pass 2026-09-11, C01.
CAST_GHOST = (17, (0.12, 0.5))
CAST_COL_W = 600.0                              # 75-80 characters at 15.6


def cast_blocks(text):
    """Field 7.1 as (bios, notes). A block whose first line carries a pipe is a bio: 'role |
    name', the paragraph, and a 'Prior credits:' line. Every other block is provenance (drafts,
    what to confirm, sources) and is never printed as copy; while any exists the page carries
    a PROOF slug. This is pairs()'s rule, a line with no pipe ends the run, at block level."""
    bios, notes = [], []
    for b in [b for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]:
        lines = [l.strip() for l in b.split("\n") if l.strip()]
        if "|" in lines[0] and len(lines) > 1:
            role, _, name = lines[0].partition("|")
            body = " ".join(l for l in lines[1:] if not l.lower().startswith("prior credits:"))
            prior = next((l for l in lines[1:] if l.lower().startswith("prior credits:")), "")
            bios.append((role.strip(), name.strip(), body, prior))
        else:
            notes.append(b)
    return bios, notes


# Roles the cast page does not bill under ALSO BILLED (Luke, 2026-09-11: "lose the two
# spectator billings"). Pages 3 (the programmer's CAST block) and 9 (CREDITS) still carry
# them from the same fields; drop them there too only on Luke's word.
CAST_PAGE_DROP = ("spectator",)


def page_cast(c, d):
    """Page 7. With bios in 7.1: the title law at the left edge, then each ROLE | NAME lockup
    (the pages 5-6 class) over its bio, flush-left on a 600 pt measure; the billed names without a bio in the two-tone rows under a label (the label
    word is Luke's call); a PROOF slug while 7.1 carries provenance. Without bios: still 40
    as a tall hero over the whole billed list, as before."""
    bios, notes = cast_blocks(field(d, "7.1"))
    billed = [(r, n) for r, n in pairs(field(d, "3.15")) if r and "coordinator" not in r.lower()]
    x = M

    def two_tone_rows(y, rows, cols):
        half = (len(rows) + 1) // 2 if len(cols) > 1 else len(rows)
        for ci, chunk in enumerate([rows[:half], rows[half:]][:len(cols)]):
            yy = y
            for role, names in chunk:
                tracked(c, cols[ci], yy, role.upper(), "Bask", BODY, Z.track_r, DIM)
                tracked(c, cols[ci] + 210, yy, " · ".join(names).upper(), "Bask", 17.0,
                        Z.track_n, CREAM)
                yy -= 28

    if bios:
        n, focus = CAST_GHOST
        ground(c, n, alpha=GHOST_ALPHA, scrim=GHOST_SCRIM, focus=focus)
        y = title(c, "CAST", H - M - 30, align="left", x=x)
        y -= 44
        for role, name, body, prior in bios:
            tracked(c, x, y, f"{role}  |  {name}".upper(), "Bask-SB", SUB, 2.2, CREAM)
            y -= 36
            y = para(c, body, x, y, CAST_COL_W, BODY, BODY_LEAD)
            # the field's 'Prior credits:' line is parsed out and not drawn: DIM is for
            # labels, never a line of running text, and each title is in the paragraph
            y -= 48
        with_bio = {b[0].lower() for b in bios}
        rest = [(r, n) for r, n in billed if r.lower() not in with_bio
                and not any(k in r.lower() for k in CAST_PAGE_DROP)]
        if rest:
            y -= 8
            label(c, x, y, "ALSO BILLED")
            two_tone_rows(y - 34, rest, [x])
        if notes:
            proof_slug(c, "PROOF — CAST BIOS ARE DRAFTS, NOT YET APPROVED BY THE ACTORS")
    else:
        ground(c)
        hero_h = 1230.0                             # the still takes the room a bio would
        im = unletterbox(load_rgb(STILL(40), 2000))
        cover(c, im, 0, H - hero_h, W, hero_h, focus=(0.5, 0.35), q=88)
        y = H - hero_h - 90
        lead_role, lead_names = billed[0]
        tracked(c, x, y, f"{lead_role}  |  {' · '.join(lead_names)}".upper(), "Bask-SB",
                SUB + 3, 2.4, CREAM)
        y -= 56
        label(c, x, y, "BILLED CAST")
        two_tone_rows(y - 34, billed, [x, x + (W - 2 * M) / 2])
    c.showPage()

def page_bts(c):
    ground(c)
    y = H
    for row_h, cells in MOSAIC:
        # cells share the width minus the gutters, so the last one lands on 1296 exactly
        scale = (W - GAP * (len(cells) - 1)) / sum(cell[1] for cell in cells)
        x = 0.0
        for cell in cells:
            f, w = cell[0], cell[1]
            focus = cell[2] if len(cell) > 2 else (0.5, 0.5)
            cw = w * scale
            im = load_rgb(BTS(f), 1500)
            cover(c, im, x, y - row_h, cw, row_h, focus=focus, q=84)
            x += cw + GAP
        y -= row_h + GAP
    y += GAP                                        # the loop pays a gap after the last row too
    assert abs(y - STRIP) < 0.01, f"mosaic rows do not sum to the page: strip would be {y:.1f}"
    tracked(c, W / 2, M * 0.45, "BEHIND THE SCENES   ·   PHOTOGRAPHS JEDIDIAH WOODS",
            "Bask", Z.role, Z.track_r, DIM, "center")   # the role-label class, on the mark line
    c.showPage()


def credit_pages(c, d):
    """Pages 9-11, drawn by the credit card's own functions on this canvas. press=True:
    a name that is still a placeholder (SOUND DESIGNER | STILL UNKNOWN) is not printed
    as a credit; the card marks the CREW page with a PROOF slug instead (C10 as amended)."""
    opts = card.Opts(press=True, proof_slug=True)
    z = card.Sz(1.0, opts)

    def stills_for(nums):
        """Still numbers become paths; (path, alpha, anchor) tuples pass through as the
        card's override form; None lets the card's own recipe rule."""
        while True:
            for n in nums:
                yield n if (n is None or isinstance(n, tuple)) else STILL(n)

    billed = pairs(field(d, "9.2"))
    cast = [e for e in billed if e[0] and e[0].lower() != "extras"]
    extras = [e for e in billed if e[0] and e[0].lower() == "extras"]
    key = [e for e in pairs(field(d, "9.1"))
           if e[0] and "unknown" not in " ".join(e[1]).lower()]
    # Since handoff-105 the card chooses its own still, opacity and anchor per page from
    # its GROUND_RECIPE; a bare path passed here is ignored with a notice. None lets the
    # recipe rule. To override, pass (path, alpha, anchor) tuples instead.
    # Taste pass 2026-09-11 (C1, C2, C6): still, alpha and anchor per page are passed as
    # tuples, so the standalone card keeps its own GROUND_RECIPE. CREDITS: still 1.1.2, the
    # cupped hands with the shells, at anchor 0.35 the hands land right of the column (the
    # spirit blur of 1.1.29 read as a light leak). CREW: 1.1.27 down to 0.45, the file's own
    # floor, because its bright streak sat under the lower-left names. THANKS: the lantern
    # in frame at 0.35 behind the middle column. Pass stills_for([None]) to take the card's
    # recipe again.
    # Gated 2026-09-11 (card.gate, worst 300 pt window per cream span, p95 against the
    # section limits 60 / 65 / 75): CREDITS 1.1.2 at 1.0 fails (p95 72, JORDAN BETINE under
    # the lit knuckles), 0.85 fails (63), 0.80 scrapes (59.9), 0.75 passes with margin (56);
    # CREW 0.45 passes (32); THANKS 0.35 passes (40).
    CREDIT_STILLS = {"CREDITS": (STILL(2), 0.75, 0.35), "CREW": (STILL(27), 0.45, 0.50),
                     "THANKS": (STILL(25), 0.35, 0.50)}
    # The card is one object: one scale moves all three pages. At 1.0 the CREDITS page is
    # one page in Baskerville; measured in a wider face (the Canva contract is measured in
    # Libre Baskerville, 2026-09-11) the poster names wrap and it overflows, so the scale
    # steps down until CREDITS is one page again, and CREW and THANKS take the same scale.
    # one_col_pages asserts before it draws, so a failed step leaves nothing on the canvas.
    for scale in (1.0, 0.98, 0.96, 0.94, 0.92, 0.90, 0.88, 0.86, 0.84):
        z = card.Sz(scale, opts)
        try:
            card.one_col_pages(c, "C A S T", [cast, key] + ([extras] if extras else []),
                               z, stills_for([CREDIT_STILLS["CREDITS"]]), False)
            break
        except AssertionError as e:
            if scale == 0.84:
                raise
            print(f"  CREDITS at scale {scale:.2f}: {e}; stepping the card down")
    if scale != 1.0:
        print(f"  credit pages at scale {scale:.2f}")
    card.two_col_pages(c, "C R E W", pairs(field(d, "10.1")), z,
                       stills_for([CREDIT_STILLS["CREW"]]), False)
    card.page_thanks(c, d, z, stills_for([CREDIT_STILLS["THANKS"]]), False)


def page_credits_variant(c, d):
    """Page 9 in the page-3 idiom, for Luke's one-object-or-two ruling (handoff-113). Not
    wired into main(); rendered beside page 9 in the review sheet. Still 1.1.13 (the oaks
    and the field, the lone figure walking in the left third; thirds L 14.1 / 16.0 / 14.6
    under the recipe) at focus 0.30; 1.1.16 was measured and cuts Mace's face at the crop's
    edge at any focus that keeps him in one third. The key credits, the 9.1 tail, the cast
    and the extras in one right-aligned column at xr with DIM roles and CREAM names."""
    ground(c, 13, alpha=GHOST_ALPHA, scrim=GHOST_SCRIM, focus=(0.30, 0.5))
    xr = W - M
    y = title(c, "CREDITS", H - M - 30, align="right", x=xr)
    size, step = COL_SIZE, COL_STEP
    room = W - 2 * M - 300

    def row(key, value):
        nonlocal y
        s_, tr = card.condense(c, f"{key}{value}".upper(), "Bask", size, Z.track_n, room)
        wv = tracked(c, xr, y, value.upper(), "Bask", s_, tr, CREAM, "right")
        if key:
            tracked(c, xr - wv, y, key.upper(), "Bask", s_, tr, DIM, "right")
        y -= step

    def head(text):
        nonlocal y
        y -= 34
        tracked(c, xr, y, text, "Bask-SB", 24.0, 2.2, CREAM, "right")
        y -= 34

    all_key = [e for e in pairs(field(d, "9.1")) if e[0]]
    key = [e for e in all_key if "unknown" not in " ".join(e[1]).lower()]
    poster, tail = card.split_at_ep(key)
    for role, names in poster:
        row(f"{role}  |  ", names[0])
        for n in names[1:]:
            row("", n)
    y -= step
    for role, names in tail:
        row(f"{role}  |  ", " · ".join(names))
    head("CAST")
    for role, names in pairs(field(d, "9.2")):
        if not role:
            continue
        if role.lower() == "extras":
            head("EXTRAS")
            for n in names:
                row("", n)
        else:
            row(f"{role}  |  ", " · ".join(names))
    if len(key) < len(all_key):
        proof_slug(c, "PROOF — SOUND DESIGNER NOT YET NAMED")
    print(f"page 9 variant: column ends {y:.0f} pt from the foot")
    c.showPage()


def main():
    d = card.load()
    now = datetime.datetime.now()
    out = os.path.join(PRESS, f"KillerOfMen_EPK_{now:%H%M}_{now:%d%m%Y}_compressed.pdf")
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("Killer of Men — Electronic Press Kit")
    c.setAuthor("AFI Conservatory")
    c.setSubject("Killer of Men (2026), directed by Jordan Betine")

    page_poster(c)                                  # 1
    page_logline(c, d)                              # 2
    page_programmer(c, d)                           # 3
    page_statement(c, d)                            # 4
    page_bios(c, d, BIOS[:3], first=True)           # 5
    page_bios(c, d, BIOS[3:], first=False, offset=3)   # 6
    page_cast(c, d)                                 # 7
    page_bts(c)                                     # 8
    credit_pages(c, d)                              # 9-11
    c.save()
    print(f"wrote {out}  ({os.path.getsize(out)/1e6:.1f} MB)")

    if "--png" in sys.argv:
        from pypdf import PdfReader
        r = PdfReader(out)
        print(f"{len(r.pages)} pages")


if __name__ == "__main__":
    main()
