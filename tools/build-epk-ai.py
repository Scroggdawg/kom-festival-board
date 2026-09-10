#!/usr/bin/env python3
"""Build the KILLER OF MEN press kit as an Adobe Illustrator project on the Drive, with
every image LINKED to its master in the Drive press folder (never embedded, never a
local copy), and export the PDF from it.

    <venv>/bin/python tools/build-epk-ai.py [--jsx-only] [--no-pdf]

What lands in  ~/Google Drive/My Drive/KILLER OF MEN/05 MARKETING/00 PRESS/Illustrator Projects/
    KillerOfMen_EPK.ai                                   eleven artboards; layers Images and Type
    KillerOfMen_EPK_<HHMM>_<DDMMYYYY>_compressed.pdf     exported from the .ai, links added after
and a copy of the PDF in press/.

It does NOT lay the pages out. tools/build-epk-kit.py does, once, for the reportlab PDF.
This tool replays that layout against a recording canvas: every text run, rule, link and
image placement the kit draws is captured as an operation, written into an ExtendScript
as a JavaScript literal, and handed to Illustrator through osascript. So the .ai, its PDF
and the reportlab PDF come out of one set of coordinates and cannot disagree.

Illustrator places each image as a link to the Drive path (the repo path the kit uses is
mapped to its Drive twin; the four headshots map to the named copies Luke made), crops it
with a clipping mask, sets the type in Baskerville with a fit loop as a second guard, saves
the .ai, then saves a PDF. Illustrator has no hyperlinks, so the recorded link rectangles
are written into the PDF as annotations with pypdf.

Gotchas that cost time (see also the memory note): the canvas is ~16,000 pt square and
centred on the origin, so the boards sit in a 4 x 3 grid; boards need a 1,600 pt gap or a
cover-fit image spills onto the neighbour's PDF page; PDFSaveOptions ignores its dpi
values unless a downsampling METHOD is set; pdfCompatible=false keeps the .ai small.
"""
import datetime, importlib.util, json, os, subprocess, sys, time

from PIL import Image
from reportlab.pdfgen import canvas as rl_canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESS = os.path.join(ROOT, "press")
ASSETS = os.path.join(PRESS, "assets")
DRIVE = os.path.expanduser("~/Google Drive/My Drive/KILLER OF MEN/05 MARKETING/00 PRESS")
OUT_DIR = os.path.join(DRIVE, "Illustrator Projects")
AI_PATH = os.path.join(OUT_DIR, "KillerOfMen_EPK.ai")
SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".epk-ai-build")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


kit = _load("kit", os.path.join(ROOT, "tools", "build-epk-kit.py"))
card = kit.card
W, H, M = kit.W, kit.H, kit.M

# Space between artboards. A full-page still placed cover-fit is about 4,100 pt wide
# before its clipping mask, so it reaches ~1,400 pt past the board on each side.
GAPX = 1600.0
FONT = {"Bask": "Baskerville", "Bask-SB": "Baskerville-SemiBold"}
ARTBOARDS = ["01 Poster", "02 Logline", "03 Programmer", "04 Statement", "05 Filmmakers",
             "06 Filmmakers", "07 Cast", "08 Behind the scenes", "09 Cast credits", "10 Crew", "11 Thanks"]

# The repo's numbered headshots and the named copies on the Drive are byte-identical
# (checked by md5, 2026-09-09). The .ai links the named ones.
HEADSHOT_DRIVE = {
    "KOM Headshots v3-1.jpg": "Editor_You_Wu.jpg",
    "KOM Headshots v3-2.jpg": "Producer_Ruoxiao_Li .jpg",
    "KOM Headshots v3-3.jpg": "Production_Designer_Rajarajeshwari_aka_RJ_Ragampudi.jpg",
    "KOM Headshots v3-4.jpg": "Cinematographer_Luke_Scroggins.jpg",
}


def to_drive(path):
    """The kit reads from press/assets; the .ai must link the Drive twin."""
    rel = os.path.relpath(path, ASSETS)
    folder, name = os.path.split(rel)
    if folder == "HEADSHOTS":
        name = HEADSHOT_DRIVE.get(name, name)
    out = os.path.join(DRIVE, folder, name)
    if not os.path.exists(out):
        raise FileNotFoundError(f"not on the Drive: {out}")
    return out


def rgb(c):
    return [int(round(c.red * 255)), int(round(c.green * 255)), int(round(c.blue * 255))]


_measure = rl_canvas.Canvas(os.devnull, pagesize=(W, H))
_rows = {}


def picture_rows(path):
    """Fractions (top, bottom) of a frame that hold picture: the stills carry their
    letterbox bars in the pixels. Detected per file, cached."""
    if path not in _rows:
        g = Image.open(path).convert("L")
        w, h = g.size
        rows = [y for y in range(h) if g.crop((0, y, w, y + 1)).getextrema()[1] > 8]
        _rows[path] = (rows[0] / h, (rows[-1] + 1) / h) if rows else (0.0, 1.0)
    return _rows[path]


# ---------- the recorded operations ----------
class Ops:
    """Page-local coordinates, y up from the page foot. An image box is (x, top, w, h)."""
    def __init__(self):
        self.ops, self.links, self.page = [], [], 0

    def new_page(self):
        self.page += 1

    def rect(self, x, top, w, h, fill, opacity=None):
        op = {"op": "rect", "p": self.page, "x": x, "top": top, "w": w, "h": h, "fill": fill}
        if opacity is not None:
            op["opacity"] = opacity
        self.ops.append(op)

    def image(self, path, box, region=(0, 0, 1, 1), focus=(0.5, 0.5), opacity=1.0, fit="cover"):
        x, top, w, h = box
        self.ops.append({"op": "image", "p": self.page, "file": path, "x": x, "top": top, "w": w,
                         "h": h, "region": list(region), "focus": list(focus),
                         "opacity": opacity, "fit": fit})

    def area(self, text, x, top, w, h, font, size, lead, fill, align, gap):
        self.ops.append({"op": "area", "p": self.page, "text": text, "x": x, "top": top, "w": w,
                         "h": h, "font": FONT[font], "size": size, "lead": lead, "fill": fill,
                         "align": align, "min": max(9.0, size - 4.0), "gap": gap})

    def point(self, text, x, y, font, size, track, fill):
        self.ops.append({"op": "point", "p": self.page, "text": text, "x": x, "y": y,
                         "font": FONT[font], "size": size, "fill": fill,
                         "track": (track / size) * 1000.0 if size else 0})

    def rule(self, x1, y1, x2, y2, width, stroke):
        self.ops.append({"op": "rule", "p": self.page, "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                         "w": width, "stroke": stroke})

    def link(self, url, x0, y0, x1, y1):
        self.links.append({"p": self.page, "url": url, "rect": [x0, y0, x1, y1]})


class Recorder:
    """Stands in for the reportlab canvas the kit and the card draw on. Fill colour and
    alpha are tracked so a ground drawn natively (rect, drawImage, rect) is recorded as
    it is drawn, whatever recipe the card uses."""
    def __init__(self, o):
        self.o = o
        self._stroke, self._lw = rgb(kit.RULE), 0.7
        self._fill, self._alpha = rgb(kit.GROUND), 1.0
        self._stack = []

    def stringWidth(self, s, font, size):
        return _measure.stringWidth(s, font, size)

    def setStrokeColor(self, c): self._stroke = rgb(c)
    def setLineWidth(self, w): self._lw = w
    def line(self, x1, y1, x2, y2): self.o.rule(x1, y1, x2, y2, self._lw, self._stroke)

    def linkURL(self, url, rect, relative=0, thickness=0):
        self.o.link(url, *rect)

    def setFillColor(self, c): self._fill = rgb(c)
    def setFillAlpha(self, a): self._alpha = float(a)
    def saveState(self): self._stack.append((self._fill, self._alpha, self._stroke, self._lw))
    def restoreState(self):
        if self._stack:
            self._fill, self._alpha, self._stroke, self._lw = self._stack.pop()

    def rect(self, x, y, w, h, fill=0, stroke=1, **k):
        if fill:
            self.o.rect(x, y + h, w, h, self._fill, None if self._alpha >= 1 else self._alpha)

    def drawImage(self, im, x, y, w, h, **kw):
        """An image object must say where it came from (.path) and which fraction of the
        frame is shown (.region); the .ai links the Drive twin of that path. The poster on
        page 1 is drawn whole (contain); anything else is a cover-fit crop."""
        if not hasattr(im, "path"):
            raise TypeError("drawImage received an image with no .path; the .ai cannot link it")
        region = getattr(im, "region", (0.0, 0.0, 1.0, 1.0))
        fit = "contain" if abs((w / h) - ((region[2] - region[0]) * im.size[0])
                               / ((region[3] - region[1]) * im.size[1])) < 0.01 else "cover"
        self.o.image(to_drive(im.path), (x, y + h, w, h), region=region, opacity=self._alpha, fit=fit)

    def showPage(self): pass
    def setFont(self, *a): pass


def install(o):
    """Point the kit's and the card's drawing primitives at the recorder."""
    def load_rgb(path, maxpx=1800):
        im = Image.open(path)                            # lazy: size only, no pixels
        im.path, im.region = path, (0.0, 0.0, 1.0, 1.0)
        return im

    def unletterbox(im):
        r0, r1 = picture_rows(im.path)
        im.region = (0.0, r0, 1.0, r1)
        return im

    def reader(im, q=84):
        return im

    def cover(c, im, x, y, w, h, alpha=1.0, focus=(0.5, 0.5), q=84):
        o.image(to_drive(im.path), (x, y + h, w, h), region=im.region, focus=focus, opacity=alpha)

    def ground(c, still_n=None, alpha=0.16, scrim=0.55, focus=(0.5, 0.5)):
        o.new_page()
        o.rect(0, H, W, H, rgb(kit.GROUND))
        if still_n is not None:
            path = to_drive(kit.STILL(still_n))
            r0, r1 = picture_rows(path)
            o.image(path, (0, H, W, H), region=(0, r0, 1, r1), focus=focus, opacity=alpha)
            o.rect(0, H, W, H, rgb(kit.GROUND), opacity=scrim)

    def card_ground(c, still=None, transparent=False):
        """Used only while the card's own ground() hands drawImage an anonymous buffer.
        Once the card publishes GROUND_RECIPE and images that carry .path/.region (the
        contract agreed with the card session, 2026-09-09), its ground() runs natively
        through the Recorder and this stand-in is not installed."""
        o.new_page()
        o.rect(0, H, W, H, rgb(kit.GROUND))
        if still:
            path = to_drive(still)
            r0, r1 = picture_rows(path)
            o.image(path, (0, H, W, H), region=(0, r0, 1, r1), opacity=0.16)
            o.rect(0, H, W, H, rgb(kit.GROUND), opacity=0.55)

    _card_ground_native = card.ground

    def card_ground_native(c, still=None, transparent=False):
        o.new_page()
        _card_ground_native(c, still, transparent)

    def tracked(c, x, y, s, font, size, track, fill, align="left"):
        wd = _measure.stringWidth(s, font, size) + track * max(len(s) - 1, 0)
        lx = x - wd if align == "right" else x - wd / 2.0 if align == "center" else x
        o.point(s, lx, y, font, size, track, rgb(fill))
        return wd

    def para(c, text, x, y, width, size=kit.BODY, lead=kit.BODY_LEAD, color=kit.CREAM,
             align="left", font="Bask", gap=None):
        g = lead * 0.6 if gap is None else gap
        h = kit.para_height(text, width, size, lead, font, g)
        o.area(text, x, y + size * 0.78, width, h + lead, font, size, lead, rgb(color), align, g)
        return y - h

    kit.load_rgb, kit.unletterbox, kit.reader = load_rgb, unletterbox, reader
    kit.cover, kit.ground, kit.tracked, kit.para = cover, ground, tracked, para
    card.tracked = tracked
    # A card that publishes its ground recipe draws its own ground through the Recorder;
    # the older card gets the stand-in that knows its one recipe.
    card.ground = card_ground_native if hasattr(card, "GROUND_RECIPE") else card_ground


def record():
    o = Ops()
    install(o)
    c = Recorder(o)
    d = card.load()
    kit.page_poster(c)
    kit.page_logline(c, d)
    kit.page_programmer(c, d)
    kit.page_statement(c, d)
    kit.page_bios(c, d, kit.BIOS[:3], first=True)
    kit.page_bios(c, d, kit.BIOS[3:], first=False)
    kit.page_cast(c, d)
    kit.page_bts(c)
    kit.credit_pages(c, d)
    assert o.page == len(ARTBOARDS), f"expected {len(ARTBOARDS)} pages, recorded {o.page}"
    return o


# ---------- ExtendScript ----------
JSX = r"""
(function () {
  var CFG = __CFG__;
  var OPS = __OPS__;
  var log = new File(CFG.log); log.open("w");
  function L(s) { log.writeln(s); }
  function rgb(a) { var c = new RGBColor(); c.red = a[0]; c.green = a[1]; c.blue = a[2]; return c; }
  function ax(p) { return CFG.x0 + (p % CFG.cols) * CFG.strideX; }
  function ay(p) { return CFG.y0 - Math.floor(p / CFG.cols) * CFG.strideY; }   // top edge
  function X(op, x) { return x + ax(op.p); }
  function Y(op, y) { return y + ay(op.p) - CFG.H; }
  function overflows(tf) {
    var n = tf.lines.length; if (n === 0) return tf.characters.length > 0;
    var last = tf.lines[n - 1];
    var end = last.characters[last.characters.length - 1].characterOffset;
    return end + 2 < tf.characters.length;
  }
  try {
    app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
    var doc = app.documents.add(DocumentColorSpace.RGB, CFG.W, CFG.H);
    for (var a = 0; a < CFG.names.length; a++) {
      var rect = [ax(a), ay(a), ax(a) + CFG.W, ay(a) - CFG.H];
      var ab = (a === 0) ? doc.artboards[0] : doc.artboards.add(rect);
      ab.artboardRect = rect;
      ab.name = CFG.names[a];
    }
    var LI = doc.layers[0]; LI.name = "Images";
    var LT = doc.layers.add(); LT.name = "Type";
    var fonts = {};
    function font(n) { if (!fonts[n]) fonts[n] = app.textFonts.getByName(n); return fonts[n]; }
    for (var i = 0; i < OPS.length; i++) {
      var op = OPS[i]; op.p = op.p - 1;
      if (op.op === "rect") {
        var r = LI.pathItems.rectangle(Y(op, op.top), X(op, op.x), op.w, op.h);
        r.filled = true; r.fillColor = rgb(op.fill); r.stroked = false;
        if (op.opacity !== undefined) r.opacity = op.opacity * 100;
      } else if (op.op === "image") {
        var img = LI.placedItems.add();
        img.file = new File(op.file);
        var nw = img.width, nh = img.height;
        var reg = op.region;
        var rw = nw * (reg[2] - reg[0]), rh = nh * (reg[3] - reg[1]);
        var s = (op.fit === "contain") ? Math.min(op.w / rw, op.h / rh) : Math.max(op.w / rw, op.h / rh);
        img.width = nw * s; img.height = nh * s;
        var rx = reg[0] * nw * s, ry = reg[1] * nh * s;
        var ox = (rw * s - op.w) * op.focus[0], oy = (rh * s - op.h) * op.focus[1];
        img.position = [X(op, op.x) - rx - ox, Y(op, op.top) + ry + oy];
        if (op.opacity < 1) img.opacity = op.opacity * 100;
        var g = LI.groupItems.add();
        var clip = LI.pathItems.rectangle(Y(op, op.top), X(op, op.x), op.w, op.h);
        clip.filled = false; clip.stroked = false;
        clip.move(g, ElementPlacement.PLACEATBEGINNING);
        img.move(g, ElementPlacement.PLACEATEND);
        clip.clipping = true; g.clipped = true;
        g.name = op.file.replace(/^.*\//, "");
      } else if (op.op === "area") {
        var frame = LT.pathItems.rectangle(Y(op, op.top), X(op, op.x), op.w, op.h);
        var tf = LT.textFrames.areaText(frame);
        tf.contents = op.text.replace(/\n\s*\n/g, "\r").replace(/\n/g, " ");
        var ca = tf.textRange.characterAttributes;
        ca.textFont = font(op.font); ca.size = op.size; ca.autoLeading = false; ca.leading = op.lead;
        ca.tracking = 0; ca.fillColor = rgb(op.fill);
        var pa = tf.textRange.paragraphAttributes;
        pa.justification = op.align === "center" ? Justification.CENTER : op.align === "right" ? Justification.RIGHT : Justification.LEFT;
        pa.spaceAfter = op.gap; pa.everyLineComposer = false;
        var size = op.size;
        for (var k = 0; k < 40 && overflows(tf) && size > op.min; k++) {
          size -= 0.5; ca.size = size; ca.leading = size * (op.lead / op.size);
        }
        if (overflows(tf)) L("OVERFLOW page " + (op.p + 1) + " at " + size + "pt: " + op.text.substring(0, 40));
        else if (size !== op.size) L("stepped page " + (op.p + 1) + " " + op.size + " -> " + size);
      } else if (op.op === "point") {
        var pt = LT.textFrames.pointText([X(op, op.x), Y(op, op.y)]);
        pt.contents = op.text;
        var pca = pt.textRange.characterAttributes;
        pca.textFont = font(op.font); pca.size = op.size; pca.tracking = op.track; pca.fillColor = rgb(op.fill);
        pt.textRange.paragraphAttributes.justification = Justification.LEFT;
      } else if (op.op === "rule") {
        var ln = LT.pathItems.add();
        ln.setEntirePath([[X(op, op.x1), Y(op, op.y1)], [X(op, op.x2), Y(op, op.y2)]]);
        ln.filled = false; ln.stroked = true; ln.strokeWidth = op.w; ln.strokeColor = rgb(op.stroke);
      }
      if ((i + 1) % 100 === 0) L("ops " + (i + 1) + "/" + OPS.length);
    }
    L("ops done " + OPS.length);
    var so = new IllustratorSaveOptions();
    so.compatibility = Compatibility.ILLUSTRATOR17; so.pdfCompatible = false;
    so.embedLinkedFiles = false; so.embedICCProfile = false; so.compressed = true;
    doc.saveAs(new File(CFG.ai), so);
    L("saved ai " + CFG.ai);
    if (CFG.pdf) {
      var po = new PDFSaveOptions();
      po.compatibility = PDFCompatibility.ACROBAT7; po.preserveEditability = false;
      po.generateThumbnails = false; po.optimization = true; po.viewAfterSaving = false;
      po.saveMultipleArtboards = true; po.artboardRange = "";
      po.colorDownsamplingMethod = DownsampleMethod.BICUBICDOWNSAMPLE;
      po.colorDownsampling = 200; po.colorDownsamplingImageThreshold = 260;
      po.colorCompression = CompressionQuality.JPEGHIGH;
      po.grayscaleDownsamplingMethod = DownsampleMethod.BICUBICDOWNSAMPLE;
      po.grayscaleDownsampling = 200; po.grayscaleDownsamplingImageThreshold = 260;
      po.grayscaleCompression = CompressionQuality.JPEGHIGH;
      doc.saveAs(new File(CFG.pdf), po);
      L("saved pdf " + CFG.pdf);
    }
    doc.close(SaveOptions.DONOTSAVECHANGES);
    L("DONE");
  } catch (e) { L("ERR line " + e.line + ": " + e.message); }
  log.close();
})();
"""


def shrink(pdf_path, target_mb=12.0):
    """Illustrator's own downsampling is the first line; this is the second, applied only
    when the export still comes out heavier than an emailable kit should be."""
    if os.path.getsize(pdf_path) / 1e6 <= target_mb:
        return
    try:
        import pymupdf
        doc = pymupdf.open(pdf_path)
        doc.rewrite_images(dpi_threshold=220, dpi_target=200, quality=82, lossy=True, lossless=True)
        tmp = pdf_path + ".tmp"
        doc.save(tmp, garbage=3, deflate=True)
        doc.close()
        os.replace(tmp, pdf_path)
        print(f"shrunk to {os.path.getsize(pdf_path)/1e6:.1f} MB with pymupdf")
    except Exception as e:                       # the kit still ships, just heavier
        print(f"shrink skipped: {e}")


def add_links(pdf_path, links):
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import Link
    shrink(pdf_path)
    r = PdfReader(pdf_path)
    w = PdfWriter()
    w.append(r)
    for lk in links:
        page = w.pages[lk["p"] - 1]
        mb = page.mediabox                       # Illustrator may not put the origin at 0,0
        ox, oy = float(mb.left), float(mb.bottom)
        x0, y0, x1, y1 = lk["rect"]
        ann = Link(rect=(x0 + ox, y0 + oy, x1 + ox, y1 + oy), url=lk["url"], border=[0, 0, 0])
        w.add_annotation(page_number=lk["p"] - 1, annotation=ann)
    w.write(pdf_path)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(SCRATCH, exist_ok=True)
    now = datetime.datetime.now()
    pdf_name = f"KillerOfMen_EPK_{now:%H%M}_{now:%d%m%Y}_compressed.pdf"
    pdf_path = os.path.join(OUT_DIR, pdf_name)
    o = record()
    kinds = {}
    for op in o.ops:
        kinds[op["op"]] = kinds.get(op["op"], 0) + 1
    print(f"{len(o.ops)} operations {kinds}, {len(o.links)} links, {o.page} pages")
    cols = 4
    rows = (len(ARTBOARDS) + cols - 1) // cols
    cfg = {"W": W, "H": H, "cols": cols, "strideX": W + GAPX, "strideY": H + GAPX,
           "x0": -(cols * (W + GAPX) - GAPX) / 2, "y0": (rows * (H + GAPX) - GAPX) / 2,
           "names": ARTBOARDS, "ai": AI_PATH,
           "pdf": None if "--no-pdf" in sys.argv else pdf_path, "log": os.path.join(SCRATCH, "build.log")}
    jsx = JSX.replace("__CFG__", json.dumps(cfg)).replace("__OPS__", json.dumps(o.ops))
    jsx_path = os.path.join(SCRATCH, "build.jsx")
    open(jsx_path, "w", encoding="utf-8").write(jsx)
    json.dump(o.links, open(os.path.join(SCRATCH, "links.json"), "w"), indent=1)
    print(f"wrote {jsx_path} ({os.path.getsize(jsx_path)//1024} KB)")
    if "--jsx-only" in sys.argv:
        return
    if os.path.exists(cfg["log"]):
        os.remove(cfg["log"])
    script = (f'with timeout of 1500 seconds\n'
              f'tell application id "com.adobe.illustrator" to do javascript (read POSIX file "{jsx_path}")\n'
              f'end timeout')
    t0 = time.time()
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=1600)
    if res.returncode:
        print("osascript:", res.stderr.strip())
    log = open(cfg["log"]).read() if os.path.exists(cfg["log"]) else "(no log written)"
    print(log.strip())
    print(f"Illustrator took {time.time()-t0:.0f}s")
    if "DONE" not in log:
        sys.exit("Illustrator did not finish; see the log above.")
    if cfg["pdf"]:
        add_links(pdf_path, o.links)
        import shutil
        shutil.copy2(pdf_path, os.path.join(PRESS, pdf_name))
        print(f"pdf {pdf_path} ({os.path.getsize(pdf_path)/1e6:.1f} MB), links added, copied to press/")
    print(f"ai  {AI_PATH} ({os.path.getsize(AI_PATH)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
