"""
Customer Journey Map — Matrix variant
───────────────────────────────────────
Column headers = stage names (user-defined, via x_values or elements).
Row headers = phase labels from elements[i].label.
Cell content from elements[i].cells (comma-separated per column).
RED accent title. Grid is full-canvas minus margins.
"""

from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    rect_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap
)

_DEFAULT_STAGES = [
    'AWARENESS', 'ENGAGEMENT', 'EVALUATION', 'PURCHASE', 'POST-PURCHASE',
]
_DEFAULT_ROWS = [
    {'label': 'ACTIONS',            'cells': ', , , , '},
    {'label': 'QUESTIONS',          'cells': ', , , , '},
    {'label': 'TOUCH POINTS',       'cells': ', , , , '},
    {'label': 'OPPORTUNITIES',      'cells': ', , , , '},
    {'label': 'CONTENT NEEDED',     'cells': ', , , , '},
]


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))

    title = params.get('title', 'CUSTOMER JOURNEY MAP').upper()

    # ── Column headers ────────────────────────────────────────────────────────
    # Accept x_values list (from extra-field) or fall back to defaults
    raw_stages = params.get('x_values', _DEFAULT_STAGES)
    if isinstance(raw_stages, str):
        raw_stages = [v.strip() for v in raw_stages.split(',') if v.strip()]
    stages = [str(s_).upper() for s_ in raw_stages if s_]
    nc = max(1, min(8, len(stages)))
    stages = stages[:nc]

    # ── Row data from elements ────────────────────────────────────────────────
    rows = params.get('elements', _DEFAULT_ROWS)
    if not rows:
        rows = _DEFAULT_ROWS
    nr = max(1, min(8, len(rows)))
    rows = rows[:nr]

    # Parse each row's cell content
    def parse_cells(row):
        raw = row.get('cells', '')
        if isinstance(raw, list):
            return [str(c) for c in raw]
        parts = raw.split(',')
        return [p.strip() for p in parts]

    cell_data = [parse_cells(r) for r in rows]
    phase_labels = [r.get('label', f'ROW {i+1}').upper() for i, r in enumerate(rows)]

    el = []

    # ── Title ─────────────────────────────────────────────────────────────────
    el.append(text_el(W / 2, 68, title,
                      fs('h1', scale), scheme['accent'],
                      weight=W_BLACK, family=FONT_TITLE))

    # ── Grid layout ───────────────────────────────────────────────────────────
    row_hdr_w = 210
    grid_left  = MARGIN + row_hdr_w
    grid_top   = 68 + fs('h1', scale) * 0.72 + 36
    grid_right = W - MARGIN
    grid_bot   = H - MARGIN

    col_hdr_h = round((grid_bot - grid_top) * 0.10)
    content_h = grid_bot - grid_top - col_hdr_h
    cell_h    = content_h / nr
    cell_w    = (grid_right - grid_left) / nc
    hdr_rx    = 5

    # ── Column headers ────────────────────────────────────────────────────────
    for c, stage in enumerate(stages):
        cx_cell = grid_left + c * cell_w
        el.append(rect_el(cx_cell + 3, grid_top + 3,
                          cell_w - 6, col_hdr_h - 6,
                          fill=LITE_GRAY, rx=hdr_rx))
        el.append(text_el(cx_cell + cell_w / 2,
                          grid_top + col_hdr_h / 2,
                          stage, fs('node', scale * 0.80),
                          BLACK, weight='700', family=FONT_BODY))

    # ── Row headers ───────────────────────────────────────────────────────────
    for r, phase in enumerate(phase_labels):
        cy_row = grid_top + col_hdr_h + r * cell_h
        el.append(rect_el(MARGIN + 3, cy_row + 3,
                          row_hdr_w - 6, cell_h - 6,
                          fill=LITE_GRAY, rx=hdr_rx))
        lines = wrap(phase, max_chars=13)
        el.append(multiline_el(MARGIN + row_hdr_w / 2,
                               cy_row + cell_h / 2,
                               lines, fs('body', scale * 0.80),
                               BLACK, family=FONT_BODY, weight='700'))

    # ── Content cells ─────────────────────────────────────────────────────────
    cell_bg = WHITE if (bg == 'transparent' or scheme['bg'] == WHITE) else '#1a1a1a'
    body_col = BLACK if cell_bg == WHITE else LITE_GRAY
    for r in range(nr):
        for c in range(nc):
            cx_cell = grid_left + c * cell_w
            cy_row  = grid_top + col_hdr_h + r * cell_h
            el.append(rect_el(cx_cell + 3, cy_row + 3,
                              cell_w - 6, cell_h - 6,
                              fill=cell_bg, stroke=LITE_GRAY, sw=1, rx=0))
            cells = cell_data[r] if r < len(cell_data) else []
            body  = cells[c] if c < len(cells) else ''
            if body:
                max_c = max(10, round(cell_w / (fs('body', scale) * 0.50)))
                lines = wrap(body, max_chars=max_c)
                el.append(multiline_el(
                    cx_cell + cell_w / 2, cy_row + cell_h / 2,
                    lines, fs('body', scale * 0.80),
                    body_col, family=FONT_BODY
                ))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
