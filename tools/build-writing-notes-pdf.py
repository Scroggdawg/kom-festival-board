#!/usr/bin/env python3
"""Rebuild press/joan-writing-notes.pdf — the writing notes from the Joan call.

Everything Joan said about the WORDS on the FilmFreeway page: logline, director
bio, director statement, and the wording rules around them. Source of truth is
meetings/2026-09-06-joan-call.md (§A, §C.1-C.3, §C.8, §C.12, §D.2.1, §F.9, §G).

One page, two columns, no commentary. Quotes are verbatim from the call; anything
that is not a quote is a note, and the section reference is on every block so any
line can be traced back.

    python3 tools/build-writing-notes-pdf.py
"""
import os, sys
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit
except ImportError:
    sys.exit("reportlab not installed")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "press", "joan-writing-notes.pdf")

INK, MUTE, RULE, QUOTE = colors.HexColor("#171310"), colors.HexColor("#6b625c"), colors.HexColor("#c9c1b8"), colors.HexColor("#5a5049")
W, H = letter
M, GUT = 0.55 * inch, 0.30 * inch
COL = (W - 2 * M - GUT) / 2

# (heading, section ref, [ ("n"|"q", text), ... ])   n = note, q = verbatim quote
BLOCKS = [
 ("The sentence the whole call is about", "§A", [
  ("q", "The application and the film itself are two different mediums. And our application, our submission is not as strong as our film right now. And so it needs to match it at least."),
  ("n", "Luke. Joan: “Exactly.” Every writing note below is that one claim applied to a field. It also reframes the rejections as feedback on the application, not a verdict on the film."),
  ("q", "you guys have a really strong film."),
  ("n", "Her critique was aimed entirely at the application."),
 ]),
 ("Logline", "§C.1", [
  ("n", "Names neither when nor where — though two chosen categories promise both:"),
  ("q", "historical means when and southern means where"),
  ("n", "Rewrite as marketing copy, not a plot summary. Shorter front half. Title in caps. Base it on the thesis-film sentence taken out of the bio."),
  ("n", "KEEP this clause — “igniting a reckoning with guilt, faith, and the violence shaping his life and identity”:"),
  ("q", "that's good. I like that."),
  ("n", "Redirected instinct (§G.11): a factual logline. The page was accurate; accuracy was not the problem."),
 ]),
 ("Director bio", "§C.2", [
  ("q", "so goddamn wordy."),
  ("n", "Lead with the MFA line. Cut “six short films across genres” — it reads as if that is all he has done:"),
  ("q", "He has directed some other stuff"),
  ("n", "Cut the thesis-film sentence; it becomes the logline. Then add the thing that is missing:"),
  ("q", "Why does he direct? … Why should I as a film festival get excited about you as a film director?"),
  ("n", "The first-time-filmmaker box is ticked and CONTRADICTS the bio (\u00a7C.10). Joan: \u201cNot a first time filmmaker, but if that's what Jordan wants to market himself, okay.\u201d Jordan's call \u2014 but the two cannot both stand."),
  ("n", "The why-test is not only Jordan's (\u00a7D.4.5): every bio in the EPK gets it, each person writing their own, including Luke's cinematographer bio."),
 ]),
 ("Director statement", "§C.3", [
  ("q", "This is a director's statement. It's fine."),
  ("n", "The changes are structural, not line edits:"),
  ("n", "• P1 stays."),
  ("n", "• Move P6 (“Killer of Men is an expression of pain…”) up to paragraph 2, so the film is introduced before the Mandingo concept."),
  ("n", "• Fold P4 into P3 — repetitive."),
  ("n", "• Replace “slavery times” with “during the period of American slavery”:"),
  ("q", "it is still slavery times"),
  ("n", "• P5, the spirituality paragraph, goes last."),
  ("n", "• Real paragraph breaks."),
  ("n", "Optional: “death by a million needles”. The height line is “a quibble”. P7 (Oriki) was never discussed — placement is Luke's call."),
 ]),
 ("Synopsis", "—", [
  ("n", "NOT DISCUSSED ON THE CALL. The synopsis appears once in the whole transcript, as one item in the delivery folder (§B.3): “Synopsis, credits & director bio”. It is a deliverable Joan expects to exist; she gave no guidance on writing it. Any synopsis rule this campaign follows came from somewhere else and should not be attributed to her."),
 ]),
 ("Wording rules elsewhere on the page", "§C.8, §C.12", [
  ("n", "Screenings & awards is empty. List ABFF 2026, Martha's Vineyard 2026, SCAD Savannah 2026 — not the AFI showcase:"),
  ("q", "It's not a premiere"),
  ("n", "Verify the phrase “Oscar-qualifying” against each festival before using it."),
  ("n", "News & reviews is empty:"),
  ("q", "we also need to get some fucking news and reviews in on this shit"),
 ]),
 ("How the writing gets approved", "§D.2.1, §F.9", [
  ("n", "Send Jordan the logline, bio and statement together with the scope of the page changes. He approves the direction and the principle once; Luke then edits without per-change sign-off, and Jordan can raise anything at any time."),
  ("q", "I'm not going to get every bit approved, but just the first time around."),
 ]),
 ("Why the notes are shaped this way", "§G.2, §G.3", [
  ("n", "Joan reads from the programmer's chair. Her test is never “is this accurate” — it is “why would a festival get excited”. Every edit rotates the page to face the reader."),
  ("n", "And the thing an outside viewer remembers is the thing the page hides: unprompted, she named the surreal ancestral sequence as what sets the film apart. No still shows it, the logline mentions faith in passing, and the spirituality paragraph is buried mid-statement."),
 ]),
]

def measure(blocks, S):
    """Height of each block at body size S, so the columns can be balanced rather
    than guessed and the whole sheet can be auto-sized to fill exactly one page."""
    lead = S + 1.5
    out = []
    for head, ref, items in blocks:
        h = S + 5.5
        for kind, text in items:
            indent = 8 if kind == "q" else 0
            font = "Helvetica-Oblique" if kind == "q" else "Helvetica"
            body = ('\u201c' + text + '\u201d') if kind == "q" else text
            h += len(simpleSplit(body, font, S, COL - indent)) * lead + 3
        out.append((h + 7, head, ref, items))
    return out

def draw_block(c, x, y, head, ref, items, S):
    lead = S + 1.5
    c.setFillColor(INK); c.setFont("Helvetica-Bold", S + 1.2)
    c.drawString(x, y, head)
    c.setFillColor(MUTE); c.setFont("Helvetica", S - 0.8)
    c.drawRightString(x + COL, y, ref)
    y -= 3.5
    c.setStrokeColor(RULE); c.setLineWidth(0.4); c.line(x, y, x + COL, y)
    y -= lead
    for kind, text in items:
        if kind == "q":
            c.setFont("Helvetica-Oblique", S); c.setFillColor(QUOTE); indent = 8
            lines_ = simpleSplit("\u201c" + text + "\u201d", "Helvetica-Oblique", S, COL - indent)
            c.setStrokeColor(RULE); c.setLineWidth(1.1)
            c.line(x + 2, y + S - 2, x + 2, y + S - 2 - len(lines_) * lead + 2)
        else:
            c.setFont("Helvetica", S); c.setFillColor(INK); indent = 0
            lines_ = simpleSplit(text, "Helvetica", S, COL)
        for ln in lines_:
            c.drawString(x + indent, y, ln); y -= lead
        y -= 3
    return y - 7


SUB = ("Everything Joan said about the words on the FilmFreeway page. Call of September 6, 2026, "
       "about 90 minutes. Italics are verbatim from the call; everything else is a note. "
       "Section refs trace to meetings/2026-09-06-joan-call.md.")
FOOT = ("Source: meetings/2026-09-06-joan-call.md \u00b7 Quotes are machine-transcribed and unattributed; "
        "speaker inferred \u00b7 Built by tools/build-writing-notes-pdf.py")

def best_split(measured):
    """Split point that minimises the TALLER column, since that is what caps the
    body size. Two earlier attempts were worse: cutting at the first block past
    half the total put four tall blocks left and four short right, and minimising
    the gap between columns optimised the wrong quantity. Reading order survives
    either way -- the split is always a single cut through the block sequence."""
    best, cut = None, 1
    for i in range(1, len(measured)):
        a = sum(m[0] for m in measured[:i]); b = sum(m[0] for m in measured[i:])
        tall = max(a, b)          # the TALLER column is what sets the type size,
        if best is None or tall < best:   # so minimise that, not the gap
            best, cut = tall, i
    return cut

def layout(S, draw=False, c=None):
    """Lowest y either column reaches at body size S. Drawing is optional so the
    size search can measure without emitting anything."""
    y = H - M
    if draw:
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 15)
        c.drawString(M, y, "Killer of Men \u2014 the writing notes")
    y -= 16
    if draw:
        c.setFillColor(MUTE); c.setFont("Helvetica", S - 0.4)
    for ln in simpleSplit(SUB, "Helvetica", S - 0.4, W - 2 * M):
        if draw: c.drawString(M, y, ln)
        y -= S + 1.5
    y -= 3
    if draw:
        c.setStrokeColor(INK); c.setLineWidth(0.8); c.line(M, y, W - M, y)
    y -= 15

    measured = measure(BLOCKS, S)
    cut = best_split(measured)
    ends = []
    for col, chunk in ((0, measured[:cut]), (1, measured[cut:])):
        x = M + col * (COL + GUT)
        yy = y
        for h, head, ref, items in chunk:
            if draw: yy = draw_block(c, x, yy, head, ref, items, S)
            else: yy -= h
        ends.append(yy)
    return min(ends)

def main():
    FOOT_SPACE = 24
    S = 7.0
    for cand in [x / 10 for x in range(70, 121)]:
        if layout(cand) - FOOT_SPACE >= M: S = cand
        else: break

    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle("Killer of Men \u2014 writing notes from the Joan call")
    bottom = layout(S, draw=True, c=c)

    foot = bottom - 4
    c.setStrokeColor(RULE); c.setLineWidth(0.4); c.line(M, foot, W - M, foot)
    c.setFillColor(MUTE); c.setFont("Helvetica", max(6.2, S - 1.6))
    c.drawString(M, foot - 10, FOOT)
    c.showPage(); c.save()
    print(f"wrote {OUT}")
    print(f"  body {S}pt | columns end at {round(bottom)} | footer at {round(foot-10)} | floor {round(M)}")
    if foot - 10 < M - 6:
        print("  OVERFLOW"); return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
