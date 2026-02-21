"""
Flowchart Diagram
──────────────────
Reference: standard flowchart shapes + red arrows.
Optional split layout: black left panel (title/list) + white right panel (chart).
Shapes: oval (start/end), rectangle (process), diamond (decision), parallelogram (input/output).
"""

import math
from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    rect_el, line_el, text_el, multiline_el, polygon_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap, arrow_el
)


def _oval(cx, cy, rw, rh, fill, stroke=None, sw=0):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rw}" ry="{rh}" '
            f'fill="{fill}"{s}/>')


def _diamond(cx, cy, w, h, fill):
    pts = [
        (cx,         cy - h / 2),
        (cx + w / 2, cy),
        (cx,         cy + h / 2),
        (cx - w / 2, cy),
    ]
    return polygon_el(pts, fill)


def _parallelogram(x, y, w, h, fill, skew=22):
    pts = [
        (x + skew,     y),
        (x + w,        y),
        (x + w - skew, y + h),
        (x,            y + h),
    ]
    return polygon_el(pts, fill)


def _shape(node_type, cx, cy, w, h, fill, label, scheme, scale, label_color=None):
    lc = label_color or WHITE
    els = []
    nt  = node_type.lower()

    if nt in ('start', 'end', 'oval', 'terminal'):
        els.append(_oval(cx, cy, w / 2, h / 2, fill))

    elif nt in ('decision', 'diamond'):
        els.append(_diamond(cx, cy, w, h, fill))
        lc = WHITE if fill == BLACK else BLACK

    elif nt in ('input', 'output', 'parallelogram', 'io'):
        els.append(_parallelogram(cx - w / 2, cy - h / 2, w, h, fill))

    else:  # process / rectangle
        els.append(rect_el(cx - w / 2, cy - h / 2, w, h, fill, rx=8))

    lines = wrap(label, max_chars=max(8, round(w / (fs('body', scale) * 0.6))))
    lh    = fs('body', scale) * 1.3
    for j, ln in enumerate(lines):
        els.append(text_el(
            cx,
            cy - (len(lines) - 1) * lh / 2 + j * lh,
            ln, fs('body', scale), lc,
            weight='700', family=FONT_BODY
        ))
    return ''.join(els)


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))
    split  = s.get('split_layout', False)

    title    = params.get('title', 'FLOW CHART INFOGRAPHIC')
    subtitle = params.get('subtitle', 'Your subtitle here')
    nodes    = params.get('nodes', [
        {'id': 'start',  'type': 'oval',         'label': 'Start'},
        {'id': 'proc1',  'type': 'process',       'label': 'Process Step'},
        {'id': 'dec1',   'type': 'decision',      'label': 'Decision Point?'},
        {'id': 'inp1',   'type': 'input',         'label': 'Input / Output'},
        {'id': 'proc2',  'type': 'process',       'label': 'Action Step'},
        {'id': 'end',    'type': 'oval',          'label': 'End'},
    ])
    connections = params.get('connections', [
        ['start', 'proc1'],
        ['proc1', 'dec1'],
        ['dec1',  'inp1',  'YES'],
        ['dec1',  'proc2', 'NO'],
        ['inp1',  'end'],
        ['proc2', 'end'],
    ])
    side_items = params.get('side_items', [
        {'label': 'Success',    'body': 'Track outcomes and wins clearly.'},
        {'label': 'Management', 'body': 'Oversight and resource allocation.'},
        {'label': 'Control',    'body': 'Quality gates and checkpoints.'},
        {'label': 'Target',     'body': 'KPIs and performance benchmarks.'},
    ])

    el = []

    # ── Split layout: black left panel ────────────────────────────────────────
    chart_left = MARGIN
    if split:
        panel_w = int(W * 0.44)
        el.append(rect_el(0, 0, panel_w, H, fill=scheme['primary']))

        # Title on left panel
        el.append(text_el(panel_w / 2, 80, title,
                          fs('h1', scale * 0.72), WHITE,
                          weight=W_BLACK, family=FONT_TITLE))
        el.append(text_el(panel_w / 2, 80 + fs('h1', scale * 0.72) * 0.72 + 10, subtitle,
                          fs('h2', scale * 0.80), LITE_GRAY,
                          weight='400', family=FONT_BODY))

        # Side items list
        item_y = 80 + fs('h1', scale * 0.72) + 60
        for i, si in enumerate(side_items[:6]):
            label = si.get('label', '').upper()
            body  = si.get('body', '')
            el.append(text_el(MARGIN, item_y, label,
                              fs('label', scale * 0.82), scheme['accent'],
                              weight='700', family=FONT_BODY, anchor='start'))
            if body:
                lines = wrap(body, max_chars=28)
                for j, ln in enumerate(lines):
                    el.append(text_el(
                        MARGIN,
                        item_y + fs('label', scale * 0.82) + j * fs('body', scale) * 1.35,
                        ln, fs('body', scale), LITE_GRAY,
                        weight='400', family=FONT_BODY, anchor='start'
                    ))
            item_y += fs('label', scale) + fs('body', scale) * len(wrap(body, 28)) * 1.35 + 20

        chart_left = panel_w + MARGIN
    else:
        # Full-width title at top
        el.append(text_el(W / 2, 68, title.upper(),
                          fs('h1', scale), scheme['primary'],
                          weight=W_BLACK, family=FONT_TITLE))
        el.append(text_el(W / 2, 68 + fs('h1', scale) * 0.72 + 10, subtitle,
                          fs('h2', scale), scheme['secondary'],
                          weight='400', family=FONT_BODY))

    # ── Node layout (vertical, centered in chart area) ─────────────────────────
    chart_w  = W - chart_left - MARGIN
    chart_cx = chart_left + chart_w / 2
    nn       = len(nodes)
    node_h   = round(min(96, (H - 200) / (nn + 1) * 0.75))
    node_w   = round(min(500, chart_w * 0.32))
    v_gap    = (H - 200) / (nn + 1)
    top_y    = 180 if not split else 150

    # Build id→position map
    pos = {}
    for i, node in enumerate(nodes):
        nid = node.get('id', str(i))
        cx  = chart_cx
        cy  = top_y + (i + 0.5) * v_gap
        pos[nid] = (cx, cy)
        fill = scheme['primary']
        el.append(_shape(node.get('type', 'process'), cx, cy,
                         node_w, node_h, fill,
                         node.get('label', ''), scheme, scale))

    # ── Connections ────────────────────────────────────────────────────────────
    # Pre-compute how many outgoing connections each node has (for branch routing)
    out_count = {}
    for conn in connections:
        if len(conn) >= 2:
            out_count[conn[0]] = out_count.get(conn[0], 0) + 1

    branch_seen = {}  # track which branch index a node is on
    for conn in connections:
        if len(conn) < 2:
            continue
        src, dst = conn[0], conn[1]
        label_conn = conn[2] if len(conn) > 2 else ''
        if src not in pos or dst not in pos:
            continue

        sx, sy = pos[src]
        dx, dy = pos[dst]
        branch_idx = branch_seen.get(src, 0)
        branch_seen[src] = branch_idx + 1

        is_branching = out_count.get(src, 1) > 1

        if is_branching and branch_idx > 0:
            # Non-primary branch: exit right, elbow down, enter from right
            elbow_x = sx + node_w / 2 + 64
            # Horizontal leg out
            el.append(line_el(sx + node_w / 2, sy, elbow_x, sy,
                              scheme['accent'], sw=3))
            # Vertical leg down (stop before node edge)
            el.append(line_el(elbow_x, sy, elbow_x, dy,
                              scheme['accent'], sw=3))
            # Horizontal leg in — arrow_el handles the arrowhead
            el.append(arrow_el(elbow_x, dy, dx + node_w / 2 + 2, dy,
                               scheme['accent'], sw=3, head=14))
            if label_conn:
                # Label just to the right of the source node, at mid-vertical
                el.append(text_el(elbow_x + 10, (sy + dy) / 2, label_conn,
                                  fs('body', scale * 0.85), scheme['accent'],
                                  weight='700', family=FONT_BODY, anchor='start'))
        else:
            el.append(arrow_el(sx, sy + node_h / 2 + 2,
                               dx, dy - node_h / 2 - 2,
                               scheme['accent'], sw=3, head=14))
            if label_conn:
                # Label to the right of the arrow, at one-third down
                lx = sx + node_w / 2 + 16
                ly = sy + (dy - sy) * 0.30
                el.append(text_el(lx, ly, label_conn,
                                  fs('body', scale * 0.85), scheme['accent'],
                                  weight='700', family=FONT_BODY, anchor='start'))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
