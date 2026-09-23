#!/usr/bin/env python3
"""Render the FilmFreeway project page from press/epk.json, as Markdown and as .docx.

    <venv>/bin/python tools/build-filmfreeway-page.py --version 7 [--out-dir press]

Writes press/filmfreeway-page-v<N>.md and .docx. Nothing is retyped: every paragraph is
the worksheet's current value (2.1 logline, 2.2 synopsis, 5.1 director bio, 4.1 statement,
3.x specs, 9.1 key credits, 3.15 cast, A.6 screenings, the picks in A.1). Alternates that
the worksheet still carries as `options` are listed by key so the page shows what is
undecided without printing every draft. v2 to v6 were written by hand; from v7 the page is
a view of the worksheet, regenerated after any epk.py set.
"""
import argparse, datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "press", "epk.json"), encoding="utf-8"))
F = {f["n"]: f for s in D["sections"] for f in s["fields"]}


def val(n):
    return F[n]["value"].strip()


def paras(text):
    """One paragraph per line is the worksheet's convention (blank lines are tolerated)."""
    return [p.strip() for p in text.splitlines() if p.strip()]


def pair_lines(text):
    """'Role | Name' lines only; the notes under them are dropped."""
    out = []
    for line in text.splitlines():
        if "|" in line and not line.lstrip().startswith(("(", "RESOLVED", "TWO", "LIKELY", "Billed")):
            a, b = [x.strip() for x in line.split("|", 1)]
            out.append((a, b))
        elif out and not line.strip():
            break
    return out


def specs():
    keys = [("3.1", "Genre"), ("3.2", "Country of origin"), ("3.3", "Shooting location"),
            ("3.4", "Production year"), ("3.5", "Completion year"), ("3.6", "Language"),
            ("3.8", "Runtime"), ("3.9", "Aspect ratio"), ("3.10", "Frame rate"),
            ("3.11", "Shooting format"), ("3.13", "Sound")]
    rows = []
    for n, label in keys:
        v = val(n).splitlines()[0] if val(n) else "—"
        rows.append((label, v))
    return rows


def stills_picked():
    m = re.search(r"The twelve for the Drive and for FilmFreeway, in film order: (.+?)\. Alternates", val("A.1"), re.S)
    if not m:
        return []
    return [x.strip() for x in m.group(1).split("·")]


def build(version):
    today = datetime.date.today().isoformat()
    logline = val("2.1")
    alternates = [o["key"] for o in F["2.1"].get("options", [])]
    synopsis = paras(val("2.2"))
    bio = paras(val("5.1"))
    statement = paras(val("4.1"))
    credits = pair_lines(val("9.1"))
    cast = [(c, a) for c, a in pair_lines(val("3.15")) if c.lower() != "stunt coordinator"]  # crew, billed in the crawl; 9.1 carries it
    screenings = [x.strip() for x in val("A.6").split("·")]
    stills = stills_picked()
    kit = sorted(p for p in os.listdir(os.path.join(ROOT, "press"))
                 if p.startswith("KillerOfMen_EPK_") and p.endswith(".pdf"))
    kit_name = kit[-1] if kit else "(kit PDF not built)"

    md = []
    w = md.append
    w(f"# Killer of Men — FilmFreeway page, v{version}")
    w("")
    w(f"*{today}, v{version}: generated from `press/epk.json` rev {D['rev']} by "
      "`tools/build-filmfreeway-page.py`. Every paragraph is the worksheet's current value; "
      "edit there, then regenerate. v6 (Sep 8) was the last hand-written draft.*")
    w("")
    w("## Logline")
    w("")
    w(logline)
    w("")
    if alternates:
        w(f"*Alternates still recorded in the worksheet (2.1 options): {', '.join(alternates)}. "
          "Jordan's pick closes them.*")
        w("")
    w("## Synopsis")
    w("")
    for p in synopsis:
        w(p)
        w("")
    w("## Director biography")
    w("")
    for p in bio:
        w(p)
        w("")
    w("## Director statement")
    w("")
    for p in statement:
        w(p)
        w("")
    w("## Specifications")
    w("")
    w("| Field | Value |")
    w("|---|---|")
    for k, v in specs():
        w(f"| {k} | {v} |")
    w("")
    w("## Credits")
    w("")
    for role, name in credits:
        if name.upper().startswith("STILL UNKNOWN"):
            w(f"- {role}: *not yet named*")
        else:
            w(f"- {role}: {name}")
    w("")
    w("## Cast")
    w("")
    for ch, actor in cast:
        w(f"- {ch}: {actor}")
    w("")
    w("## Screenings and awards")
    w("")
    for s in screenings:
        w(f"- Official selection, {s}")
    w("")
    w("## Stills to upload")
    w("")
    w("Twelve frames, in film order, from `press/assets/STILLS/` (gallery numbers) and the Drive folder "
      "`05 MARKETING/00 PRESS/EPK-2026-09-23/03 STILLS/`:")
    w("")
    for s in stills:
        w(f"- {s}")
    w("")
    w("## Attachments")
    w("")
    w(f"- Press kit PDF: `press/{kit_name}`")
    w("- Student ID with the number redacted (Jordan)")
    w("")
    w("## Links")
    w("")
    w(f"- Website: {val('1.3')}")
    w(f"- Instagram: {val('3.18')}")
    w(f"- IMDb: {val('3.19')}")
    w(f"- Press contact: {val('3.20')}")
    w("")
    w("## Open on this page")
    w("")
    w("- Logline: Jordan's pick between the worksheet's text and the alternates (2.1).")
    w("- Statement: 4.1 is Jordan's text as supplied; the Sep 7 edited version in v6 needs his approval before it replaces it.")
    w("- Completion date: a 2026 date before April 24, 2026; the DCP regenerated to match (3.5, 3.12).")
    w("- Sound designer, composer credit line and the full post-sound block: not named (9.1).")
    w("- Categories: remove \"experimental\". First-time filmmaker: Jordan's call.")
    return "\n".join(md), dict(logline=logline, alternates=alternates, synopsis=synopsis, bio=bio,
                              statement=statement, specs=specs(), credits=credits, cast=cast,
                              screenings=screenings, stills=stills, kit=kit_name)


def docx(path, version, parts):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Georgia"
    st.font.size = Pt(11)
    doc.add_heading(f"Killer of Men — FilmFreeway page, v{version}", 0)
    doc.add_paragraph(f"Generated from press/epk.json rev {D['rev']} on {datetime.date.today().isoformat()}.")
    doc.add_heading("Logline", 1)
    doc.add_paragraph(parts["logline"])
    if parts["alternates"]:
        doc.add_paragraph("Alternates still recorded in the worksheet: " + ", ".join(parts["alternates"]) + ".").italic = True
    doc.add_heading("Synopsis", 1)
    for p in parts["synopsis"]:
        doc.add_paragraph(p)
    doc.add_heading("Director biography", 1)
    for p in parts["bio"]:
        doc.add_paragraph(p)
    doc.add_heading("Director statement", 1)
    for p in parts["statement"]:
        doc.add_paragraph(p)
    doc.add_heading("Specifications", 1)
    t = doc.add_table(rows=0, cols=2)
    for k, v in parts["specs"]:
        r = t.add_row().cells
        r[0].text, r[1].text = k, v
    doc.add_heading("Credits", 1)
    for role, name in parts["credits"]:
        doc.add_paragraph(f"{role}: {name}", style="List Bullet")
    doc.add_heading("Cast", 1)
    for ch, actor in parts["cast"]:
        doc.add_paragraph(f"{ch}: {actor}", style="List Bullet")
    doc.add_heading("Screenings and awards", 1)
    for s in parts["screenings"]:
        doc.add_paragraph(f"Official selection, {s}", style="List Bullet")
    doc.add_heading("Stills to upload", 1)
    for s in parts["stills"]:
        doc.add_paragraph(s, style="List Bullet")
    doc.add_heading("Attachments", 1)
    doc.add_paragraph(f"Press kit PDF: {parts['kit']}", style="List Bullet")
    doc.add_paragraph("Student ID with the number redacted (Jordan)", style="List Bullet")
    doc.add_heading("Links", 1)
    for n in ("1.3", "3.18", "3.19", "3.20"):
        doc.add_paragraph(f"{F[n]['label']}: {val(n)}", style="List Bullet")
    doc.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", type=int, required=True)
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "press"))
    a = ap.parse_args()
    md, parts = build(a.version)
    base = os.path.join(a.out_dir, f"filmfreeway-page-v{a.version}")
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write(md)
    docx(base + ".docx", a.version, parts)
    print(f"wrote {base}.md and .docx from epk.json rev {D['rev']}")


if __name__ == "__main__":
    main()
