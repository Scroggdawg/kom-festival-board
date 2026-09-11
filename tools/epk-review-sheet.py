#!/usr/bin/env python3
"""Before/after review sheet for a kit draft: every page side by side, the changed regions
boxed on the after render, and the notes for each page.

    venv/bin/python tools/epk-review-sheet.py --before OLD.pdf --after NEW.pdf \
        --notes notes.json --out press/drafts/<date> [--scale 0.5]

notes.json:
    {"title": "...", "before_label": "...", "after_label": "...",
     "pages": {"7": {"verdict": "redesigned|adjusted|unchanged",
                     "changes": ["..."], "confirm": ["...things only Luke can settle..."]}},
     "variants": [{"name": "p09-kit-idiom", "pdf": "path.pdf", "page": 1, "compare_to": 9,
                   "notes": ["..."]}]}

Writes pNN-before.jpg, pNN-after.jpg, pNN-diff.jpg (after with change boxes), one
<name>.jpg per variant, index.html (self-contained, images embedded) and review.md.
Clean Bank: a readout, no flourish. Nothing in the repo is modified except --out.
"""
import argparse, base64, io, json, os, sys

import pymupdf
from PIL import Image, ImageChops, ImageDraw, ImageFilter

OUTLINE = (223, 0, 1)        # one outline colour for change boxes; a readout, not a surface


def render(pdf, scale):
    d = pymupdf.open(pdf)
    out = []
    for p in d:
        pix = p.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        out.append((im, len(p.get_text()), len(p.get_links())))
    return out


def boxes(a, b, cell=24, thresh=48):
    """Rectangles (in pixels) around regions where a and b differ, from a coarse grid."""
    if a.size != b.size:
        b = b.resize(a.size)
    diff = ImageChops.difference(a, b).convert("L").filter(ImageFilter.MaxFilter(5))
    w, h = diff.size
    cols, rows = (w + cell - 1) // cell, (h + cell - 1) // cell
    grid = [[False] * cols for _ in range(rows)]
    px = diff.load()
    for r in range(rows):
        for c in range(cols):
            x0, y0 = c * cell, r * cell
            region = diff.crop((x0, y0, min(x0 + cell, w), min(y0 + cell, h)))
            if region.getextrema()[1] > thresh:
                grid[r][c] = True
    seen = [[False] * cols for _ in range(rows)]
    rects = []
    for r in range(rows):
        for c in range(cols):
            if not grid[r][c] or seen[r][c]:
                continue
            stack, cells = [(r, c)], []
            seen[r][c] = True
            while stack:
                rr, cc = stack.pop()
                cells.append((rr, cc))
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] and not seen[nr][nc]:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            rs = [x[0] for x in cells]; cs = [x[1] for x in cells]
            rects.append((min(cs) * cell, min(rs) * cell,
                          min((max(cs) + 1) * cell, w), min((max(rs) + 1) * cell, h)))
    return rects


def draw_boxes(im, rects):
    im = im.copy()
    d = ImageDraw.Draw(im, "RGBA")
    for x0, y0, x1, y1 in rects:
        d.rectangle((x0, y0, x1, y1), outline=OUTLINE + (255,), width=3)
        d.rectangle((x0, y0, x1, y1), fill=OUTLINE + (28,))
    return im


def data_uri(im, q=80):
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--notes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale", type=float, default=0.5)
    a = ap.parse_args()
    notes = json.load(open(a.notes, encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    before = render(a.before, a.scale)
    after = render(a.after, a.scale)
    n = max(len(before), len(after))
    rows_html, md = [], []
    md.append(f"# {notes.get('title', 'Review sheet')}\n")
    md.append(f"Before: `{os.path.basename(a.before)}` ({len(before)} pages). After: `{os.path.basename(a.after)}` ({len(after)} pages).\n")
    md.append("| Page | Verdict | Chars before → after | Links before → after | Changed regions |\n|---|---|---|---|---|")
    table, notes_md = [], []
    for i in range(n):
        pn = i + 1
        bi = before[i] if i < len(before) else None
        ai = after[i] if i < len(after) else None
        note = notes.get("pages", {}).get(str(pn), {})
        verdict = note.get("verdict", "unchanged" if (bi and ai and ImageChops.difference(bi[0], ai[0]).getbbox() is None) else "changed")
        rects = boxes(bi[0], ai[0]) if bi and ai else []
        imgs = {}
        if bi:
            bi[0].save(os.path.join(a.out, f"p{pn:02d}-before.jpg"), quality=85); imgs["before"] = bi[0]
        if ai:
            ai[0].save(os.path.join(a.out, f"p{pn:02d}-after.jpg"), quality=85); imgs["after"] = ai[0]
            boxed = draw_boxes(ai[0], rects)
            boxed.save(os.path.join(a.out, f"p{pn:02d}-diff.jpg"), quality=85); imgs["diff"] = boxed
        table.append(f"| {pn} | {verdict} | {bi[1] if bi else '—'} → {ai[1] if ai else '—'} | {bi[2] if bi else '—'} → {ai[2] if ai else '—'} | {len(rects)} |")
        changes = note.get("changes", []); confirm = note.get("confirm", [])
        cells = "".join(
            f'<figure><img src="{data_uri(imgs[k])}" alt="page {pn} {k}"><figcaption>{k}</figcaption></figure>'
            for k in ("before", "after", "diff") if k in imgs)
        li = "".join(f"<li>{esc(c)}</li>" for c in changes) or "<li>No change.</li>"
        lc = "".join(f"<li>{esc(c)}</li>" for c in confirm)
        rows_html.append(
            f'<section id="p{pn}"><h2>Page {pn} <span class="v">{esc(verdict)}</span></h2>'
            f'<div class="row">{cells}</div>'
            f'<div class="notes"><h3>Changes</h3><ul>{li}</ul>'
            + (f'<h3>For Luke to confirm</h3><ul>{lc}</ul>' if lc else '')
            + f'<p class="stat">text {bi[1] if bi else "—"} → {ai[1] if ai else "—"} chars · links {bi[2] if bi else "—"} → {ai[2] if ai else "—"} · changed regions {len(rects)}</p></div></section>')
        if changes:
            notes_md.append("")
            notes_md.append(f"**Page {pn}**")
            notes_md.extend(f"- {c}" for c in changes)
            notes_md.extend(f"- CONFIRM: {c}" for c in confirm)
    md.extend(table)
    md.extend(notes_md)
    for v in notes.get("variants", []):
        vr = render(v["pdf"], a.scale)
        vim = vr[v.get("page", 1) - 1][0]
        vim.save(os.path.join(a.out, f"{v['name']}.jpg"), quality=85)
        cmp_n = v.get("compare_to")
        cmp_im = after[cmp_n - 1][0] if cmp_n and cmp_n - 1 < len(after) else None
        cells = ""
        if cmp_im is not None:
            cells += f'<figure><img src="{data_uri(cmp_im)}" alt="page {cmp_n} draft"><figcaption>draft page {cmp_n}</figcaption></figure>'
        cells += f'<figure><img src="{data_uri(vim)}" alt="{esc(v["name"])}"><figcaption>{esc(v["name"])}</figcaption></figure>'
        li = "".join(f"<li>{esc(c)}</li>" for c in v.get("notes", []))
        rows_html.append(f'<section id="{esc(v["name"])}"><h2>Variant: {esc(v["name"])} <span class="v">for Luke\'s ruling</span></h2><div class="row">{cells}</div><div class="notes"><ul>{li}</ul></div></section>')
        md.append(""); md.append(f"**Variant {v['name']}** (compare to page {cmp_n})"); md.extend(f"- {c}" for c in v.get("notes", []))
    title = esc(notes.get("title", "Review sheet"))
    html = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>
body{{margin:0;background:#141210;color:#e8e2d6;font:14px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
header{{padding:24px 28px;border-bottom:1px solid #2a251f}} header h1{{font-size:18px;font-weight:600;margin:0 0 6px}} header p{{margin:0;color:#a89c88}}
section{{padding:24px 28px;border-bottom:1px solid #2a251f}} h2{{font-size:15px;font-weight:600;margin:0 0 12px}} .v{{font-weight:400;color:#a89c88;margin-left:10px}}
.row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;align-items:start}}
figure{{margin:0}} figure img{{width:100%;height:auto;display:block;background:#000}} figcaption{{color:#a89c88;font-size:12px;margin-top:4px}}
.notes{{max-width:900px;margin-top:12px}} h3{{font-size:13px;font-weight:600;margin:12px 0 4px;color:#cfc4b2}} ul{{margin:0;padding-left:18px}} li{{margin:2px 0}}
.stat{{color:#a89c88;font-size:12px}} nav{{padding:10px 28px;color:#a89c88;font-size:12px;border-bottom:1px solid #2a251f}} nav a{{color:#cfc4b2;text-decoration:none;margin-right:10px}}
</style></head><body>
<header><h1>{title}</h1><p>Before: {esc(notes.get('before_label', os.path.basename(a.before)))} · After: {esc(notes.get('after_label', os.path.basename(a.after)))} · Boxes on the third image mark regions that changed.</p></header>
<nav>{''.join(f'<a href="#p{i+1}">{i+1}</a>' for i in range(n))}{''.join(f'<a href="#{esc(v["name"])}">{esc(v["name"])}</a>' for v in notes.get('variants', []))}</nav>
{''.join(rows_html)}
</body></html>"""
    open(os.path.join(a.out, "index.html"), "w", encoding="utf-8").write(html)
    open(os.path.join(a.out, "review.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"wrote {a.out}/index.html ({os.path.getsize(os.path.join(a.out, 'index.html'))/1e6:.1f} MB), review.md, {n} pages, {len(notes.get('variants', []))} variant(s)")


if __name__ == "__main__":
    main()
