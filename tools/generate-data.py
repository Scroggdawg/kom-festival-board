#!/usr/bin/env python3
"""Generate data.json (schema 2) for the KOM festival board.

Sources: the FESTIVALS array extracted from index.html (the 46 curated targets,
extracted via node) and ../research-2026-08-25.json (the full 117-record sweep
with per-record sources). Emits: targets (+S16 promoted), bench, out — with
provenance — plus key dates, premiere ledger, and a fresh rev uuid.
Reports counts, consumed aliases, and dedupe decisions. Run from site/.
"""
import json, re, subprocess, sys, uuid, unicodedata
from datetime import date

SITE = "."
RESEARCH = "../research-2026-08-25.json"

# --- load curated targets from index.html via node ---
node_script = r"""
const fs = require('fs');
const html = fs.readFileSync('index.html','utf8');
const m = html.match(/const FESTIVALS = (\[[\s\S]*?\n\]);/);
if (!m) { console.error('FESTIVALS array not found'); process.exit(1); }
const FESTIVALS = eval(m[1]);
console.log(JSON.stringify(FESTIVALS));
"""
targets_raw = json.loads(subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True, cwd=SITE).stdout)

research = json.load(open(RESEARCH))["festivals"]

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60]

# board target name -> research record names it consumes (aliases eat duplicates)
ALIASES = {
  "Sundance 2027": ["Sundance Film Festival 2027"],
  "PAFF 2027": ["Pan African Film & Arts Festival (PAFF)"],
  "Tampere 57th": ["Tampere Film Festival"],
  "Atlanta FF 51st": ["Atlanta Film Festival"],
  "Flickerfest 36th": ["Flickerfest International Short Film Festival"],
  "SXSW 2027": ["SXSW Film & TV Festival 2027 - Narrative Shorts"],
  "Carthage JCC 37th": ["Carthage Film Festival — JCC (37th edition)"],
  "SBIFF 42nd": ["Santa Barbara International Film Festival (SBIFF)"],
  "FESPACO 30th": ["FESPACO — Panafrican Film and Television Festival of Ouagadougou (30th edition)"],
  "Clermont-Ferrand 49th": ["Clermont-Ferrand International Short Film Festival (+ Marché du Film Court)"],
  "Aspen Shortsfest 36th": ["Aspen Shortsfest"],
  "Cleveland CIFF51": ["Cleveland International Film Festival"],
  "Florida FF 36th": ["Florida Film Festival"],
  "College Television Awards 46th": ["College Television Awards, 46th (Television Academy Foundation)"],
  "Joburg FF 9th": ["Joburg Film Festival (9th edition)"],
  "Toronto Black FF": ["Toronto Black Film Festival"],
  "REGARD 31st": ["REGARD — Saguenay International Short Film Festival"],
  "Berlinale Shorts 77th": ["Berlinale Shorts 2027"],
  "Krakow FF 67th": ["Krakow Film Festival"],
  "Luxor African FF 16th": ["Luxor African Film Festival (16th edition)"],
  "Seattle SIFF 2027": ["Seattle International Film Festival (SIFF)"],
  "Vienna Shorts 2027": ["Vienna Shorts"],
  "ABFF — HBO Short Film Award": [
      "HBO Short Film Award at the American Black Film Festival (ABFF 2027)",
      "American Black Film Festival — HBO Short Film Award",
      "American Black Film Festival (ABFF)"],
  "Tribeca 2027": ["Tribeca Festival 2027 - Narrative Shorts"],
  "Cannes — La Cinef 2027": ["Cannes - La Cinef 2027 (student film selection)"],
  "Cannes — Short Films in Competition 2027": ["Cannes Short Films in Competition 2027 (Short Film Palme d'Or)"],
  "Durban IFF 48th": ["Durban International Film Festival (48th edition)"],
  "Indy Shorts 2027": ["Indy Shorts International Film Festival (Heartland Film)"],
  "BlackStar 2027": ["BlackStar Film Festival"],
  "DGA Student Awards 2027": ["DGA Student Spotlight Awards for Underrepresented Directors (2027)"],
  "Student Academy Awards 54th": ["Student Academy Awards (54th, 2027 cycle) — AMPAS"],
  "BronzeLens 18th": ["BronzeLens Film Festival"],
  "Curtas Vila do Conde 35th": ["Curtas Vila do Conde — International Film Festival", "Curtas Vila do Conde (Portugal)"],
  "TIFF Short Cuts 2027": ["TIFF Short Cuts 2027"],
  "Venice — Orizzonti Corti 2027": ["Venice - Orizzonti Short Films 2027 (Orizzonti Corti)"],
  "Aesthetica 17th": ["Aesthetica Film Festival (ASFF)"],
  "New Orleans FF 2027": ["New Orleans Film Festival"],
  "HollyShorts 23rd": ["HollyShorts Film Festival"],
  "AMAA 2027": ["AMAA — Africa Movie Academy Awards (shorts categories)"],
  "AFI FEST 2027 + Conservatory Showcase": [
      "AFI FEST (Conservatory Showcase 2026 + open call 2027)",
      "AFI Conservatory Showcase at AFI FEST 2026 (+ AFI Thesis Showcase)"],
  "Chicago Intl 63rd": ["Chicago International Film Festival"],
  "ADIFF NY 2027": ["ADIFF — African Diaspora International Film Festival",
                     "African Diaspora International Film Festival (ADIFF)"],
  "Winterthur 31st": ["Internationale Kurzfilmtage Winterthur"],
  "Urbanworld 2027": ["Urbanworld Film Festival"],
  "AFRIFF 2027": ["AFRIFF — Africa International Film Festival"],
  "Palm Springs ShortFest 2027": ["Palm Springs International ShortFest"],
}

OUT = {  # research name fragments -> verdict (from the board's ruled-out table)
  "International Film Festival Rotterdam": "Dates collide head-on with Sundance and shorts must commit world/international/European premiere status; no longer Oscar-qualifying. The one winter major deliberately let go.",
  "BFI London Film Festival": "UK and Irish films only — a US-produced AFI thesis cannot submit.",
  "Africa in Motion": "Defunct — ran 2006–2022; domain dead.",
  "NBCUniversal Short Film Festival": "Dormant — no confirmed editions; re-check only if news breaks.",
  "New Voices in Black Cinema": "Dormant — BAM festival page 404s; no confirmed edition.",
  "Smithsonian NMAAHC": "Dormant since the 2018 inaugural edition; unreachable.",
  "BAFTA Student Awards": "Likely defunct since 2023 after BAFTA restructured its North America programs.",
  "Middleburg Film Festival": "Curated awards-season features event; no open shorts lane.",
  "BSC Short Film Cinematography": "UK-linked eligibility; ruled out.",
  "Princess Grace Awards": "School-nominated scholarships for upcoming thesis work; nomination window passed.",
  "Morehouse College Human Rights": "Thematic bullseye but Oscar-qualifying status has lapsed (not on the 99th list) — community submission at best.",
  "Indie Memphis": "Great Southern room, no live-action qualifying path — winnable-circuit next ring, not this list.",
  "RiverRun": "Oscar-qualifying only for doc/animated shorts — no live-action path. Regional depth only.",
  "Sidewalk Film Festival": "No qualifying path; beloved Southern room for the winnable-circuit next ring.",
}

def close_from_research(rec):
    fd = rec.get("final_deadline") or ""
    m = re.search(r"(~?)(\d{4})-(\d{2})(?:-(\d{2}))?", fd)
    if not m: return None, True
    est = bool(m.group(1)) or "estimat" in fd.lower() or bool(rec.get("estimated"))
    return f"{m.group(2)}-{m.group(3)}-{m.group(4) or '01'}", est

def first_source(rec):
    s = rec.get("sources") or []
    return s[0] if s else ""

consumed, out_recs, bench_recs, report = set(), [], [], []
by_norm = {}
for r in research:
    by_norm.setdefault(norm(r.get("name","")), []).append(r)

# consume aliases
alias_sources = {}
for board, names in ALIASES.items():
    found = []
    for n in names:
        recs = by_norm.get(norm(n))
        if recs:
            consumed.add(norm(n)); found += recs
    if not found:
        report.append(f"UNMATCHED TARGET: {board} (aliases {names})")
    alias_sources[board] = found

# S16 promotion (target #47)
s16 = by_norm.get(norm("S16 Film Festival"))
if s16: consumed.add(norm("S16 Film Festival"))

# out records
for r in research:
    k = norm(r.get("name",""))
    if k in consumed: continue
    for frag, verdict in OUT.items():
        if norm(frag) in k:
            consumed.add(k)
            cl, est = close_from_research(r)
            out_recs.append({
                "id": slug(r["name"]), "name": r["name"],
                "loc": ", ".join(x for x in [r.get("city"), r.get("country")] if x),
                "disposition": "out", "outVerdict": verdict,
                "fit": r.get("fit_score"), "close": cl, "estimated": est,
                "source": first_source(r), "lastChecked": "2026-08-25",
                "events": [], "notes": [],
            })
            break

# bench = everything else, deduped by normalized name
seen_bench = set()
for r in research:
    k = norm(r.get("name",""))
    if k in consumed or k in seen_bench: continue
    seen_bench.add(k)
    cl, est = close_from_research(r)
    why = (r.get("fit_reason") or "").strip()
    bench_recs.append({
        "id": slug(r["name"]), "name": r["name"],
        "loc": ", ".join(x for x in [r.get("city"), r.get("country")] if x),
        "disposition": "bench",
        "benchNote": (why[:200] + "…") if len(why) > 200 else why,
        "fit": r.get("fit_score"), "close": cl, "estimated": est,
        "path": (r.get("oscar_qualifying") or "")[:80],
        "source": first_source(r), "lastChecked": "2026-08-25",
        "events": [], "notes": [],
    })

# targets: curated board rows + provenance from consumed research
targets = []
for t in targets_raw:
    recs = alias_sources.get(t["name"], [])
    src = first_source(recs[0]) if recs else ""
    targets.append({
        "id": slug(t["name"]), "name": t["name"], "loc": t["loc"], "cat": t["cat"],
        "tier": t["tier"], "disposition": "target",
        "edition": t["edition"], "open": t["open"], "close": t["close"],
        "estimated": t["estimated"], "feesText": t["fees"], "tiers": [],
        "path": t["path"], "why": t["why"], "festDate": t.get("festDate",""),
        "links": {"site": "", "filmfreeway": ""},
        "source": src, "lastChecked": "2026-08-25",
        "events": [], "notes": [],
    })

# S16 as target 47
if s16:
    r = s16[0]
    targets.append({
        "id": "s16-2027", "name": "S16 Film Festival 2027", "loc": "Lagos, Nigeria",
        "cat": "Nigerian arthouse — Surreal16", "tier": "strong", "disposition": "target",
        "edition": "~Dec 2027", "open": "2027-05-01", "close": "2027-07-03",
        "estimated": True, "feesText": "$15–25", "tiers": [],
        "path": "AFP Critics Prize", "festDate": "2027-12-09",
        "why": "Run by the Surreal16 collective (C.J. Obasi, Abba Makama, Michael Omonua) — the exact lineage of chiaroscuro Yoruba-spiritual cinema. The 2026 window closed before the campaign started; 2027 is the play. Nigerian premiere required — sequence after AFRIFF decisions, not before.",
        "links": {"site": "", "filmfreeway": ""},
        "source": first_source(r), "lastChecked": "2026-08-25",
        "events": [], "notes": [],
    })

festivals = targets + bench_recs + out_recs
ids = [f["id"] for f in festivals]
dups = {i for i in ids if ids.count(i) > 1}
if dups: report.append(f"DUPLICATE IDS: {dups}")

data = {
    "schema": 2,
    "rev": str(uuid.uuid4()),
    "updated": date.today().isoformat(),
    "keyDates": [
        {"id": "sundance-final", "label": "until the Sundance final deadline", "date": "2026-08-31", "showDate": True, "detail": "Aug 31, 2026 · $95"},
        {"id": "oscar-window", "label": "100th-Oscars qualifying window", "date": "2026-10-01", "endDate": "2027-09-30", "showDate": False, "detail": ""},
    ],
    "premieres": [
        {"id": "world", "label": "World premiere", "state": "available", "byFestivalId": None, "date": None, "note": ""},
        {"id": "international", "label": "International premiere", "state": "available", "byFestivalId": None, "date": None, "note": "Survives US-only screenings — Berlinale/TIFF's door"},
        {"id": "north-america", "label": "North American premiere", "state": "available", "byFestivalId": None, "date": None, "note": "REGARD's Grand Prize rides on it"},
        {"id": "us", "label": "US premiere", "state": "available", "byFestivalId": None, "date": None, "note": "Tribeca's award track rides on it"},
        {"id": "la", "label": "Los Angeles premiere", "state": "available", "byFestivalId": None, "date": None, "note": "Reserved by plan for ABFF-HBO"},
        {"id": "ny", "label": "New York premiere", "state": "available", "byFestivalId": None, "date": None, "note": "Held for Urbanworld"},
        {"id": "atlanta", "label": "Atlanta premiere", "state": "available", "byFestivalId": None, "date": None, "note": "Atlanta FF first, then BronzeLens"},
        {"id": "france", "label": "France unscreened", "state": "available", "byFestivalId": None, "date": None, "note": "A Clermont screening spends it — closes both Cannes doors"},
    ],
    "festivals": festivals,
}

with open("data.json", "w") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)

t, b, o = len(targets), len(bench_recs), len(out_recs)
print(f"targets={t} bench={b} out={o} total={t+b+o} (research raw={len(research)})")
for line in report: print(line)
print("rev:", data["rev"])
