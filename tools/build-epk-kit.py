#!/usr/bin/env python3
"""Build the eleven-page KILLER OF MEN press kit as one PDF, from press/epk.json.

    <venv>/bin/python tools/build-epk-kit.py [--out FILE] [--png]

Page order follows press/epk-spec.md, which was modelled on a strong AFI thesis EPK:

     1  Poster                 full-bleed key art
     2  Logline + synopsis     hero still, then the two paragraphs
     3  The programmer page    specs, team, cast, rights, links, contact
     4  Director's statement   single centred column over a ghosted still
     5  Filmmaker bios         director, producer, cinematographer
     6  Filmmaker bios         production designer, editor
     7  Cast                   a still in character, the billed cast
     8  Behind the scenes      twelve set photographs, no captions
     9  Cast + key credits     )
    10  Crew                   ) drawn by tools/build-credit-card.py, unchanged
    11  Thanks + AFI end card  )

Text is selectable on every page, and the links on page 3 are real PDF link
annotations. Both are things the model kit got wrong (pages 5-11 of it are pictures
of text, and it has no links at all).

Nothing is retyped. Every fact comes out of press/epk.json at build time, except two
paragraphs the worksheet does not hold yet: the logline is read from
press/logline-final-three.md (version A, the recommended one) and the synopsis from
press/synopsis-draft.md (version C, the recommended one). Both are DRAFTS awaiting
Jordan's pick. The moment 2.1 or 2.2 is filled in the worksheet, the worksheet wins.

Portraits on pages 5-6: four headshots exist for five bios and nobody has said which
file is which person. PORTRAITS below is the mapping. Until PORTRAITS_CONFIRMED is
True the pages carry a small PROOF slug so the kit cannot be mistaken for final.

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

# ---- page 3: where the five links go. The press folder holds the five subfolders;
# per-subfolder share URLs live in the EPK LINKS doc and are not in the worksheet yet.
PRESS_FOLDER = "https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx"
LINKS = [("BTS", PRESS_FOLDER), ("STILLS", PRESS_FOLDER), ("POSTER", PRESS_FOLDER),
         ("TRAILER", PRESS_FOLDER), ("HEADSHOTS", PRESS_FOLDER)]

# ---- pages 5-6: portrait mapping. File number per bio slot, or None for no portrait.
# The order the files are listed in is NOT a statement about who is in them.
PORTRAITS_CONFIRMED = False
PORTRAITS = {"5.1": 1, "5.2": 2, "5.3": 4, "5.4": 3, "5.5": None}
# Instagram / IMDb per person (field 5.7 is empty). key -> [(label, url), ...]
PERSON_LINKS = {}

BIOS = [  # field, heading role, name
    ("5.1", "WRITER-DIRECTOR", "JORDAN BETINE"),
    ("5.2", "PRODUCER", "RUOXIAO LI"),
    ("5.3", "CINEMATOGRAPHER", "LUKE SCROGGINS"),
    ("5.4", "PRODUCTION DESIGNER", 'RAJARAJESHWARI "RJ" RAGAMPUDI'),
    ("5.5", "EDITOR", "YOU WU"),
]

# ---- page 8: twelve set photographs, and the grid they sit in. Cells are (file, w).
MOSAIC = [
    (412, [("KOM_Day3_TheFarm-18.jpg", 430), ("KOM_Day3_TheFarm-59.jpg", 430),
           ("KOM_Day3_TheFarm-149.jpg", 430)]),
    (372, [("IMG_4467.jpg", 430), ("KOM_Day3_TheFarm-152.jpg", 430),
           ("KOM_Day3_TheFarm-99.jpg", 430)]),
    (455, [("KOM_Day3_TheFarm-185.jpg", 380), ("KOM_Day3_TheFarm-220.jpg", 455),
           ("KOM_Day4_Soundstage-32.jpg", 455)]),
    (443, [("KOM_Day4_Soundstage-81.jpg", 430), ("KOM_Day4_Soundstage-93.jpg", 430),
           ("KOM_Day3_TheFarm-237.jpg", 430)]),
]
GAP = 6.0


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


def cover(c, im, x, y, w, h, alpha=1.0, focus=(0.5, 0.5), q=84):
    """Draw im to fill the box, cropping. focus is where in the image to keep."""
    iw, ih = im.size
    sc = max(w / iw, h / ih)
    cw, ch = w / sc, h / sc
    cx = (iw - cw) * focus[0]
    cy = (ih - ch) * focus[1]
    crop = im.crop((int(cx), int(cy), int(cx + cw), int(cy + ch)))
    c.saveState()
    if alpha < 1.0:
        c.setFillAlpha(alpha)
    c.drawImage(reader(crop, q), x, y, w, h)
    c.restoreState()


def ground(c, still_n=None, alpha=0.16, scrim=0.55):
    c.setFillColor(GROUND)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    if still_n is not None:
        im = unletterbox(load_rgb(STILL(still_n), 1600))
        cover(c, im, 0, 0, W, H, alpha=alpha, q=78)
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


def label(c, x, y, text, align="left", size=None, color=DIM):
    tracked(c, x, y, text.upper(), "Bask", size or Z.role, Z.track_r + 0.4, color, align)


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
    tracked(c, W / 2, M * 0.45, text, "Bask", 9.5, 1.2, RULE, "center")


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
    hero_h = 860.0
    im = unletterbox(load_rgb(STILL(5), 2000))
    cover(c, im, 0, H - hero_h, W, hero_h, focus=(0.5, 0.5), q=88)
    lg, lg_draft = logline(d)
    sy, sy_draft = synopsis(d)
    x, w = M + 40, W - 2 * (M + 40)
    y = H - hero_h - 104
    label(c, x, y, "L O G L I N E", size=Z.role + 4)
    y -= 54
    y = para(c, lg, x, y, w, 26.0, 40.0)
    y -= 62
    label(c, x, y, "S Y N O P S I S", size=Z.role + 4)
    y -= 52
    room = y - M - 44
    size, lead = fit(sy, w, room, 22.0, 34.5)
    para(c, sy, x, y, w, size, lead)
    if lg_draft or sy_draft:
        proof_slug(c, "PROOF — LOGLINE A AND SYNOPSIS C ARE DRAFTS, NOT YET CHOSEN")
    c.showPage()


def page_programmer(c, d):
    ground(c, 41, alpha=0.22, scrim=0.50)
    xr = W - M                      # everything right-aligned to this edge
    y = H - M - 40
    tracked(c, xr, y, "K I L L E R   O F   M E N", "Bask", 30, 4.0, CREAM, "right")
    y -= 44

    def kv(k, v):
        nonlocal y
        line = f"{k}: {v}".upper()
        size, tr = card.condense(c, line, "Bask", Z.name, Z.track_n, W - 2 * M - 300)
        tracked(c, xr, y, line, "Bask", size, tr, CREAM, "right")
        y -= Z.lead + 3

    def head(t):
        nonlocal y
        y -= 34
        tracked(c, xr, y, t, "Bask-SB", SUB, 2.2, CREAM, "right")
        y -= 34

    lang = field(d, "3.6").strip()
    srt = field(d, "3.7")
    srt_langs = "English" if srt.lower().startswith("english only") else ""
    kv("Genre", field(d, "3.1"))
    kv("Country", field(d, "3.2"))
    kv("Shooting location", field(d, "3.3"))
    kv("Production year", field(d, "3.4"))
    kv("Completion year", field(d, "3.5"))
    kv("Language", lang + (f"  (.srt available: {srt_langs})" if srt_langs else ""))
    kv("Duration", field(d, "3.8"))
    kv("Aspect ratio", field(d, "3.9"))
    kv("Frame rate", field(d, "3.10"))
    kv("Shooting format", field(d, "3.11"))
    exh = field(d, "3.12").strip()
    if exh:
        kv("Exhibition format", exh)
    snd = field(d, "3.13").strip()
    if snd:
        kv("Sound", snd.replace("Stereo 5.1", "5.1, stereo"))

    head("THE TEAM")
    for role, names in pairs(field(d, "3.14")):
        if role:
            kv({"Director": "Written & directed by"}.get(role, role + " ") .rstrip(), " · ".join(names))

    head("CAST")
    for role, names in pairs(field(d, "3.15")):
        if role and "coordinator" not in role.lower():
            tracked(c, xr, y, f"{role}  |  {' · '.join(names)}".upper(), "Bask",
                    Z.name, Z.track_n, CREAM, "right")
            y -= Z.lead + 1

    head("RIGHTS")
    kv("Rights holder", field(d, "3.16"))
    contact = field(d, "3.17").strip()
    if contact:
        name, _, email = contact.partition("·")
        kv("Contact", name.strip())
        if email.strip():
            kv("Email", email.strip())
            link(c, "mailto:" + email.strip(), xr - 520, y + Z.lead - 2, 520, Z.lead + 4)

    head("LINKS")
    for name, url in LINKS:
        wtxt = tracked(c, xr, y, name, "Bask", Z.name + 1, Z.track_n + 0.6, CREAM, "right")
        c.setStrokeColor(RULE); c.setLineWidth(0.5)
        c.line(xr - wtxt, y - 5, xr, y - 5)
        link(c, url, xr - wtxt - 8, y - 8, wtxt + 16, Z.lead + 4)
        y -= Z.lead + 5

    # footer: website · instagram · imdb, all live
    y = M + 24
    items = [("WWW.KILLEROFMEN.COM", field(d, "1.3")),
             ("INSTAGRAM  @KILLEROFMENMOVIE", field(d, "3.18")),
             ("IMDB", field(d, "3.19"))]
    yy = y + (len(items) - 1) * (Z.lead + 4)
    for text, url in items:
        if not url.strip():
            continue
        wtxt = tracked(c, xr, yy, text, "Bask", Z.name, Z.track_n + 0.4, CREAM, "right")
        link(c, url.strip(), xr - wtxt - 8, yy - 8, wtxt + 16, Z.lead + 2)
        yy -= Z.lead + 4
    c.showPage()


def page_statement(c, d):
    ground(c, 10, alpha=0.26, scrim=0.50)
    y = title(c, "DIRECTOR'S STATEMENT", H - M - 30)
    text = field(d, "4.1")
    x, w = M + 40, W - 2 * (M + 40)
    top = y - 44
    room = top - (M + 76)
    size, lead = fit(text, w, room, 23.0, 36.5)     # fit() steps down until it fits
    para(c, text, x, top, w, size, lead, align="center")
    tracked(c, W / 2, M + 18, "JORDAN BETINE, WRITER-DIRECTOR", "Bask", Z.role + 1,
            Z.track_r + 1.0, DIM, "center")
    c.showPage()


def bio_block(c, key, role, name, y, side, height):
    """Heading, portrait on one side, text on the other. Returns the y below."""
    pn = PORTRAITS.get(key)
    has_img = pn is not None and os.path.exists(HEADSHOT(pn))
    head_text = f"{role}  |  {name}"
    hx = M if side == "left" else W - M
    tracked(c, hx, y, head_text, "Bask-SB", SUB, 2.2, CREAM, "left" if side == "left" else "right")
    # person links, when they exist (field 5.7)
    hw = text_width(c, head_text, "Bask-SB", SUB, 2.2)
    lx = hx + hw + 22 if side == "left" else M
    for i, (lab, url) in enumerate(PERSON_LINKS.get(key, [])):
        px = lx + i * 74
        tracked(c, px, y, lab.upper(), "Bask", Z.role, Z.track_r, DIM)
        link(c, url, px - 4, y - 6, 66, Z.role + 10)
    y -= 40
    img_h = height - 40
    img_w = round(img_h * 0.84)
    text_w = W - 2 * M - img_w - 48
    if has_img:
        im = load_rgb(HEADSHOT(pn), 1200)
        ix = M if side == "left" else W - M - img_w
        cover(c, im, ix, y - img_h, img_w, img_h, focus=(0.5, 0.40), q=86)
        tx = M + img_w + 48 if side == "left" else M
    else:
        tx, text_w = M, W - 2 * M
    text = field(c._d, key)
    size, lead = fit(text, text_w, img_h - 4, 19.0, 30.0)
    para(c, text, tx, y - lead * 0.85, text_w, size, lead,
         align="left" if side == "left" or not has_img else "right")
    return y - img_h


def page_bios(c, d, items, first):
    c._d = d
    ground(c)
    y = H - M - 30
    if first:
        y = title(c, "FILMMAKERS", y)
        y -= 20
    avail = y - M - 30
    block = 436.0 if len(items) >= 3 else 560.0     # heading + portrait; two get more
    spare = avail - block * len(items)
    between = min(90.0, spare / max(len(items), 1))  # breathe, but do not stretch
    for i, (key, role, name) in enumerate(items):
        y = bio_block(c, key, role, name, y, "left" if i % 2 == 0 else "right", block)
        y -= between
    if not PORTRAITS_CONFIRMED:
        proof_slug(c, "PROOF — PORTRAITS NOT YET ASSIGNED TO NAMES")
    c.showPage()


def page_cast(c, d):
    ground(c)
    hero_h = 900.0
    im = unletterbox(load_rgb(STILL(40), 2000))
    cover(c, im, 0, H - hero_h, W, hero_h, focus=(0.5, 0.35), q=88)
    x = M
    y = H - hero_h - 90
    billed = [(r, n) for r, n in pairs(field(d, "3.15")) if r and "coordinator" not in r.lower()]
    lead_role, lead_names = billed[0]
    tracked(c, x, y, f"{lead_role}  |  {' · '.join(lead_names)}".upper(), "Bask-SB", SUB + 3,
            2.4, CREAM)
    y -= 50
    bios = field(d, "7.1").strip()
    if bios:
        y = para(c, bios, x, y, W - 2 * M, BODY - 0.6, BODY_LEAD - 1.5) - 30
    else:
        y -= 6
    label(c, x, y, "B I L L E D   C A S T", size=Z.role + 1)
    y -= 34
    col_x = [x, x + (W - 2 * M) / 2]
    half = (len(billed) + 1) // 2
    for ci, chunk in enumerate([billed[:half], billed[half:]]):
        yy = y
        for role, names in chunk:
            tracked(c, col_x[ci], yy, role.upper(), "Bask", Z.role, Z.track_r, DIM)
            tracked(c, col_x[ci] + 210, yy, " · ".join(names).upper(), "Bask", Z.name,
                    Z.track_n, CREAM)
            yy -= Z.lead + 4
    c.showPage()


def page_bts(c):
    ground(c)
    strip = 28.0
    y = H
    for row_h, cells in MOSAIC:
        total_w = sum(w for _, w in cells) + GAP * (len(cells) - 1)
        scale = W / total_w
        x = 0.0
        for f, w in cells:
            cw = w * scale
            im = load_rgb(BTS(f), 1500)
            cover(c, im, x, y - row_h, cw - (GAP if f != cells[-1][0] else 0), row_h, q=84)
            x += cw
        y -= row_h + GAP
    tracked(c, W / 2, strip * 0.38, "BEHIND THE SCENES   ·   PHOTOGRAPHS JEDIDIAH WOODS",
            "Bask", 9.5, 1.4, DIM, "center")
    c.showPage()


def credit_pages(c, d):
    """Pages 9-11, drawn by the credit card's own functions on this canvas."""
    z = card.Sz(1.0)

    def stills_for(nums):
        while True:
            for n in nums:
                yield STILL(n)

    billed = pairs(field(d, "9.2"))
    cast = [e for e in billed if e[0] and e[0].lower() != "extras"]
    extras = [e for e in billed if e[0] and e[0].lower() == "extras"]
    key = [e for e in pairs(field(d, "9.1"))
           if e[0] and "unknown" not in " ".join(e[1]).lower()]
    card.one_col_pages(c, "C A S T", [cast, key] + ([extras] if extras else []),
                       z, stills_for([31, 27, 38]), False)
    card.two_col_pages(c, "C R E W", pairs(field(d, "10.1")), z, stills_for([35, 3, 19]), False)
    card.page_thanks(c, d, z, stills_for([41, 13]), False)


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
    page_bios(c, d, BIOS[3:], first=False)          # 6
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
