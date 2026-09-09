#!/usr/bin/env python3
"""EPK INFO, coloured to match the progress bars.

Each section takes its own hue, the same one its bar uses. That hue then carries the
authorship signal too: coloured body text is Claude's and wants checking, black body
text is a person's. One signal, not two — an authorship blue would have sat five
deltaE from section 2's blue, which no reader can separate.

All eleven hues were validated against white: 5.3 to 8.9 to 1, every one clear of
the 4.5 body-text gate.
"""
import json, html, datetime, sys
d = json.load(open("press/epk.json", encoding="utf-8"))
BANDS = {"1": "#635ad0", "2": "#0051a1", "3": "#007588", "4": "#005e42", "5": "#007c1a",
         "7": "#6a4400", "8": "#ae5000", "9": "#822f00", "10": "#a61c52", "11": "#8c598e",
         "A": "#4d427f"}   # the same hues the progress bars use; all >= 5.3:1 on white
bands = BANDS
e = html.escape
INK, GREY, FAINT = "#171310", "#6b6b6b", "#d8d5cc"
PERSON = ("Luke", "festival lane", "Jordan", "killerofmen.com", "end-credit roll")
by_person = lambda f: any(k in ((f.get("history") or [{}])[-1].get("by", "")) for k in PERSON)

flds = [(s, f) for s in d["sections"] for f in s["fields"]]
tot, got = len(flds), sum(1 for _, f in flds if f["value"].strip())
open_ = [(s, f) for s, f in flds if not f["value"].strip()]

o = [f'''<html><head><meta charset="utf-8"><style>
body{{background:#fff;color-scheme:light;font-family:Georgia,'Times New Roman',serif;
 font-size:11.5pt;color:{INK};line-height:1.62;margin:0}}
h1{{font-size:22pt;margin:0 0 5pt;letter-spacing:.3pt}}
h2{{font-size:13pt;margin:30pt 0 12pt;padding-bottom:4pt;letter-spacing:.5pt;text-transform:uppercase}}
h3{{font-size:11.5pt;margin:20pt 0 4pt;color:{INK}}}
p{{margin:0 0 6pt}}
.lead{{font-size:10.5pt;color:{GREY};margin:0 0 4pt}}
.val{{margin:0 0 7pt 24pt}}
.none{{margin:0 0 7pt 24pt;color:{GREY};font-style:italic}}
.opt{{margin:12pt 0 3pt 24pt;font-weight:bold}}
.need{{margin:6pt 0 6pt 14pt;font-size:10.5pt}}
.who{{color:{GREY};font-style:italic;font-size:9.5pt;font-weight:normal}}
</style></head><body>''']
o.append('<h1>Killer of Men — EPK Info</h1>')
o.append(f'<p class="lead">Every piece of text the press kit needs, numbered. '
         f'{got} of {tot} supplied · {len(open_)} still open. '
         f'Rebuilt from press/epk.json rev {d["rev"]} on {datetime.date.today().strftime("%B %-d, %Y")}.</p>')
o.append(f'<p class="lead">Each section has its own colour, the same one it has on the progress bars. '
         f'<b>Text in colour was written by Claude</b> — including anything read off the poster — so it wants '
         f'checking against the source. <b style="color:{INK}">Text in black was written by a person.</b></p>')

o.append(f'<h2 style="color:{INK};border-bottom:1.5pt solid {INK}">Still needed</h2>')
for s, f in open_:
    c = bands[s["num"]]
    who = f' <span class="who">— {e(f["waiting"])}</span>' if f.get("waiting") else ""
    extra = f' — {len(f["options"])} versions written, pick one' if f.get("options") else ""
    o.append(f'<p class="need"><b style="color:{c}">{e(f["n"])}</b> &nbsp;{e(f["label"])}{e(extra)}{who}</p>')

for s in d["sections"]:
    c = bands[s["num"]]
    n = len(s["fields"]); g = sum(1 for f in s["fields"] if f["value"].strip())
    o.append(f'<h2 style="color:{c};border-bottom:1.5pt solid {c}">{e(s["num"])} &nbsp;·&nbsp; {e(s["name"])} '
             f'<span style="font-size:9.5pt;letter-spacing:0;text-transform:none;color:{GREY}">({g} of {n})</span></h2>')
    for f in s["fields"]:
        who = f' <span class="who">waiting on {e(f["waiting"])}</span>' if f.get("waiting") else ""
        o.append(f'<h3><b style="color:{c};margin-right:8pt">{e(f["n"])}</b> {e(f["label"])}{who}</h3>')
        v = f["value"]
        if v:
            col = INK if by_person(f) else c
            for line in v.split("\n"):
                o.append(f'<p class="val" style="color:{col}">{e(line) if line.strip() else "&nbsp;"}</p>')
        elif f.get("options"):
            for opt in f["options"]:
                note = f' <span class="who">— {e(opt["note"])}</span>' if opt.get("note") else ""
                o.append(f'<p class="opt" style="color:{c}">{e(opt["key"])}{note}</p>')
                for line in opt["value"].split("\n"):
                    o.append(f'<p class="val" style="color:{INK}">{e(line)}</p>')
        else:
            o.append('<p class="none">not supplied</p>')
o.append('</body></html>')
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(o))
print(f"{tot} items · {got} supplied · {len(open_)} open · 11 section hues")
