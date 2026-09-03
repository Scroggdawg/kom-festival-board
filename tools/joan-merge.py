#!/usr/bin/env python3
"""One-shot merge of Joan's 75 picks into data.json (2026-09-03).

- Flags the 25 existing targets joanPick.
- Promotes 9 bench + 3 ruled-out records to target, enriched to full shape.
- Adds 38 new target records from Joan's sheet + the Sep 3 research raid.
Run from site/. Idempotent enough to re-run (skips already-present ids).
"""
import json, sys, uuid
from datetime import date

D = json.load(open("data.json"))
by_id = {f["id"]: f for f in D["festivals"]}
TODAYS = "2026-09-03"

EXISTING_TARGETS = [
 "vienna-shorts-2027","flickerfest-36th","sbiff-42nd","paff-2027",
 "palm-springs-shortfest-2027","hollyshorts-23rd","regard-31st","toronto-black-ff",
 "sundance-2027","aspen-shortsfest-36th","tampere-57th","clermont-ferrand-49th",
 "cannes-la-cinef-2027","atlanta-ff-51st","bronzelens-18th","chicago-intl-63rd",
 "new-orleans-ff-2027","tribeca-2027","urbanworld-2027","afriff-2027",
 "cleveland-ciff51","blackstar-2027","durban-iff-48th","sxsw-2027","seattle-siff-2027",
]

# substring -> (tier, enrich dict) for bench/out promotions
PROMOTE = {
 "slamdance": ("strong", dict(cat="LA indie institution · Oscar-qualifying", edition="Feb 18–24, 2027",
   close="2026-10-06", estimated=False, feesText="$63",
   path="Oscar-qualifying — Grand Jury Award for Narrative Short",
   why="Founded by Sundance rejects, now in LA; considers films regardless of premiere status, so nothing already spent costs anything here. Caveat: a February LA screening spends the LA premiere that HollyShorts and LA Shorts require.",
   festDate="2027-02-18")),
 "interfilm": ("worthy", dict(cat="Berlin shorts · Oscar-qualifying", edition="Nov 10–15, 2026 (next entrable: 2027)",
   path="Oscar-qualifying — Best Live Action, International Competition",
   why="Berlin's accessible shorts festival since 1982, qualifying since 2018, no premiere requirement. The Nov 2026 edition closed May 29; the Nov 2027 edition falls outside the 100th-Awards window — a next-cycle play.",
   festDate="2026-11-10")),
 "st-louis": ("strong", dict(cat="Midwest major · Oscar-qualifying ×4", edition="Nov 5–15, 2026",
   feesText="$30", path="Oscar-qualifying — Best of Fest AND Best Live Action both qualify",
   why="Four qualifying awards give a narrative short two live routes, and November 2026 is one of the earliest qualifying swings inside the window. St. Louis-only premiere rule. Confirm the current deadline on FilmFreeway immediately.",
   festDate="2026-11-05")),
 "new-hampshire": ("worthy", dict(cat="New England regional · Oscar-qualifying", edition="Oct 2027 (next entrable)",
   feesText="$27", path="Oscar-qualifying — Shorts Jury Award, Live Action",
   why="Qualifying in all three shorts categories with no premiere requirement and a student category. 2026 closed Jul 15; the Oct 2027 edition lands after the 100th window — next-cycle value.",
   festDate="2027-10-15")),
 "raindance": ("strong", dict(cat="London indie major · Oscar/BAFTA-qualifying", edition="Jun 16–25, 2027",
   close="2027-03-08", estimated=False, feesText="$42 early (Dec 7) · rises to final Mar 8",
   path="Oscar-qualifying — Best Live Action Short; BAFTA-qualifying",
   why="No premiere policy for shorts at all, late deadlines that fit after the winter majors resolve, and June 2027 sits comfortably inside the qualifying window. UK industry exposure for a Black diaspora story.",
   festDate="2027-06-16")),
 "virginia": ("worthy", dict(cat="UVA program · student category", edition="Oct 21–25, 2027",
   feesText="$2.50 student (non-VA university)", path="No qualifying path",
   why="A University of Virginia program running nearly 40 years, 20,000+ attendances. At $2.50 the cost-to-credibility ratio is unbeatable, and a slavery-era Southern story carries obvious weight for a Charlottesville audience.",
   festDate="2027-10-21")),
 "oberhausen": ("worthy", dict(cat="Oldest shorts fest on earth · Oscar-qualifying", edition="Apr 27–May 2, 2027",
   close="2027-01-18", estimated=False, feesText="Free",
   path="Oscar-qualifying — Grand Prize of the City of Oberhausen",
   why="The world's oldest short film festival, free to enter, qualifying, German-premiere rule untouched by US screenings. Curation is avant-garde-first — frame the ritual and spiritual formal elements. Entering forecloses other German festivals first (collides with Hamburg).",
   festDate="2027-04-27")),
 "zinebi": ("worthy", dict(cat="Bilbao shorts · Oscar-qualifying", edition="Nov 20–27, 2026 (next entrable: 2027)",
   path="Oscar-qualifying — ZINEBI Grand Prize, International Short Film Competition (€8,000)",
   why="FIAPF-recognized since 1974; the Spanish-premiere rule binds Spanish productions only. The 2026 deadline passed Jul 1 and Nov 2027 falls outside the 100th window — next-cycle value with a real cash prize.",
   festDate="2026-11-20")),
 "deadcenter": ("strong", dict(cat="Oklahoma's Oscar-qualifying fest", edition="Jun 9–13, 2027",
   close="2026-10-15", estimated=True, feesText="$30",
   path="Oscar-qualifying — Best Live Action Short (winner only)",
   why="Oklahoma's largest festival and its only Oscar qualifier — triple-qualifying, MovieMaker '20 Coolest,' strong hospitality. Possibly the best win-probability-to-qualification ratio on Joan's whole list, and June 2027 is inside the window.",
   festDate="2027-06-09")),
 "sidewalk": ("worthy", dict(cat="Birmingham · Black Lens program", edition="Aug 2027",
   feesText="$24 student", path="No qualifying path",
   why="Birmingham's flagship since 1999 with a dedicated Black Lens program for Black filmmakers and $10k+ in cash awards. No Oscar path — reinstated on Joan's case: Deep South audience resonance and a winnable student category.",
   festDate="2027-08-24")),
 "rotterdam": ("worthy", dict(cat="A-list Europe · Tiger Shorts", edition="Jan 28–Feb 7, 2027",
   close="2026-09-15", estimated=False, feesText="€85",
   path="Not Oscar-qualifying; EFA pipeline",
   why="A genuine A-list slot — the Tiger Short Competition is among Europe's most prestigious. Requires at minimum a European premiere (a US-only history preserves it) and its dates collide with Sundance. A deliberate Europe-first pivot, not a default: deadline Sep 15.",
   festDate="2027-01-28")),
 "riverrun": ("worthy", dict(cat="Southern regional · qualifying doc/anim only", edition="Apr 16–24, 2027",
   close="2026-12-01", estimated=True, feesText="$20",
   path="Oscar-qualifying for animated + documentary shorts ONLY — no live-action path",
   why="Respected Winston-Salem festival 200 miles from where the story is set. The Academy list settles it: no live-action narrative award qualifies, so this is regional resonance and press, not an Oscar play. NC premiere required — intact.",
   festDate="2027-04-16")),
}

def N(id, name, loc, cat, tier, edition, close, est, fees, path, why, festDate, site="", ff="", source="", open_=""):
    return dict(id=id, name=name, loc=loc, cat=cat, tier=tier, disposition="target",
        edition=edition, open=open_, close=close, estimated=est, feesText=fees, tiers=[],
        path=path, why=why, festDate=festDate,
        links={k: v for k, v in (("site", site), ("filmfreeway", ff)) if v},
        source=source or site or ff, lastChecked=TODAYS, events=[], notes=[], joanPick=True)

NEW = [
 N("sffilm-2027","SFFILM 2027","San Francisco, USA","Longest-running fest in the Americas · Oscar-qualifying","strong",
   "Apr 22–May 2, 2027","2026-11-11",False,"$50",
   "Oscar-qualifying — Golden Gate Award for Best Narrative Short",
   "Founded 1957; blue-chip curatorial brand whose premiere bar is only Bay Area — prior screenings elsewhere cost nothing. Highly selective: a reach, not a banker.",
   "2027-04-22", site="https://sffilm.org", source="https://sffilm.org"),
 N("sf-black-ff-2027","San Francisco Black FF 2027","San Francisco, USA","Juneteenth community festival","worthy",
   "Jun 17–20, 2027","2026-10-17",True,"$22.50 student","No qualifying path",
   "Founded 1998 by publicist Ave Montague with a $200 budget; a beloved Juneteenth-tied community festival, now family-run. Diaspora audience-building at low cost.",
   "2027-06-17"),
 N("la-shorts-2027","LA Shorts Fest 2027","Los Angeles, USA","LA institution · qualifies via Best of Fest only","worthy",
   "Jul 16–27, 2027","2027-06-01",True,"$49",
   "Oscar-qualifying awards: Best of Fest / Animation / Documentary / International — a US fiction short's only route is Best of Fest",
   "Longest-running shorts festival in LA (1997), 69 alumni Oscar nominations. Requires no prior LA County screening — mutually exclusive with a February LA play.",
   "2027-07-16", site="https://www.lashortsfest.com", source="https://www.lashortsfest.com/submit-film"),
 N("san-jose-shorts-2027","San Jose Int'l Short FF 2027","San Jose, USA","Boutique shorts fest · qualifies after this window","worthy",
   "Oct 22–25, 2027","2027-06-30",True,"$35",
   "Oscar-qualifying — Best of the Fest only; Oct 2027 dates land after the 100th-Awards window",
   "MovieMaker 'worth the entry fee' pick. A win here counts toward the 101st Oscars, not the 100th — second-year backstop.",
   "2027-10-22", site="https://sjsff.com", source="https://sjsff.com/festival/"),
 N("slo-iff-2027","San Luis Obispo IFF 2027","San Luis Obispo, USA","Central Coast regional · doc-only qualifying","worthy",
   "Apr 22–27, 2027","2026-09-30",True,"$30",
   "Oscar-qualifying for Best Documentary Short ONLY — no narrative path",
   "Respected regional with $500 cash prizes in the George Sidney competition and no premiere requirement. Worth $30 as exposure and a possible cash prize; not an Oscar play for a fiction short.",
   "2027-04-22", site="https://www.slofilmfest.org", source="https://www.slofilmfest.org/submissions/"),
 N("santa-fe-iff-2027","Santa Fe IFF 2027","Santa Fe, USA","Young qualifier · $15k Panavision prize","worthy",
   "Oct 2027","2027-07-09",True,"$36",
   "Oscar-qualifying — Best Narrative Short (+$15,000 Panavision package + $500 cash); Oct 2027 lands after the 100th window",
   "Newly qualifying since Oct 2024 in New Mexico's production hub, with softer competition than coastal qualifiers. The 2026 edition closed Jul 9 — this records the 2027 edition, which feeds the following cycle.",
   "2027-10-14"),
 N("ann-arbor-65th","Ann Arbor FF 65th","Ann Arbor, USA","Oldest avant-garde fest · narrative qualifying path","worthy",
   "Mar 23–28, 2027","2026-09-30",False,"$80 late tier",
   "Oscar-qualifying — Lawrence Kasdan Award for Best Narrative Film (+ Ken Burns Best of Fest)",
   "Founded 1963, ~$40,000 in awards, no premiere requirement. Curation is experimental-first — frame the film around its ritual and spiritual formal elements. Late deadline Sep 30, 2026 is still open.",
   "2027-03-23", site="https://www.aafilmfest.org", source="https://www.aafilmfest.org/call-for-entries"),
 N("mspiff-45th","MSPIFF 45","Minneapolis–St. Paul, USA","Upper Midwest's largest · near-free entry","worthy",
   "Apr 7–18, 2027","2026-09-01",True,"~$12 with student ID (50% off $24)","No qualifying path (verified)",
   "Running since 1981, 200+ films for a big Twin Cities audience. With the student discount and a known fee-waiver email, likely the best cost-per-audience ratio on Joan's sheet.",
   "2027-04-07", site="https://mspfilm.org", source="https://mspfilm.org/mspiff45/"),
 N("montclair-2027","Montclair FF 2027","Montclair, NJ, USA","Awards-season regional · NYC industry","worthy",
   "Oct 2027","2027-04-30",True,"$25 student","No shorts qualifying path",
   "Founded 2012 with the Colbert family as backers; trade press calls it an early Oscar proving ground for features. High-credibility NYC-adjacent exposure rare at this price. Joan ranked it #1 in New Jersey.",
   "2027-10-16"),
 N("teaneck-2027","Teaneck IFF 2027","Teaneck, NJ, USA","Social-justice festival · Puffin Foundation","worthy",
   "Nov 2027","2027-06-13",True,"$20","No qualifying path",
   "Founded 2006, themed 'Activism: Making Change'; programs heavily around racial-justice history. A story of enslavement, faith and resistance is a near-perfect mission fit — position it as social-justice storytelling in the cover note.",
   "2027-11-05"),
 N("ashland-26th","Ashland Independent FF 26th","Ashland, OR, USA","Rebuilding Rogue Valley indie","worthy",
   "Spring 2027","2026-10-01",True,"$35 ($10 student discount)","No qualifying path (did not survive its financial crisis)",
   "Historically a filmmaker-hospitality standout; a reorganized board eliminated the debt and is rebuilding at roughly half the former footprint. Southern-Oregon-only premiere bar. Price the laurel at post-crisis value.",
   "2027-04-15"),
 N("dirty-popcorn-2027","Dirty Popcorn Black FF 2027","Wilmington, DE, USA","Museum-hosted micro-fest · free","worthy",
   "Aug 2027","2027-07-12",True,"Free","No qualifying path",
   "Two-day showcase hosted by the Delaware Art Museum. Free to submit; stated priority is BIPOC filmmakers from DE/MD/NJ/PA/NY. Verify a 2026 edition actually ran before counting on 2027.",
   "2027-08-09"),
 N("gary-black-ff-16th","Gary Int'l Black FF 16th","Gary, IN, USA","City-backed Chicagoland Black fest","worthy",
   "Oct 15–18, 2026","2026-09-21",False,"$15","No qualifying path",
   "Founded ~2010, 30 minutes from Chicago, backed by the mayor's office, with genuine Chicagoland Black audience reach. A plausible win on the mid-tier — and the 2026 deadline is Sep 21, two and a half weeks out.",
   "2026-10-15", ff="https://filmfreeway.com/GIBFF", source="https://gary.capitalbnews.org/gary-international-black-film-festival/"),
 N("twin-cities-black-2027","Twin Cities Black FF 2027","Minneapolis, USA","Longest-standing Black fest in the Upper Midwest","worthy",
   "Sep 2027","2027-06-20",True,"$22.50 student","No qualifying path",
   "Founded ~2002 by Natalie Morrow; small (~1,000 attendees, 3 awards) but 24 years running. The official site is stale while FilmFreeway is active — one email before paying.",
   "2027-09-24", ff="https://filmfreeway.com/tcbff", source="https://filmfreeway.com/tcbff"),
 N("newark-black-ff-2027","Newark Black FF 2027","Newark, NJ, USA","Oldest Black film festival in the US (1974)","worthy",
   "Jul–Aug 2027","2027-05-01",True,"TBC","No qualifying path; juried Paul Robeson Awards (historically biennial — confirm cycle)",
   "Run by The Newark Museum of Art annually since 1974; early platforms for Spike Lee, Barry Jenkins, Ava DuVernay. 'Official selection of America's oldest Black film festival' is a laurel with historical weight, and the museum setting suits a period drama about ancestral faith.",
   "2027-07-08", site="https://newarkblackfilmfestival.com", source="https://newarkblackfilmfestival.com/"),
 N("nc-black-ff-25th","North Carolina Black FF 25th","Wilmington, NC, USA","Black Arts Alliance · 24 straight years","worthy",
   "May 2027","2027-02-01",True,"TBC","No qualifying path",
   "Presented by Wilmington's Black Arts Alliance for 24 consecutive years, drawing entries from NC to Kenya. A South Carolina story plays close to home in a legacy production town.",
   "2027-05-01"),
 N("gcuff-16th","Greater Cleveland Urban FF 16th","Cleveland, USA","Nine-day hybrid diaspora platform","worthy",
   "Sep 2027","2027-05-31",False,"$25","No qualifying path",
   "Founded 2012; nine days in-person plus virtual means real audience exposure, not one slot. Submission window runs Feb 1–May 31 every year — calendar February.",
   "2027-09-17", site="https://www.gcuff.org", source="https://www.gcuff.org/filmmakers"),
 N("greenwood-2027","Greenwood FF 2027","Tulsa — Greenwood, USA","Black Wall Street · massacre-centennial founding","worthy",
   "Sep 2027","2027-04-03",True,"TBC","No qualifying path",
   "Launched June 2021 — the Tulsa Race Massacre centennial — in the historic Greenwood district, with OSU-Tulsa as sponsor. A film about an enslaved man reclaiming ancestral faith, screening where Black self-determination was burned and rebuilt: unmatched narrative alignment.",
   "2027-09-06"),
 N("tallgrass-2027","Tallgrass FF 2027 — Gordon Parks Award","Wichita, KS, USA","Named award for Black excellence · free entry","strong",
   "Oct 2027","2027-02-09",True,"Free (Gordon Parks category)",
   "Gordon Parks Award for Black Excellence in Filmmaking — Short Film (category added 2025; short-film prize amount unconfirmed)",
   "The award honors the pioneering Black photographer-director whose period craft mirrors this film's, backed by the Kansas African American Museum and the Wichita NAACP. Feature-level winners get $5,000 + $15,000 Panavision rental.",
   "2027-10-15", site="https://tallgrassfilm.org", source="https://tallgrassfilm.org/tallgrass-film-festival-announces-5000-gordon-parks-award-for-outstanding-black-filmmaker/"),
 N("seattle-black-ff-2027","Seattle Black FF 2027","Seattle, USA","Langston Hughes legacy since 2003","worthy",
   "Late Apr 2027","2026-10-21",True,"$35","No qualifying path",
   "Founded 2003 as the Langston Hughes African American Film Festival; renamed 2020 explicitly to embrace the whole Black diaspora — a Nigerian-directed Yoruba story is what the rebrand courts. Run by LANGSTON at the city-owned institute.",
   "2027-04-22"),
 N("denton-black-ff-13th","Denton Black FF 13th","Denton, TX, USA","Largest Black fest in Texas/Southwest","worthy",
   "Late Jan 2027","2026-10-15",True,"$31.50 college category","No qualifying path",
   "Founded 2015, now a major regional draw — film, music, spoken word, tech expo. The college category means competing against student work in a big Southern Black market during Black History Month season.",
   "2027-01-27", site="https://dentonbff.com", source="https://dentonbff.com/about/"),
 N("roxbury-2027","Roxbury Int'l FF 2027","Boston, USA","New England's largest fest for filmmakers of color","strong",
   "Jun–Jul 2027","2027-01-17",True,"$25","No qualifying path",
   "Running since ~1998; screens inside the Museum of Fine Arts Boston as an official partner — museum-grade curatorial validation for a high-craft period drama, in Boston's academic and Black arts community.",
   "2027-06-18", site="https://www.roxfilmfest.com", source="https://www.roxfilmfest.com/ourstory"),
 N("cascade-african-37th","Cascade Festival of African Films 37th","Portland, OR, USA","Longest-running African film fest in the US","worthy",
   "Feb–Mar 2027","2026-08-31",True,"$5","No qualifying path",
   "Founded 1991 by Portland Community College faculty; 36 consecutive editions, always free to the public. A month-long run means genuine community audience for $5. Sheet deadline has likely passed — email to confirm.",
   "2027-02-05"),
 N("buff-2027","British Urban FF 2027","London, UK","Longest-standing Black-owned UK festival","worthy",
   "May 2027","2027-01-31",True,"$21","No qualifying path",
   "Founded 2005; 20th-anniversary Screen Daily profile. The UK beachhead — London's large Nigerian diaspora, with trade-press attention rare at this size. Mid-transition (new leadership, date move): some execution risk.",
   "2027-05-03"),
 N("affa-2027","Africa Film Fest Australia 2027","Sydney, Australia","African-heritage shorts · Opera House venue","worthy",
   "Sep 2027","2027-06-01",True,"$12.49","No qualifying path",
   "Founded ~2023 by Kenyan-Australian filmmakers with Screen NSW backing; 2026 ran at the Sydney Opera House. The shorts category is explicitly for filmmakers of African heritage — the director qualifies directly. $12.49 buys a third continent.",
   "2027-09-03"),
 N("ficaa-15th","Int'l African FF in Argentina 15th","Buenos Aires, Argentina","Latin America's African-diaspora window","worthy",
   "Aug–Sep 2027","2027-03-15",True,"$9.60","No qualifying path",
   "Run by nonprofit Observatorio Sur (~14 editions) across three cities plus a tour. Essentially the only Latin American window for African-diaspora cinema; the Yoruba thread resonates with Afro-Latin religious traditions. Spanish subtitles likely required.",
   "2027-08-01"),
 N("hamburg-43rd","Kurzfilm Festival Hamburg 43rd","Hamburg, Germany","Beloved German indie shorts fest","worthy",
   "Jun 1–6, 2027","2027-01-31",False,"~€8","Not Oscar-qualifying (verified); BAFTA/BIFA-qualifying",
   "Scrappy, respected, more narrative-friendly than Oberhausen. German-premiere rule for the international competition collides with Oberhausen — Germany goes to one of them. Tightest completion window of the group: production not older than Jan 2026.",
   "2027-06-01"),
 N("warsaw-2027","Warsaw FF 2027","Warsaw, Poland","A-list features fest · qualifying shorts sidebar","worthy",
   "Oct 2027","2027-07-31",True,"~€28",
   "Oscar-qualifying — Grand Prix + Best Live Action Short; Oct 2027 lands after the 100th window",
   "FIAPF A-list with four qualifying shorts awards. The 2026 edition closed Jul 31 and Oct 2027 feeds the following cycle — recorded for the long campaign.",
   "2027-10-09"),
 N("in-the-palace-24th","In the Palace 24th","Varna, Bulgaria","Bulgaria's flagship shorts fest · Oscar + SAA qualifying","worthy",
   "Jun 26–Jul 3, 2027","2026-10-01",False,"~$30",
   "Oscar-qualifying — Best Short Fiction (main competition; the student track feeds the Student Academy Awards instead)",
   "Qualifying since 2017 and cheap. Category trap: enter the MAIN fiction competition (or both) — the student category alone doesn't reach the Oscar award. Bulgarian premiere intact. Deadline Oct 1.",
   "2027-06-26"),
 N("drama-disff-2027","Drama ISFF 2027","Drama, Greece","Triple-qualifier for nine euros","strong",
   "Sep 7–13, 2027","2027-04-30",True,"~€9",
   "Oscar-qualifying — Grand Prix, International Competition; BAFTA (new 2026) + EFA qualifying",
   "Greece's leading shorts festival for nearly 50 years — early platform for Lanthimos and Villeneuve. Greek premiere preserved by a US-only history. Its Sep 2027 dates land days before the window closes: a win counts, with zero slack.",
   "2027-09-07"),
 N("anonimul-2027","Anonimul IFF 2027","Sfântu Gheorghe, Romania","Danube Delta indie · hosts one guest","worthy",
   "Aug 2027","2027-05-20",True,"Free","No qualifying path; no premiere requirement",
   "Romania's 'Danube Delta Sundance' (est. 2004), ~5,000 attendees. Free entry, and the festival covers accommodation for one team member if selected. A free bonus, not a pillar.",
   "2027-08-10"),
 N("bafici-2027","BAFICI 2027","Buenos Aires, Argentina","Latin America's premier indie festival · free entry","worthy",
   "Apr 15–26, 2027","2026-12-18",True,"Free","Not Oscar-qualifying; Argentine-premiere-only rule",
   "400+ titles for a huge cinephile audience since 1999. Free entry to genuine critical credibility without spending any premiere that matters. A long international run by April could soften selection odds.",
   "2027-04-15"),
 N("viff-2027","Vancouver IFF 2027","Vancouver, Canada","Big audience fest · NOT Oscar-qualifying","worthy",
   "Oct 2027","2027-06-05",True,"$36",
   "Not on the Academy qualifying list (verified against every Canadian entry)",
   "One of North America's largest audience festivals. Joan's sheet marked it qualifying — it isn't, and both reachable editions miss the 100th window anyway. Recorded as exposure for the long campaign.",
   "2027-10-01"),
 N("fnc-2027","Montréal FNC 2027","Montréal, Canada","Canada's oldest festival · Oscar-qualifying","worthy",
   "Oct 2027","2027-05-01",True,"$35",
   "Oscar-qualifying — Best Short Film, International Competition (Loup Argenté); Oct 2027 feeds the following cycle",
   "Founded 1971; a prestigious auteur/avant-garde house whose taste for formally bold, culturally hybrid work could embrace the film's Yoruba spiritual dimension. Quebec premiere intact.",
   "2027-10-07"),
 N("show-me-shorts-2027","Show Me Shorts 2027","Auckland, New Zealand","NZ's Academy-accredited shorts fest","worthy",
   "Oct 2027","2027-04-01",True,"$15 (30% film-school bulk discount)",
   "Oscar-qualifying — Best International Film; Oct 2027 feeds the following cycle",
   "New Zealand's leading shorts festival and its first Academy-accredited one — a warm nationwide tour. International films explicitly eligible for the qualifying award. A low-cost hedge for a campaign that extends.",
   "2027-10-06"),
 N("bisff-44th","Busan Int'l Short FF 44th","Busan, South Korea","Korea's first Oscar-qualifying festival","worthy",
   "Late Apr 2027","2027-01-05",True,"~$13",
   "Oscar-qualifying — Grand Prix in International Competition (KRW 10,000,000; winner-take-all)",
   "Korea's premier shorts festival at the Busan Cinema Center, also BAFTA/Goya-qualifying. Korean premiere required for international competition — intact. A cheap, genuine qualifying lottery ticket.",
   "2027-04-23"),
 N("short-shorts-2027","Short Shorts FF & Asia 2027","Tokyo, Japan","One of Asia's largest · five qualifying awards","strong",
   "May 31–Jun 9, 2027","2027-01-15",False,"$30",
   "Oscar-qualifying — Best Short awards in International / Asia International / Japan / Animation / Non-Fiction",
   "Founded 1999 by Tetsuya Bessho; George Lucas Award Grand Prix. Multiple qualifying categories beat single-award fests on odds. Japan premiere must hold until ~June 2027: no Japan screenings, no streaming with Japanese subtitles. US screenings fine.",
   "2027-05-31"),
 N("isc-osaka-2027","ISC Award Osaka 2027","Osaka, Japan","Student award · flights + hotel for finalists","worthy",
   "Dec 2027","2027-07-31",True,"Free","No qualifying path; student-enrollment eligibility — confirm post-graduation rules",
   "Run by Osaka's Knowledge Capital: ~1,000 entries from 88 countries, six winners, and finalists get roundtrip flights plus accommodation. The 2026 window closed Jul 31 — this records 2027; confirm films made while enrolled still qualify.",
   "2027-12-04"),
]

# 1) flag existing targets
flagged = 0
for tid in EXISTING_TARGETS:
    f = by_id.get(tid)
    if not f: sys.exit(f"missing expected target id: {tid}")
    if not f.get("joanPick"): f["joanPick"] = True; flagged += 1

# 2) promotions
promoted = []
for key, (tier, enrich) in PROMOTE.items():
    hits = [f for f in D["festivals"] if key in f["id"]]
    if len(hits) != 1: sys.exit(f"promotion key '{key}' matched {len(hits)} records")
    f = hits[0]
    prior = f.pop("benchNote", None) or f.pop("outVerdict", None)
    f.pop("fit", None)
    f["disposition"] = "target"; f["tier"] = tier; f["joanPick"] = True
    for k, v in enrich.items(): f[k] = v
    f.setdefault("open", ""); f.setdefault("tiers", []); f.setdefault("links", {})
    f.setdefault("feesText", ""); f.setdefault("festDate", "")
    f["lastChecked"] = TODAYS
    promoted.append(f["name"])

# 3) new records
added = []
for rec in NEW:
    if rec["id"] in by_id: continue
    D["festivals"].append(rec); added.append(rec["name"])

# dup guard
ids = [f["id"] for f in D["festivals"]]
if len(ids) != len(set(ids)): sys.exit("DUPLICATE IDS — aborting")

D["rev"] = str(uuid.uuid4())
D["updated"] = TODAYS
json.dump(D, open("data.json", "w"), ensure_ascii=False, indent=1)

from collections import Counter
c = Counter(f["disposition"] for f in D["festivals"])
jp = sum(1 for f in D["festivals"] if f.get("joanPick"))
print(f"flagged existing: {flagged} · promoted: {len(promoted)} · added: {len(added)} · joanPick total: {jp}")
print(f"dispositions: {dict(c)} · total: {len(D['festivals'])} · rev: {D['rev']}")
