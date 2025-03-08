"""
ETF 가격 데이터 수집 배치
매일 미국 EST 18:00 (서머타임 미적용)에 실행됨
"""
from app.db.database import SessionLocal
from app.services.price_service import PriceService

def fetch_and_save_prices() -> None:
    """
    모든 ETF의 가격을 수집하여 DB에 저장
    """
    db = SessionLocal()
    try:
        service = PriceService(db)
        results = service.update_etf_prices()
        
        # 결과 출력
        for result in results:
            if result["success"]:
                print(f"Saved {result['ticker']}: {result['date']} - ${result['price']:.2f}")
            else:
                print(f"Failed to fetch {result['ticker']}: {result['error']}")
                
    finally:
        db.close()

def main():
    """
    배치 프로그램 메인 함수
    
    Note:
        이 스크립트는 매일 미국 EST 18:00 (서머타임 미적용)에 실행되도록
        crontab에 다음과 같이 등록됩니다:
        
        0 18 * * * /usr/bin/python /path/to/backtest/batch/daily_fetch.py
    """
    print("Starting daily ETF price fetch...")
    fetch_and_save_prices()
    print("Completed daily ETF price fetch.")

if __name__ == "__main__":
    main() 