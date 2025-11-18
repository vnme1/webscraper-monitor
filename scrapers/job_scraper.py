"""
채용 공고 스크래퍼
"""
from typing import Dict, List
from .base_scraper import BaseScraper
from utils import setup_logger

logger = setup_logger(__name__)

class JobScraper(BaseScraper):
    """채용 공고 스크래퍼"""
    
    def scrape(self, url: str) -> Dict:
        """
        채용 공고 정보 스크래핑
        
        Args:
            url: 채용 공고 페이지 URL
            
        Returns:
            채용 정보 딕셔너리 (title, company, location, url)
        """
        soup = self.fetch_page(url)
        
        title = self._extract_title(soup)
        company = self._extract_company(soup)
        location = self._extract_location(soup)
        
        logger.info(f"스크래핑 성공: {title} - {company}")
        
        return {
            'url': url,
            'title': title,
            'company': company,
            'location': location
        }
    
    def scrape_listings(self, search_url: str, keywords: List[str]) -> List[Dict]:
        """
        키워드로 채용 공고 목록 검색
        
        Args:
            search_url: 검색 페이지 URL
            keywords: 검색 키워드 리스트
            
        Returns:
            채용 공고 리스트
        """
        soup = self.fetch_page(search_url)
        job_listings = []
        
        # 공고 목록 추출 (사이트별로 셀렉터 수정 필요)
        job_elements = soup.select('div.job-listing')
        
        for element in job_elements:
            try:
                title = element.select_one('h2.job-title').get_text(strip=True)
                
                # 키워드 필터링
                if any(keyword.lower() in title.lower() for keyword in keywords):
                    job_url = element.select_one('a')['href']
                    company = element.select_one('span.company-name').get_text(strip=True)
                    
                    job_listings.append({
                        'title': title,
                        'company': company,
                        'url': job_url
                    })
            except Exception as e:
                logger.warning(f"공고 파싱 실패: {e}")
                continue
        
        logger.info(f"총 {len(job_listings)}개 공고 발견")
        return job_listings
    
    def _extract_title(self, soup) -> str:
        """채용 공고 제목 추출"""
        selectors = [
            'h1.job-title',
            'h1#job_title',
            'div.job-header h1',
            'h1'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "제목 없음"
    
    def _extract_company(self, soup) -> str:
        """회사명 추출"""
        selectors = [
            'span.company-name',
            'div.company-info',
            'a.company-link'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "회사명 없음"
    
    def _extract_location(self, soup) -> str:
        """근무 지역 추출"""
        selectors = [
            'span.job-location',
            'div.location',
            'span.address'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "지역 정보 없음"