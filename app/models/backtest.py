"""
백테스트 관련 데이터 모델
pydantic으로 setting과 validation
"""
from typing import List, Tuple
from pydantic import BaseModel, Field

class BacktestInput(BaseModel):
    """백테스트 입력 파라미터"""
    start_year: int = Field(..., description="시작년도")
    start_month: int = Field(..., ge=1, le=12, description="시작월")
    initial_investment: float = Field(..., gt=0, description="초기 투자금액")
    trade_day: int = Field(..., ge=1, le=31, description="매월 매매일")
    fee_rate: float = Field(..., ge=0, lt=1, description="거래 수수료율")
    momentum_window: int = Field(..., gt=0, description="비중 계산 기준 개월 수")

class BacktestResult(BaseModel):
    """백테스트 결과"""
    total_return: float = Field(..., description="전체 기간 수익률")
    cagr: float = Field(..., description="연환산수익률")
    annual_volatility: float = Field(..., description="연 변동성")
    sharpe_ratio: float = Field(..., description="샤프 지수")
    max_drawdown: float = Field(..., description="최대 손실폭")
    last_weights: List[Tuple[str, float]] = Field(..., description="마지막 리밸런싱 비중")
    final_investment_value: float = Field(..., description="최종 투자금액") 