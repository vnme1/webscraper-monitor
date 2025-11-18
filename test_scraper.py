"""
스크래핑 테스트
"""
from scrapers import ShopScraper
from storage import Database
from notifier import DiscordNotifier
from config import settings
from utils import setup_logger

logger = setup_logger(__name__)

# 테스트할 URL
TEST_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def test_scraping():
    """스크래핑 및 알림 테스트"""
    logger.info("=== 스크래핑 테스트 시작 ===")
    
    scraper = ShopScraper()
    
    try:
        # 1. 스크래핑
        print("\n1️⃣ 웹페이지 스크래핑 중...")
        product_data = scraper.scrape(TEST_URL)
        
        print(f"✅ 상품명: {product_data['name']}")
        print(f"✅ 가격: {product_data['price']:,.0f}원")
        print(f"✅ URL: {product_data['url']}")
        
        # 2. 데이터베이스 저장
        print("\n2️⃣ 데이터베이스에 저장 중...")
        with Database() as db:
            existing_product = db.get_product(TEST_URL)
            
            if existing_product:
                print(f"   기존 가격: {existing_product.price:,.0f}원")
            
            db.save_product(
                url=product_data['url'],
                name=product_data['name'],
                price=product_data['price']
            )
            print("✅ 데이터베이스 저장 완료")
            
            # 3. 가격 변동 시 알림
            if existing_product and existing_product.price != product_data['price']:
                print("\n3️⃣ 가격 변동 감지! Discord 알림 전송 중...")
                if settings.ENABLE_DISCORD:
                    notifier = DiscordNotifier()
                    notifier.send_price_alert(product_data)
                    print("✅ Discord 알림 전송 완료")
            else:
                print("\n3️⃣ 가격 변동 없음 (첫 실행이거나 가격이 동일)")
        
        print("\n=== 테스트 완료! ===\n")
        
    except Exception as e:
        logger.error(f"테스트 중 오류: {e}")
        print(f"\n❌ 오류 발생: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    test_scraping()