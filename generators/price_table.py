"""
Price / Feature Card Table
───────────────────────────
Reference: N equal columns, each with:
  - Black rounded-rect header (white bold text)
  - Red icon placeholder
  - Large price + period
  - Feature list (regular weight)
  - Black CTA button
  - Gray chevron footer indicator
Supports 2–5 columns.
"""

from .base import (
    W, H, MARGIN, FONT_TITLE, FONT_BODY,
    get_scheme, fs,
    rect_el, polygon_el, text_el, multiline_el, line_el,
    BLACK, WHITE, RED, GRAY, LITE_GRAY, build_svg, wrap
)


def _chevron_down(cx, y, size, fill):
    """Small downward-pointing chevron indicator."""
    hw = size
    hh = size * 0.55
    pts = [
        (cx - hw, y),
        (cx + hw, y),
        (cx,      y + hh),
    ]
    return polygon_el(pts, fill)


def _icon_placeholder(cx, cy, size, color):
    """Simple geometric icon: a bold circle with a star-like cross."""
    r = size
    lines = [
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" '
        f'stroke="{color}" stroke-width="4"/>',
        f'<line x1="{cx:.1f}" y1="{cy-r*0.55:.1f}" x2="{cx:.1f}" y2="{cy+r*0.55:.1f}" '
        f'stroke="{color}" stroke-width="4"/>',
        f'<line x1="{cx-r*0.55:.1f}" y1="{cy:.1f}" x2="{cx+r*0.55:.1f}" y2="{cy:.1f}" '
        f'stroke="{color}" stroke-width="4"/>',
    ]
    return ''.join(lines)


def generate(params):
    s      = params.get('settings', {})
    scheme = get_scheme(s.get('color_scheme', 'brand'), s)
    bg     = s.get('background', 'transparent')
    scale  = float(s.get('text_scale', 1.0))

    title    = params.get('title', 'PRICE TABLE').upper()
    subtitle = params.get('subtitle', 'WRITE YOUR SUBTITLE HERE').upper()
    items    = params.get('elements', [
        {'name': 'SILVER',   'price': '$1.99',  'period': '/month',
         'features': ['Feature One', 'Feature Two', 'Feature Three', 'Feature Four'],
         'button': 'SIGN UP'},
        {'name': 'GOLD',     'price': '$4.99',  'period': '/month',
         'features': ['Feature One', 'Feature Two', 'Feature Three', 'Feature Four'],
         'button': 'SIGN UP'},
        {'name': 'PLATINUM', 'price': '$9.99',  'period': '/month',
         'features': ['Feature One', 'Feature Two', 'Feature Three', 'Feature Four'],
         'button': 'SIGN UP'},
        {'name': 'DIAMOND',  'price': '$19.99', 'period': '/month',
         'features': ['Feature One', 'Feature Two', 'Feature Three', 'Feature Four'],
         'button': 'SIGN UP'},
    ])
    n     = max(2, min(5, len(items)))
    items = items[:n]

    el = []

    # ── Title block ───────────────────────────────────────────────────────────
    el.append(text_el(W / 2, 72, title,
                      fs('h1', scale), scheme['accent'],
                      weight='400', family=FONT_TITLE))
    el.append(text_el(W / 2, 72 + fs('h1', scale) * 0.72 + 10, subtitle,
                      fs('h2', scale), scheme['primary'],
                      weight='700', family=FONT_BODY))

    # ── Card layout ───────────────────────────────────────────────────────────
    card_gap   = 28
    total_card_w = W - 2 * MARGIN - (n - 1) * card_gap
    card_w     = total_card_w / n
    card_top   = 72 + fs('h1', scale) * 0.72 + 10 + fs('h2', scale) + 36
    card_bot   = H - MARGIN
    card_h     = card_bot - card_top
    header_h   = round(card_h * 0.115)
    rx         = 14

    for i, item in enumerate(items):
        cx_card = MARGIN + i * (card_w + card_gap)

        # ── Header block ──────────────────────────────────────────────────────
        el.append(rect_el(cx_card, card_top, card_w, header_h,
                          fill=scheme['primary'], rx=rx))
        # Fix bottom radius of header by overlapping bottom corners
        el.append(rect_el(cx_card, card_top + header_h / 2, card_w, header_h / 2,
                          fill=scheme['primary']))
        el.append(text_el(cx_card + card_w / 2, card_top + header_h / 2,
                          item.get('name', f'TIER {i+1}').upper(),
                          fs('label', scale * 0.88), WHITE,
                          weight='700', family=FONT_BODY))

        # ── Red icon ──────────────────────────────────────────────────────────
        icon_y = card_top + header_h + 42
        el.append(_icon_placeholder(cx_card + card_w / 2, icon_y,
                                    fs('label', scale) * 0.72, scheme['accent']))

        # ── Price ─────────────────────────────────────────────────────────────
        price_y = icon_y + fs('label', scale) + 28
        el.append(text_el(cx_card + card_w / 2, price_y,
                          item.get('price', '$0.00'),
                          fs('huge', scale * 0.72), scheme['primary'],
                          weight='400', family=FONT_TITLE))
        el.append(text_el(cx_card + card_w / 2, price_y + fs('huge', scale * 0.72) * 0.55,
                          item.get('period', '/month'),
                          fs('body', scale), scheme['secondary'],
                          weight='400', family=FONT_BODY))

        # ── Feature list ──────────────────────────────────────────────────────
        features = item.get('features', [])
        feat_y   = price_y + fs('huge', scale * 0.72) + 36
        lh       = fs('body', scale) * 1.7
        for j, feat in enumerate(features[:6]):
            el.append(text_el(cx_card + card_w / 2,
                              feat_y + j * lh,
                              feat, fs('body', scale),
                              scheme['primary'], weight='400', family=FONT_BODY))

        # ── CTA button ────────────────────────────────────────────────────────
        btn_h  = round(card_h * 0.092)
        btn_y  = card_bot - btn_h - 52
        btn_rx = 10
        el.append(rect_el(cx_card + 16, btn_y, card_w - 32, btn_h,
                          fill=scheme['primary'], rx=btn_rx))
        el.append(text_el(cx_card + card_w / 2, btn_y + btn_h / 2,
                          item.get('button', 'SIGN UP'),
                          fs('node', scale * 0.88), WHITE,
                          weight='700', family=FONT_BODY))

        # ── Gray chevron footer ───────────────────────────────────────────────
        el.append(_chevron_down(cx_card + card_w / 2,
                                card_bot - 36, 18, LITE_GRAY))

    mode = params.get('_mode', 'preview')
    return build_svg(el, bg=bg if bg != 'transparent' else scheme['bg'], mode=mode)
