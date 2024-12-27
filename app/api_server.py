# app/api_server.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # .env 파일 불러오기
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.api-pdf-converter.env')
    load_dotenv(env_path)

    # 디버깅: 환경 변수 출력
    for key, value in os.environ.items():
        if key.startswith("UPLOAD") or key.startswith("CONVERT") or key.startswith("DOWNLOAD") or key.startswith("DELETE") or key == "FLASK_RUN_PORT":
            print(f"DEBUG: {key} = {value}")

    port = int(os.getenv("FLASK_RUN_PORT", 8000))
    app.run(host="0.0.0.0", port=port)