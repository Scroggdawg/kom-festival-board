# EPK spec — modelled on a strong AFI thesis EPK

Source: an 11-page thesis EPK built in Illustrator, exported from Canva-sized portrait pages (1296 × 1728 pt), shared as `Title_EPK_<HHMM>_<DDMMYYYY>_compressed.pdf`. Its structure is what to copy. Two things to do better: keep every page's text selectable (pages 5–11 of the model are rasterised), and keep bios to ~150 words.

The EPK is a **link hub**, not a container. Every asset category on page 3 is a live link into the Drive folder; bios link to Instagram and IMDb. The PDF's job is to route a programmer into the assets in one click.

## Page order

| Page | Section | Contents | Links |
|---|---|---|---|
| 1 | Poster | Full-bleed key art. Billing block. Website URL printed | — |
| 2 | Logline + synopsis | One hero still (top ~60%). LOGLINE ~50 words. SYNOPSIS ~100 words. One page | — |
| 3 | Specs · team · cast · rights · links · contact | **The programmer page.** See spec block below. THE TEAM: five HoD roles. CAST: principals. RIGHTS: AFI Conservatory + named contact. LINKS: BTS · STILLS · POSTER · TRAILER · HEADSHOTS. Footer: email · website · Instagram | every LINK → Drive folder; site; IG |
| 4 | Director's statement | ~300–350 words, signed "Jordan Betine, director", personal-to-thematic arc, photo ghosted behind | — |
| 5–6 | Filmmaker bios | `ROLE | NAME` + Instagram/IMDb/website icons, headshot alternating sides, ~150 words each, max three per page. Director, producer, DP, production designer, editor | IG, IMDb per person |
| 7 | Cast | `CHARACTER | ACTOR`, a still from the film rather than a headshot, credits-forward bio. One page per principal | IG, IMDb |
| 8 | BTS mosaic | 8–12 set photos, irregular grid, no captions. Mix wide setups and faces | — |
| 9 | Key credits + cast | Writer-director, producer, DP, PD, editor, composer, sound designer, casting, EPs; then full cast as `character | actor`. Over one strong still | — |
| 10 | Full crew | Two `role / name` columns. Expected in a thesis EPK | — |
| 11 | Thanks + AFI end card | Thanks list, partner logos, AFI boilerplate: property/copyright notice, "produced at the AFI Conservatory in partial fulfillment of the MFA", fellows listed by discipline, © AFI, AFI Conservatory logo | — |

## Page 3 spec block — fields to fill

```
GENRE
COUNTRY
SHOOTING LOCATION
PRODUCTION YEAR
COMPLETION YEAR
LANGUAGE            (SRT available: list)
DURATION
ASPECT RATIO
FRAME RATE
SHOOTING FORMAT
EXHIBITION FORMAT   (2K DCP · 4K DCP · 2K ProRes · 4K ProRes — whichever exist)
SOUND               (5.1 · stereo)
```

## Drive skeleton the EPK links into

```
KILLER OF MEN/
  05 MARKETING/
    00 PRESS/
      BTS/
      HEADSHOTS/            KILLER_OF_MEN_First_Last_Role.jpg
      POSTER/
      STILLS/
      TRAILER/
      z_Old_EPKs/
      EPK INFO   (doc — all the text)
      EPK LINKS  (doc — every share URL)
      FAQs
      Social Toolkit
    07 FESTIVALS/
      Accepted Festivals/
      Festival Cover Letters/
      Festival Details/
      Festival Social Media Posts/
      Festival Submission Receipts/
      Festival Laurels/
      Instagram Posts/
      LOGINS (doc — private; never in this repo)
      Festival List (sheet)
      Notes — festivals | awards | distribution (doc)
```

## Delivery folder (MyAirBridge or Dropbox) — pre-built before the first request

```
KILLER_OF_MEN/
  DCP/                        ISDCF-style names, e.g. KillerOfMen_SHR-1-F-…_EN_XX_…_51_AFI_<date>_AFI_IOP_VF
  KOM_Quicktimes_NoSubtitles/ KOM_2K_<ratio>_422HQ_5.1_<date>.mov · …_ST-LTRT_<date>.mov · …_H265.m4v · KOM_13m00s.mp4
  KOM - with English subtitles/
  SRT/                        KillerOfMen_English.srt
  Trailer/
  Resolve project files/
  OLD/
  <Festival name>/            per accepted festival: laureled poster · laureled trailer · localised screener · SRT · 60-second intro
```

Share per festival: one **read-only** link to a dated folder `Killer of Men ~ YYYY-MM-DD` containing DCP · EPK · Film Stills & Director Photo · Film_Master (clean, no subtitle, 2K, MOV or MP4) · Poster · SRT File · Synopsis, Credits & Director Bio · Trailer. Log the link and permission on the board.

## Vimeo uploads — one per audience

| Upload name | Audience | Download | Tracked |
|---|---|---|---|
| KOM — Festivals A | first-tier festivals | no | yes |
| KOM — Festivals B | second-tier festivals | no | yes |
| KOM — Downloadable | festivals that require download at submission | yes | yes |
| KOM — Press / Friends | press, friends, family | no | excluded from festival reads |
| KOM — EN subtitles | festivals requiring burned-in subtitles | as needed | yes |

Names are explicit suffixes. Log which upload each festival received, and the view count at send.

## Build order

1. Gather (Luke): every text field, credits from the end crawl, stills, BTS, headshots, trailer, laurels, links.
2. Text version of the EPK in `EPK INFO`.
3. Layout (Joan offered Illustrator; Canva acceptable). Text selectable. Export `KillerOfMen_EPK_<HHMM>_<DDMMYYYY>_compressed.pdf`; move superseded versions to `z_Old_EPKs`.
4. Attach to FilmFreeway; link from page 3 to every Drive folder.
