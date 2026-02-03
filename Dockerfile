FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD sh -c "\
    echo '==> Migratsiya bajarilmoqda...' && \
    python manage.py migrate --noinput && \
    echo '==> Admin yaratilmoqda...' && \
    python manage.py create_admin || true && \
    echo '==> Server ishga tushmoqda...' && \
    uvicorn config.asgi:application --host 0.0.0.0 --port 8000 \
"
