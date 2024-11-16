# 베이스 이미지
FROM python:3.11-slim

# 작업 디렉터리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

ENV PYTHONPATH=/app

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
