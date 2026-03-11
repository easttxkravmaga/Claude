FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE $PORT

# Start gunicorn
CMD gunicorn backend.app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
