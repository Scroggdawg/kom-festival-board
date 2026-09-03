#!/usr/bin/env python3
"""Expand the fit heat map from 17 rows to all 97 targets (2026-09-03).

Scoring rubric (assessed, not measured — same five dimensions as before):
  prestige  industry weight of the laurel itself
  craft     how much the festival notices/rewards cinematography and craft
  story     fit with THIS film (Black American story, Yoruba faith, 1834 SC)
  oscar     value toward the 100th Academy Awards SPECIFICALLY — a qualifying
            festival whose reachable edition falls outside the Oct 1 2026–
            Sep 30 2027 window scores low, because it cannot help this cycle
  access    realistic odds of selection / winning the award that matters

Also: sorts heat rows by tier then composite score, and stars Joan's picks.
Run from site/.
"""
import re, sys

NEW = {
 # --- Joan picks + existing targets not previously scored ---
 "tampere-57th":                    (8, 7, 6, 8, 5),
 "flickerfest-36th":                (7, 7, 5, 7, 5),
 "carthage-jcc-37th":               (6, 5, 9, 2, 6),
 "sbiff-42nd":                      (7, 6, 5, 7, 4),
 "cleveland-ciff51":                (6, 6, 5, 8, 6),
 "florida-ff-36th":                 (6, 6, 5, 7, 6),
 "college-television-awards-46th":  (6, 6, 6, 1, 5),
 "joburg-ff-9th":                   (5, 5, 9, 1, 7),
 "toronto-black-ff":                (5, 4, 9, 1, 8),
 "regard-31st":                     (8, 7, 6, 6, 5),
 "krakow-ff-67th":                  (7, 7, 6, 7, 5),
 "luxor-african-ff-16th":           (5, 5, 10, 1, 7),
 "seattle-siff-2027":               (6, 6, 5, 7, 5),
 "vienna-shorts-2027":              (7, 7, 6, 8, 6),
 "tribeca-2027":                    (9, 7, 7, 8, 3),
 "indy-shorts-2027":                (6, 6, 5, 8, 6),
 "dga-student-awards-2027":         (7, 6, 7, 1, 5),
 "student-academy-awards-54th":     (8, 7, 7, 9, 4),
 "bronzelens-18th":                 (6, 5, 10, 8, 7),
 "curtas-vila-do-conde-35th":       (7, 7, 6, 7, 5),
 "venice-orizzonti-corti-2027":     (10, 8, 6, 8, 2),
 "aesthetica-17th":                 (6, 8, 5, 2, 6),
 "new-orleans-ff-2027":             (6, 6, 10, 3, 6),
 "hollyshorts-23rd":                (6, 6, 5, 8, 5),
 "amaa-2027":                       (6, 5, 10, 1, 6),
 "chicago-intl-63rd":               (7, 7, 6, 3, 4),
 "adiff-ny-2027":                   (4, 4, 10, 1, 8),
 "winterthur-31st":                 (7, 7, 5, 7, 5),
 "urbanworld-2027":                 (7, 5, 10, 3, 6),
 "s16-2027":                        (5, 8, 5, 1, 6),
 "st-louis-international-film-festival-sliff": (6, 6, 6, 9, 7),
 "deadcenter-film-festival":        (5, 5, 5, 8, 8),
 "raindance-film-festival":         (6, 6, 6, 8, 6),
 "interfilm-international-short-film-festival-berlin": (6, 6, 5, 2, 6),
 "virginia-film-festival":          (6, 5, 8, 1, 7),
 "slamdance-film-festival":         (7, 6, 5, 8, 5),
 "zinebi-international-festival-of-documentary-and-short-film-": (6, 6, 5, 2, 5),
 "new-hampshire-film-festival":     (5, 5, 4, 2, 7),
 "international-short-film-festival-oberhausen": (8, 7, 5, 7, 3),
 "international-film-festival-rotterdam-ammodo-tiger-short-com": (9, 8, 6, 1, 3),
 "riverrun-international-film-festival": (5, 5, 8, 1, 6),
 "sidewalk-film-festival":          (5, 5, 9, 1, 7),
 "sffilm-2027":                     (8, 7, 6, 8, 4),
 "sf-black-ff-2027":                (4, 4, 9, 1, 8),
 "la-shorts-2027":                  (5, 5, 5, 4, 5),
 "san-jose-shorts-2027":            (4, 4, 4, 2, 7),
 "slo-iff-2027":                    (4, 5, 5, 1, 7),
 "santa-fe-iff-2027":               (5, 6, 5, 2, 6),
 "ann-arbor-65th":                  (7, 7, 4, 7, 4),
 "mspiff-45th":                     (5, 5, 5, 1, 7),
 "montclair-2027":                  (6, 5, 5, 1, 5),
 "teaneck-2027":                    (3, 3, 9, 1, 9),
 "ashland-26th":                    (4, 5, 5, 1, 7),
 "dirty-popcorn-2027":              (2, 2, 8, 1, 8),
 "gary-black-ff-16th":              (3, 3, 9, 1, 9),
 "twin-cities-black-2027":          (3, 3, 8, 1, 6),
 "newark-black-ff-2027":            (6, 4, 10, 1, 6),
 "nc-black-ff-25th":                (3, 3, 9, 1, 8),
 "gcuff-16th":                      (4, 4, 9, 1, 8),
 "greenwood-2027":                  (3, 3, 10, 1, 8),
 "tallgrass-2027":                  (5, 6, 10, 1, 7),
 "seattle-black-ff-2027":           (4, 4, 9, 1, 7),
 "denton-black-ff-13th":            (4, 4, 9, 1, 8),
 "roxbury-2027":                    (6, 6, 10, 1, 7),
 "cascade-african-37th":            (4, 4, 10, 1, 8),
 "buff-2027":                       (5, 4, 9, 1, 7),
 "affa-2027":                       (3, 3, 9, 1, 8),
 "ficaa-15th":                      (3, 3, 9, 1, 8),
 "hamburg-43rd":                    (5, 6, 5, 1, 6),
 "warsaw-2027":                     (6, 6, 5, 2, 5),
 "in-the-palace-24th":              (5, 5, 5, 7, 6),
 "drama-disff-2027":                (7, 7, 6, 6, 5),
 "anonimul-2027":                   (4, 4, 5, 1, 7),
 "bafici-2027":                     (7, 6, 6, 1, 5),
 "viff-2027":                       (6, 5, 5, 1, 5),
 "fnc-2027":                        (7, 7, 6, 2, 5),
 "show-me-shorts-2027":             (5, 5, 5, 2, 6),
 "bisff-44th":                      (6, 6, 5, 6, 4),
 "short-shorts-2027":               (7, 7, 6, 8, 5),
 "isc-osaka-2027":                  (3, 4, 4, 1, 6),
}

html = open("index.html").read()

m = re.search(r"(const HEAT = \{\n)(.*?)(\};\n)", html, re.S)
if not m: sys.exit("HEAT block not found")
existing_ids = set(re.findall(r'"([^"]+)":', m.group(2)))

lines = []
for fid, (p, c, s, o, a) in NEW.items():
    if fid in existing_ids:
        print(f"  skip (already scored): {fid}")
        continue
    lines.append(f'  "{fid}": {{ prestige: {p}, craft: {c}, story: {s}, oscar: {o}, access: {a} }},\n')

html = html[:m.end(2)] + "".join(lines) + html[m.end(2):]
print(f"added {len(lines)} heat rows")

# --- sort rows by tier then composite, and star Joan picks ---
old_rows = '''  const rows = Object.keys(HEAT).map(id => {
    const f = DATA.festivals.find(v => v.id === id);
    if (!f) return "";
    const h = HEAT[id];
    const ramp = RAMPS[f.tier] || RAMPS.strong;
    return `<tr><td class="rowlabel"><span class="tiermark" style="background:${tierColor[f.tier]}"></span>${esc(f.name)}</td>${dims.map(d => {'''
new_rows = '''  const tierRank = { dream: 0, strong: 1, worthy: 2 };
  const scored = Object.keys(HEAT).map(id => {
    const f = DATA.festivals.find(v => v.id === id);
    if (!f || f.disposition !== "target") return null;
    const h = HEAT[id];
    return { id, f, h, total: h.prestige + h.craft + h.story + h.oscar + h.access };
  }).filter(Boolean).sort((a, b) =>
    (tierRank[a.f.tier] ?? 3) - (tierRank[b.f.tier] ?? 3) || b.total - a.total || a.f.name.localeCompare(b.f.name));
  const rows = scored.map(({ id, f, h }) => {
    const ramp = RAMPS[f.tier] || RAMPS.strong;
    return `<tr><td class="rowlabel"><span class="tiermark" style="background:${tierColor[f.tier]}"></span>${esc(f.name)}${f.joanPick ? ` <span style="color:var(--gold)" title="Joan pick">★</span>` : ""}</td>${dims.map(d => {'''
if old_rows not in html: sys.exit("renderHeat row builder not found")
html = html.replace(old_rows, new_rows, 1)

# section note
old_note = "Assessed fit of the seventeen highest-value targets across five dimensions, 0–10."
new_note = ("Assessed fit of all 97 targets across five dimensions, 0–10, ranked by tier then total score. "
            "★ marks Joan's picks. Oscar path scores the 100th Awards specifically — a qualifying festival whose "
            "reachable edition falls outside the Oct 1, 2026–Sep 30, 2027 window scores low, because it cannot help this cycle.")
if old_note not in html: sys.exit("section note not found")
html = html.replace(old_note, new_note, 1)

open("index.html", "w").write(html)
print("renderHeat sorted + starred; section note updated")
