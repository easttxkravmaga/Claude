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
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    circle_el, arc_segment_el, line_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap
)

# Geometry
CX        = W // 2
CY        = int(H * 0.540)
R_OUT     = int(H * 0.320)
R_IN      = int(H * 0.190)
R_CENTER  = int(H * 0.140)
LABEL_R   = R_OUT + 48          # radius for label text anchor


def _segment_color(i, n, emp, scheme):
    if i == emp:
        return scheme['accent']
    return scheme['primary'] if i % 2 == 0 else scheme['secondary']


def _label_anchor(angle_deg):
    """Return SVG text-anchor based on which side of the circle the label falls."""
    a = angle_deg % 360
    if 80 <= a <= 100:
        return 'middle'
    if 260 <= a <= 280:
        return 'middle'
    if a < 180:
        return 'start'
    return 'end'


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))
    emp    = int(s.get('emphasis_index', 0))

    title        = params.get('title', 'Mind Map')
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

    # ── Title block (top of canvas) ───────────────────────────────────────────
    # Split title into bold first word + ultra-bold rest
    words = title.split()
    if len(words) >= 2:
        part1 = ' '.join(words[:-1])
        part2 = words[-1].upper()
        title_str = part1 + ' ' + part2
    else:
        title_str = title.upper()

    el.append(text_el(W / 2, 68, title_str,
                      fs('h1', scale), scheme['primary'],
                      weight='400', family=FONT_TITLE))
    el.append(text_el(W / 2, 68 + fs('h1', scale) * 0.72 + 10, subtitle,
                      fs('h2', scale), scheme['secondary'],
                      weight='400', family=FONT_BODY))

    # ── Donut segments ────────────────────────────────────────────────────────
    seg_angle = 360 / n
    # Start at top (-90°) so first segment is at 12 o'clock
    start_offset = -90

    for i in range(n):
        start = start_offset + i * seg_angle
        end   = start + seg_angle
        fill  = _segment_color(i, n, emp, scheme)
        el.append(arc_segment_el(CX, CY, R_IN, R_OUT, start, end, fill, gap=4))

        # Small icon placeholder (number in white) centered in segment
        mid_angle = math.radians((start + end) / 2)
        icon_r    = (R_IN + R_OUT) / 2
        ix = CX + icon_r * math.cos(mid_angle)
        iy = CY + icon_r * math.sin(mid_angle)
        icon_text = items[i].get('icon', str(i + 1))
        el.append(text_el(ix, iy, icon_text,
                          fs('label', scale * 0.80), WHITE,
                          weight='400', family=FONT_TITLE))

    # ── Center circle ──────────────────────────────────────────────────────────
    el.append(circle_el(CX, CY, R_CENTER, fill=scheme['bg'] if bg != 'transparent' else WHITE,
                        stroke=scheme['accent'], sw=3, dash='12 6'))
    el.append(text_el(CX, CY, center_label,
                      fs('label', scale), scheme['accent'],
                      weight='400', family=FONT_TITLE))

    # ── External labels + body text ────────────────────────────────────────────
    label_pad = 28
    for i, item in enumerate(items):
        start = start_offset + i * seg_angle
        end   = start + seg_angle
        mid   = (start + end) / 2
        mid_r = math.radians(mid)

        # Anchor point at edge of ring
        lx = CX + (R_OUT + label_pad) * math.cos(mid_r)
        ly = CY + (R_OUT + label_pad) * math.sin(mid_r)

        anchor = _label_anchor(mid % 360)

        label = item.get('label', f'Item {i+1}').upper()
        body  = item.get('body', '')

        el.append(text_el(lx, ly - fs('label', scale) * 0.35, label,
                          fs('label', scale * 0.82), scheme['primary'],
                          weight='700', family=FONT_BODY, anchor=anchor))

        if body:
            lines = wrap(body, max_chars=24)
            for j, ln in enumerate(lines):
                el.append(text_el(
                    lx,
                    ly + fs('body', scale) * 0.5 + j * fs('body', scale) * 1.35,
                    ln, fs('body', scale), scheme['secondary'],
                    weight='400', family=FONT_BODY, anchor=anchor
                ))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
