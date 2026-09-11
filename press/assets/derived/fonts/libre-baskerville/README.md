# Libre Baskerville, for measuring the Canva contract

Canva draws the kit in Libre Baskerville (an app cannot use an uploaded font), so
`tools/build-epk-canva.py` measures every fit, wrap, width and anchor in this face
(`--face libre`, the default) and the PDF and the .ai keep macOS Baskerville.

| File | What | From |
|---|---|---|
| `LibreBaskerville[wght].ttf`, `LibreBaskerville-Italic[wght].ttf` | The upstream variable fonts, version 2.005 | github.com/google/fonts `ofl/librebaskerville`, fetched 2026-09-11 |
| `LibreBaskerville-Regular.ttf`, `-Bold.ttf`, `-Italic.ttf` | Static instances at wght 400 / 700 / 400, made with fontTools `varLib.instancer` (`updateFontNames=True`) | the variable fonts above |
| `OFL.txt`, `FONTLOG.txt`, `METADATA.pb` | Licence (SIL Open Font License 1.1) and provenance | same |

The instances' advance widths equal the static v1.051 files Google served before the
2025-10-17 variable replacement (316 shared codepoints, 0 differences, checked 2026-09-11),
so they measure what Canva draws whichever build Canva serves.

Regenerate the instances:

    venv/bin/python -c "
    from fontTools.ttLib import TTFont; from fontTools.varLib import instancer
    D='press/assets/derived/fonts/libre-baskerville/'
    for n,w,s in (('Regular',400,'LibreBaskerville[wght].ttf'),('Bold',700,'LibreBaskerville[wght].ttf'),('Italic',400,'LibreBaskerville-Italic[wght].ttf')):
        instancer.instantiateVariableFont(TTFont(D+s), {'wght': w}, updateFontNames=True).save(D+f'LibreBaskerville-{n}.ttf')"

Copyright 2012 The Libre Baskerville Project Authors (https://github.com/impallari/Libre-Baskerville). Licensed under the SIL Open Font License, Version 1.1 (`OFL.txt`).
