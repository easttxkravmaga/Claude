"""
Timeline Dots
─────────────────────────────────────────────────────
Horizontal red line with evenly spaced dots.
Items alternate above / below the line.
Each element: heading (bold) + body text.
Supports 2–9 elements.
"""

import math

from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    circle_el, line_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap, polygon_el,
)


def _arrowhead(cx, tip_y, size, pointing_down, fill):
    """Solid triangle arrowhead pointing toward the timeline."""
    h = size
    w = size * 0.7
    if pointing_down:
        pts = [(cx, tip_y), (cx - w, tip_y - h), (cx + w, tip_y - h)]
    else:
        pts = [(cx, tip_y), (cx - w, tip_y + h), (cx + w, tip_y + h)]
    pts_str = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polygon points="{pts_str}" fill="{fill}"/>'


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))
    emp    = int(s.get('emphasis_index', 0))

    title    = params.get('title', 'TIME LINE').upper()
    subtitle = params.get('subtitle', 'Your subtitle here').upper()
    items    = params.get('elements', [
        {'heading': 'MILESTONE 01', 'body': 'Description text here.'},
        {'heading': 'MILESTONE 02', 'body': 'Description text here.'},
        {'heading': 'MILESTONE 03', 'body': 'Description text here.'},
        {'heading': 'MILESTONE 04', 'body': 'Description text here.'},
        {'heading': 'MILESTONE 05', 'body': 'Description text here.'},
    ])
    n = max(2, min(9, len(items)))
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

    # ── Layout geometry ───────────────────────────────────────────────────────
    header_bottom = subtitle_y + fs('h2', scale) + 28
    available_h   = H - MARGIN - header_bottom
    timeline_y    = header_bottom + available_h * 0.5   # center of available space

    half_space = available_h * 0.5
    dot_r      = max(8, min(13, round(11 * scale)))
    arrow_h    = max(40, min(90, round(half_space * 0.24)))
    head_size  = fs('label', scale * 0.9)
    body_size  = fs('body',  scale)
    body_lh    = round(body_size * 1.45)

    # Horizontal positions
    total_w   = W - 2 * MARGIN
    step      = total_w / (n - 1) if n > 1 else total_w
    col_chars = max(12, round(26 - n * 1.5))

    # ── Timeline line ─────────────────────────────────────────────────────────
    el.append(line_el(MARGIN, timeline_y, W - MARGIN, timeline_y,
                      scheme['accent'], sw=4))

    # ── Items ─────────────────────────────────────────────────────────────────
    for i, item in enumerate(items):
        cx    = MARGIN + i * step if n > 1 else W / 2
        above = (i % 2 == 0)

        dot_fill = scheme['accent'] if i == emp else scheme['primary']

        # Dot
        el.append(circle_el(cx, timeline_y, dot_r, dot_fill))

        # Arrow stem
        if above:
            stem_start = timeline_y - dot_r
            stem_end   = stem_start - arrow_h
        else:
            stem_start = timeline_y + dot_r
            stem_end   = stem_start + arrow_h

        el.append(line_el(cx, stem_start, cx, stem_end, scheme['accent'], sw=3))

        # Arrowhead pointing AWAY from the line (toward text)
        ah_size = max(7, round(9 * scale))
        el.append(_arrowhead(cx, stem_end, ah_size,
                              pointing_down=not above,  # above→arrowhead points up (away from line)
                              fill=scheme['accent']))

        # Heading
        if above:
            head_y = stem_end - ah_size - head_size * 0.5 - 8
        else:
            head_y = stem_end + ah_size + head_size * 0.5 + 8

        heading = item.get('heading', f'MILESTONE {i+1:02d}').upper()
        el.append(text_el(cx, head_y, heading,
                          head_size, scheme['primary'],
                          weight=W_BOLD, family=FONT_BODY, anchor='middle'))

        # Body text
        body = item.get('body', '')
        if body:
            lines    = wrap(body, max_chars=col_chars)
            body_blk = (len(lines) - 1) * body_lh + body_size
            if above:
                body_y = head_y - head_size * 0.5 - 8 - body_blk * 0.5
            else:
                body_y = head_y + head_size * 0.5 + 8 + body_blk * 0.5
            el.append(multiline_el(cx, body_y, lines, body_size,
                                   scheme['secondary'],
                                   family=FONT_BODY, anchor='middle'))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
