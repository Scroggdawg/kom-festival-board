#!/usr/bin/env python3
"""Render todo.json as the in-chat widget (an HTML fragment, same look as docket.html).
  widget.py            print the fragment to stdout
Read-only. A snapshot: the footer says so, with rev and write time."""
import json, os, sys, datetime, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "todo.json"), encoding="utf-8"))
ST = d["statuses"]; SC = d["statusColors"]; LAB = d["statusLabels"]
e = html.escape
def sprite(k, c):
    s = '<svg viewBox="0 0 18 18" aria-hidden="true" style="width:18px;height:18px;flex:none">'
    if k == 0: s += f'<circle cx="9" cy="9" r="6.5" fill="none" stroke="{c}" stroke-width="1.6"/>'
    elif k == 1: s += f'<circle cx="9" cy="9" r="6.5" fill="none" stroke="{c}" stroke-width="1.6"/><path d="M9 2.5a6.5 6.5 0 0 1 0 13z" fill="{c}"/>'
    elif k == 2: s += f'<circle cx="9" cy="9" r="6.5" fill="none" stroke="{c}" stroke-width="1.6"/><line x1="4.4" y1="13.6" x2="13.6" y2="4.4" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>'
    else: s += f'<circle cx="9" cy="9" r="7.3" fill="{c}"/>'
    return s + '</svg>'
def fmt(iso):
    if not iso: return ''
    try: return datetime.date.fromisoformat(iso[:10]).strftime('%b %-d')
    except ValueError: return iso
def blocks(s):
    return ''.join(f'<i class="dk-blk{" s"+str(ST.index(it["status"])) if ST.index(it["status"]) else ""}"></i>' for it in s["items"])
css = """<style>
.dk{background:#14213d;color:#f3ecd8;border-radius:12px;padding:18px 22px 14px;font-family:'Archivo','Helvetica Neue',Arial,sans-serif;font-size:14px;line-height:1.4;--s1:#5fb3e0;--s2:#e6a92a;--s3:#2bb673;--mute:#b7bdcc;--dim:#7f8aa6;--line:#2a3d66}
.dk *{box-sizing:border-box}.dk-top{display:grid;grid-template-columns:1fr auto;gap:16px;align-items:start;padding-bottom:14px;border-bottom:1px solid var(--line)}
.dk-ttl{font-size:20px;font-weight:500;color:#f3ecd8}.dk-ttl small{display:block;font-size:12px;color:var(--mute);font-weight:400;margin-top:5px}
.dk-map{display:flex;flex-direction:column;gap:5px;align-items:flex-end}.dk-mrow{display:flex;gap:3px;align-items:center}.dk-mrow .k{width:6px;height:6px;border-radius:50%;margin-right:6px}
.dk-blk{display:inline-block;width:12px;height:8px;border-radius:1.5px;border:1px solid var(--sc);background:transparent}.dk-blk.s1{background:var(--s1);border-color:var(--s1)}.dk-blk.s2{background:var(--s2);border-color:var(--s2)}.dk-blk.s3{background:var(--s3);border-color:var(--s3)}
.dk-g{border-bottom:1px solid var(--line)}.dk-h{display:grid;grid-template-columns:18px 1fr auto 96px;gap:12px;align-items:center;min-height:52px;cursor:pointer;user-select:none}
.dk-h .ch{color:var(--dim);font-size:11px;transition:transform .15s}.dk-g.open .dk-h .ch{transform:rotate(90deg)}
.dk-h .nm{font-size:16px;font-weight:500;color:var(--sc)}.dk-h .nm small{font-size:11px;color:var(--mute);font-weight:400;margin-left:8px}
.dk-h .bl{display:flex;gap:3px;flex-wrap:wrap;max-width:200px}.dk-h .ct{font-size:12px;color:var(--mute);text-align:right;font-variant-numeric:tabular-nums}
.dk-items{display:none;padding:0 0 10px 30px;border-left:2px solid var(--sc);margin-left:8px}.dk-g.open .dk-items{display:block}
.dk-it{display:grid;grid-template-columns:160px 1fr 64px;gap:12px;align-items:center;padding:8px 0;border-top:1px solid rgba(42,61,102,.6)}.dk-it:first-child{border-top:0}
.dk-dial{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--mute);white-space:nowrap}.dk-it.c1 .w{color:var(--s1)}.dk-it.c2 .w{color:var(--s2)}.dk-it.c3 .w{color:var(--s3)}
.dk-t{color:#f3ecd8}.dk-t .ref{color:var(--dim);font-size:11px;margin-right:6px;font-variant-numeric:tabular-nums}.dk-t .who{display:block;font-size:11.5px;color:var(--mute);margin-top:2px}.dk-t .who.w:before{content:"⌀ ";color:var(--s2)}
.dk-it.c3 .dk-t{color:var(--mute)}.dk-d{font-size:12px;color:var(--mute);text-align:right;font-variant-numeric:tabular-nums}.dk-d b{color:#f3ecd8;font-weight:500}
.dk-foot{margin-top:10px;font-size:11px;color:var(--mute);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}.dk-leg{display:flex;gap:14px}.dk-leg span{display:inline-flex;align-items:center;gap:5px}.dk-leg svg{width:14px!important;height:14px!important}
</style>"""
done = sum(it["status"] == "complete" for s in d["sections"] for it in s["items"]); N = sum(len(s["items"]) for s in d["sections"])
out = [f'<h2 class="sr-only">Campaign to-do list: {done} of {N} items complete across {len(d["sections"])} sections.</h2>', css, '<div class="dk">']
out.append(f'<div class="dk-top"><div class="dk-ttl">{e(d["title"])}<small>{done} of {N} complete</small></div><div class="dk-map">' +
    ''.join(f'<div class="dk-mrow" style="--sc:{s["color"]}"><i class="k" style="background:{s["color"]}"></i>{blocks(s)}</div>' for s in d["sections"]) + '</div></div>')
for gi, s in enumerate(d["sections"]):
    c = sum(it["status"] == "complete" for it in s["items"])
    rows = ''
    for it in s["items"]:
        k = ST.index(it["status"]); who = f'waiting on {it["waitingOn"]}' if it.get("waitingOn") else it.get("owner", "")
        rows += (f'<div class="dk-it c{k}"><div class="dk-dial">{sprite(k, SC[it["status"]])}<span class="w">{e(LAB[it["status"]])}</span></div>'
                 f'<div class="dk-t"><span class="ref">{e(it["id"])}</span>{e(it["title"])}<span class="who{" w" if it.get("waitingOn") else ""}">{e(who)}</span></div>'
                 f'<div class="dk-d">{"<b>"+fmt(it.get("due"))+"</b>" if it.get("due") else ""}</div></div>')
    timing = f'<small>{e(s["timing"])}</small>' if s.get("timing") else ''
    out.append(f'<div class="dk-g{" open" if gi == 0 else ""}" style="--sc:{s["color"]}"><div class="dk-h" onclick="this.parentElement.classList.toggle(\'open\')"><span class="ch">▶</span><span class="nm">{e(s["name"])}{timing}</span><div class="bl">{blocks(s)}</div><span class="ct">{c} / {len(s["items"])} complete</span></div><div class="dk-items">{rows}</div></div>')
when = datetime.datetime.fromisoformat(d["updated"]).strftime('%-I:%M %p').lower()
out.append('<div class="dk-foot"><div class="dk-leg">' + ''.join(f'<span style="color:{SC[k]}">{sprite(i, SC[k])}{e(LAB[k])}</span>' for i, k in enumerate(ST)) +
           f'</div><span>snapshot · todo.json rev {d["rev"]} · written {when} by {e(d["updatedBy"])}</span></div></div>')
print(''.join(out))
