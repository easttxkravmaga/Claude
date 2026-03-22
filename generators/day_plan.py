"""
Day Plan (30-60-90 style)
──────────────────────────────────────────────────────
User-defined rows, each row:
  [LEFT — large label + unit] [MIDDLE — body text] [STAGE A] [STAGE B]
Supports 1–6 rows.
"""

from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    rect_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap,
)


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))
    emp    = int(s.get('emphasis_index', 0))

    title    = params.get('title', '30 60 90 DAY PLAN').upper()
    subtitle = params.get('subtitle', 'Your subtitle here').upper()
    items    = params.get('elements', [
        {'label': '30', 'unit': 'DAYS',
         'body':  'Describe your primary objectives and focus areas for this period.',
         'stage_a': 'STAGE A', 'stage_a_body': 'Key milestone or deliverable.',
         'stage_b': 'STAGE B', 'stage_b_body': 'Secondary milestone or deliverable.'},
        {'label': '60', 'unit': 'DAYS',
         'body':  'Build on early wins and deepen execution across all priorities.',
         'stage_a': 'STAGE A', 'stage_a_body': 'Key milestone or deliverable.',
         'stage_b': 'STAGE B', 'stage_b_body': 'Secondary milestone or deliverable.'},
        {'label': '90', 'unit': 'DAYS',
         'body':  'Drive results, measure outcomes, and set the next cycle of goals.',
         'stage_a': 'STAGE A', 'stage_a_body': 'Key milestone or deliverable.',
         'stage_b': 'STAGE B', 'stage_b_body': 'Secondary milestone or deliverable.'},
    ])
    n = max(1, min(6, len(items)))
    items = items[:n]

    el = []

    # ── Title block ───────────────────────────────────────────────────────────
    title_y    = 72
    subtitle_y = title_y + fs('h1', scale) * 0.72 + 8
    el.append(text_el(W / 2, title_y, title,
                      fs('h1', scale), scheme['accent'],
                      weight=W_BLACK, family=FONT_TITLE))
    el.append(text_el(W / 2, subtitle_y + 12, subtitle,
                      fs('h2', scale), scheme['secondary'],
                      weight='700', family=FONT_BODY))

    # ── Grid geometry ─────────────────────────────────────────────────────────
    header_bottom = subtitle_y + fs('h2', scale) + 30
    grid_top  = header_bottom
    grid_bot  = H - MARGIN
    row_h     = (grid_bot - grid_top) / n
    total_w   = W - 2 * MARGIN

    left_w   = round(total_w * 0.14)   # big number block
    stage_w  = round(total_w * 0.14)   # each stage block
    mid_w    = total_w - left_w - 2 * stage_w

    x_left   = MARGIN
    x_mid    = MARGIN + left_w
    x_sa     = x_mid + mid_w
    x_sb     = x_sa  + stage_w

    rx = 4   # corner radius for blocks

    for i, item in enumerate(items):
        y   = grid_top + i * row_h
        cy  = y + row_h / 2  # vertical center of row
        pad = 14              # inner padding

        # ── Left block (label + unit) ─────────────────────────────────────
        left_fill = scheme['accent'] if i == emp else scheme['primary']
        el.append(rect_el(x_left + 3, y + 3,
                          left_w - 6, row_h - 6, left_fill, rx=rx))

        lbl  = item.get('label', str((i + 1) * 30)).upper()
        unit = item.get('unit', 'DAYS').upper()

        # Large number
        num_sz   = fs('huge', scale * min(1.0, 160 / (n * row_h * 0.55)))
        unit_sz  = fs('label', scale * 0.75)
        num_y    = cy - unit_sz * 0.6
        unit_y   = cy + num_sz * 0.38

        el.append(text_el(x_left + left_w / 2, num_y, lbl,
                          num_sz, WHITE,
                          weight=W_BLACK, family=FONT_TITLE, anchor='middle'))
        el.append(text_el(x_left + left_w / 2, unit_y, unit,
                          unit_sz, WHITE,
                          weight=W_BOLD, family=FONT_BODY, anchor='middle'))

        # ── Middle block (body text) ──────────────────────────────────────
        mid_bg = WHITE if scheme['bg'] != BLACK else '#1a1a1a'
        el.append(rect_el(x_mid + 3, y + 3,
                          mid_w - 6, row_h - 6, mid_bg, rx=rx))

        body = item.get('body', '')
        if body:
            mid_chars = max(20, round(mid_w / (fs('body', scale) * 0.52)))
            lines     = wrap(body, max_chars=mid_chars)
            mid_text_color = BLACK if mid_bg == WHITE else scheme['primary']
            el.append(multiline_el(x_mid + mid_w / 2, cy, lines,
                                   fs('body', scale),
                                   mid_text_color, family=FONT_BODY, anchor='middle'))

        # ── Stage A ───────────────────────────────────────────────────────
        sa_fill = scheme['primary']
        el.append(rect_el(x_sa + 3, y + 3,
                          stage_w - 6, row_h - 6, sa_fill, rx=rx))

        sa_lbl  = item.get('stage_a', 'STAGE A').upper()
        sa_body = item.get('stage_a_body', '')
        _render_stage(el, x_sa, y, stage_w, row_h, sa_lbl, sa_body, WHITE, scale)

        # ── Stage B ───────────────────────────────────────────────────────
        sb_fill = scheme['secondary']
        el.append(rect_el(x_sb + 3, y + 3,
                          stage_w - 6, row_h - 6, sb_fill, rx=rx))

        sb_lbl  = item.get('stage_b', 'STAGE B').upper()
        sb_body = item.get('stage_b_body', '')
        _render_stage(el, x_sb, y, stage_w, row_h, sb_lbl, sb_body, WHITE, scale)

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)


def _render_stage(el, x, y, w, h, lbl, body, text_color, scale):
    cx = x + w / 2
    cy = y + h / 2

    lbl_sz  = fs('label', scale * 0.82)
    body_sz = fs('body',  scale * 0.78)
    body_lh = round(body_sz * 1.4)

    if body:
        lines    = wrap(body, max_chars=max(10, round(w / (body_sz * 0.52))))
        blk_h    = lbl_sz + 8 + (len(lines) - 1) * body_lh + body_sz
        lbl_y    = cy - blk_h / 2 + lbl_sz * 0.5
        body_top = lbl_y + lbl_sz * 0.5 + 8
        body_ctr = body_top + ((len(lines) - 1) * body_lh + body_sz) * 0.5
    else:
        lbl_y    = cy
        body_ctr = cy

    el.append(text_el(cx, lbl_y, lbl,
                      lbl_sz, text_color,
                      weight=W_BOLD, family=FONT_BODY, anchor='middle'))
    if body:
        el.append(multiline_el(cx, body_ctr, lines, body_sz,
                               text_color, family=FONT_BODY, anchor='middle'))
