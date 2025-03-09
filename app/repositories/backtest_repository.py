"""백테스트 Repository"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import Backtest
from app.models.backtest import BacktestInput, BacktestResult

class BacktestRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, input_data: BacktestInput, result: BacktestResult) -> int:
        """백테스트 결과 저장"""
        backtest = Backtest(
            start_year=input_data.start_year,
            start_month=input_data.start_month,
            initial_investment=input_data.initial_investment,
            trade_day=input_data.trade_day,
            fee_rate=input_data.fee_rate,
            momentum_window=input_data.momentum_window,
            nav_history={"values": result.nav_values, "dates": result.nav_dates},
            weight_history=result.weight_history
        )
        self.db.add(backtest)
        self.db.commit()
        self.db.refresh(backtest)
        return backtest.id

    def get_all(self) -> List[Backtest]:
        """모든 백테스트 결과 조회"""
        return self.db.query(Backtest).all()

    def get_by_id(self, backtest_id: int) -> Optional[Backtest]:
        """특정 백테스트 결과 조회"""
        return self.db.query(Backtest).filter(Backtest.id == backtest_id).first()

    def delete(self, backtest_id: int) -> bool:
        """백테스트 결과 삭제"""
        backtest = self.get_by_id(backtest_id)
        if not backtest:
            return False
        self.db.delete(backtest)
        self.db.commit()
        return True 