#!/usr/bin/env python3
"""Build the credit cards as real Illustrator documents, with live editable text.

    <venv>/bin/python tools/build-credit-card-ai.py [--medium|--large] [--transparent]
                                                    [--out DIR]

It does NOT redraw the card. It replays build-credit-card.py's own layout against a
recording canvas, turns the recorded operations into an ExtendScript, and hands that to
Illustrator. So the .ai and the .pdf come out of one set of coordinates and cannot
disagree — which is the whole reason for doing it this way instead of by hand.

What lands in the .ai:
  * one artboard per page, at the EPK's 1296 x 1728 pt
  * layer TYPE      — every credit as live point text, Baskerville, tracked
  * layer BACKGROUND— the ground, the backdrop still and its scrim, locked
  * --transparent    omits the BACKGROUND layer entirely

Needs Adobe Illustrator installed; it is driven through AppleScript.
"""
import importlib.util, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

spec = importlib.util.spec_from_file_location("bcc", os.path.join(HERE, "build-credit-card.py"))
bcc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bcc)

from reportlab.pdfbase import pdfmetrics


class TextObj:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.font = "Bask"
        self.size = 12.0
        self.fill = "#000000"
        self.track = 0.0
        self.text = ""

    def setFont(self, f, s):
        self.font, self.size = f, s

    def setFillColor(self, c):
        self.fill = "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in (c.red, c.green, c.blue))

    def setCharSpace(self, t):
        self.track = t

    def textOut(self, s):
        self.text = s


class Recorder:
    """Mimics just enough of a reportlab canvas to capture what the layout draws."""

    def __init__(self):
        self.pages, self.ops = [], []
        self._fill = "#000000"
        self._stroke = "#000000"
        self._lw = 1.0
        self._alpha = 1.0
        self._stack = []

    # measurement is delegated, so line breaking matches the PDF exactly
    def stringWidth(self, s, font, size):
        return pdfmetrics.stringWidth(s, font, size)

    def setFont(self, *a):
        pass

    def setTitle(self, *a):
        pass

    def beginText(self, x, y):
        return TextObj(x, y)

    def drawText(self, t):
        if t.text.strip():
            self.ops.append(("text", t.x, t.y, t.text, t.font, t.size, t.track, t.fill))

    def setFillColor(self, c):
        self._fill = "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in (c.red, c.green, c.blue))

    def setStrokeColor(self, c):
        self._stroke = "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in (c.red, c.green, c.blue))

    def setLineWidth(self, w):
        self._lw = w

    def setFillAlpha(self, a):
        self._alpha = a

    def saveState(self):
        self._stack.append((self._fill, self._stroke, self._lw, self._alpha))

    def restoreState(self):
        if self._stack:
            self._fill, self._stroke, self._lw, self._alpha = self._stack.pop()

    def rect(self, x, y, w, h, fill=0, stroke=0):
        if fill:
            self.ops.append(("rect", x, y, w, h, self._fill, self._alpha))

    def line(self, x1, y1, x2, y2):
        self.ops.append(("line", x1, y1, x2, y2, self._stroke, self._lw))

    def drawImage(self, img, x, y, w, h, mask=None):
        path = getattr(img, "_kom_path", None)
        if path:
            self.ops.append(("image", x, y, w, h, path, self._alpha))

    def showPage(self):
        self.pages.append(self.ops)
        self.ops = []

    def save(self):
        if self.ops:
            self.pages.append(self.ops)
            self.ops = []


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def emit(pages, out_ai, transparent):
    W, H = bcc.W, bcc.H
    GAPX = GAPY = 120
    # Illustrator's canvas is 227in square and centred on the first artboard, so a
    # single row runs out of room at the seventh page (error 5001). Grid instead.
    COLS = 4

    def origin(i):
        return (i % COLS) * (W + GAPX), -((i // COLS) * (H + GAPY))
    L = []
    a = L.append
    a("#target illustrator")
    a("while (app.documents.length > 0) app.documents[0].close(SaveOptions.DONOTSAVECHANGES);")
    a("var W=%f, H=%f;" % (W, H))
    a("var doc = app.documents.add(DocumentColorSpace.RGB, W, H);")
    a("while (doc.artboards.length > 1) doc.artboards[1].remove();")
    a("doc.artboards[0].artboardRect = [0, 0, W, -H];")
    for i in range(1, len(pages)):
        ox, oy = origin(i)
        a("doc.artboards.add([%f, %f, %f, %f]);" % (ox, oy, ox + W, oy - H))
    a("""
function pickFont(want, fallbackContains) {
  try { return app.textFonts.getByName(want); } catch (e) {}
  for (var i = 0; i < app.textFonts.length; i++)
    if (app.textFonts[i].name.indexOf(fallbackContains) === 0) return app.textFonts[i];
  return app.textFonts[0];
}
var FONTS = { "Bask": pickFont("Baskerville", "Baskerville"),
              "Bask-SB": pickFont("Baskerville-SemiBold", "Baskerville") };
function rgb(hex) {
  var c = new RGBColor();
  c.red = parseInt(hex.substr(1,2),16); c.green = parseInt(hex.substr(3,2),16);
  c.blue = parseInt(hex.substr(5,2),16); return c;
}
var layType = doc.layers.add(); layType.name = "TYPE";
""")
    if not transparent:
        a('var layBg = doc.layers.add(); layBg.name = "BACKGROUND";')
        a("layBg.move(doc, ElementPlacement.PLACEATEND);")
    a("""
function T(layer, x, y, s, fontKey, size, track, hex) {
  var t = layer.textFrames.add();
  t.contents = s;
  var ca = t.textRange.characterAttributes;
  ca.textFont = FONTS[fontKey];
  ca.size = size;
  ca.tracking = Math.round(track / size * 1000);
  ca.fillColor = rgb(hex);
  t.paragraphs[0].paragraphAttributes.justification = Justification.LEFT;
  t.position = [x, y + size];   // AI positions a text frame by its top-left box corner

  return t;
}
function R(layer, x, y, w, h, hex, alpha) {
  var r = layer.pathItems.rectangle(y, x, w, h);
  r.stroked = false; r.filled = true; r.fillColor = rgb(hex); r.opacity = alpha * 100;
  return r;
}
function LN(layer, x1, y1, x2, y2, hex, lw) {
  var p = layer.pathItems.add();
  p.setEntirePath([[x1, y1], [x2, y2]]);
  p.filled = false; p.stroked = true; p.strokeColor = rgb(hex); p.strokeWidth = lw;
  return p;
}
function IMG(layer, path, x, y, w, h, alpha) {
  var f = new File(path);
  if (!f.exists) return null;
  var pl = layer.placedItems.add();
  pl.file = f;
  pl.width = w; pl.height = h;
  pl.position = [x, y];
  pl.opacity = alpha * 100;
  try { pl.embed(); } catch (e) {}
  return pl;
}
""")
    for pi, ops in enumerate(pages):
        ox, oy = origin(pi)
        for op in ops:
            kind = op[0]
            if kind == "text":
                _, x, y, s, font, size, track, fill = op
                # reportlab y is from the page bottom; Illustrator y is negative downward
                # tracked() already shifted x for alignment, so the recorded x is the
                # left edge of the drawn string; point text anchors there with LEFT.
                a('T(layType, %f, %f, "%s", "%s", %f, %f, "%s");'
                  % (ox + x, oy - (H - y), esc(s), font, size, track, fill))
            elif kind == "rect" and not transparent:
                _, x, y, w, h, fill, alpha = op
                a('R(layBg, %f, %f, %f, %f, "%s", %f);'
                  % (ox + x, oy - (H - (y + h)), w, h, fill, alpha))
            elif kind == "line":
                _, x1, y1, x2, y2, col, lw = op
                a('LN(layType, %f, %f, %f, %f, "%s", %f);'
                  % (ox + x1, oy - (H - y1), ox + x2, oy - (H - y2), col, lw))
            elif kind == "image" and not transparent:
                _, x, y, w, h, path, alpha = op
                a('IMG(layBg, "%s", %f, %f, %f, %f, %f);'
                  % (esc(path), ox + x, oy - (H - (y + h)), w, h, alpha))
    a('try { doc.layers.getByName("BACKGROUND").locked = true; } catch(e) {}')
    a('var out = new File("%s");' % esc(out_ai))
    a("var o = new IllustratorSaveOptions(); o.compatibility = Compatibility.ILLUSTRATOR17;")
    a("doc.saveAs(out, o);")
    a("doc.close(SaveOptions.DONOTSAVECHANGES);")
    a('var log = new File("%s"); log.open("w"); log.write("pages=%d"); log.close();'
      % (esc(out_ai + ".done"), len(pages)))
    return "\n".join(L)


def main():
    large = "--large" in sys.argv
    medium = "--medium" in sys.argv
    transparent = "--transparent" in sys.argv
    outdir = (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv
              else os.path.join(ROOT, "press", "illustrator"))
    os.makedirs(outdir, exist_ok=True)
    name = ("KillerOfMen_Credits"
            + ("_large" if large else "_medium" if medium else "")
            + ("_transparent" if transparent else "") + ".ai")
    out_ai = os.path.join(outdir, name)

    z = bcc.Sz(1.75 if large else 1.30 if medium else 1.0)
    d = bcc.load()

    # keep the backdrop bytes on disk so Illustrator can place them
    tmpdir = tempfile.mkdtemp(prefix="komcard-")
    real_unletterbox = bcc.unletterbox

    def recording_unletterbox(path):
        img = real_unletterbox(path)
        p = os.path.join(tmpdir, os.path.basename(path).replace(".png", ".jpg"))
        if not os.path.exists(p):
            from PIL import Image
            im = Image.open(path).convert("RGB")
            g = im.convert("L")
            w, h = g.size
            rows = [y for y in range(h) if g.crop((0, y, w, y + 1)).getextrema()[1] > 8]
            if rows and (rows[0] > 2 or rows[-1] < h - 3):
                im = im.crop((0, rows[0], w, rows[-1] + 1))
            im.thumbnail((1600, 1600), Image.LANCZOS)
            im.save(p, "JPEG", quality=78, optimize=True)
        img._kom_path = p
        return img

    bcc.unletterbox = recording_unletterbox

    c = Recorder()
    pool = sorted(f for f in os.listdir(bcc.BG) if f.endswith(".png"))

    def pick(n):
        for st in pool:
            if st.endswith(f"1.1.{n}.png"):
                return os.path.join(bcc.BG, st)
        return None

    def stills_for(nums):
        while True:
            for n in nums:
                yield pick(n)

    billed = bcc.pairs(bcc.field(d, "9.2"))
    cast = [e for e in billed if e[0] and e[0].lower() != "extras"]
    extras = [e for e in billed if e[0] and e[0].lower() == "extras"]
    key = [e for e in bcc.pairs(bcc.field(d, "9.1"))
           if e[0] and "unknown" not in " ".join(e[1]).lower()]
    bcc.one_col_pages(c, "C A S T", [cast, key] + ([extras] if extras else []),
                      z, stills_for([31, 27, 38]), transparent)
    crew = bcc.pairs(bcc.field(d, "10.1"))
    if z.stacked:
        bcc.one_col_pages(c, "C R E W", [crew], z, stills_for([35, 3, 19]), transparent)
    else:
        bcc.two_col_pages(c, "C R E W", crew, z, stills_for([35, 3, 19]), transparent)
    bcc.page_thanks(c, d, z, stills_for([41, 13]), transparent)
    c.save()

    jsx = emit(c.pages, out_ai, transparent)
    jsx_path = os.path.join(tmpdir, "build.jsx")
    open(jsx_path, "w", encoding="utf-8").write(jsx)
    scpt = os.path.join(tmpdir, "run.applescript")
    # AppleScript's default reply timeout is two minutes; ten artboards of text take
    # longer than that, and the failure looks like error -1712 rather than anything useful.
    open(scpt, "w").write(
        'set jsx to POSIX file "%s"\n'
        'with timeout of 3600 seconds\n'
        '  tell application id "com.adobe.illustrator"\n'
        '    activate\n    do javascript jsx\n  end tell\n'
        'end timeout\n' % jsx_path)
    done = out_ai + ".done"
    if os.path.exists(done):
        os.remove(done)
    print(f"{len(c.pages)} artboards -> {name}")
    r = subprocess.run(["osascript", scpt], capture_output=True, text=True, timeout=1800)
    if not os.path.exists(done):
        sys.exit("Illustrator did not report success.\n" + r.stdout + r.stderr)
    os.remove(done)
    print(f"  wrote {out_ai}  ({os.path.getsize(out_ai)/1048576:.2f} MB)")


if __name__ == "__main__":
    main()
