FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# app 디렉토리 복사
COPY app /app/app

# Flask 애플리케이션 실행
EXPOSE 5001
CMD ["python", "app/api_server.py"]
