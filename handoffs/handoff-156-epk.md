# handoff-156-epk — what the 16 MB compression costs: measured

## Recap (newest first)
- Luke asked what he loses. Rendered both PDFs at 144 dpi (PyMuPDF) and diffed every page.
  PSNR 45.4–68.7 dB (>40 ≈ indistinguishable by eye). Worst page: 1 Poster (45.4 dB; 0.21% of pixels off by >8 of 255 levels, max 30), at the painted edges and lettering in the poster art. Page 9 BTS 48.6 dB (0.02%, max 18). Every other page has 0.00–0.01% of pixels off by >8 levels.
  Unchanged: text, fonts (vector), links, page size, image pixel dimensions.
- The loss is a second JPEG pass (q88): faint ringing at hard edges, slight loss of fine grain. Not resolution.
- handoff-155: the compressed copy.

## Guidance given
Use the compressed copy for uploads and email. Keep the 29 MB master for print and as the source for any future edit; never compress the compressed copy again.
Open: B.E.S.T. award laurels; BTS footer credit; Drive sharing; kit PDF + INFO doc; contract lag.
