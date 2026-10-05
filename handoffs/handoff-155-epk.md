# handoff-155-epk — EPK PDF under the 20 MB limit: 16.4 MB compressed copy

## Recap (newest first)
- Luke: the upload limit is 20 MB; the pro export is 29 MB.
- Canva "regular" export = 4.0 MB, but every image is cut to ~800 px (soft on an 18-inch page); not used.
- Compressed the pro export locally: PyMuPDF 1.26.5 (/usr/bin/python3) rewrite_images(dpi_threshold=260, dpi_target=220, quality=88), then save with garbage=4 and deflate. Result 16.37 MB, 12 pages, 48 links, same text. In practice it recompressed the JPEGs at q88; no image was resized. A detail crop of page 6 matches the original by eye.
- Files: ~/Downloads/KillerOfMen_EPK_1316_05102026_compressed.pdf, also in Drive 00 PRESS/EPK BUILDS/CANVA/ beside the 29 MB master and its contact sheet.

## Open
B.E.S.T. award laurels (from Jordan or the festival); BTS footer credit; Drive sharing (Viewer); kit PDF + EPK INFO doc; contract/checker lag the laurel page.
