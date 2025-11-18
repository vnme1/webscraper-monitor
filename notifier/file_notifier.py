"""
파일 알림 모듈
"""
from datetime import datetime
from pathlib import Path
from typing import Dict
from utils import setup_logger

logger = setup_logger(__name__)

class FileNotifier:
    """파일로 알림 저장"""
    
    def __init__(self):
        self.alert_dir = Path("alerts")
        self.alert_dir.mkdir(exist_ok=True)
    
    def send_price_alert(self, product_data: Dict) -> bool:
        """
        가격 변동 알림을 파일로 저장
        
        Args:
            product_data: 상품 정보 딕셔너리
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.alert_dir / f"alert_{timestamp}.txt"
            
            content = f"""
[가격 변동 알림]
시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
상품: {product_data['name']}
가격: {product_data['price']:,.0f}원
링크: {product_data['url']}
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content.strip())
            
            logger.info(f"알림 파일 저장: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"파일 저장 실패: {e}")
            return False
```

---

## 📊 **추천 순서**

### 1️⃣ **초급 (제일 쉬움)**
```
알림 없이 실행 → 콘솔/로그만 확인
↓
스크래핑이 잘 되는지 먼저 확인
↓
나중에 알림 추가
```

### 2️⃣ **중급 (추천)**
```
Discord 웹훅 설정 (30초)
↓
알림 받으면서 테스트
↓
나중에 텔레그램 추가
```

### 3️⃣ **고급**
```
파일 저장 → Discord → 텔레그램 → 이메일
모두 동시에 작동 가능