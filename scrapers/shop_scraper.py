"""
쇼핑몰 스크래퍼
"""
from typing import Dict
from .base_scraper import BaseScraper
from utils import setup_logger

logger = setup_logger(__name__)

class ShopScraper(BaseScraper):
    """쇼핑몰 상품 가격 스크래퍼"""
    
    def scrape(self, url: str) -> Dict:
        """
        쇼핑몰 상품 정보 스크래핑
        
        Args:
            url: 상품 페이지 URL
            
        Returns:
            상품 정보 딕셔너리 (name, price, url)
        """
        soup = self.fetch_page(url)
        
        # 예시: 일반적인 쇼핑몰 구조
        # 실제로는 각 사이트별로 셀렉터를 조정해야 함
        name = self._extract_name(soup)
        price = self._extract_price(soup)
        
        logger.info(f"스크래핑 성공: {name} - {price}원")
        
        return {
            'url': url,
            'name': name,
            'price': price
        }
    
    def _extract_name(self, soup) -> str:
        """상품명 추출"""
        # 여러 가능한 셀렉터 시도
        selectors = [
            'h1.product-title',
            'h1#product_title',
            'div.product-name',
            'h1'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "상품명 없음"
    
    def _extract_price(self, soup) -> float:
        """가격 추출"""
        # 여러 가능한 셀렉터 시도
        selectors = [
            'span.product-price',
            'span#product_price',
            'div.price',
            'strong.price'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # 숫자만 추출 (쉼표, 원 등 제거)
                price = ''.join(filter(str.isdigit, price_text))
                if price:
                    return float(price)
        
        return 0.0