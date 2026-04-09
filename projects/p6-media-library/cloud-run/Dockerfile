FROM python:3.11-slim

# Pillow requires libjpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Cloud Run injects $PORT at runtime; gunicorn binds to it via sh -c form
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120"]
