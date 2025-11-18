"""
이메일 알림 모듈
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from config import load_secrets
from utils import setup_logger

logger = setup_logger(__name__)

class EmailNotifier:
    """이메일 메시지 전송"""
    
    def __init__(self):
        secrets = load_secrets()
        email_config = secrets['email']
        
        self.smtp_server = email_config['smtp_server']
        self.smtp_port = email_config['smtp_port']
        self.sender_email = email_config['sender_email']
        self.sender_password = email_config['sender_password']
        self.receiver_email = email_config['receiver_email']
    
    def send_message(self, subject: str, body: str) -> bool:
        """
        이메일 전송
        
        Args:
            subject: 제목
            body: 본문
            
        Returns:
            성공 여부
        """
        try:
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = self.receiver_email
            message['Subject'] = subject
            
            message.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info("이메일 전송 성공")
            return True
            
        except Exception as e:
            logger.error(f"이메일 전송 실패: {e}")
            return False
    
    def send_price_alert(self, product_data: Dict) -> bool:
        """
        가격 변동 알림 이메일 전송
        
        Args:
            product_data: 상품 정보 딕셔너리
        """
        subject = "🔔 가격 변동 알림"
        
        body = f"""
가격 변동이 감지되었습니다.

상품명: {product_data['name']}
가격: {product_data['price']:,.0f}원
링크: {product_data['url']}

---
WebScraper Monitor
"""
        return self.send_message(subject, body.strip())