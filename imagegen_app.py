"""
Nano Banana Pro — AI Image Generation App
Run:  python imagegen_app.py
Open: http://localhost:5001
Requires: GEMINI_API_KEY environment variable
"""

import os
import base64
import traceback
import requests

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

MODELS = {
    'nano-banana': 'imagen-3.0-fast-generate-001',
    'nano-banana-pro': 'imagen-3.0-generate-002',
}

ASPECT_RATIOS = ['1:1', '16:9', '9:16', '4:3', '3:4']


@app.route('/')
def index():
    return render_template('imagegen.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(force=True)

    prompt = (data.get('prompt') or '').strip()
    if not prompt:
        return jsonify({'ok': False, 'error': 'Prompt is required.'}), 400

    api_key = data.get('api_key') or GEMINI_API_KEY
    if not api_key:
        return jsonify({'ok': False, 'error': 'No API key provided. Set GEMINI_API_KEY or enter it in the UI.'}), 400

    model_key = data.get('model', 'nano-banana-pro')
    model_id = MODELS.get(model_key, MODELS['nano-banana-pro'])

    negative_prompt = (data.get('negative_prompt') or '').strip()
    aspect_ratio = data.get('aspect_ratio', '1:1')
    if aspect_ratio not in ASPECT_RATIOS:
        aspect_ratio = '1:1'

    count = int(data.get('count', 1))
    count = max(1, min(4, count))

    style_suffix = data.get('style_suffix', '')
    if style_suffix:
        prompt = f"{prompt}, {style_suffix}"

    url = (
        f'https://generativelanguage.googleapis.com/v1beta/models/'
        f'{model_id}:predict?key={api_key}'
    )

    payload = {
        'instances': [{'prompt': prompt}],
        'parameters': {
            'sampleCount': count,
            'aspectRatio': aspect_ratio,
        }
    }
    if negative_prompt:
        payload['parameters']['negativePrompt'] = negative_prompt

    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        result = resp.json()
    except requests.exceptions.HTTPError as e:
        try:
            err_body = e.response.json()
            msg = err_body.get('error', {}).get('message', str(e))
        except Exception:
            msg = str(e)
        return jsonify({'ok': False, 'error': msg}), 502
    except Exception:
        return jsonify({'ok': False, 'error': traceback.format_exc()}), 500

    images = []
    for prediction in result.get('predictions', []):
        b64 = prediction.get('bytesBase64Encoded', '')
        mime = prediction.get('mimeType', 'image/jpeg')
        if b64:
            images.append({'data': b64, 'mime': mime})

    if not images:
        return jsonify({'ok': False, 'error': 'No images returned by API.'}), 502

    return jsonify({'ok': True, 'images': images, 'model': model_id})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f'\n  Nano Banana Pro Image Generator → http://localhost:{port}\n')
    app.run(debug=True, port=port, host='0.0.0.0')
