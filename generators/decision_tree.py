"""
Decision Tree Diagram
──────────────────────
Reference: left-to-right branching tree.
           Black rounded-rect nodes, RED connector lines with arrows.
           Root → N mid nodes → 2 leaves each.
Supports 2–4 branches (total nodes: 1 + N + N*2).
"""

import math
from .base import (
    W_BLACK, W_BOLD, W_REGULAR,
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    rect_el, line_el, text_el, multiline_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap, arrow_el
)


def _node(x, y, w, h, label, body, scheme, scale, rx=12):
    """Render a rounded-rect node with label and optional body."""
    els = []
    els.append(rect_el(x, y, w, h, fill=scheme['primary'], rx=rx))
    # Label
    lines = wrap(label, max_chars=max(8, round(w / (fs('node', scale) * 0.55))))
    label_y = y + h / 2 - (len(lines) - 1) * fs('node', scale * 0.7) / 2
    for j, ln in enumerate(lines):
        els.append(text_el(
            x + w / 2,
            label_y + j * fs('node', scale * 0.75) * 1.3,
            ln.upper(), fs('node', scale * 0.75), WHITE,
            weight='700', family=FONT_BODY
        ))
    return ''.join(els)


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))

    title    = params.get('title', 'DECISION TREE DIAGRAM').upper()
    subtitle = params.get('subtitle', 'YOUR TITLE').upper()
    root     = params.get('root', {'label': 'START', 'body': ''})
    branches = params.get('branches', [
        {'label': 'Option A', 'leaves': [
            {'label': 'Result 1', 'body': 'Outcome description.'},
            {'label': 'Result 2', 'body': 'Outcome description.'},
        ]},
        {'label': 'Option B', 'leaves': [
            {'label': 'Result 3', 'body': 'Outcome description.'},
            {'label': 'Result 4', 'body': 'Outcome description.'},
        ]},
        {'label': 'Option C', 'leaves': [
            {'label': 'Result 5', 'body': 'Outcome description.'},
            {'label': 'Result 6', 'body': 'Outcome description.'},
        ]},
    ])
    nb = max(2, min(4, len(branches)))
    branches = branches[:nb]

    el = []

    # ── Title ─────────────────────────────────────────────────────────────────
    title_y = 68
    el.append(text_el(W / 2, title_y, title,
                      fs('h1', scale), scheme['primary'],
                      weight=W_BLACK, family=FONT_TITLE))
    sub_y = title_y + fs('h1', scale) * 0.72 + 10
    el.append(text_el(W / 2, sub_y, subtitle,
                      fs('h2', scale), scheme['secondary'],
                      weight='700', family=FONT_BODY))

    # ── Layout geometry ───────────────────────────────────────────────────────
    tree_top = sub_y + fs('h2', scale) + 48
    tree_bot = H - MARGIN - 40
    tree_h   = tree_bot - tree_top

    # Node sizes
    node_w  = round(min(220, (W - 2 * MARGIN) * 0.14))
    node_h  = round(node_w * 0.45)

    # 3 columns: root, mid, leaves
    # Leaf nodes shifted left so body text fits to their right without clipping
    body_w   = int(W * 0.20)  # max width for body text block
    leaf_cx_x = W - MARGIN - node_w * 0.5 - body_w
    col_xs   = [
        MARGIN + node_w * 0.5,
        W * 0.38,
        leaf_cx_x,
    ]

    total_leaves = nb * 2
    leaf_spacing = tree_h / total_leaves

    # ── Root node ─────────────────────────────────────────────────────────────
    root_cx = col_xs[0]
    root_cy = tree_top + tree_h / 2
    el.append(_node(root_cx - node_w / 2, root_cy - node_h / 2,
                    node_w, node_h,
                    root.get('label', 'START'), root.get('body', ''),
                    scheme, scale))

    # ── Branch nodes + leaves ─────────────────────────────────────────────────
    for bi, branch in enumerate(branches):
        # Mid node y-center: evenly divide tree_h among branches
        mid_cy = tree_top + tree_h * (bi + 0.5) / nb
        mid_cx = col_xs[1]

        # Arrow: root → mid
        el.append(arrow_el(
            root_cx + node_w / 2, root_cy,
            mid_cx - node_w / 2,  mid_cy,
            scheme['accent'], sw=3, head=16
        ))

        el.append(_node(mid_cx - node_w / 2, mid_cy - node_h / 2,
                        node_w, node_h,
                        branch.get('label', f'Branch {bi+1}'), '',
                        scheme, scale))

        # Leaves
        leaves = branch.get('leaves', [
            {'label': f'Result {bi*2+1}', 'body': ''},
            {'label': f'Result {bi*2+2}', 'body': ''},
        ])[:2]

        for li, leaf in enumerate(leaves):
            leaf_cy = tree_top + (bi * 2 + li + 0.5) * leaf_spacing
            leaf_cx = col_xs[2]

            # Arrow: mid → leaf
            el.append(arrow_el(
                mid_cx + node_w / 2, mid_cy,
                leaf_cx - node_w / 2, leaf_cy,
                scheme['accent'], sw=3, head=16
            ))

            el.append(_node(leaf_cx - node_w / 2, leaf_cy - node_h / 2,
                            node_w, node_h,
                            leaf.get('label', f'Leaf {bi*2+li+1}'), '',
                            scheme, scale))

            # Body text to the right of leaf node (clamped to canvas)
            body = leaf.get('body', '')
            if body:
                text_x  = leaf_cx + node_w / 2 + 14
                max_x   = W - MARGIN
                if text_x < max_x - 20:
                    chars = max(10, round((max_x - text_x) / (fs('body', scale) * 0.6)))
                    lines = wrap(body, max_chars=chars)
                    for j, ln in enumerate(lines):
                        el.append(text_el(
                            text_x,
                            leaf_cy - fs('body', scale) * 0.4 + j * fs('body', scale) * 1.4,
                            ln, fs('body', scale), scheme['secondary'],
                            weight=W_REGULAR, family=FONT_BODY, anchor='start'
                        ))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
