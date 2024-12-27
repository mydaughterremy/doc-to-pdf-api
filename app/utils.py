# app/utils.py
import logging
import os

def setup_logging(log_dir):
    # 환경 변수에서 로그 레벨 가져오기
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        filename=os.path.join(log_dir, 'app.log'),
        level=getattr(logging, log_level, logging.INFO),  # 기본값은 INFO
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.getLogger().addHandler(logging.StreamHandler())