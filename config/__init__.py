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

def load_monitor_config():
    """monitor_config.json 파일 로드"""
    config_path = Path(__file__).parent / "monitor_config.json"
    
    if not config_path.exists():
        # 기본 설정 반환
        return {
            "monitor_urls": [],
            "notification": {
                "discord": True,
                "telegram": False,
                "email": False
            }
        }
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_monitor_config(config):
    """monitor_config.json 파일 저장"""
    config_path = Path(__file__).parent / "monitor_config.json"
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)