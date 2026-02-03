# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Dependencies o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani ko'chirish
COPY . .

EXPOSE 8000

CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]