import os
from dotenv import load_dotenv

# .env 파일 로드
env_path = os.path.join(os.path.dirname(__file__), '../.api-pdf-converter.env')
load_dotenv(env_path)

print("UPLOAD_URL:", os.getenv('UPLOAD_URL'))
print("CONVERT_URL:", os.getenv('CONVERT_URL'))
print("DOWNLOAD_URL:", os.getenv('DOWNLOAD_URL'))
print("DELETE_URL:", os.getenv('DELETE_URL'))
