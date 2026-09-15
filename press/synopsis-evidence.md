# Where the synopsis came from

Compiled 15 September 2026 from the repository's commits and files, the worksheet's own history, and the session transcripts on this Mac. The synopsis on page 2 of the EPK and in worksheet field 2.2 is **draft C from `press/synopsis-draft.md`**, written by Claude (Opus 5) on 8 September from facts already on record, recommended but never picked by Jordan, and carried into the worksheet on 14 September because the design showed it without its proof mark. Every phrase of it is traced below; seven of its details are inferences, not recorded facts.

Times are Central unless marked. The Sep 7 and 8 work was committed from Luke's other machine (git author `C <c@x>`, whose clock is stamped -0700), so those sessions' transcripts are not on this Mac; their record is the commits, the files they wrote, and handoffs 043 to 058.

## The chain

| When | What | Record |
|---|---|---|
| 6 Sep | Joan's call. The synopsis is not discussed; it appears once, as an item in her delivery-folder list ("Synopsis, credits & director bio"). Joan's note on the existing logline: it says neither when nor where; write it as a marketing logline. | `meetings/2026-09-06-joan-call.md`; handoff-081-festival |
| 6 Sep | The starting text, the FilmFreeway page as it stood: "Killer of Men follows Mace, an enslaved man forced into mandingo fights. After killing an opponent, he stumbles upon the burial of the man he killed, igniting a reckoning with guilt, faith, and the violence shaping his life and identity." Jordan's. | `press/logline-idea-box.md`, "Where it started" |
| 7 Sep, 17:21 to 22:40 (-0700) | The logline day: 24 generations of Luke's dictation, preserved verbatim in `logline-idea-box.md`; Claude's studio and models; a 119-logline reference corpus; a deep pass of 36 drafts, three reviewers and an adversary, leaving three finals. Luke's rulings that shaped the synopsis: **1834**; "A South Carolina plantation"; the fights in a barn; "held in the faith of their shared ancestors"; and **"No 'the god he would have been.' No god anything."** The film facts he gave: the elder in the cabin says **"You would have been a god"**; Mace's prayer to Ogun. | commits 7dc5e8f through 92aed44 (16 commits, author `C <c@x>`); `press/logline-where-we-are.md` fact table (each fact with its source: Luke, the page, the README, the statement); `press/logline-final-three.md` |
| 8 Sep, 11:44 (-0700) | The EPK inventory names the gap: "Synopsis (~100 words): NOT WRITTEN, and nobody has raised it." | commit 1171d2b; `press/epk-inventory.md` line 29 |
| 8 Sep, 12:33 (-0700) | **`press/synopsis-draft.md` written**: three drafts, A (98 words), B (101), C (96), "from the facts already on record. Nothing invented"; a table of what each assumes and who settles it; recommendation C. Same commit: two draft messages to send. | commit 18a5808, `C <c@x>`, co-authored Claude Opus 5; handoff-057-festival ("the EPK gap nobody had raised") |
| 8 Sep, 22:41 (-0700) | Luke, in chat, gives two candidate synopses for field 2.2: the killerofmen.com paragraph and the full director's statement. Neither made primary: "i don't know which one we'll use." The three drafts are noted but "not added unasked". | field 2.2 history; commit e7956a0; handoff-082-epk |
| 9 Sep | The kit renders synopsis C on page 2 whenever 2.2 is empty, under a PROOF mark ("LOGLINE A AND SYNOPSIS C ARE DRAFTS, NOT YET CHOSEN"). Jordan owns the pick. | `tools/build-epk-kit.py` `synopsis()`; handoff-100-epk |
| 11 Sep | The Canva design is built from the kit; page 2 carries draft C and the proof mark. | handoffs 114, 115 |
| by 14 Sep | Luke deletes the proof mark on page 2 in Canva. | read-back, `canva/readback/latest.json`; handoff-118 |
| 14 Sep, 12:56 | Draft C written into field 2.2, verbatim from the design, under Luke's rule that his Canva edits win (rev 31). | field 2.2 history, `by: epk.py`; commit aff9d25 |

**What 2.2 holds today:** value = draft C; options = the website paragraph and the director's statement (Luke's two candidates); `waiting = Jordan Betine`. Jordan has not chosen a synopsis. The only synopsis-like text written by the filmmakers themselves is the killerofmen.com paragraph.

## Draft C, phrase by phrase

The text: *Mace fights because the alternative is the field, and then the ground. On a South Carolina plantation in 1834 his owner stages bouts against other enslaved men and takes the wagers; Mace has never lost, and every win buys him another season. Then a fight ends in a death, and he follows the body to a burial held in secret in the Yoruba faith he was born to. The rites are for a man he killed. An elder tells him what he would have been across the water, and he sees, for the first time, what he has become.*

| Piece | Rests on | Status |
|---|---|---|
| "Mace" | The FilmFreeway page names him; the fact table: "Mace, an enslaved man; his physicality is why he is valuable (the page; the director's statement)". The draft's own table asks that the name be confirmed against the credits; the end-credit roll (8 Sep) confirms Mace, played by Erik Orjiako. | recorded |
| "fights because the alternative is the field, and then the ground" | "The ground" is death: the page's "fight to the death", Luke's "win or die". "The field" is what losing costs him short of death. The draft's own table: **"an inference about what losing costs him. Does the film establish this?" (Jordan)**. | **inference** |
| "On a South Carolina plantation in 1834" | Luke, Sep 7: "1834, better than the 1830s"; "A South Carolina plantation" ("I liked it"). | recorded (Luke) |
| "his owner stages bouts against other enslaved men" | The page: "forced into mandingo fights"; Jordan's statement on Mandingo fighting; Luke: "fight for spectacle", "for the entertainment of others"; the fights in a barn. | recorded |
| "and takes the wagers" | No record states wagering. The idea entered on Sep 7 in Claude's own studio lines ("the owner who bets on him in the pit", "their owners' wagers") and the adversary's "cannot buy" fix; it is the Mandingo-fighting trope, not a stated film fact. | **inference** |
| "Mace has never lost" | No record states it. The fact table says his physicality is why he is valuable; Luke's fragments say he must win or die. "Never lost" is the draft's compression. | **inference** |
| "every win buys him another season" | Claude's line from the Sep 7 deep pass: final A, "Every victory buys him another night and costs a man his life"; built on Luke's "win or die". | Claude's phrasing on a recorded premise |
| "Then a fight ends in a death" | The page: "After killing an opponent". | recorded |
| "he follows the body to a burial" | The page says he "stumbles upon the burial". "Follows the body" is the draft's staging of how he gets there. | **inference** |
| "held in secret" | No record says the burial is secret. It is the reading Claude gave draft B ("the one ceremony his owners have no claim on"), which the draft's own table marks "a reading, not a stated fact". | **inference** |
| "in the Yoruba faith" | The repo README: he "reconnects with the Yoruba faith of his ancestors"; Luke's Ogun fact; the website paragraph names Ogun and Yoruba. | recorded |
| "he was born to" | The README says the faith of his ancestors; the statement speaks of new enslaved people brought from Africa. Whether Mace himself was born into the faith is not stated. | **inference** |
| "The rites are for a man he killed" | The page: "the burial of the man he killed". | recorded |
| "An elder tells him what he would have been across the water" | Luke, Sep 7: in the cabin the elder tells him the man he would have been in the motherland, "You would have been a god." Paraphrased because Luke ruled "No god anything" for the logline; the draft's table: **"Confirm the elder scene plays as described" (Jordan)**. | recorded (Luke), paraphrased |
| "and he sees, for the first time, what he has become" | Claude's ending. The page's "igniting a reckoning with ... the violence shaping his life and identity" and Luke's Raging Bull frame ("reckon with the man he has become") are behind it; the draft chose "seeing rather than deciding" as "truer to a thirteen-minute film". | Claude's phrasing on a recorded premise |

Seven pieces are inferences: the field, the wagers, never lost, follows the body, held in secret, born to, and the ending's "sees what he has become". None contradicts a record; none is stated by one. The draft's own "What each needs before it ships" table flagged three of them on the day it was written (the field, the secrecy reading, the elder scene) and one omission: **the surreal or ancestral sequence, "the thing that sets the film apart", is in none of the drafts** because nobody had described it.

## The filmmakers' own texts on record

- **Jordan's FilmFreeway logline** (the page as it stood 6 Sep): the "follows Mace ... mandingo fights ... burial of the man he killed ... reckoning with guilt, faith, and the violence" sentence. Now field 2.1 option "FilmFreeway", and since 11 Sep the logline on page 2 (Luke's choice).
- **killerofmen.com's paragraph**, read off the site 8 Sep: "KILLER OF MEN is a powerful and intense exploration of a man, Mace, who is trapped in the brutal reality of slavery and forced combat. It combines elements of historical fiction with spiritual and psychological themes, particularly focusing on Mace's internal struggle and his connection to his African roots and gods, like Ogun, the god of war in Yoruba religion." Field 2.2 option "Website".
- **Jordan's director's statement**, his corrected text of 8 Sep. Field 4.1, and 2.2 option "Director's statement".
- Luke's own dictated loglines, 24 generations, in `press/logline-idea-box.md`; the two he locked on 8 Sep are the FilmFreeway page's A and B.

## Where the raw evidence lives

- `press/synopsis-draft.md` (the three drafts and their assumptions table); `press/logline-where-we-are.md` (the fact table with a source per fact, and Luke's rulings); `press/logline-idea-box.md` (Luke's words, verbatim, 24 generations); `press/logline-final-three.md` (the deep pass); `press/logline-studio.md` (Claude's material); `press/epk-inventory.md` line 29.
- Commits 1171d2b, 18a5808, e7956a0, 3a6f22e (8 Sep) and 7dc5e8f to 92aed44 (7 Sep), all `C <c@x>`, co-authored Claude Opus 5.
- Field 2.2's history and options in `press/epk.json`; the kit's `synopsis()` fallback in `tools/build-epk-kit.py`.
- Handoffs 043 to 058 (festival lane, Sep 7 to 8), 081, 082, 100, 118.
