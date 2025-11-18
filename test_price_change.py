"""
가격 변동 알림 테스트
"""
from storage import Database
from notifier import DiscordNotifier
from config import settings
from utils import setup_logger

logger = setup_logger(__name__)

TEST_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def test_price_change():
    """가격 변동 시뮬레이션"""
    print("=== 가격 변동 테스트 ===\n")
    
    with Database() as db:
        # 기존 상품 조회
        product = db.get_product(TEST_URL)
        
        if not product:
            print("❌ 먼저 test_scraper.py를 실행하세요!")
            return
        
        print(f"현재 상품: {product.name}")
        print(f"현재 가격: {product.price:,.0f}원")
        
        # 가격 변경 (시뮬레이션)
        new_price = product.price - 5000  # 5,000원 할인!
        
        print(f"\n💰 가격 변동 시뮬레이션: {product.price:,.0f}원 → {new_price:,.0f}원")
        
        # DB 업데이트
        db.save_product(
            url=TEST_URL,
            name=product.name,
            price=new_price
        )
        
        # Discord 알림
        if settings.ENABLE_DISCORD:
            print("\n📢 Discord 알림 전송 중...")
            notifier = DiscordNotifier()
            notifier.send_price_alert({
                'name': product.name,
                'price': new_price,
                'url': TEST_URL
            })
            print("✅ Discord로 가격 변동 알림 전송 완료!")
            print("\nDiscord를 확인하세요! 🎉")

if __name__ == "__main__":
    test_price_change()