#!/usr/bin/env python3
"""Verify a PDF exported from the Canva design against the contract it was built from.

    <venv>/bin/python tools/check-canva-export.py <export.pdf>

Per page: the page size, the characters the PDF carries against the contract's text (a
paragraph Canva clipped at the page foot loses characters), every paragraph's rendered
bottom against lines * leading (Canva setting it longer), every pair of text lines that
share a baseline and overlap (a handle on its lockup), the link annotations, the fonts.
Exit 1 on any finding. Reads nothing but the PDF and canva/ops/epk-canva.json.
"""
import json, os, re, sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS = os.path.join(ROOT, "canva", "ops", "epk-canva.json")
FOOT = 74.0            # the kit's margin, pt


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    pdf = sys.argv[1]
    doc = json.load(open(OPS))
    d = pymupdf.open(pdf)
    W, H = doc["page"]["width_pt"], doc["page"]["height_pt"]
    print(f"{os.path.basename(pdf)}: {len(d)} pages, {os.path.getsize(pdf)/1e6:.1f} MB; contract generated {doc['generated']}, "
          f"measured in {doc.get('measured_face')}")
    problems = 0
    fonts = set()
    total_links = 0
    if len(d) != len(doc["pages"]):
        print(f"  PAGE COUNT {len(d)} != {len(doc['pages'])}"); problems += 1
    for i, p in enumerate(doc["pages"]):
        if i >= len(d):
            break
        page = d[i]
        pw, ph = page.rect.width, page.rect.height
        size_ok = abs(pw - W) < 1 and abs(ph - H) < 1
        text = page.get_text()
        n_links = len(page.get_links()); total_links += n_links
        for f in page.get_fonts():
            fonts.add(f[3])
        # words with bboxes, for paragraph bottoms and line overlaps
        words = page.get_text("words")          # x0, y0, x1, y1, word, block, line, wordno
        findings = []
        # 1. every paragraph: its last word must be on the page and its bottom near lines*lead
        for e in p["elements"]:
            if e["type"] != "text":
                continue
            if e["kind"] == "paragraph":
                expected_bottom = e["y"] + e["lines"] * e["leading_pt"]
                # words of this paragraph: inside its box horizontally, below its top
                ws = [w for w in words if w[0] >= e["x"] - 2 and w[2] <= e["x"] + e["w"] + 2 and w[1] >= e["y"] - 2
                      and w[1] <= expected_bottom + 3 * e["leading_pt"]]
                first = norm(e["text"])[:24]
                last_word = norm(e["text"]).split()[-1] if e["text"].strip() else ""
                present = norm(text)
                if first not in present:
                    findings.append(f"paragraph '{e['text'][:30]}' not found in the page text")
                    continue
                # the paragraph's tail: is its last word on the page?
                if last_word and last_word not in present:
                    findings.append(f"paragraph '{e['text'][:30]}' loses its tail ('{last_word}') — clipped")
                    continue
                bottoms = [w[3] for w in ws]
                if bottoms:
                    got = max(bottoms)
                    if got > expected_bottom + 0.6 * e["leading_pt"]:
                        findings.append(f"paragraph '{e['text'][:30]}' bottom {got:.0f} > expected {expected_bottom:.0f} "
                                        f"({(got - expected_bottom) / e['leading_pt']:.1f} lines longer)")
                    if got > H - FOOT:
                        findings.append(f"paragraph '{e['text'][:30]}' ends at {got:.0f}, past the foot margin {H - FOOT:.0f}")
        # 2. lines sharing a baseline whose words overlap horizontally (rendered, not measured)
        lines = {}
        for w in words:
            key = round(w[3])            # bottom ~ baseline+descent, good enough to bucket
            lines.setdefault(key, []).append(w)
        for key, ws in lines.items():
            ws.sort(key=lambda w: w[0])
            for a, b in zip(ws, ws[1:]):
                if b[0] < a[2] - 1.5:     # next word starts before the previous ends
                    findings.append(f"overlap on y~{key}: '{a[4]}' [{a[0]:.0f}..{a[2]:.0f}] and '{b[4]}' [{b[0]:.0f}..{b[2]:.0f}]")
        # 3. characters carried, against the contract's text
        contract_chars = sum(len(e["text"]) for e in p["elements"] if e["type"] == "text")
        pdf_chars = len(re.sub(r"\s", "", text))
        contract_nospace = sum(len(re.sub(r"\s", "", e["text"])) for e in p["elements"] if e["type"] == "text")
        flag = ""
        if contract_nospace and pdf_chars < contract_nospace * 0.97:
            flag = "  <-- FEWER CHARACTERS THAN THE CONTRACT"
            findings.append(f"characters {pdf_chars} vs contract {contract_nospace}")
        print(f"  p{p['n']:02d} {p['name']:22} {pw:.0f}x{ph:.0f} pt{'' if size_ok else ' SIZE!'}  chars {pdf_chars:5} (contract {contract_nospace:5})  "
              f"links {n_links:2}{flag}")
        for f in findings:
            print(f"       ! {f}")
        problems += len(findings) + (0 if size_ok else 1)
    print(f"  links total {total_links}; fonts {sorted(fonts)}")
    print(f"{problems} finding(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
