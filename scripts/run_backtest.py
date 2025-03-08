"""백테스트 실행 스크립트"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.backtest import BacktestInput
from app.services.backtest_service import BacktestService
from app.core.constants import DATABASE_URL


def main():
    # DB 연결
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 백테스트 입력값 설정
        input_data = BacktestInput(
            start_year=2020,
            start_month=1,
            initial_investment=1000000,  # 100만원
            trade_day=15,               # 매월 15일
            fee_rate=0.001,            # 0.1%
            momentum_window=3           # 3개월
        )
        
        # 백테스트 실행
        service = BacktestService(db)
        result = service.run_backtest(input_data)
        
        print("\n=== 백테스트 결과 ===")
        print(f"전체 기간 수익률: {result.total_return:.2%}")
        print(f"연환산수익률 (CAGR): {result.cagr:.2%}")
        print(f"연 변동성: {result.annual_volatility:.2%}")
        print(f"샤프 지수: {result.sharpe_ratio:.2f}")
        print(f"최대 손실폭 (MDD): {result.max_drawdown:.2%}")
        
        print(f"\n초기 투자금액: {input_data.initial_investment:,.0f}원")
        print(f"최종 투자금액: {result.final_investment_value:,.0f}원")
        
        print("\n최종 자산 비중:")
        for ticker, weight in result.last_weights:
            if weight > 0:
                print(f"{ticker}: {weight:.2%}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main() 