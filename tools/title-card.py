#!/usr/bin/env python3
"""Killer of Men title card studies on the oak-glade frame (Luke, 2026-10-14). Red type, black ground.
Renders 1920x1080 frames (the 2.39 picture inside its letterbox, as in the film) with the title set by
hand-tuned treatments; see main() for the sheets."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FD = "press/assets/derived/fonts/title-candidates"
RED = (168, 30, 26); RED_BRIGHT = (190, 38, 32)

def tracked_width(font, text, track):
    return sum(font.getlength(c) for c in text) + track * (len(text) - 1)

def draw_tracked(d, text, font, cx, y, track, fill):
    x = cx - tracked_width(font, text, track) / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill); x += font.getlength(c) + track

def cap_height(font):
    b = font.getbbox("H"); return b[3] - b[1], b[1]

def burn(img, box, strength=0.45, blur=120):
    """Darken softly under the title, the way a title designer brings the background down."""
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle(box, radius=60, fill=int(255 * strength))
    m = m.filter(ImageFilter.GaussianBlur(blur)); black = Image.new("RGB", img.size, (0, 0, 0))
    return Image.composite(black, img, m)

def title(img, text, fontfile, cap, cx, cy, track_em=0.32, rule=True, color=RED, rule_w=None, rule_gap=0.9, weight=None, burn_it=True):
    f = ImageFont.truetype(fontfile, 100)
    if weight is not None:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    ch, _ = cap_height(f); size = int(100 * cap / ch); f = ImageFont.truetype(fontfile, size)
    if weight is not None:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    ch, top = cap_height(f); track = track_em * size; w = tracked_width(f, text, track)
    y = cy - ch / 2 - top
    if burn_it: img = burn(img, (cx - w / 2 - 80, cy - ch - 40, cx + w / 2 + 80, cy + ch * 2 + 40))
    d = ImageDraw.Draw(img); draw_tracked(d, text, f, cx, y, track, color)
    if rule:
        rw = rule_w or w * 0.42; ry = cy + ch / 2 + ch * rule_gap
        d.line([(cx - rw / 2, ry), (cx + rw / 2, ry)], fill=color, width=max(2, int(cap / 16)))
    return img

# --- layouts (after the research brief, 2026-10-14) -----------------------------------------
INK = (150, 26, 22)          # dark ink red for type on pure black
def setfont(fontfile, cap, weight=None):
    f = ImageFont.truetype(fontfile, 100)
    ch, _ = cap_height(f); f = ImageFont.truetype(fontfile, int(100 * cap / ch))
    if weight is not None:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    return f

def scotch_rule(d, cx, y, w, color, thick=4, thin=1, gap=4, align="center", x0=None):
    x0 = cx - w / 2 if align == "center" else x0
    d.rectangle([x0, y, x0 + w, y + thick - 1], fill=color); d.rectangle([x0, y + thick + gap, x0 + w, y + thick + gap + thin - 1], fill=color)

def block(img, fontfile, cx, cy, cap=34, track=.32, color=RED, rule="plain", rule_color=None, locator=None, loc_font=None, loc_color=None,
          align="center", x0=None, weight=None, burn_it=False, rule_ratio=.42):
    f = setfont(fontfile, cap, weight); size = f.size; ch, top = cap_height(f); tr = track * size; w = tracked_width(f, "KILLER OF MEN", tr)
    if burn_it:
        bx0 = (cx - w / 2) if align == 'center' else (x0 if align == 'left' else x0 - w)
        img = burn(img, (bx0 - 110, cy - ch - 70, bx0 + w + 110, cy + ch * 3 + 70), burn_it if isinstance(burn_it, float) else .55)
    d = ImageDraw.Draw(img); rc = rule_color or color
    if align == "center": draw_tracked(d, "KILLER OF MEN", f, cx, cy - ch / 2 - top, tr, color); left = cx - w / 2
    else:
        if align == "right": x0 = x0 - w
        x = x0
        for c in "KILLER OF MEN": d.text((x, cy - ch / 2 - top), c, font=f, fill=color); x += f.getlength(c) + tr
        left = x0
    ry = cy + ch / 2 + ch * .85; rw = w * rule_ratio
    if rule == "plain": d.line([(cx - rw / 2, ry), (cx + rw / 2, ry)] if align == "center" else ([(left, ry), (left + rw, ry)] if align == "left" else [(left + w - rw, ry), (left + w, ry)]), fill=rc, width=max(2, cap // 17))
    elif rule == "scotch": scotch_rule(d, cx, ry, rw, rc, thick=max(3, cap // 9), thin=max(1, cap // 30), gap=max(3, cap // 10), align='center' if align == 'center' else 'left', x0=left if align != 'right' else left + w - rw)
    if locator:
        lf = setfont(loc_font or fontfile, cap * .5); lch, ltop = cap_height(lf); ly = ry + ch * .9
        lw = tracked_width(lf, locator, .28 * lf.size)
        if align == "center": draw_tracked(d, locator, lf, cx, ly - ltop, .28 * lf.size, loc_color or rc)
        else:
            x = left if align == "left" else left + w - lw
            for c in locator: d.text((x, ly - ltop), c, font=lf, fill=loc_color or rc); x += lf.getlength(c) + .28 * lf.size
    return img
