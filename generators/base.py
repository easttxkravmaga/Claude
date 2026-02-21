"""
ETKM Visual Aide — Base SVG Utilities
Brand: Black #000000 | White #FFFFFF | Red #FF0000 | Gray #575757 | Lite Gray #BBBBBB
Design: Swiss International — grid, hierarchy, negative space, zero decoration
"""

import math
import os
import re
import requests

# ── Brand Colors ────────────────────────────────────────────────────────────
BLACK     = '#000000'
WHITE     = '#FFFFFF'
RED       = '#FF0000'
GRAY      = '#575757'
LITE_GRAY = '#BBBBBB'

# ── Canvas ───────────────────────────────────────────────────────────────────
W      = 1920
H      = 1080
MARGIN = 80

# ── Font Families ─────────────────────────────────────────────────────────────
FONT_TITLE = 'Anton'   # ultra-bold condensed — headings, labels, chevrons
FONT_BODY  = 'Inter'   # humanist sans — body text, subtitles

# ── Base Font Sizes (at scale 1.0) ───────────────────────────────────────────
SIZES = {
    'h1':    88,   # main title
    'h2':    30,   # subtitle
    'label': 28,   # section / column / row labels
    'node':  26,   # node labels, cell headings
    'body':  20,   # body / description text
    'huge':  108,  # years, prices, big numbers
    'large': 68,   # mid-scale emphasis (pyramid levels, chevron inner text)
}

def fs(key, scale=1.0):
    return round(SIZES[key] * scale)

# ── Color Schemes ─────────────────────────────────────────────────────────────
SCHEMES = {
    'brand': {
        'bg':        WHITE,
        'primary':   BLACK,
        'accent':    RED,
        'secondary': GRAY,
        'muted':     LITE_GRAY,
        'on_dark':   WHITE,
        'on_light':  BLACK,
    },
    'bw': {
        'bg':        WHITE,
        'primary':   BLACK,
        'accent':    BLACK,
        'secondary': GRAY,
        'muted':     LITE_GRAY,
        'on_dark':   WHITE,
        'on_light':  BLACK,
    },
    'inverted': {
        'bg':        BLACK,
        'primary':   WHITE,
        'accent':    RED,
        'secondary': GRAY,
        'muted':     LITE_GRAY,
        'on_dark':   WHITE,
        'on_light':  WHITE,
    },
}

def get_scheme(name, settings=None):
    scheme = dict(SCHEMES.get(name, SCHEMES['brand']))
    if settings:
        if settings.get('accent_color_override'):
            scheme['accent'] = settings['accent_color_override']
        if settings.get('primary_color_override'):
            scheme['primary'] = settings['primary_color_override']
            # on_dark stays WHITE, on_light follows primary
            scheme['on_light'] = settings['primary_color_override']
    return scheme

# ── Chevron color sequence ────────────────────────────────────────────────────
def chevron_color(i, n, emphasis_i, scheme):
    """Return fill color for chevron at index i."""
    if i == emphasis_i:
        return scheme['accent']
    if i % 2 == 0:
        return scheme['primary']
    return scheme['secondary']

# ── Fonts / SVG Defs ──────────────────────────────────────────────────────────
FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts')

FONT_PATHS = {
    'Anton':      os.path.join(FONTS_DIR, 'Anton-Regular.ttf'),
    'Inter':      os.path.join(FONTS_DIR, 'Inter-Regular.ttf'),
    'Inter-Bold': os.path.join(FONTS_DIR, 'Inter-Bold.ttf'),
}

def download_font(name, url, path):
    if os.path.exists(path):
        return True
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        with open(path, 'wb') as f:
            f.write(r.content)
        print(f'[fonts] Downloaded {name}')
        return True
    except Exception as e:
        print(f'[fonts] Failed to download {name}: {e}')
        return False

def _gfont_ttf_url(family_css):
    """Fetch Google Fonts CSS and extract TTF URL using old UA trick."""
    try:
        url = f'https://fonts.googleapis.com/css?family={family_css}'
        r = requests.get(url,
                         headers={'User-Agent': 'Mozilla/4.0 (MSIE 6.0)'},
                         timeout=10)
        r.raise_for_status()
        urls = re.findall(r'url\((https://fonts\.gstatic[^)]+)\)', r.text)
        return urls[0] if urls else None
    except Exception:
        return None

def ensure_fonts():
    os.makedirs(FONTS_DIR, exist_ok=True)
    specs = [
        ('Anton',      'Anton',     FONT_PATHS['Anton']),
        ('Inter',      'Inter',     FONT_PATHS['Inter']),
        ('Inter-Bold', 'Inter:700', FONT_PATHS['Inter-Bold']),
    ]
    for name, family_css, path in specs:
        if not os.path.exists(path):
            url = _gfont_ttf_url(family_css)
            if url:
                download_font(name, url, path)

def _font_face(family, path, weight='400'):
    if not os.path.exists(path):
        return ''
    abs_path = os.path.abspath(path)
    return (
        f'@font-face {{'
        f'font-family:"{family}";'
        f'font-weight:{weight};'
        f'src:url("file://{abs_path}") format("truetype");'
        f'}}'
    )

def svg_style_export():
    """Font declarations for PNG export via CairoSVG (local file paths, CDATA-wrapped)."""
    css = (
        _font_face('Anton', FONT_PATHS['Anton'], '400') +
        _font_face('Inter', FONT_PATHS['Inter'], '400') +
        _font_face('Inter', FONT_PATHS['Inter-Bold'], '700')
    )
    if css:
        return f'<defs><style><![CDATA[{css}]]></style></defs>'
    return '<defs/>'

def svg_style_preview():
    """Font declarations for browser SVG preview (Google Fonts CDN, CDATA-wrapped)."""
    css = (
        '@import url("https://fonts.googleapis.com/css2?'
        'family=Anton&family=Inter:wght@400;700&display=swap");'
    )
    return f'<defs><style><![CDATA[{css}]]></style></defs>'

# ── SVG Root ─────────────────────────────────────────────────────────────────
def svg_open():
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    )

def svg_close():
    return '</svg>'

# ── Background ────────────────────────────────────────────────────────────────
def bg_rect(color):
    if not color or color == 'transparent':
        return ''
    return f'<rect width="{W}" height="{H}" fill="{color}"/>'

# ── Primitive Elements ────────────────────────────────────────────────────────
def _x(v):
    return f'{v:.2f}' if isinstance(v, float) else str(v)

def rect_el(x, y, w, h, fill, stroke=None, sw=1, rx=0):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return (
        f'<rect x="{_x(x)}" y="{_x(y)}" width="{_x(w)}" height="{_x(h)}" '
        f'fill="{fill}" rx="{rx}"{s}/>'
    )

def line_el(x1, y1, x2, y2, stroke, sw=2):
    return (
        f'<line x1="{_x(x1)}" y1="{_x(y1)}" x2="{_x(x2)}" y2="{_x(y2)}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )

def circle_el(cx, cy, r, fill, stroke=None, sw=2, dash=''):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<circle cx="{_x(cx)}" cy="{_x(cy)}" r="{_x(r)}" fill="{fill}"{s}{d}/>'

def polygon_el(points, fill, stroke=None, sw=1):
    pts = ' '.join(f'{_x(x)},{_x(y)}' for x, y in points)
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<polygon points="{pts}" fill="{fill}"{s}/>'

def path_el(d, fill='none', stroke=None, sw=2):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<path d="{d}" fill="{fill}"{s}/>'

# ── Text ──────────────────────────────────────────────────────────────────────
def _esc(s):
    return (str(s)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))

def text_el(x, y, content, size, fill, weight='400',
            anchor='middle', family=None, transform='', spacing=0):
    fam  = family or FONT_TITLE
    ls   = f' letter-spacing="{spacing}"' if spacing else ''
    tr   = f' transform="{transform}"' if transform else ''
    return (
        f'<text x="{_x(x)}" y="{_x(y)}" '
        f'font-family="{fam}, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" '
        f'dominant-baseline="central"{ls}{tr}>'
        f'{_esc(content)}</text>'
    )

def multiline_el(x, y, lines, size, fill, family=None,
                 anchor='middle', line_h=None, weight='400'):
    """Render a list of strings as vertically-centered multi-line text."""
    fam = family or FONT_BODY
    lh  = line_h or round(size * 1.45)
    total_h = (len(lines) - 1) * lh
    parts = []
    for i, ln in enumerate(lines):
        dy = i * lh - total_h / 2
        parts.append(
            f'<tspan x="{_x(x)}" dy="{dy:.1f}" '
            f'font-family="{fam}, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">'
            f'{_esc(ln)}</tspan>'
        )
    return f'<text x="{_x(x)}" y="{_x(y)}" dominant-baseline="central">{"".join(parts)}</text>'

def wrap(text_str, max_chars=38):
    """Word-wrap a string to max_chars per line."""
    if not text_str:
        return []
    words = text_str.split()
    lines, current = [], ''
    for word in words:
        test = (current + ' ' + word).strip()
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or ['']

# ── Chevron ───────────────────────────────────────────────────────────────────
def chevron_el(x, y, w, h, fill, is_first=False):
    """Chevron polygon. First chevron has a flat left edge; others have a notch."""
    nd = h * 0.40
    if is_first:
        pts = [
            (x,          y),
            (x + w - nd, y),
            (x + w,      y + h / 2),
            (x + w - nd, y + h),
            (x,          y + h),
        ]
    else:
        pts = [
            (x,          y),
            (x + w - nd, y),
            (x + w,      y + h / 2),
            (x + w - nd, y + h),
            (x,          y + h),
            (x + nd,     y + h / 2),
        ]
    return polygon_el(pts, fill)

# ── Arc Segment (donut / mind map) ───────────────────────────────────────────
def arc_segment_el(cx, cy, r_in, r_out, start_deg, end_deg, fill, gap=3):
    s = math.radians(start_deg + gap / 2)
    e = math.radians(end_deg   - gap / 2)
    span  = (end_deg - start_deg - gap)
    large = 1 if span > 180 else 0

    ox1, oy1 = cx + r_out * math.cos(s), cy + r_out * math.sin(s)
    ox2, oy2 = cx + r_out * math.cos(e), cy + r_out * math.sin(e)
    ix1, iy1 = cx + r_in  * math.cos(s), cy + r_in  * math.sin(s)
    ix2, iy2 = cx + r_in  * math.cos(e), cy + r_in  * math.sin(e)

    d = (f'M {ox1:.2f},{oy1:.2f} '
         f'A {r_out} {r_out} 0 {large} 1 {ox2:.2f},{oy2:.2f} '
         f'L {ix2:.2f},{iy2:.2f} '
         f'A {r_in} {r_in} 0 {large} 0 {ix1:.2f},{iy1:.2f} Z')
    return path_el(d, fill=fill)

# ── Arrow connector ───────────────────────────────────────────────────────────
def arrow_el(x1, y1, x2, y2, color, sw=3, head=14):
    """Draw a line with an arrowhead at (x2,y2)."""
    angle = math.atan2(y2 - y1, x2 - x1)
    ah    = head
    ax1 = x2 - ah * math.cos(angle - math.pi / 6)
    ay1 = y2 - ah * math.sin(angle - math.pi / 6)
    ax2 = x2 - ah * math.cos(angle + math.pi / 6)
    ay2 = y2 - ah * math.sin(angle + math.pi / 6)
    return (
        line_el(x1, y1, x2, y2, color, sw) +
        polygon_el([(x2, y2), (ax1, ay1), (ax2, ay2)], color)
    )

# ── Divider line ──────────────────────────────────────────────────────────────
def h_rule(x, y, w, color=LITE_GRAY, sw=1):
    return line_el(x, y, x + w, y, color, sw)

# ── Build complete SVG ────────────────────────────────────────────────────────
def build_svg(elements, bg='transparent', mode='preview'):
    """Assemble final SVG string. mode='preview' uses CDN fonts; mode='export' uses local."""
    defs = svg_style_preview() if mode == 'preview' else svg_style_export()
    parts = [svg_open(), defs]
    if bg and bg != 'transparent':
        parts.append(bg_rect(bg))
    parts.extend(e for e in elements if e)
    parts.append(svg_close())
    return '\n'.join(parts)


def get_mode(params):
    """Extract rendering mode from params."""
    return params.get('_mode', 'preview')
