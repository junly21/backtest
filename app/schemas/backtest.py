"""백테스트 API 응답 스키마"""
from typing import List, Dict, Tuple
from pydantic import BaseModel

from app.models.backtest import BacktestInput

class BacktestOutput(BaseModel):
    """백테스트 결과 출력"""
    data_id: int
    total_return: float
    cagr: float
    vol: float
    sharpe: float
    mdd: float

class BacktestResponse(BaseModel):
    """백테스트 실행 응답"""
    data_id: int
    output: Dict[str, float]
    last_rebalance_weight: List[Tuple[str, float]]

class BacktestListResponse(BaseModel):
    """백테스트 목록 응답"""
    data_id: int
    last_rebalance_weight: List[Tuple[str, float]]

class BacktestDetailResponse(BaseModel):
    """백테스트 상세 정보 응답"""
    input: BacktestInput
    output: BacktestOutput
    last_rebalance_weight: List[Tuple[str, float]]

class BacktestDeleteResponse(BaseModel):
    """백테스트 삭제 응답"""
    data_id: int 