# handoff-132-epk — DP headshot + bio 5.3 staged on Canva page 6, awaiting Luke's OK

## Recap (newest first)
- Canva master DAHU6a7HKPs, page 6 Filmmakers (PBsZlZtSqPVJzCwx): OPEN transaction `7262572383280615412`, NOT committed. Expires ~1h after 2026-10-04 evening.
  - Headshot frame LB6yDBkP3jgZhrHF: update_fill → asset MAHXGkSpjWU (Scroggins_DP_BW.png from raw.githubusercontent main).
  - Bio box LBHYpp78N2Thn7KN: replace_text → epk.json 5.3 verbatim (3 paragraphs).
  - At the old 25.333px the new bio ran to y≈2384, past the 2304 page edge. Draft fix: all three bios (LB4S8q2LhmLJM9KZ, LBQ6LDJHdCxMwLmK, LBHYpp78N2Thn7KN) set to 22px. Bio now ends y≈2261 (43px bottom margin vs 98 side margins).
- Pushed 41b9013 + handoff-131 to origin/main; merged origin/claude/admiring-keller-38qjll (handoffs 128–130, laurels, credits-bts); origin/main = bbfebc6.

## Waiting on Luke
Commit as is / other fix (trim bio, nudge block up) / cancel.
If the transaction expired: re-read page 6 with open_transaction, redo the ops above, asset MAHXGkSpjWU is already in Canva.

## Seen, not fixed (097 link audit)
On page 6 each @handle text links to IMDb and each "IMDB" label has no link — all three filmmakers.

## After commit
STATE.json edited_in_place for page 6; rebuild EPK INFO doc + kit PDF; STATE/epk-canva.json/worksheet still lag the laurel page + page shift; mock-up designs DAHWzZ_mZow, DAHWzLd9m8k, DAHW0-KVvy8 still to delete (ask); rename backup DAHXGqNwRqM.
