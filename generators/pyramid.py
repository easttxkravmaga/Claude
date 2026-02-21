"""
Pyramid Diagram
───────────────
Reference: stacked trapezoids (all-RED by default), white separator lines,
           bold white labels centered in each level.
           Right side: numbered bullet list aligned to each level.
Supports 2–6 levels.
"""

import math
from .base import (
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    polygon_el, line_el, text_el, multiline_el, rect_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap
)

# Pyramid geometry constants
PYRAMID_CX   = int(W * 0.255)    # horizontal center of pyramid
PYRAMID_BASE = int(W * 0.370)    # width of bottom level
PYRAMID_TOP  = int(H * 0.155)    # y of pyramid apex
PYRAMID_BOT  = int(H * 0.920)    # y of pyramid base
BULLET_X     = int(W * 0.550)    # x start of bullet list
BULLET_W     = int(W * 0.400)    # width of bullet area


def _trapezoid(cx, total_h, level_h, level_i, n, fill, sep_color=WHITE):
    """Return trapezoid + separator line for one pyramid level."""
    base_w  = PYRAMID_BASE
    # Width at each y (straight pyramid sides)
    y_top_r = level_i * level_h
    y_bot_r = (level_i + 1) * level_h
    w_top   = base_w * y_top_r / total_h
    w_bot   = base_w * y_bot_r / total_h

    y_abs_top = PYRAMID_TOP + y_top_r
    y_abs_bot = PYRAMID_TOP + y_bot_r

    pts = [
        (cx - w_top / 2, y_abs_top),
        (cx + w_top / 2, y_abs_top),
        (cx + w_bot / 2, y_abs_bot),
        (cx - w_bot / 2, y_abs_bot),
    ]
    els = [polygon_el(pts, fill)]

    # Separator line (not at bottom of last level)
    if level_i < n - 1:
        els.append(line_el(
            cx - w_bot / 2, y_abs_bot,
            cx + w_bot / 2, y_abs_bot,
            sep_color, sw=3
        ))
    return ''.join(els)


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))
    p_color = s.get('pyramid_color', scheme['accent'])  # default RED

    title    = params.get('title', '4-LEVEL PYRAMID DIAGRAM').upper()
    subtitle = params.get('subtitle', 'YOUR SUBTITLE HERE').upper()
    items    = params.get('elements', [
        {'label': 'KIT',      'body': 'The foundational equipment and tools required for training.'},
        {'label': 'SKILLS',   'body': 'Core techniques and physical capabilities developed through repetition.'},
        {'label': 'TACTICS',  'body': 'Strategic decision-making under pressure and in live scenarios.'},
        {'label': 'MINDSET',  'body': 'Mental toughness, situational awareness, and adaptive thinking.'},
    ])
    n     = max(2, min(6, len(items)))
    items = items[:n]

    el = []

    # ── Title ─────────────────────────────────────────────────────────────────
    title_cx = W / 2
    el.append(text_el(title_cx, 68, title,
                      fs('h1', scale), scheme['primary'],
                      weight='400', family=FONT_TITLE))
    el.append(text_el(title_cx, 68 + fs('h1', scale) * 0.72 + 8, subtitle,
                      fs('h2', scale), scheme['secondary'],
                      weight='700', family=FONT_BODY))

    # Red accent line under subtitle
    acc_y  = 68 + fs('h1', scale) * 0.72 + 8 + fs('h2', scale) * 0.75
    acc_w  = 200
    el.append(line_el(title_cx - acc_w / 2, acc_y,
                      title_cx + acc_w / 2, acc_y,
                      scheme['accent'], sw=4))

    # ── Pyramid ───────────────────────────────────────────────────────────────
    total_h = PYRAMID_BOT - PYRAMID_TOP
    level_h = total_h / n

    for i in range(n):
        el.append(_trapezoid(PYRAMID_CX, total_h, level_h, i, n,
                             fill=p_color, sep_color=WHITE))

        # Level label
        y_mid = PYRAMID_TOP + (i + 0.5) * level_h
        label = items[i].get('label', f'LEVEL {i+1}').upper()
        el.append(text_el(PYRAMID_CX, y_mid, label,
                          fs('label', scale), WHITE,
                          weight='400', family=FONT_TITLE))

    # ── Bullet list ───────────────────────────────────────────────────────────
    bullet_r  = 9
    text_x    = BULLET_X + bullet_r * 2 + 12

    for i in range(n):
        y_mid   = PYRAMID_TOP + (i + 0.5) * level_h
        body    = items[i].get('body', '')
        label   = items[i].get('label', f'LEVEL {i+1}').upper()

        # Bullet dot
        el.append(
            f'<circle cx="{BULLET_X + bullet_r}" cy="{y_mid:.1f}" '
            f'r="{bullet_r}" fill="{scheme["primary"]}"/>'
        )

        # Bold label
        el.append(text_el(text_x, y_mid - fs('node', scale) * 0.55, label,
                          fs('node', scale), scheme['primary'],
                          weight='700', family=FONT_BODY, anchor='start'))

        # Body text
        if body:
            lines = wrap(body, max_chars=46)
            for j, ln in enumerate(lines):
                el.append(text_el(
                    text_x,
                    y_mid + fs('body', scale) * 0.30 + j * fs('body', scale) * 1.35,
                    ln, fs('body', scale), scheme['secondary'],
                    weight='400', family=FONT_BODY, anchor='start'
                ))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
