"""
Chevron Flow / Milestone Timeline
────────────────────────────────
Reference: horizontal alternating chevrons (Black → Red → Gray)
           with year/stage labels INSIDE and content columns below.
Supports 2–8 elements.
"""

from .base import (
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, chevron_color, fs, SIZES,
    chevron_el, text_el, multiline_el, h_rule, bg_rect,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap
)


def generate(params):
    s        = params.get('settings', {})
    scheme   = get_scheme(s.get('color_scheme', 'brand'), s)
    bg       = s.get('background', 'transparent')
    scale    = float(s.get('text_scale', 1.0))
    emp      = int(s.get('emphasis_index', 1))
    show_sub = s.get('show_content', True)

    title    = params.get('title', 'PROCESS TITLE').upper()
    subtitle = params.get('subtitle', 'YOUR SUBTITLE HERE').upper()
    items    = params.get('elements', [
        {'label': 'STEP 1', 'sub_label': 'MILESTONE 01', 'body': 'Description text goes here for this stage.'},
        {'label': 'STEP 2', 'sub_label': 'MILESTONE 02', 'body': 'Description text goes here for this stage.'},
        {'label': 'STEP 3', 'sub_label': 'MILESTONE 03', 'body': 'Description text goes here for this stage.'},
    ])
    n = max(2, min(8, len(items)))
    items = items[:n]

    el = []

    # ── Title block ───────────────────────────────────────────────────────────
    title_y    = 72
    subtitle_y = title_y + fs('h1', scale) * 0.72
    el.append(text_el(W / 2, title_y, title,
                      fs('h1', scale), scheme['primary'],
                      weight='400', family=FONT_TITLE))
    el.append(text_el(W / 2, subtitle_y + 12, subtitle,
                      fs('h2', scale), scheme['secondary'],
                      weight='700', family=FONT_BODY))

    # ── Chevron band ──────────────────────────────────────────────────────────
    ch_y  = subtitle_y + fs('h2', scale) + 36
    ch_h  = max(100, min(160, round(130 * scale)))
    total_w = W - 2 * MARGIN
    ch_w    = total_w / n

    for i, item in enumerate(items):
        x    = MARGIN + i * ch_w
        fill = chevron_color(i, n, emp, scheme)
        el.append(chevron_el(x, ch_y, ch_w, ch_h, fill, is_first=(i == 0)))

        # Inner label (stage label / year / short text)
        label = item.get('label', f'ITEM {i+1}').upper()
        cx    = x + ch_w / 2
        cy    = ch_y + ch_h / 2
        # Adjust cx so text clears the notch (shift right for non-first)
        nd    = ch_h * 0.40
        if i > 0:
            cx += nd * 0.18
        text_color = scheme['on_dark'] if fill != WHITE else scheme['on_light']
        el.append(text_el(cx, cy, label,
                          fs('large', scale * 0.75), text_color,
                          weight='400', family=FONT_TITLE))

    # ── Content below chevrons ────────────────────────────────────────────────
    if show_sub:
        content_top = ch_y + ch_h + 48
        col_w       = total_w / n

        for i, item in enumerate(items):
            cx  = MARGIN + i * col_w + col_w / 2
            cy  = content_top

            # Sub-label / milestone heading
            sub = item.get('sub_label', f'MILESTONE {i+1:02d}').upper()
            el.append(text_el(cx, cy + fs('label', scale) * 0.5, sub,
                              fs('label', scale), scheme['primary'],
                              weight='700', family=FONT_BODY))

            # Body text
            body = item.get('body', '')
            if body:
                lines = wrap(body, max_chars=max(20, round(28 / (n / 3))))
                body_y = cy + fs('label', scale) + 18
                el.append(multiline_el(cx, body_y + (len(lines) - 1) * fs('body', scale) * 0.72,
                                       lines, fs('body', scale),
                                       scheme['secondary'],
                                       family=FONT_BODY, anchor='middle'))

            # Column separator (lite gray vertical rule, except last)
            if i < n - 1:
                rx = MARGIN + (i + 1) * col_w
                el.append(h_rule(rx, content_top - 12, 0,
                                  color=LITE_GRAY, sw=1))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
