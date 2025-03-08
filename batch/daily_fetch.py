"""
ETF 가격 데이터 수집 배치
매일 미국 EST 18:00 (서머타임 미적용)에 실행됨
"""
from app.core.constants import ETF_TICKERS
from app.crawlers.yahoo_finance import fetch_etf_price
from app.repositories.price_repository import PriceRepository
from app.db.database import SessionLocal

def fetch_and_save_prices():
    """
    모든 ETF의 가격을 수집하여 DB에 저장
    """
    db = SessionLocal()
    try:
        repository = PriceRepository(db)
        
        for ticker in ETF_TICKERS:
            result = fetch_etf_price(ticker)
            if result:
                repository.save_price(
                    ticker=ticker,
                    price_date=result['date'],
                    price=result['price']
                )
                print(f"Saved {ticker}: {result['date']} - ${result['price']:.2f}")
            else:
                print(f"Failed to fetch price for {ticker}")
                
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