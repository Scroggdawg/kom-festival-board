# Where each cast bio came from

Compiled 2026-09-14 from the worksheet's own history, the repository, and the recorded session transcripts and subagent logs on Luke's Mac. Every fact in the four bios in field 7.1 traces to a page that was opened and read on 2026-09-10, and every claim was then checked by two independent checkers and a merger. Nothing in the bios was typed from memory. The raw captures are in `press/cast-bios-evidence/`.

Times below are Central (Luke's clock); the transcripts stamp them in UTC, five hours later.

## The chain

| When | What | Where the record is |
|---|---|---|
| 2026-09-08 14:58 | The names first enter the worksheet: Luke, in chat, gives Erik Orjiako (Mace) and Sandra McDaniels (The Elder); Kenner's actor left empty | field 3.15 history, `by: "Luke, in chat"`; commit 8b30cd8 |
| 2026-09-08 22:48 | The full billed cast, with Eric Pargac and Jamal Dennis, from the end-credit roll (`2513 KOM Credits 11-5-SDnotes.xlsx`, End Titles tab) | fields 3.15 and 9.2 history; commit eae7e7e; `press/credits/` |
| 2026-09-10 13:35 | Luke, with a screenshot of a festival form's Key Cast section: "find bios for these actors on either imdb or elsewhere. make sure it is the correct person" | session 4ceb6483 (project folder `25_01 KILLER OF MEN (THESIS)`), first message |
| 13:35 to 13:51 | The research: 9 web searches, 33 page fetches, and, because IMDb and Backstage answer 403 to fetches, 11 reads through the Browser pane | same session; the reads are copied to `press/cast-bios-evidence/source-reads.json` and `browser-reads-full.txt` |
| 13:51 to 14:48 | The four drafts written from the captured facts (the session's own words: "paraphrased from facts, not copied from source bios"), and `kom-cast-bios.md` compiled | `press/cast-bios.md` (moved into the repo with the commit below) |
| 14:48 | The fact-check: a workflow of eight checkers, two per actor (one "source by source", one "overreach and attribution"), then a ninth agent merging the verdicts and producing the final wording. All nine ran on Claude Opus 5 | workflow `wf_7518a3a9-83f`; verdicts copied to `press/cast-bios-evidence/factcheck-verdicts.json` |
| 14:51 to 15:11 | The final bios pasted into the EPK INFO Google Doc's Cast bios section | same session, Browser pane on docs.google.com |
| 14:58 | Field 7.1 written (worksheet rev 23) | commit f00ba4d, co-authored by Claude Opus 5; handoff-110-cast |
| since | 7.1 has one history entry: the text has not changed. The EPK build sessions (this one included) laid the bios out on page 7 and did not touch the words | field 7.1 history; `git log -- press/epk.json` |

**Identity, all four.** The IMDb full-credits page for *Killer of Men* (Short, 2026), tt37523933, was read in the Browser pane at 13:45 and links to exactly these profiles: Erik Orjiako nm8803339 (Mace), Sandra McDaniels nm5062558 (Elder), Eric Pargac nm1655191 (Master Kenner), Jamal Dennis nm2156703 (credited "Fighter2 Kojo"). TMDB's cast page for the film (movie 1705049, fetched 13:36) lists the same four. "Sandra McDaniel" nm12969202, nm12184837, nm8587652 and nm2650381 are other people, checked and ruled out.

## Erik Orjiako (Mace)

**Pages read on 2026-09-10**

| Page | How | Time | What it gave |
|---|---|---|---|
| IMDb nm8803339, bio page | Browser pane | 13:42 | No written bio; "known for Minx (2022), Al Davis: Just Win Baby (2024) and The Imperfection (2021)" |
| IMDb nm8803339, credits | Browser pane | 13:47 | Killer of Men (Short, Mace, 2026); Al Davis: Just Win Baby (TV Special, Raider #1, 2024); Minx (Male Model, 1 episode, 2022); The Imperfection (Podcast Series, Legs (voice), 9 episodes, 2021); The Orjiako Hour (2020); shorts Happiness (2019), Hey, The Candle, Eyes of Isaac (2017) |
| secondcity.com/people/hollywood/erik-ojiako | fetch | 13:36 | His own bio, verbatim: "Erik Orjiako, a Swedish born Nigerian American actor ... Ecstatic to be performing with Second City's sketch team and Grad Revue" (the page heading and URL misspell him "Ojiako") |
| networkisa.org/profile/erik-orjiako | fetch | 13:36 | Self-written: MFA in screenwriting from the New York Film Academy; script reader and creative executive; Second City performances in Hollywood; a comedy web series made in Los Angeles in the lockdown; three spec projects |
| backstage.com/u/erik-orjiako | Browser pane (fetch was 403) | 13:50 | Location Los Angeles, CA; SAG-AFTRA; representation Wild Models Talent; education "Umass Amherst English/Communications 2018", "Second City Improv Hollywood Ca 2018", "New York Film Acadmey Screenwriting"; highlight "Graduated Second City Hollywood's improv program"; credits incl. Single Parents (ABC), The Neighborhood (CBS), Second City shows |
| erikorjiako.com | Browser pane | 13:50 to 13:51 | Home page: "Actor, Los Angeles CA"; writer/director page: scripts and Second City theatre pieces |
| TMDB person 3472001 | fetch | 13:36 | No biography; Walkies (2026), Killer of Men (dated 2022 there), Minx |

**Claim by claim**

| The bio says | Source | Checkers | Result |
|---|---|---|---|
| Swedish-born Nigerian American | Second City bio, his own words, the only source | supported by both, both note it is self-reported | kept; **confirm with the actor** |
| actor and writer | Backstage (Actor, SAG-AFTRA); NetworkISA "Screenwriter, Actor"; IMDb "Actor, Writer, Producer" | supported | kept (no produced writing credit exists) |
| based in Los Angeles | Backstage location; his site's "Actor, Los Angeles CA"; NetworkISA | supported | kept |
| studied English and communications at UMass Amherst | Backstage education field, no degree named | supported as "studied" | kept; do not upgrade to a degree |
| MFA in screenwriting, New York Film Academy | NetworkISA, his own words; Backstage names the school but no credential; a NYFA Jan 2017 graduation list names a "Chiedozie Orjiako" under MFA Screenwriting, identity inferred | supported, one self-written source | kept; **confirm with the actor** |
| graduate of Second City Hollywood's improv program | Backstage highlight and education | supported | kept |
| has performed with its sketch team and written shows there | Second City bio (performing); NetworkISA (writing shows at Second City) | draft said "written and performed with its sketch team": **overstated**, both lenses | reworded to the sources |
| credits: Minx | IMDb, TMDB (Male Model, 1 episode) | supported | kept |
| credits: the short film Al Davis: Just Win Baby | IMDb calls it a TV Special; the production company (Bridgenext) calls it a short film for Super Bowl LVIII; no broadcast confirmed | draft said "television special": **overstated** | changed to "short film" |
| credits: the podcast series The Imperfection | IMDb (Legs, voice, 9 episodes, 2021); a real 2021 fiction podcast, Tribeca 2021 | supported | kept |
| script reader and creative executive | NetworkISA, his own words, no employer named | supported, self-reported | kept; **confirm with the actor** |
| plays Mace | IMDb credits; title page link | supported | kept |

Left out on purpose: Backstage's Single Parents and The Neighborhood (not on IMDb; the role names read as background work).

## Eric Pargac (Master Kenner)

**Pages read on 2026-09-10**

| Page | How | Time | What it gave |
|---|---|---|---|
| ericpargac.com/bio | fetch | 13:35 | His own bio: "actor and filmmaker based in Los Angeles"; Artists Rep, IRT Theatre, Dixon Place; Succession, The Late Show; founding artistic director of Furious; "2007 Actor of the Year award from Stage Scene LA" for An Impending Rupture of the Belly; iO West, Freudian Slip at Texas A&M; The Digressions "co-directed and produced"; NYTVF 2014 and 2015 |
| IMDb nm1655191, bio page | Browser pane (fetch was 403) | 13:42 | Self-written ("IMDb mini biography by: Eric Pargac"): "grew up in Texas"; founding artistic director of Furious; "starred in 10 productions"; Gold Crown Award, Back Stage West Debut Award; Theo in all three seasons of The Digressions, "co-produced and co-directed"; ImprovOlympic house team |
| IMDb nm1655191, full credits | Browser pane | 13:49 | Killer of Men (Master Kenner, 2026); Succession (Dr. Lipe, 1 episode, 2018); The Digressions (Theo, 19 episodes; co-director; executive producer; editor; cinematographer, 2013 to 2015); Pure Shock Value (2009); Stunt C*cks (2004) |
| artistsrep.org/artists/eric-pargac | fetch | 13:36 | Magellanica, 1984; Koan of Seymour at IRT, Dido and Aeneas at Dixon Place; co-founder and Co-Artistic Director of Furious 2001 to 2010; Paradise Lost at Intiman; SAG-AFTRA and Actors' Equity |
| His resume PDF (squarespace, file dated March 2018) | fetch, saved as binary; text extracted for this report | 13:49 | Header "SAG-AFTRA/AEA"; Succession (Co-Star, HBO, dir. Mark Mylod); The Late Show w/Stephen Colbert (Co-Star, CBS); The Digressions (Series Regular); the ten Furious productions with roles (Clay, Sam, Ruffman, Sweets, Shawn Keogh ...); Magellanica (Artists Rep), Paradise Lost (Intiman), The Koan of Seymour (IRT Theatre) |
| TMDB person 4625392 | fetch | 13:36 | No biography; Killer of Men, Succession |

The checkers added, from their own searches: the StageSceneLA 2006-2007 Scenies page, Wikipedia's Furious Theatre Company article, IRT Theater's page for The Koan of Seymour (September 2016), BroadwayWorld and Portland Mercury on Magellanica (2018), The Digressions' cast and creatives page, and the Sweibel Arts crew page ("Eric Pargac (he/him, Los Angeles)", "moved back to Los Angeles in 2018").

**Claim by claim**

| The bio says | Source | Checkers | Result |
|---|---|---|---|
| Los Angeles-based | ericpargac.com/bio; Sweibel Arts crew page (undated) | source lens: unsupported (found only a data-broker listing); overreach lens: supported; merger: supported | kept; confirm he is still there |
| actor and filmmaker | IMDb bio; ericpargac.com | supported | kept |
| grew up in Texas | IMDb bio, his own words; Texas A&M improv on his resume | supported, self-reported | kept |
| founding artistic director of Furious Theatre Company in Los Angeles | ericpargac.com; IMDb bio; Artists Rep; Wikipedia (six founders, 2001) | supported | kept |
| performed in ten productions | resume lists ten Furious roles; IMDb bio says "starred" | "starred": **overstated** (supporting parts among the ten) | changed to "performed in" |
| shared StageSceneLA's 2006-2007 Lead Actor of the Year (Drama) award for An Impending Rupture of the Belly | stagescenela.com Scenies page: listed under "Lead Actor of the Year/Drama (Tie)" | "named 2007 Actor of the Year": **overstated** | reworded to the award page |
| Artists Repertory Theatre in Portland | artistsrep.org; resume; press coverage | supported | kept |
| Intiman Theatre in Seattle | Artists Rep bio; resume (Paradise Lost) | supported | kept |
| the IRT Theater in New York | ericpargac.com; resume; irttheater.org | supported; the merger changed "Theatre" to "Theater" from the venue's domain, unopened | kept; styling to confirm against the venue |
| The Late Show with Stephen Colbert | resume (Co-Star, CBS); ericpargac.com; Artists Rep; not in IMDb | supported; reordered so "HBO's" attaches only to Succession | kept |
| HBO's Succession | IMDb (Dr. Lipe, 1 episode); resume; ericpargac.com | supported | kept |
| starred in, co-directed and co-produced the web series The Digressions | IMDb credits; IMDb bio; ericpargac.com; the series' creatives page lists four producers | "produced": **overstated** | changed to "co-produced" |
| member of SAG-AFTRA and Actors' Equity | resume header (2018); Artists Rep profile (2018 to 2020) | supported, dated | kept; **confirm current membership** |
| plays Master Kenner | IMDb credits; title page link | supported | kept |

## Jamal Dennis (Kojo)

**Pages read on 2026-09-10**

| Page | How | Time | What it gave |
|---|---|---|---|
| IMDb nm2156703, bio page | Browser pane (fetch was 403) | 13:42 | Self-written ("IMDb mini biography by: JD"): a professional actor based in Los Angeles; "recently studied at RADA"; studying with Craig Archibald and Lesly Kahn; "a black belt in martial arts and weapons training", styles Kyokushin, Wu-Shu, Ninjitsu, Shotokan; lead on Be Someone; time in Atlanta and New Orleans; Instagram @theejamaldennis. Trivia: Wushu with Eric Chen, wire work with Tim Storms |
| IMDb nm2156703, credits | Browser pane | 13:42 to 13:49 | Killer of Men ("Fighter2 Kojo", 2026); Is God Is (stunts, 2026); Sinners (stunt performer, 2025); The Family Business: New Orleans (2025); The Young and the Restless (Fireman, 2024); Be Someone (Lavelle Sanders, 4 episodes, 2023); Emancipation (stunts, 2022); S.W.A.T. (Henchman, 2022); Runaways (Security Guard, 2019); Roots (stunts, 2016); Mississippi Grind (Baller, 2015); Zoo (Prison Guard, 2015); NCIS: New Orleans (2015); Grudge Match (stunts, 2013); Hatchet III (2013); Glory Road (Big Guy, as Jamal Rashawn Dennis, 2006) |
| resumes.actorsaccess.com/JamalDennis | fetch | 13:36 | His resume: "JAMAL R DENNIS - SAG-AFTRA"; LA representation; television, film and theatre credits; training "Royal Academy Of Dramatic Arts", Lesly Kahn, Craig Archibald, Caitlin Adams, Mikal Vega, 87 North, Tim Storms; skills Karate (Shotokan), Kung Fu (WuShu), Kyokushin Karate, Ninjitsu, wire work |
| TMDB person 2348530 | fetch | 13:36 | 15 credits; Killer of Men (Kojo, dated 2025 there); Sinners and Is God Is under stunts |
| amazon.com actor page; kinorium | fetch | 13:36 | 503; empty |

The checkers added: Tubi's Be Someone page (he is billed first), Apple TV's show page (cast list says "J.D."), stuntlisting.com, stuntpoc.com, Letterboxd's stunts page, TMDB's Sinners crew, TV Guide, and a Just Acting Up podcast episode (17 Sept 2025) on his Sinners work.

**Claim by claim**

| The bio says | Source | Checkers | Result |
|---|---|---|---|
| Los Angeles-based actor and stunt performer | IMDb bio; Actors Access (LA reps; "Actor and Stunt Performer") | supported | kept |
| training includes technique and scene study at the Royal Academy of Dramatic Art | Actors Access training: "Royal Academy Of Dramatic Arts - Technique/Scene Study (United Kingdom)"; IMDb bio "recently studied at RADA" | "studied at RADA": **overstated** (reads as conservatoire training; no programme, dates or length) | reworded to the resume's own description; **confirm the programme with the actor** |
| scene study with Lesly Kahn and Craig Archibald | Actors Access training; IMDb bio | supported | kept |
| black belt in martial arts | IMDb bio only, his own words, no style named | supported, self-reported | kept; **confirm** |
| trained in Kyokushin, Wushu, Ninjutsu and Shotokan | IMDb bio; Actors Access skills | supported ("Ninjutsu" is the standard spelling of the sources' "Ninjitsu") | kept |
| played the lead, Lavelle Sanders, in Be Someone | IMDb (4 episodes, 2023); Actors Access "Lead, Tubi"; Tubi bills him first | supported; Apple TV's cast list names the character "J.D.", a data discrepancy | kept |
| The Young and the Restless, S.W.A.T., Marvel's Runaways, Zoo, Mississippi Grind, Glory Road | IMDb; Actors Access; TMDB; TV Guide (Glory Road credited on screen as Jamal Rashawn Dennis, tied by the resume) | supported (each a single-episode or small role, not characterised) | kept |
| stunts on Sinners, Emancipation and Grudge Match | IMDb; TMDB (Sinners); Actors Access (Grudge Match "Boxer (Stunt)"); TV Guide; the podcast | supported (Emancipation rests on IMDb and TV Guide only) | kept |
| member of SAG-AFTRA | Actors Access resume header only | supported, self-maintained | kept; **confirm** |
| plays Kojo | IMDb "Fighter2 Kojo"; TMDB "Kojo"; the film's crawl "Kojo" | supported | kept, matching the crawl |

## Sandra McDaniels (Elder)

**Pages read on 2026-09-10**

| Page | How | Time | What it gave |
|---|---|---|---|
| IMDb nm5062558, bio page | Browser pane (fetch was 403) | 13:39 | No written bio; "known for Truth Be Told (2019), Gingersnap Christmas (2024) and Providence (2018)" |
| IMDb nm5062558, credits | Browser pane | 13:43 and 13:47 | Killer of Men (Elder, 2026); Gingersnap Christmas (Gramma Belle, 2024); 172 Push-Ups (2024); Truth Be Told (Homeless Woman, 1 episode, 2021); Providence (Maryanne, 2018); Se Cree Joven (2018); Bus People (2012) |
| backstage.com/u/sandramcdaniels | Browser pane (fetch was 403) | 13:43 to 13:45 | Location Los Angeles, CA; SAG-AFTRA; representation NTA Talent Agency and Michael Zanuck Agency; playing age 45 to 65; credits incl. "172 Pushups (Principal, 2024)" and Gingersnap Christmas as "Grandma Belle"; no bio text |
| TMDB person 3238462 and 6251807 | fetch | 13:36 | Two records, no biography on either: the first has Gingersnap Christmas (Gramma Belle) and Truth Be Told (Homeless Woman, 1 episode); the second only Killer of Men ("The elder") |
| projectcasting.com/professional/sandra-mcdaniels-337806 | fetch | 13:45 | Los Angeles; a boilerplate profile with no credits, training or bio of her own |
| Web searches ×4 | search | 13:35 to 13:43 | No written bio anywhere |

The checkers added: Wikipedia's Truth Be Told article (Apple TV+, 2019 to 2023; season 2 aired Aug to Oct 2021), TMDB, Letterboxd, Plex and AllMovie for Gingersnap Christmas (all "Gramma Belle"), Leomark Studios (its distributor), the IMDb character page for Providence (tt9079484, dir. Braden Joe), and Mystic Film Festival, Seed&Spark and HollyShorts 2024 for 172 Push-Ups (14 min 34 s).

**Claim by claim**

| The bio says | Source | Checkers | Result |
|---|---|---|---|
| Los Angeles-based actress | Backstage (self-reported); Project Casting; IMDb "Actress" | supported | kept |
| member of SAG-AFTRA | Backstage profile field, self-reported; no public directory exists | supported to the standard of the source | kept; **confirm** |
| the Apple TV+ series Truth Be Told | IMDb and TMDB: Homeless Woman, 1 episode, season 2, 2021; Wikipedia for the platform | overreach lens flagged the one-episode scope; merger kept "credits include" as the kit's uniform wording | kept ("Apple TV+" was the name when the episode aired; Apple renamed the service in Oct 2025) |
| the short films Providence and 172 Push-Ups | IMDb (Maryanne, 2018; 2024); Backstage; festival pages | supported (Providence rests on IMDb and TMDB, which imports from IMDb) | kept |
| the film Gingersnap Christmas, in which she plays Gramma Belle | IMDb, TMDB, Letterboxd, Plex, AllMovie, Leomark | supported; classed a TV movie by some databases, a film by IMDb and the studio | kept; the credit list was reordered for clarity only |
| plays the Elder | IMDb credits; title page link | supported | kept |

**No written bio of Sandra McDaniels exists on IMDb, TMDB, Backstage or Project Casting.** Her paragraph is built from credits only. NTA Talent Agency or Michael Zanuck Agency, from her Backstage profile, are the route to her own.

## What still rests on the actors' own word

| Actor | Claim | Only source |
|---|---|---|
| Erik Orjiako | Swedish-born, Nigerian American; the MFA; script reader and creative executive | profiles he wrote himself (Second City, NetworkISA) |
| Eric Pargac | SAG-AFTRA and Actors' Equity today; Los Angeles today | a 2018 resume, a 2018 to 2020 theatre profile, an undated crew page |
| Jamal Dennis | the black belt; SAG-AFTRA; what the RADA training was | his IMDb bio and his Actors Access resume |
| Sandra McDaniels | SAG-AFTRA | her Backstage profile |

Nothing here contradicts the bios. These are the claims a press outlet could not verify from a public record, so each actor's approval of their paragraph is the fix, as field 7.1's note has said since 2026-09-10.

## Discrepancies noticed on the way

- IMDb credits Jamal Dennis as "Fighter2 Kojo"; the crawl and the bio say Kojo.
- IMDb's full credits spell the co-writer "Kiera Bratton-Lewis" and the production designer "Rajeshwari Ragampudi"; the poster and the kit say Kierra and Rajarajeshwari.
- TMDB dates Erik Orjiako's Killer of Men to 2022 and Jamal Dennis's to 2025; the film page says 2026.
- Two TMDB person records exist for Sandra McDaniels.
- Apple TV's Be Someone cast list gives Jamal Dennis's character as "J.D."; IMDb, Tubi and his resume say Lavelle Sanders.

## Where the raw evidence lives

- `press/cast-bios.md`: the 2026-09-10 write-up with the source tables and the fact-check summary.
- `press/cast-bios-evidence/source-reads.json`: every successful fetch in the research window with the text it returned; `browser-reads-full.txt`: the eleven Browser pane reads (IMDb, Backstage, his site) in full; `factcheck-verdicts.json`: all nine agents' verdicts, claim by claim, with their evidence; `Eric_Pargac_Resume_2018.txt`: the resume PDF's text.
- The session transcript: `~/.claude/projects/-Users-scrogdawg-BMF-Headquarters-Previous-Years-2025---SEW-TO-GROW-25-01-KILLER-OF-MEN--THESIS-/4ceb6483-0feb-43fb-9a30-9773a2d0ea28.jsonl`; the fact-check agents under `4ceb6483-0feb-43fb-9a30-9773a2d0ea28/subagents/workflows/wf_7518a3a9-83f/`; the saved resume PDF under that session's `tool-results/`.
- The worksheet: field 7.1 and its history in `press/epk.json`; commit f00ba4d.
