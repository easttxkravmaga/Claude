"""
Customer Journey Map — Matrix variant
───────────────────────────────────────
Reference: column headers (stages) as gray rounded-rect cells,
           row headers (phases) as bold gray left labels,
           white content cells, thin gray borders.
           RED title. Grid is full-canvas minus margins.
"""

from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    rect_el, line_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap
)


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))

    title   = params.get('title', 'CUSTOMER JOURNEY MAP').upper()
    stages  = params.get('x_values', [
        'AWARENESS', 'ENGAGEMENT', 'EVALUATION', 'PURCHASE', 'POST-PURCHASE',
    ])
    phases  = params.get('y_values', [
        'ACTIONS', 'QUESTIONS & THOUGHTS', 'TOUCH POINTS',
        'OPPORTUNITIES', 'CONTENT NEEDED',
    ])
    cells   = params.get('cells', [['' for _ in stages] for _ in phases])

    nc = max(2, min(6, len(stages)))
    nr = max(2, min(7, len(phases)))
    stages = stages[:nc]
    phases = phases[:nr]
    cells  = [row[:nc] for row in cells[:nr]]

    el = []

    # ── Title ─────────────────────────────────────────────────────────────────
    el.append(text_el(W / 2, 68, title,
                      fs('h1', scale), scheme['accent'],
                      weight=W_BLACK, family=FONT_TITLE))

    # ── Grid layout ───────────────────────────────────────────────────────────
    row_hdr_w = 220          # width of row header column
    grid_left = MARGIN + row_hdr_w
    grid_top  = 68 + fs('h1', scale) * 0.72 + 36
    grid_right = W - MARGIN
    grid_bot   = H - MARGIN

    col_hdr_h = round((grid_bot - grid_top) * 0.11)
    content_h = grid_bot - grid_top - col_hdr_h
    cell_h    = content_h / nr
    cell_w    = (grid_right - grid_left) / nc

    rx = 0   # sharp corners for grid cells
    hdr_rx = 6

    # ── Column headers (stage labels) ─────────────────────────────────────────
    for c, stage in enumerate(stages):
        cx_cell = grid_left + c * cell_w
        cy_hdr  = grid_top
        el.append(rect_el(cx_cell + 3, cy_hdr + 3,
                          cell_w - 6, col_hdr_h - 6,
                          fill=LITE_GRAY, rx=hdr_rx))
        el.append(text_el(cx_cell + cell_w / 2, cy_hdr + col_hdr_h / 2,
                          stage.upper(), fs('node', scale * 0.82),
                          WHITE if scheme['primary'] == BLACK else BLACK,
                          weight='700', family=FONT_BODY))

    # ── Row headers (phase labels) ────────────────────────────────────────────
    for r, phase in enumerate(phases):
        cy_row = grid_top + col_hdr_h + r * cell_h
        # Background
        el.append(rect_el(MARGIN + 3, cy_row + 3,
                          row_hdr_w - 6, cell_h - 6,
                          fill=LITE_GRAY, rx=hdr_rx))
        lines = wrap(phase.upper(), max_chars=14)
        el.append(multiline_el(
            MARGIN + row_hdr_w / 2, cy_row + cell_h / 2,
            lines, fs('body', scale * 0.82),
            BLACK, family=FONT_BODY, weight='700'
        ))

    # ── Content cells ─────────────────────────────────────────────────────────
    for r in range(nr):
        for c in range(nc):
            cx_cell = grid_left + c * cell_w
            cy_row  = grid_top + col_hdr_h + r * cell_h
            el.append(rect_el(cx_cell + 3, cy_row + 3,
                              cell_w - 6, cell_h - 6,
                              fill=scheme['bg'] if bg != 'transparent' else WHITE,
                              stroke=LITE_GRAY, sw=1, rx=0))
            body = cells[r][c] if r < len(cells) and c < len(cells[r]) else ''
            if body:
                lines = wrap(body, max_chars=max(12, round(18 * (4 / nc))))
                el.append(multiline_el(
                    cx_cell + cell_w / 2, cy_row + cell_h / 2,
                    lines, fs('body', scale * 0.80),
                    scheme['secondary'], family=FONT_BODY
                ))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
