"""
HTML 파싱 유틸리티 함수
"""
from typing import Optional, List
from bs4 import BeautifulSoup

def extract_text(soup: BeautifulSoup, selectors: List[str], default: str = "") -> str:
    """
    여러 셀렉터를 시도하여 텍스트 추출
    
    Args:
        soup: BeautifulSoup 객체
        selectors: 시도할 CSS 셀렉터 리스트
        default: 기본값
        
    Returns:
        추출된 텍스트 또는 기본값
    """
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            return element.get_text(strip=True)
    return default

def extract_number(text: str) -> float:
    """
    텍스트에서 숫자만 추출
    
    Args:
        text: 입력 텍스트
        
    Returns:
        추출된 숫자 (float)
    """
    number_str = ''.join(filter(str.isdigit, text))
    return float(number_str) if number_str else 0.0

def extract_price(soup: BeautifulSoup, selectors: List[str]) -> float:
    """
    가격 정보 추출 및 숫자 변환
    
    Args:
        soup: BeautifulSoup 객체
        selectors: 시도할 CSS 셀렉터 리스트
        
    Returns:
        추출된 가격 (float)
    """
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            price_text = element.get_text(strip=True)
            return extract_number(price_text)
    return 0.0

def extract_attribute(soup: BeautifulSoup, selector: str, attribute: str) -> Optional[str]:
    """
    HTML 속성값 추출
    
    Args:
        soup: BeautifulSoup 객체
        selector: CSS 셀렉터
        attribute: 추출할 속성명
        
    Returns:
        속성값 또는 None
    """
    element = soup.select_one(selector)
    if element and element.has_attr(attribute):
        return element[attribute]
    return None

def clean_text(text: str) -> str:
    """
    텍스트 정리 (공백, 특수문자 제거)
    
    Args:
        text: 입력 텍스트
        
    Returns:
        정리된 텍스트
    """
    # 여러 공백을 하나로
    text = ' '.join(text.split())
    # 앞뒤 공백 제거
    text = text.strip()
    return text

def find_elements_by_text(soup: BeautifulSoup, tag: str, text: str) -> List:
    """
    텍스트로 요소 찾기
    
    Args:
        soup: BeautifulSoup 객체
        tag: HTML 태그명
        text: 검색할 텍스트
        
    Returns:
        찾은 요소 리스트
    """
    return soup.find_all(tag, string=lambda t: text in t if t else False)