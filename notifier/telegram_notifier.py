"""
텔레그램 알림 모듈
"""
import requests
from typing import Dict
from config import load_secrets
from utils import setup_logger

logger = setup_logger(__name__)

class TelegramNotifier:
    """텔레그램 메시지 전송"""
    
    def __init__(self):
        secrets = load_secrets()
        self.bot_token = secrets['telegram']['bot_token']
        self.chat_id = secrets['telegram']['chat_id']
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message: str) -> bool:
        """
        텔레그램 메시지 전송
        
        Args:
            message: 전송할 메시지
            
        Returns:
            성공 여부
        """
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            logger.info("텔레그램 메시지 전송 성공")
            return True
            
        except Exception as e:
            logger.error(f"텔레그램 메시지 전송 실패: {e}")
            return False
    
    def send_price_alert(self, product_data: Dict) -> bool:
        """
        가격 변동 알림 전송
        
        Args:
            product_data: 상품 정보 딕셔너리
        """
        message = f"""
🔔 <b>가격 변동 알림</b>

📦 상품: {product_data['name']}
💰 가격: {product_data['price']:,.0f}원
🔗 링크: {product_data['url']}
"""
        return self.send_message(message.strip())