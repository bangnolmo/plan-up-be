FROM python:3.11-slim

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app

COPY requirements.txt .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
