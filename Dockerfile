FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/

CMD ["sh", "-c", "gunicorn backend.app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60"]
