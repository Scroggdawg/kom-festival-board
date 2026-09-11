#!/usr/bin/env python3
"""Render the kit's test pages (layouts not wired into main()) for review.

    <venv>/bin/python tools/build-epk-variants.py [--out DIR] [name ...]

Writes DIR/<name>.pdf and DIR/<name>.png (one page, 1 px per pt) for each variant, default
all, DIR default press/drafts/<today>/. The variants:
    p05-variant-five-on-one   all five filmmakers on one page (page_bios_single)
    p09-variant-kit-idiom     page 9 in page 3's idiom (page_credits_variant)
"""
import datetime, importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


kit = _load("kit", os.path.join(ROOT, "tools", "build-epk-kit.py"))
VARIANTS = {
    "p05-variant-five-on-one": lambda c, d: kit.page_bios_single(c, d, kit.BIOS),
    "p09-variant-kit-idiom": lambda c, d: kit.page_credits_variant(c, d),
}


def main():
    args = sys.argv[1:]
    out = os.path.join(ROOT, "press", "drafts", f"{datetime.date.today():%Y-%m-%d}")
    if "--out" in args:
        i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
    names = args or list(VARIANTS)
    os.makedirs(out, exist_ok=True)
    d = kit.card.load()
    for name in names:
        pdf = os.path.join(out, f"{name}.pdf")
        c = kit.canvas.Canvas(pdf, pagesize=(kit.W, kit.H))
        VARIANTS[name](c, d)
        c.save()
        import pymupdf
        pg = pymupdf.open(pdf)[0]
        png = os.path.join(out, f"{name}.png")
        pg.get_pixmap(dpi=72).save(png)
        print(f"wrote {os.path.relpath(pdf, ROOT)} and .png ({os.path.getsize(pdf)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
