"""
Config 패키지 초기화
"""
import json
from pathlib import Path

def load_secrets():
    """secrets.json 파일 로드"""
    secrets_path = Path(__file__).parent / "secrets.json"
    
    if not secrets_path.exists():
        raise FileNotFoundError(
            f"secrets.json 파일이 없습니다. "
            f"secrets.example.json을 복사하여 secrets.json을 생성하세요."
        )
    
    with open(secrets_path, 'r', encoding='utf-8') as f:
        return json.load(f)