"""
데이터베이스 연동 로직
"""
from typing import Optional
from datetime import datetime
from .models import SessionLocal, Product, PriceHistory, init_db
from utils import setup_logger

logger = setup_logger(__name__)

class Database:
    """데이터베이스 관리 클래스"""
    
    def __init__(self):
        init_db()
        self.session = SessionLocal()
    
    def save_product(self, url: str, name: str, price: float) -> Product:
        """상품 정보 저장 또는 업데이트"""
        product = self.session.query(Product).filter_by(url=url).first()
        
        if product:
            # 기존 상품 업데이트
            old_price = product.price
            product.price = price
            product.updated_at = datetime.now()
            
            # 가격 변동 이력 저장
            if old_price != price:
                self._save_price_history(product.id, price)
                logger.info(f"가격 변동: {name} {old_price}원 → {price}원")
        else:
            # 새 상품 저장
            product = Product(url=url, name=name, price=price)
            self.session.add(product)
            logger.info(f"새 상품 등록: {name} {price}원")
        
        self.session.commit()
        return product
    
    def _save_price_history(self, product_id: int, price: float):
        """가격 변동 이력 저장"""
        history = PriceHistory(product_id=product_id, price=price)
        self.session.add(history)
    
    def get_product(self, url: str) -> Optional[Product]:
        """URL로 상품 조회"""
        return self.session.query(Product).filter_by(url=url).first()
    
    def get_all_products(self):
        """모든 상품 조회"""
        return self.session.query(Product).all()
    
    def close(self):
        """세션 종료"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()