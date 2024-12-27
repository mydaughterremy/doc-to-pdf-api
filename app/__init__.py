# app/__init__.py
import os
from dotenv import load_dotenv
from flask import Flask
from app.utils import setup_logging

# 환경 변수 로드
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.api-pdf-converter.env')
load_dotenv(env_path)

# 디버깅: 환경 변수 출력
print("DEBUG: UPLOAD_URL =", os.getenv("UPLOAD_URL"))
print("DEBUG: CONVERT_URL =", os.getenv("CONVERT_URL"))
print("DEBUG: DOWNLOAD_URL =", os.getenv("DOWNLOAD_URL"))
print("DEBUG: DELETE_URL =", os.getenv("DELETE_URL"))
print("DEBUG: LOG_LEVEL =", os.getenv("LOG_LEVEL"))

# 로그 설정
log_dir = os.getenv("LOG_DIR", "./logs")
os.makedirs(log_dir, exist_ok=True)
setup_logging(log_dir)

from app.services import file_upload, file_convert, file_download, file_delete, file_process

def create_app():
    app = Flask(__name__)
    app.register_blueprint(file_upload.bp)
    app.register_blueprint(file_convert.bp)
    app.register_blueprint(file_download.bp)
    app.register_blueprint(file_delete.bp)
    app.register_blueprint(file_process.bp)
    return app