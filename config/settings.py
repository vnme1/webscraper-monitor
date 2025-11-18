"""
프로젝트 기본 설정
"""
import os
from pathlib import Path

# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent

# 데이터베이스 설정
DATABASE_URL = f"sqlite:///{BASE_DIR}/data/monitor.db"

# 스케줄러 설정
SCHEDULE_INTERVAL_MINUTES = 10  # 10분 실행

# 로그 설정
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "monitor.log"
LOG_LEVEL = "INFO"

# 스크래핑 설정
REQUEST_TIMEOUT = 10  # 초
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# 알림 설정
ENABLE_TELEGRAM = False
ENABLE_DISCORD = True  # ← 추가
ENABLE_SLACK = False
ENABLE_EMAIL = False

# 디렉토리 생성
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BASE_DIR / "data", exist_ok=True)