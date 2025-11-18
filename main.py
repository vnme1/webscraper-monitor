"""
WebScraper Monitor - 메인 실행 파일
"""
from scrapers import ShopScraper
from storage import Database
from notifier import TelegramNotifier, DiscordNotifier  # ← Discord 추가
from scheduler import TaskScheduler
from config import settings
from utils import setup_logger

logger = setup_logger(__name__)

# 모니터링할 상품 URL 목록
MONITOR_URLS = [
    # 여기에 모니터링할 상품 URL을 추가하세요
    # "https://example.com/product/1",
    # "https://example.com/product/2",
    "https://www.coupang.com/vp/products/7654321098",  # 쿠팡 예시
    "https://smartstore.naver.com/cotini/products/5663284952",  # 네이버 쇼핑 예시
]

def monitor_prices():
    """가격 모니터링 메인 로직"""
    logger.info("=== 가격 모니터링 시작 ===")
    
    if not MONITOR_URLS:
        logger.warning("모니터링할 URL이 없습니다. MONITOR_URLS에 URL을 추가하세요.")
        return
    
    scraper = ShopScraper()
    
    try:
        with Database() as db:
            for url in MONITOR_URLS:
                try:
                    # 스크래핑
                    product_data = scraper.scrape(url)
                    
                    # 기존 상품 조회
                    existing_product = db.get_product(url)
                    
                    # DB에 저장
                    db.save_product(
                        url=product_data['url'],
                        name=product_data['name'],
                        price=product_data['price']
                    )
                    
                    # 가격 변동 시 알림
                    if existing_product and existing_product.price != product_data['price']:
                        if settings.ENABLE_TELEGRAM:
                            notifier = TelegramNotifier()
                            notifier.send_price_alert(product_data)
                        
                        if settings.ENABLE_DISCORD:
                            notifier = DiscordNotifier()
                            notifier.send_price_alert(product_data)

                except Exception as e:
                    logger.error(f"상품 처리 실패: {url} - {e}")
                    continue
        
        logger.info("=== 가격 모니터링 완료 ===\n")
        
    except Exception as e:
        logger.error(f"모니터링 중 오류 발생: {e}")
    finally:
        scraper.close()

def main():
    """메인 함수"""
    logger.info("WebScraper Monitor 시작")
    
    # 즉시 한 번 실행
    monitor_prices()
    
    # 스케줄러 시작
    scheduler = TaskScheduler()
    scheduler.add_job(monitor_prices)
    
    logger.info(f"스케줄러 시작 - 매 {settings.SCHEDULE_INTERVAL_MINUTES}분마다 실행")
    scheduler.start()

if __name__ == "__main__":
    main()
