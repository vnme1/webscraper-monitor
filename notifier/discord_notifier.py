"""
Discord 알림 모듈
"""
import requests
from typing import Dict
from config import load_secrets
from utils import setup_logger

logger = setup_logger(__name__)

class DiscordNotifier:
    """Discord 메시지 전송"""
    
    def __init__(self):
        secrets = load_secrets()
        self.webhook_url = secrets['discord']['webhook_url']
    
    def send_message(self, message: str) -> bool:
        """
        Discord 메시지 전송
        
        Args:
            message: 전송할 메시지
            
        Returns:
            성공 여부
        """
        try:
            payload = {
                'content': message
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info("Discord 메시지 전송 성공")
            return True
            
        except Exception as e:
            logger.error(f"Discord 메시지 전송 실패: {e}")
            return False
    
    def send_price_alert(self, product_data: Dict) -> bool:
        """
        가격 변동 알림 전송
        
        Args:
            product_data: 상품 정보 딕셔너리
        """
        message = f"""
🔔 **가격 변동 알림**

📦 상품: {product_data['name']}
💰 가격: {product_data['price']:,.0f}원
🔗 링크: {product_data['url']}
"""
        return self.send_message(message.strip())