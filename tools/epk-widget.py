#!/usr/bin/env python3
"""Render press/epk.json as the in-chat EPK readout (an HTML fragment for show_widget).

    python3 tools/epk-widget.py            print the fragment to stdout

This IS the established widget — the one Luke means by "make the widget". Do not redesign
it. Its look is a decision already made:

  * headline: percent supplied, then "N of T supplied · U written but not settled · O outstanding"
  * legend: settled · written, use not settled (hatched) · not supplied
  * one row per section: number, name, a bar in the section's own hue, "n / N", percent
  * "What is left": every open field with an owner chip where one is known

Section hues are BANDS in tools/build-epk-doc.py — the same hues the EPK document's bands use.
They fail the dataviz validator as a chart palette (adjacent 3/4 under the normal-vision
floor; six under 3:1 on a dark surface). That is recorded here, not acted on: the bars are
wayfinding, identity is carried by number and name, and the colours are Luke's choice.

The hatching rule (handoff-091): a field is drawn "written, use not settled" if it has open
options, OR if its text is itself a candidate inside another field's open choice — which is
why the director's statement hatches while the synopsis is undecided. Computed, not hardcoded.
Read-only; nothing here writes epk.json.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "press", "epk.json"), encoding="utf-8"))
_doc = open(os.path.join(ROOT, "tools", "build-epk-doc.py"), encoding="utf-8").read()
BANDS = dict(re.findall(r'"([0-9A]+)":\s*"(#[0-9a-fA-F]{6})"',
                        re.search(r"BANDS\s*=\s*\{(.*?)\}", _doc, re.S).group(1)))

# Owners for the open items, as the readout has shown them since handoff-086. "Yeo" in the
# worksheet's notes is shown as You Wu here, the inference the readout has carried; the
# worksheet itself still does not assert it.
OWNER = {"2.1": "Jordan Betine", "2.2": "Jordan Betine", "3.12": "You Wu",
         "A.2": "You Wu", "A.5": "Jordan Betine"}
HINT = {"2.1": lambda f: f"Logline — {len(f['options'])} versions written, pick one",
        "2.2": lambda f: f"Synopsis — {len(f['options'])} versions written, pick one"}

e = html.escape
norm = lambda t: " ".join(t.split()).lower()
CANDS = [norm(o["value"]) for s in d["sections"] for f in s["fields"]
         for o in (f.get("options") or []) if o.get("value", "").strip()]


def state(f):
    v = f["value"].strip()
    if not v:
        return "und" if f.get("options") else "need"
    nv = norm(v)
    if any(nv == c or (len(nv) > 80 and (nv in c or c in nv)) for c in CANDS):
        return "have_unsettled"
    return "have"


def hatch(h):
    return f"repeating-linear-gradient(135deg,{h} 0 4px,transparent 4px 8px)"


rows, left = [], []
tot = sup = uns = out = 0
for s in d["sections"]:
    n = len(s["fields"]); settled = hatched = 0
    for f in s["fields"]:
        st = state(f)
        if st == "have":
            settled += 1; sup += 1
        elif st == "have_unsettled":
            hatched += 1; sup += 1; uns += 1
        elif st == "und":
            hatched += 1; uns += 1
            left.append((f["n"], HINT[f["n"]](f) if f["n"] in HINT else f["label"], OWNER.get(f["n"])))
        else:
            out += 1
            left.append((f["n"], f["label"], OWNER.get(f["n"])))
    tot += n
    rows.append((s["num"], s["name"], n, settled, hatched, settled + hatched - sum(
        1 for f in s["fields"] if state(f) == "und")))
pct = round(100 * sup / tot)

o = []; w = o.append
w(f'<h2 class="sr-only" style="position:absolute;left:-9999px">Killer of Men EPK: {sup} of {tot} supplied ({pct} percent), {uns} written but not settled, {out} outstanding. Worksheet rev {d["rev"]}.</h2>')
w('<div style="font-family:var(--font-sans);color:var(--text-primary);max-width:760px">')
w('<div style="display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;margin:2px 0 12px">')
w(f'<div style="font-size:64px;font-weight:700;line-height:1;letter-spacing:-1px">{pct}%</div>')
w(f'<div style="font-size:16px;line-height:1.5"><b>{sup} of {tot}</b> supplied · <b>{uns}</b> written but not settled · <b>{out}</b> outstanding<br><span style="color:var(--text-secondary);font-size:14px">rev {d["rev"]}</span></div></div>')
w('<div style="display:flex;gap:22px;font-size:14px;color:var(--text-secondary);padding:10px 0 6px;border-top:1px solid var(--border);flex-wrap:wrap">'
  f'<span><span style="display:inline-block;width:38px;height:12px;border-radius:3px;background:{BANDS["1"]};vertical-align:-1px;margin-right:8px"></span>settled</span>'
  f'<span><span style="display:inline-block;width:38px;height:12px;border-radius:3px;background:{hatch(BANDS["2"])};vertical-align:-1px;margin-right:8px"></span>written, use not settled</span>'
  '<span><span style="display:inline-block;width:38px;height:12px;border-radius:3px;background:var(--text-muted);opacity:.45;vertical-align:-1px;margin-right:8px"></span>not supplied</span></div>')
for num, name, n, settled, hatched, counted in rows:
    h = BANDS.get(num, "#6b6b6b"); p = round(100 * counted / n)
    w('<div style="display:grid;grid-template-columns:34px 1fr 236px 60px 56px;gap:0 12px;align-items:center;padding:12px 0;border-top:1px solid var(--border)">')
    w(f'<div style="font-size:14px;color:var(--text-muted);text-align:right">{e(num)}</div>')
    w(f'<div style="font-size:19px;font-weight:500">{e(name)}</div>')
    w(f'<div style="display:flex;height:14px;border-radius:7px;overflow:hidden;background:{h};position:relative" aria-hidden="true"><div style="position:absolute;inset:0;background:var(--surface-0);opacity:.78"></div>'
      f'<div style="position:relative;width:{100 * settled / n:.1f}%;background:{h}"></div>'
      + (f'<div style="position:relative;width:{100 * hatched / n:.1f}%;background:{hatch(h)}"></div>' if hatched else '') + '</div>')
    w(f'<div style="font-size:16px;text-align:right;white-space:nowrap">{counted} / {n}</div>')
    w(f'<div style="font-size:16px;font-weight:600;text-align:right">{p}%</div></div>')
w('<div style="font-size:19px;font-weight:600;margin:22px 0 6px">What is left</div>')
for k, label, owner in left:
    w('<div style="display:grid;grid-template-columns:70px 1fr auto;gap:0 12px;align-items:center;padding:8px 0;border-top:1px solid var(--border)">')
    w(f'<div style="font-size:15px;color:var(--text-muted)">{e(k)}</div><div style="font-size:17px">{e(label)}</div>')
    w((f'<div style="font-size:14px;color:var(--text-secondary);border:1px solid var(--border-strong);border-radius:14px;padding:3px 12px;white-space:nowrap">{e(owner)}</div>' if owner else '<div></div>') + '</div>')
w(f'<div style="font-size:13px;color:var(--text-muted);padding:12px 0 2px;border-top:1px solid var(--border)">press/epk.json rev {d["rev"]} · hatching computed: a field whose text is a candidate in another field\'s open choice is drawn unsettled</div></div>')
print("\n".join(o))
