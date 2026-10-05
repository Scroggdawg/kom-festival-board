# handoff-136-epk — link audit of the Canva master: 18 links, 4 wrong, sharing is "anyone can EDIT"

## Recap (newest first)
- Luke: check every link goes where it says. Read all 12 pages of DAHU6a7HKPs in a transaction (cancelled, no change). 18 linked text runs, all on page titles "03 Programmer", "05 Filmmakers", "06 Filmmakers". Verified: web via curl (killerofmen.com), IMDb + Instagram via the built-in browser (page titles), Drive via the Drive connector (title + parent + permissions).
- handoff-135: page 6 saved, records pushed.

## Findings
| Label | Goes to | Verdict |
|---|---|---|
| BTS | Drive folder "BTS" (00 PRESS/BTS) | OK |
| STILLS | Drive folder "KOM STILLS" (owned by Jordan, inside 00 PRESS/STILLS) | OK |
| POSTER | KillerOfMen_Poster_2160x2700.jpg | OK |
| TRAILER | 00 PRESS root (1utGEFQb…) | WRONG → TRAILER folder 1xE8e38_oiRks_XQme-MffSYJZWdThNuS (holds 2513_KOM_Trailer_H264_ST_VIMEO.mov + 422HQ) |
| HEADSHOTS | 00 PRESS root (1utGEFQb…) | WRONG → HEADSHOTS folder 1Usfn18LMSoL2RYQ6OAYraTuiU4W8P0UW |
| WWW.KILLEROFMEN.COM | killerofmen.com, "Killer of Men I Movie" | OK |
| INSTAGRAM @KILLEROFMENMOVIE | Killer of Men (@killerofmenmovie) | OK |
| IMDB (title) | Killer of Men (Short 2026) | OK |
| 5 × ROLE \| NAME lockups | each person's Instagram | OK (matches) |
| 5 × @handle | each person's IMDb page (right person) | WRONG KIND: the handle should open Instagram |
| 5 × "IMDB" label | no link | MISSING: should open the IMDb page now on the handle |
| SDRETZKA@AFI.COM, KILLEROFMENMOVIE@GMAIL.COM | no link | optional mailto: |

IMDb names confirmed: Jordan Betine nm17461892, Ruoxiao Li nm15376948, Luke Scroggins nm3596666, Rajeshwari Ragampudi nm15956329, You Wu nm17461889.

## Sharing (bigger than links)
Every linked Drive item (00 PRESS, BTS, KOM STILLS, poster) is shared "anyone with the link — EDITOR". Anyone holding the EPK can delete or replace the masters. Recommend Viewer. Not changed: Luke's call.
Drive HEADSHOTS folder doesn't have the two new portraits (Betine_Director_seated.jpg, Scroggins_DP_BW.png).

## Proposed fix (awaiting Luke)
format_text link on: TRAILER, HEADSHOTS, 5 handles → Instagram, 5 IMDB labels → IMDb, 2 emails → mailto:. One transaction, preview, commit.
