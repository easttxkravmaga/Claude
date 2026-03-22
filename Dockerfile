FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/__init__.py backend/__init__.py
COPY backend/app.py backend/app.py

EXPOSE 8080

CMD exec gunicorn backend.app:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 60
