FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure backend is a proper Python package (empty __init__.py can be
# dropped by source-upload tools, which breaks "gunicorn backend.app:app").
RUN touch backend/__init__.py

CMD ["sh", "-c", "gunicorn backend.app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60"]
