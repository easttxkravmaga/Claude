"""
Performance Matrix / Grid
─────────────────────────
Reference: N×M rounded-rect cells, gray borders, white fills.
           Bold RED title. L-shaped RED axis lines.
           Rotated Y-axis label on left. X-axis label at bottom.
           Row labels (left), column labels (bottom).
Supports 2×2 through 4×4 grids.
"""

import math
from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    rect_el, line_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap
)

# Layout constants — extra left margin for rotated y-axis title + row labels
GRID_LEFT   = 310    # left edge of grid
GRID_RIGHT  = W - MARGIN
GRID_TOP    = 200    # top edge of grid
GRID_BOT    = H - 130  # bottom edge (room for x-axis label)


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))

    title    = params.get('title', 'PERFORMANCE INFOGRAPHIC').upper()
    x_label  = params.get('x_label', 'POTENTIAL ASSESSMENT').upper()
    y_label  = params.get('y_label', 'PERFORMANCE ASSESSMENT').upper()
    x_values = params.get('x_values', ['LOW', 'MODERATE', 'HIGH'])
    y_values = params.get('y_values', ['HIGH', 'MODERATE', 'LOW'])
    cells    = params.get('cells', [
        ['Star performer. Promote and develop as priority.', 'High performer with growth ceiling. Stretch assignments.', 'Exceptional talent. Fast-track for leadership.'],
        ['Needs coaching to unlock potential.', 'Solid contributor. Recognize and retain.', 'High potential. Invest in development now.'],
        ['Re-evaluate fit or exit path.', 'Average performer. Clarify expectations.', 'Coachable. Needs clear skill-building plan.'],
    ])

    cols    = max(2, min(4, len(x_values)))
    rows    = max(2, min(4, len(y_values)))
    x_values = x_values[:cols]
    y_values = y_values[:rows]
    cells    = [row[:cols] for row in cells[:rows]]

    el = []

    # ── Title (RED) ───────────────────────────────────────────────────────────
    el.append(text_el(W / 2, 88, title,
                      fs('h1', scale), scheme['accent'],
                      weight=W_BLACK, family=FONT_TITLE))

    # ── Grid dimensions ───────────────────────────────────────────────────────
    gw      = GRID_RIGHT - GRID_LEFT
    gh      = GRID_BOT - GRID_TOP
    cell_w  = gw / cols
    cell_h  = gh / rows
    rx      = 10   # border-radius for cells

    # ── Cells ──────────────────────────────────────────────────────────────────
    for r in range(rows):
        for c in range(cols):
            cx = GRID_LEFT + c * cell_w
            cy = GRID_TOP  + r * cell_h
            el.append(rect_el(cx + 4, cy + 4,
                              cell_w - 8, cell_h - 8,
                              fill=scheme['bg'] if bg != 'transparent' else WHITE,
                              stroke=LITE_GRAY, sw=1, rx=rx))
            body = cells[r][c] if r < len(cells) and c < len(cells[r]) else ''
            if body:
                lines = wrap(body, max_chars=max(18, round(22 * (3 / cols))))
                el.append(multiline_el(
                    cx + cell_w / 2,
                    cy + cell_h / 2,
                    lines, fs('body', scale * 0.88),
                    scheme['muted'], family=FONT_BODY
                ))

    # ── RED L-shaped axis ────────────────────────────────────────────────────
    axis_sw = 4
    # Vertical (left edge of grid)
    el.append(line_el(GRID_LEFT, GRID_TOP - 10, GRID_LEFT, GRID_BOT + 10,
                      scheme['accent'], sw=axis_sw))
    # Horizontal (bottom edge of grid)
    el.append(line_el(GRID_LEFT - 10, GRID_BOT, GRID_RIGHT + 10, GRID_BOT,
                      scheme['accent'], sw=axis_sw))

    # ── Column labels (below x-axis) ─────────────────────────────────────────
    for c, lbl in enumerate(x_values):
        cx = GRID_LEFT + c * cell_w + cell_w / 2
        el.append(text_el(cx, GRID_BOT + 36, lbl.upper(),
                          fs('node', scale * 0.85), scheme['primary'],
                          weight='700', family=FONT_BODY))

    # ── Row labels (left of y-axis) ───────────────────────────────────────────
    for r, lbl in enumerate(y_values):
        cy = GRID_TOP + r * cell_h + cell_h / 2
        el.append(text_el(GRID_LEFT - 20, cy, lbl.upper(),
                          fs('node', scale * 0.85), scheme['primary'],
                          weight='700', family=FONT_BODY, anchor='end'))

    # ── X-axis title ──────────────────────────────────────────────────────────
    el.append(text_el(GRID_LEFT + gw / 2, GRID_BOT + 80, x_label,
                      fs('label', scale * 0.90), scheme['primary'],
                      weight='700', family=FONT_BODY))

    # ── Y-axis title (rotated) ────────────────────────────────────────────────
    y_axis_cx = GRID_LEFT - 170   # moved left; row labels at GRID_LEFT-20
    y_axis_cy = GRID_TOP + gh / 2
    el.append(text_el(
        y_axis_cx, y_axis_cy, y_label,
        fs('label', scale * 0.90), scheme['primary'],
        weight='700', family=FONT_BODY,
        transform=f'rotate(-90,{y_axis_cx:.1f},{y_axis_cy:.1f})'
    ))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
