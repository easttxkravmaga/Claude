"""
Cycle Diagram — Circular Arrows
────────────────────────────────────────────────────
N arc segments forming a donut ring.
Each segment: label inside + heading & body outside.
Supports 3–7 elements.
"""

import math

from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    arc_segment_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap,
)


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))
    emp    = int(s.get('emphasis_index', 0))

    title    = params.get('title', 'CYCLE DIAGRAM').upper()
    subtitle = params.get('subtitle', 'Your subtitle here').upper()
    items    = params.get('elements', [
        {'label': 'COMPETITION', 'heading': 'Competition', 'body': 'Assess market forces and competitors.'},
        {'label': 'EXECUTION',   'heading': 'Execution',   'body': 'Implement tactics with precision.'},
        {'label': 'TARGET',      'heading': 'Target',      'body': 'Define goals and key results.'},
        {'label': 'PROFIT',      'heading': 'Profit',      'body': 'Maximize returns on investment.'},
        {'label': 'PLANNING',    'heading': 'Planning',    'body': 'Build roadmap and allocate resources.'},
    ])
    n = max(3, min(7, len(items)))
    items = items[:n]

    el = []

    # ── Title block ───────────────────────────────────────────────────────────
    title_y    = 72
    subtitle_y = title_y + fs('h1', scale) * 0.72 + 8
    el.append(text_el(W / 2, title_y, title,
                      fs('h1', scale), scheme['primary'],
                      weight=W_BLACK, family=FONT_TITLE))
    el.append(text_el(W / 2, subtitle_y + 12, subtitle,
                      fs('h2', scale), scheme['secondary'],
                      weight='700', family=FONT_BODY))

    # ── Circle geometry ───────────────────────────────────────────────────────
    header_bottom = subtitle_y + fs('h2', scale) + 28
    cx     = W / 2
    cy     = (header_bottom + H - MARGIN) / 2
    r_out  = min(230, round((H - MARGIN - header_bottom) * 0.42))
    r_in   = round(r_out * 0.58)

    # Start angle offset so segments are nicely positioned (first at upper-right)
    start_offset = -90 + (360 / n) * 0.0   # start at top for even N, offset for odd
    seg_span     = 360 / n

    # Text placement: just outside the ring
    txt_r     = r_out + 55
    max_chars = max(14, round(32 * (4 / n)))

    # Colors: accent for emp, alternate primary/secondary for others
    def seg_fill(i):
        if i == emp:
            return scheme['accent']
        if (i % 2) == 0:
            return scheme['primary']
        return scheme['secondary']

    for i, item in enumerate(items):
        seg_start  = start_offset + i * seg_span
        seg_end    = seg_start + seg_span
        theta_mid  = math.radians(seg_start + seg_span / 2)
        fill       = seg_fill(i)

        # Arc segment
        el.append(arc_segment_el(cx, cy, r_in, r_out,
                                 seg_start, seg_end, fill, gap=4))

        # Label inside segment (at arc midpoint)
        lbl_r  = (r_in + r_out) / 2
        lx     = cx + lbl_r * math.cos(theta_mid)
        ly     = cy + lbl_r * math.sin(theta_mid)
        t_fill = scheme['on_dark'] if fill != WHITE else scheme['on_light']
        lbl_text = item.get('label', f'ITEM {i+1}').upper()
        el.append(text_el(lx, ly, lbl_text,
                          fs('body', scale * 0.82), t_fill,
                          weight=W_BOLD, family=FONT_BODY, anchor='middle'))

        # External text anchor: start (right half), end (left half), middle (top/bottom)
        cos_v  = math.cos(theta_mid)
        if abs(cos_v) < 0.25:
            anchor = 'middle'
        elif cos_v > 0:
            anchor = 'start'
        else:
            anchor = 'end'

        tx = cx + txt_r * math.cos(theta_mid)
        ty = cy + txt_r * math.sin(theta_mid)

        heading  = item.get('heading', '').upper()
        body     = item.get('body', '')
        head_sz  = fs('label', scale * 0.95)
        body_sz  = fs('body',  scale)
        lh       = round(body_sz * 1.45)

        # Position: heading above, body below (centered on ty)
        lines    = wrap(body, max_chars=max_chars)
        blk_h    = head_sz + (len(lines) * lh if body else 0) + (8 if body else 0)
        head_y   = ty - blk_h / 2 + head_sz * 0.5
        body_top = head_y + head_sz * 0.5 + 8

        el.append(text_el(tx, head_y, heading,
                          head_sz, scheme['primary'],
                          weight=W_BOLD, family=FONT_BODY, anchor=anchor))

        if body:
            body_ctr = body_top + ((len(lines) - 1) * lh + body_sz) * 0.5
            el.append(multiline_el(tx, body_ctr, lines, body_sz,
                                   scheme['secondary'],
                                   family=FONT_BODY, anchor=anchor))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
