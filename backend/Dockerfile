FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh","-c","until python -c \"import socket; socket.create_connection(('mysql',3306),2).close()\"; do echo 'Waiting for MySQL...'; sleep 2; done; alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]