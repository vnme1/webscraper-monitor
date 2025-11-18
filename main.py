"""
WebScraper Monitor - 메인 실행 파일
"""
import argparse
from scrapers import ShopScraper
from storage import Database
from notifier import TelegramNotifier, DiscordNotifier
from scheduler import TaskScheduler
from config import settings
from utils import setup_logger

logger = setup_logger(__name__)

# 모니터링할 상품 URL 목록
MONITOR_URLS = [
    # 여기에 모니터링할 상품 URL을 추가하세요
    # "https://example.com/product/1",
]

# 가격 임계값 설정 (이 가격 이하일 때만 알림)
PRICE_THRESHOLD = {}  # URL: 최대가격

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
                    should_notify = False
                    
                    if existing_product and existing_product.price != product_data['price']:
                        # 가격 임계값 체크
                        if url in PRICE_THRESHOLD:
                            threshold = PRICE_THRESHOLD[url]
                            if product_data['price'] <= threshold:
                                logger.info(f"💰 목표 가격 달성! {product_data['price']:,.0f}원 <= {threshold:,.0f}원")
                                should_notify = True
                            else:
                                logger.info(f"가격 변동 있으나 임계값 미달성: {product_data['price']:,.0f}원 > {threshold:,.0f}원")
                        else:
                            # 임계값 설정 안 되어 있으면 모든 변동 알림
                            should_notify = True
                        
                        if should_notify:
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
    # 커맨드 라인 인자 파싱
    parser = argparse.ArgumentParser(
        description='웹 스크래핑 기반 가격 모니터링 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python main.py --interval 30                    # 30분마다 실행
  python main.py --once                           # 한 번만 실행
  python main.py --interval 10 --threshold 50000  # 10분마다, 50000원 이하만 알림
        """
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=settings.SCHEDULE_INTERVAL_MINUTES,
        help=f'모니터링 간격 (분) (기본값: {settings.SCHEDULE_INTERVAL_MINUTES})'
    )
    
    parser.add_argument(
        '--once',
        action='store_true',
        help='한 번만 실행하고 종료'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        help='가격 임계값 (이 가격 이하일 때만 알림)'
    )
    
    args = parser.parse_args()
    
    # 가격 임계값 설정
    if args.threshold:
        logger.info(f"💰 가격 임계값 설정: {args.threshold:,.0f}원 이하일 때만 알림")
        for url in MONITOR_URLS:
            PRICE_THRESHOLD[url] = args.threshold
    
    logger.info("WebScraper Monitor 시작")
    
    # 즉시 한 번 실행
    monitor_prices()
    
    # --once 옵션이면 여기서 종료
    if args.once:
        logger.info("한 번 실행 모드 - 프로그램 종료")
        return
    
    # 스케줄러 시작
    scheduler = TaskScheduler()
    scheduler.add_job(monitor_prices, interval_minutes=args.interval)
    
    logger.info(f"스케줄러 시작 - 매 {args.interval}분마다 실행")
    logger.info("종료하려면 Ctrl+C를 누르세요")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("\n프로그램을 종료합니다...")
        scheduler.scheduler.shutdown(wait=False)
        logger.info("종료 완료!")

if __name__ == "__main__":
    main()