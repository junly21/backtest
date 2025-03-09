"""백테스트 API 라우터"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.backtest import BacktestInput
from app.schemas.backtest import (
    BacktestResponse,
    BacktestListResponse,
    BacktestDetailResponse,
    BacktestDeleteResponse,
    BacktestOutput
)
from app.services.backtest_service import BacktestService
from app.repositories.backtest_repository import BacktestRepository

router = APIRouter()

@router.post("/backtest", response_model=BacktestResponse)
def create_backtest(input_data: BacktestInput, db: Session = Depends(get_db)):
    """백테스트를 실행하고 결과를 저장합니다."""
    service = BacktestService(db)
    repository = BacktestRepository(db)
    
    # 백테스트 실행
    result = service.run_backtest(input_data)
    
    # 결과 저장
    data_id = repository.save(input_data, result)
    
    return BacktestResponse(
        data_id=data_id,
        output={
            "total_return": result.total_return,
            "cagr": result.cagr,
            "vol": result.annual_volatility,
            "sharpe": result.sharpe_ratio,
            "mdd": result.max_drawdown
        },
        last_rebalance_weight=result.last_weights
    )

@router.get("/backtest", response_model=List[BacktestListResponse])
def list_backtests(db: Session = Depends(get_db)):
    """저장된 백테스트 결과 목록을 반환합니다."""
    repository = BacktestRepository(db)
    backtests = repository.get_all()
    
    return [
        BacktestListResponse(
            data_id=backtest.id,
            last_rebalance_weight=backtest.weight_history[-1].items()
        )
        for backtest in backtests
    ]

@router.get("/backtest/{data_id}", response_model=BacktestDetailResponse)
def get_backtest_detail(data_id: int, db: Session = Depends(get_db)):
    """특정 백테스트의 상세 정보를 반환합니다."""
    repository = BacktestRepository(db)
    service = BacktestService(db)
    
    backtest = repository.get_by_id(data_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    # 입력값 재구성
    input_data = BacktestInput(
        start_year=backtest.start_year,
        start_month=backtest.start_month,
        initial_investment=backtest.initial_investment,
        trade_day=backtest.trade_day,
        fee_rate=backtest.fee_rate,
        momentum_window=backtest.momentum_window
    )
    
    # 통계 재계산
    result = service.run_backtest(input_data)
    
    return BacktestDetailResponse(
        input=input_data,
        output=BacktestOutput(
            data_id=data_id,
            total_return=result.total_return,
            cagr=result.cagr,
            vol=result.annual_volatility,
            sharpe=result.sharpe_ratio,
            mdd=result.max_drawdown
        ),
        last_rebalance_weight=list(backtest.weight_history[-1].items())
    )

@router.delete("/backtest/{data_id}", response_model=BacktestDeleteResponse)
def delete_backtest(data_id: int, db: Session = Depends(get_db)):
    """특정 백테스트 결과를 삭제합니다."""
    repository = BacktestRepository(db)
    if not repository.delete(data_id):
        raise HTTPException(status_code=404, detail="Backtest not found")
    return BacktestDeleteResponse(data_id=data_id) 