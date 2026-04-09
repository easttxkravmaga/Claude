"""
ETKM P6 — B&W Image Conversion Microservice
Cloud Run Flask app: accepts image, converts to grayscale, returns JPEG.

Endpoints:
  POST /convert   — multipart/form-data with 'image' field
  GET  /health    — liveness check
"""

import io
import os
import logging

from flask import Flask, request, jsonify, send_file
from PIL import Image

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("etkm-bw-convert")

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB hard ceiling


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "etkm-bw-convert"})


@app.route("/convert", methods=["POST"])
def convert():
    """
    Accept an image via multipart/form-data (field: 'image').
    Return the grayscale JPEG as binary response.
    """
    if "image" not in request.files:
        return jsonify({"error": "No 'image' field in request"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    raw = file.read()
    if len(raw) > MAX_FILE_SIZE:
        return jsonify({"error": "File exceeds 25 MB limit"}), 413

    try:
        img = Image.open(io.BytesIO(raw))

        # Strip EXIF orientation so conversion is clean
        img = _apply_exif_orientation(img)

        # Convert to grayscale
        bw = img.convert("L")

        # Encode as JPEG
        buf = io.BytesIO()
        bw.save(buf, format="JPEG", quality=90)
        buf.seek(0)

        original_name = file.filename or "image.jpg"
        log.info("Converted %s (%d bytes) → grayscale JPEG", original_name, len(raw))

        return send_file(
            buf,
            mimetype="image/jpeg",
            as_attachment=False,
        )

    except Exception as exc:
        log.exception("Conversion failed for %s", file.filename)
        return jsonify({"error": str(exc)}), 500


def _apply_exif_orientation(img: Image.Image) -> Image.Image:
    """Rotate image according to EXIF orientation tag if present."""
    try:
        from PIL import ExifTags
        exif = img._getexif()
        if exif is None:
            return img
        orientation_key = next(
            (k for k, v in ExifTags.TAGS.items() if v == "Orientation"), None
        )
        if orientation_key and orientation_key in exif:
            orientation = exif[orientation_key]
            rotations = {3: 180, 6: 270, 8: 90}
            if orientation in rotations:
                img = img.rotate(rotations[orientation], expand=True)
    except Exception:
        pass  # Non-fatal — proceed without EXIF correction
    return img


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
