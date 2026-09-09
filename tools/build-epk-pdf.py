#!/usr/bin/env python3
"""Rebuild press/EPK-breakdown.pdf from press/epk.json.

Run after epk.json changes so the PDF never drifts from the data:
    <venv>/bin/python tools/build-epk-pdf.py

Needs reportlab (this machine has no LibreOffice, pandoc or pdftoppm; reportlab
lives in the session scratch venv). Balances the eleven page-blocks across two
columns by total height, then draws the two footer blocks below whichever column
runs longer, so the layout survives fields being added.
"""
import json, os, sys
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit
except ImportError:
    sys.exit("reportlab not installed. pip install reportlab")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "press", "epk.json")
OUT = os.path.join(ROOT, "press", "EPK-breakdown.pdf")

INK = colors.HexColor("#14213d"); MUT = colors.HexColor("#6b7280"); RULE = colors.HexColor("#d7d3c8")
HAVE = colors.HexColor("#1e8f5a"); SELF = colors.HexColor("#2b7cb8"); BLK = colors.HexColor("#c07c12")
PAPER = colors.HexColor("#fbfaf6"); BODY = colors.HexColor("#2c2c2c")
COL = {"have": HAVE, "self": SELF, "blk": BLK}

# who holds each field: stable id -> (status, note). Keyed by id, not by the label —
# a label can be reworded, and a lookup that misses would silently downgrade a row.
# Status is overridden to "have" when epk.json carries a value, unless the field is
# blocked on a person.
HOLD = {
 "p1-key-art": ("have", "in the repo — press/assets/POSTER"), "p1-billing-block": ("have", "from the poster"),
 "p1-website-url": ("blk", "donate page — decide"), "p2-logline": ("have", "3 versions by destination"),
 "p2-synopsis": ("self", "3 drafts written — pick one"), "p2-hero-still": ("self", "pick from the 41 stills"),
 "p3-genre": ("have", ""), "p3-country": ("have", ""), "p3-shooting-location": ("have", ""),
 "p3-production-year": ("have", ""), "p3-completion-year": ("have", "vs © MMXXV on the crawl"),
 "p3-language": ("have", ""), "p3-subtitles": ("have", "EN srt + scc"), "p3-duration": ("have", ""),
 "p3-aspect-ratio": ("have", ""), "p3-frame-rate": ("have", ""), "p3-shooting-format": ("have", ""),
 "p3-exhibition-formats": ("blk", "You Wu"), "p3-sound": ("have", ""),
 "p3-heads-of-department": ("have", "from the poster"), "p3-cast-principals": ("have", "from the end credits"),
 "p3-rights-holder": ("have", ""), "p3-press-contact": ("self", "needs a name and email"),
 "p3-instagram": ("have", ""), "p3-imdb": ("have", ""), "p4-statement": ("have", "final draft — needs Jordan"),
 "p4-photo-behind": ("self", "pick from the 41 stills"), "p5-bio-director": ("have", "draft — 2 brackets for Jordan"),
 "p5-bio-producer": ("have", "from the website"), "p5-bio-cinematographer": ("self", 'credits list — needs the "why"'),
 "p5-bio-production-designer": ("have", "from the website"), "p5-bio-editor": ("have", "from the website"),
 "p5-headshots": ("have", "complete set — name the files"), "p5-links": ("self", "ask each person"),
 "p7-cast-bios": ("self", "names known — bios from IMDb"), "p7-stills-in-character": ("self", "pick from the 41 stills"),
 "p8-bts-photos": ("have", "102 originals in press/assets/BTS — pick 8-12"), "p9-key-credits": ("have", "sound designer still unknown"),
 "p9-full-cast": ("have", "from the end credits"), "p9-still-behind": ("self", "pick from the 41 stills"),
 "p10-full-crew": ("have", "12 blanks on the sheet"), "p11-thanks": ("have", "30 names — needs alphabetising"),
 "p11-partner-logos": ("self", "placeholders on the sheet"), "p11-afi-boilerplate": ("have", "director name mismatch"),
 "a-stills": ("have", "41 in press/assets/STILLS — pick 12"), "a-trailer": ("blk", "You Wu"),
 "a-laurels": ("self", "email the 3 festivals"), "a-drive-folders": ("have", "built — Drive, synced"),
 "a-intro": ("blk", "Jordan"), "a-screenings": ("have", ""),
}
ROW, HEAD, GAP = 9.4, 12.0, 6.5

def main():
    D = json.load(open(SRC, encoding="utf-8"))
    blocks, unknown = [], []
    for p in D["sections"]:
        rows = []
        for f in p["fields"]:
            if f["id"] not in HOLD: unknown.append(f["n"])
            st, note = HOLD.get(f["id"], ("self", ""))
            if f.get("waiting"):                      # the file's own record wins over the table
                st, note = "blk", f["waiting"]
            if f.get("value") and st != "blk": st = "have"
            rows.append((f["n"], f["label"], st, note))
        blocks.append((p["num"], p["name"], rows, HEAD + len(rows) * ROW + GAP))
    if unknown: print("WARNING: no holder recorded for " + ", ".join(unknown) + " — add them to HOLD")

    half = sum(b[3] for b in blocks) / 2
    c1, c2, run = [], [], 0
    for b in blocks:
        if run + b[3] / 2 <= half and not c2: c1.append(b); run += b[3]
        else: c2.append(b)

    W, H = letter; M = 0.5 * inch
    c = canvas.Canvas(OUT, pagesize=letter); c.setTitle("Killer of Men — EPK breakdown")
    c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    y = H - M
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 16.5); c.drawString(M, y - 4, "KILLER OF MEN — EPK breakdown")
    n = sum(len(p["fields"]) for p in D["sections"])
    c.setFont("Helvetica", 8.5); c.setFillColor(MUT)
    c.drawRightString(W - M, y - 3, f"{len(D['sections'])} sections · {n} fields · rev {D.get('rev')} · {D.get('updated','')[:10]}")
    y -= 17; c.setStrokeColor(INK); c.setLineWidth(1.1); c.line(M, y, W - M, y); y -= 13
    c.setFont("Helvetica", 8); lx = M
    for k, lab in (("have", "have it"), ("self", "you can get it — nobody blocking"), ("blk", "waiting on someone")):
        c.setFillColor(COL[k]); c.rect(lx, y - 1.5, 6, 6, fill=1, stroke=0)
        c.setFillColor(INK); c.drawString(lx + 9, y, lab); lx += c.stringWidth(lab, "Helvetica", 8) + 28
    y -= 14
    CW = (W - 2 * M - 18) / 2

    def draw(col, x, top):
        cy = top
        for secnum, name, rows, _ in col:
            c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.8); c.drawString(x, cy, f"{secnum}   {name}")
            cy -= 2.5; c.setStrokeColor(RULE); c.setLineWidth(0.5); c.line(x, cy, x + CW, cy); cy -= 8.6
            for n, lab, st, note in rows:
                c.setFillColor(COL[st]); c.rect(x, cy - 0.6, 4.5, 4.5, fill=1, stroke=0)
                c.setFillColor(MUT); c.setFont("Helvetica", 7.5); c.drawString(x + 8, cy, n)
                c.setFillColor(BODY); c.drawString(x + 30, cy, lab)
                if note:
                    c.setFillColor(MUT); c.setFont("Helvetica-Oblique", 6.7); c.drawRightString(x + CW, cy, note)
                cy -= ROW
            cy -= GAP
        return cy

    fy = min(draw(c1, M, y), draw(c2, M + CW + 18, y)) - 6
    c.setStrokeColor(INK); c.setLineWidth(1.1); c.line(M, fy, W - M, fy); fy -= 13
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.8); c.drawString(M, fy, "WHAT THE END CREDITS ANSWERED")
    c.setFont("Helvetica", 7.5); c.setFillColor(BODY)
    t = ("The end credits are in. They filled cast, full crew, executive producers, thanks and the AFI boilerplate. "
         "Three things they did NOT settle: no sound designer is named anywhere, the fellows list calls the director "
         "Jordan Uwhubetine where everything else says Jordan Betine, and the crawl is dated MMXXV against a 2026 completion.")
    for i, l in enumerate(simpleSplit(t, "Helvetica", 7.5, CW)): c.drawString(M, fy - 11 - i * 9.2, l)
    x2 = M + CW + 18
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.8); c.drawString(x2, fy, "NEXT, NEEDING NOBODY")
    c.setFont("Helvetica", 7.5); c.setFillColor(BODY)
    for i, l in enumerate(["1  Pick the pictures: hero, BTS mosaic, cast, credits", "2  Pick a synopsis",
                           "3  Rewrite your bio to answer 'why do you shoot'", "4  Ask Jordan: Betine or Uwhubetine?",
                           "5  Email the 3 festivals for laurels", "6  Find the sound designer"]):
        c.drawString(x2, fy - 11 - i * 9.2, l)
    c.setFillColor(MUT); c.setFont("Helvetica", 6.6)
    c.drawString(M, M - 8, "Killer of Men · AFI thesis · 13 min · full detail in press/epk-one-sheet.md")
    c.drawRightString(W - M, M - 8, "Still with You Wu: exhibition formats · the trailer · the masters · the DCP")
    c.showPage(); c.save()
    print(f"wrote {OUT} — {len(c1)}+{len(c2)} blocks, footer at y={fy:.0f}, margin {M:.0f}")
    if fy < M + 70: print("WARNING: footer is close to the bottom margin; content may be overflowing")

if __name__ == "__main__":
    main()
