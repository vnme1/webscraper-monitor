"""
기본 스크래퍼 클래스
"""
from abc import ABC, abstractmethod
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from config import settings
from utils import setup_logger

logger = setup_logger(__name__)

class BaseScraper(ABC):
    """모든 스크래퍼의 기본 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': settings.USER_AGENT})
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """웹 페이지 가져오기"""
        try:
            response = self.session.get(url, timeout=settings.REQUEST_TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logger.error(f"페이지 가져오기 실패: {url} - {e}")
            raise
    
    @abstractmethod
    def scrape(self, url: str) -> Dict:
        """스크래핑 메인 로직 (각 스크래퍼에서 구현)"""
        pass
    
    def scrape_multiple(self, urls: List[str]) -> List[Dict]:
        """여러 URL 스크래핑"""
        results = []
        for url in urls:
            try:
                result = self.scrape(url)
                results.append(result)
            except Exception as e:
                logger.error(f"스크래핑 실패: {url} - {e}")
        return results
    
    def close(self):
        """세션 종료"""
        self.session.close()