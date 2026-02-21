"""
ETKM Visual Aide — Flask Application
Run:  python app.py
Open: http://localhost:5000
"""

import io
import os
import json
import traceback

from flask import Flask, render_template, request, jsonify, send_file

from generators import generate_diagram, LABELS
from generators.base import ensure_fonts, build_svg

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ── Font setup on startup ─────────────────────────────────────────────────────
@app.before_request
def _setup():
    app.before_request_funcs[None].remove(_setup)
    print('[ETKM] Checking fonts...')
    try:
        ensure_fonts()
        print('[ETKM] Fonts ready.')
    except Exception as e:
        print(f'[ETKM] Font setup warning: {e}')


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html', diagram_labels=LABELS)


@app.route('/preview', methods=['POST'])
def preview():
    """Return SVG string for browser preview."""
    try:
        params = request.get_json(force=True)
        params.setdefault('settings', {})
        svg = generate_diagram(params)
        return jsonify({'ok': True, 'svg': svg})
    except Exception:
        return jsonify({'ok': False, 'error': traceback.format_exc()}), 500


@app.route('/export', methods=['POST'])
def export():
    """Return transparent PNG via CairoSVG, SVG fallback if Cairo unavailable."""
    params = request.get_json(force=True)
    params.setdefault('settings', {})
    params['_mode'] = 'export'
    try:
        import cairosvg
        svg = generate_diagram(params)
        png_bytes = cairosvg.svg2png(
            bytestring=svg.encode('utf-8'),
            background_color=None,
            dpi=144,
        )
        buf = io.BytesIO(png_bytes)
        buf.seek(0)
        diagram_type = params.get('diagram_type', 'visual')
        title_slug   = params.get('title', diagram_type)[:30].replace(' ', '_').lower()
        filename     = f'etkm_{title_slug}.png'
        return send_file(buf, mimetype='image/png',
                         as_attachment=True,
                         download_name=filename)
    except (ImportError, OSError):
        # Cairo native library not installed — fall back to SVG download
        return _export_svg_fallback(params)
    except Exception:
        return jsonify({'ok': False, 'error': traceback.format_exc()}), 500


def _export_svg_fallback(params):
    """Serve SVG when cairosvg is unavailable."""
    try:
        svg = generate_diagram(params)
        buf = io.BytesIO(svg.encode('utf-8'))
        buf.seek(0)
        return send_file(buf, mimetype='image/svg+xml',
                         as_attachment=True,
                         download_name='etkm_visual.svg')
    except Exception:
        return jsonify({'ok': False, 'error': 'Export failed.'}), 500


@app.route('/diagram_types')
def diagram_types():
    return jsonify(LABELS)


# ── Dev server ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f'\n  ETKM Visual Aide running → http://localhost:{port}\n')
    app.run(debug=True, port=port, host='0.0.0.0')
