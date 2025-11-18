"""
데이터베이스 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

Base = declarative_base()

class Product(Base):
    """상품 정보 모델"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"

class PriceHistory(Base):
    """가격 변동 이력"""
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<PriceHistory(product_id={self.product_id}, price={self.price})>"

# 데이터베이스 엔진 생성
engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """데이터베이스 초기화"""
    Base.metadata.create_all(bind=engine)