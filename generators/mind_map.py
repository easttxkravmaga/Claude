"""
Mind Map / Radial Diagram
──────────────────────────
Reference: donut ring divided into N equal segments (alternating Black/Gray),
           ONE red focal segment, center circle with label + dashed border,
           external labels (bold) + body text at segment midpoint angles.
Supports 3–8 segments.
"""

import math
from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    circle_el, arc_segment_el, line_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap
)

# Geometry — ring centered lower to give title room at top
CX       = W // 2
CY       = int(H * 0.560)
R_OUT    = int(H * 0.295)
R_IN     = int(H * 0.180)
R_CENTER = int(H * 0.130)

# Label anchor radius — generous gap so text clears the ring
LABEL_R  = R_OUT + 52


def _segment_color(i, n, emp, scheme):
    if i == emp:
        return scheme['accent']
    return scheme['primary'] if i % 2 == 0 else scheme['secondary']


def _label_anchor(angle_deg):
    """SVG text-anchor: start on right half, end on left half, middle top/bottom."""
    a = angle_deg % 360
    if 75 <= a <= 105:
        return 'middle'
    if 255 <= a <= 285:
        return 'middle'
    if a < 180:
        return 'start'
    return 'end'


def _label_pos(angle_deg, base_r, body_lines, body_size, lh, label_size):
    """
    Return (lx, ly, anchor) for a label block so it does not clip canvas edges.
    lx/ly is the anchor point for the label line; body renders below it.
    """
    a    = math.radians(angle_deg)
    raw_lx = CX + base_r * math.cos(a)
    raw_ly = CY + base_r * math.sin(a)
    anchor = _label_anchor(angle_deg)

    # Estimate text block width (rough: 12px per char, cap 200px)
    max_line = max((len(ln) for ln in body_lines), default=0)
    block_w  = min(200, max_line * (body_size * 0.62))
    block_h  = (1 + len(body_lines)) * lh

    # Clamp lx so block stays within canvas
    pad = MARGIN - 10
    if anchor == 'start':
        lx = max(pad, min(W - block_w - pad, raw_lx))
    elif anchor == 'end':
        lx = max(block_w + pad, min(W - pad, raw_lx))
    else:
        lx = max(block_w / 2 + pad, min(W - block_w / 2 - pad, raw_lx))

    # Clamp ly
    ly = max(block_h / 2 + MARGIN, min(H - block_h - MARGIN + 20, raw_ly))

    return lx, ly, anchor


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))
    emp    = int(s.get('emphasis_index', 0))

    # Title: display as given (user controls casing)
    title        = params.get('title', 'Mind Map Infographic')
    center_label = params.get('center_label', 'FOCUS').upper()
    subtitle     = params.get('subtitle', 'Your subtitle here')
    items        = params.get('elements', [
        {'label': 'Target',     'body': 'Primary objective and key result area.'},
        {'label': 'Strategy',   'body': 'Planned approach and decision framework.'},
        {'label': 'Execution',  'body': 'Implementation steps and tactical actions.'},
        {'label': 'Review',     'body': 'Performance assessment and adjustment loop.'},
        {'label': 'Growth',     'body': 'Continuous development and skill building.'},
        {'label': 'Culture',    'body': 'Team values, standards, and shared identity.'},
    ])
    n     = max(3, min(8, len(items)))
    items = items[:n]

    el = []

    # ── Title block ───────────────────────────────────────────────────────────
    el.append(text_el(W / 2, 62, title,
                      fs('h1', scale), scheme['primary'],
                      weight=W_BLACK, family=FONT_TITLE))
    el.append(text_el(W / 2, 62 + fs('h1', scale) * 0.72 + 10, subtitle,
                      fs('h2', scale), scheme['secondary'],
                      weight='400', family=FONT_BODY))

    # ── Donut segments ────────────────────────────────────────────────────────
    seg_angle    = 360 / n
    start_offset = -90   # first segment starts at 12 o'clock

    for i in range(n):
        start = start_offset + i * seg_angle
        end   = start + seg_angle
        fill  = _segment_color(i, n, emp, scheme)
        el.append(arc_segment_el(CX, CY, R_IN, R_OUT, start, end, fill, gap=4))

        # Segment number / icon in white
        mid_a = math.radians((start + end) / 2)
        icon_r = (R_IN + R_OUT) / 2
        el.append(text_el(
            CX + icon_r * math.cos(mid_a),
            CY + icon_r * math.sin(mid_a),
            items[i].get('icon', str(i + 1)),
            fs('label', scale * 0.82), WHITE,
            weight=W_BLACK, family=FONT_TITLE
        ))

    # ── Center circle ──────────────────────────────────────────────────────────
    center_bg = WHITE if bg == 'transparent' else scheme['bg']
    el.append(circle_el(CX, CY, R_CENTER, fill=center_bg,
                        stroke=scheme['accent'], sw=3, dash='12 6'))
    el.append(text_el(CX, CY, center_label,
                      fs('label', scale), scheme['accent'],
                      weight=W_BLACK, family=FONT_TITLE))

    # ── External labels + body text ────────────────────────────────────────────
    body_size = fs('body', scale)
    lbl_size  = fs('label', scale * 0.84)
    lh        = round(body_size * 1.38)

    for i, item in enumerate(items):
        start = start_offset + i * seg_angle
        end   = start + seg_angle
        mid   = (start + end) / 2

        label  = item.get('label', f'Item {i+1}').upper()
        body   = item.get('body', '')
        blines = wrap(body, max_chars=22) if body else []

        lx, ly, anchor = _label_pos(mid, LABEL_R, blines, body_size, lh, lbl_size)

        # For upper-half labels (sin < 0), text stack runs upward from the anchor so
        # body text doesn't fall back toward the ring.  Compute stack origin accordingly.
        sin_mid = math.sin(math.radians(mid))
        if sin_mid < -0.10:
            # Upper half — place the BOTTOM of the stack at ly.
            # Heading is above the body lines.
            n_body   = len(blines)
            stack_h  = lbl_size + n_body * lh
            heading_y = ly - stack_h + lbl_size * 0.5
            body_y0   = heading_y + lbl_size * 0.80
        else:
            # Lower half or sides — heading at top, body below.
            heading_y = ly
            body_y0   = ly + lbl_size * 0.80

        el.append(text_el(lx, heading_y, label, lbl_size, scheme['primary'],
                          weight=W_BOLD, family=FONT_BODY, anchor=anchor))

        for j, ln in enumerate(blines):
            el.append(text_el(
                lx, body_y0 + j * lh,
                ln, body_size, scheme['secondary'],
                weight=W_REGULAR, family=FONT_BODY, anchor=anchor
            ))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
