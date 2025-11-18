"""
부동산 매물 스크래퍼
"""
from typing import Dict
from .base_scraper import BaseScraper
from utils import setup_logger

logger = setup_logger(__name__)

class RealEstateScraper(BaseScraper):
    """부동산 매물 스크래퍼"""
    
    def scrape(self, url: str) -> Dict:
        """
        부동산 매물 정보 스크래핑
        
        Args:
            url: 매물 페이지 URL
            
        Returns:
            매물 정보 딕셔너리 (title, price, location, area, url)
        """
        soup = self.fetch_page(url)
        
        title = self._extract_title(soup)
        price = self._extract_price(soup)
        location = self._extract_location(soup)
        area = self._extract_area(soup)
        property_type = self._extract_type(soup)
        
        logger.info(f"스크래핑 성공: {title} - {price}만원")
        
        return {
            'url': url,
            'title': title,
            'price': price,
            'location': location,
            'area': area,
            'type': property_type
        }
    
    def _extract_title(self, soup) -> str:
        """매물 제목 추출"""
        selectors = [
            'h1.property-title',
            'div.item-title',
            'h2.title',
            'h1'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "매물 제목 없음"
    
    def _extract_price(self, soup) -> float:
        """가격 추출 (만원 단위)"""
        selectors = [
            'span.property-price',
            'div.price-info',
            'strong.price'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # 숫자만 추출
                price = ''.join(filter(str.isdigit, price_text))
                if price:
                    return float(price)
        
        return 0.0
    
    def _extract_location(self, soup) -> str:
        """위치 정보 추출"""
        selectors = [
            'span.location',
            'div.address',
            'p.area-info'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "위치 정보 없음"
    
    def _extract_area(self, soup) -> str:
        """면적 정보 추출"""
        selectors = [
            'span.area',
            'div.area-info',
            'span.size'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "면적 정보 없음"
    
    def _extract_type(self, soup) -> str:
        """매물 유형 추출 (아파트, 빌라, 오피스텔 등)"""
        selectors = [
            'span.property-type',
            'div.type-info',
            'span.category'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "유형 정보 없음"