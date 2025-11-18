"""
Discord 알림 테스트
"""
from notifier import DiscordNotifier

def test_discord():
    """Discord 메시지 전송 테스트"""
    try:
        notifier = DiscordNotifier()
        
        message = """
🎉 **Discord 웹훅 연결 성공!**

✅ 웹훅이 정상적으로 작동합니다.
이제 가격 변동 알림을 받을 수 있어요!
"""
        
        result = notifier.send_message(message.strip())
        
        if result:
            print("✅ 메시지 전송 성공! Discord를 확인하세요.")
        else:
            print("❌ 메시지 전송 실패. secrets.json 설정을 확인하세요.")
            
    except FileNotFoundError:
        print("❌ secrets.json 파일이 없습니다!")
        print("\n다음 단계를 진행하세요:")
        print("1. Copy-Item config\\secrets.example.json config\\secrets.json")
        print("2. config/secrets.json 파일 확인")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("\n다음을 확인하세요:")
        print("1. config/secrets.json 파일이 존재하는지")
        print("2. discord.webhook_url이 올바른지")

if __name__ == "__main__":
    test_discord()