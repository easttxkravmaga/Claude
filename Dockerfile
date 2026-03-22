FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/

CMD exec gunicorn backend.app:app --bind :$PORT --workers 2 --timeout 60
