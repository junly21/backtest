"""
투자 전략 관련 클래스
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import List

class WeightingStrategy(ABC):
    """투자 전략 인터페이스"""
    @abstractmethod
    def calculate_weights(self, prices: pd.DataFrame, 
                        current_date: pd.Timestamp,
                        lookback_date: pd.Timestamp) -> pd.Series:
        """
        투자 비중 계산
        
        Args:
            prices: 가격 데이터
            current_date: 현재 날짜
            lookback_date: 과거 기준 날짜
            
        Returns:
            각 자산의 목표 비중
        """
        pass

class MomentumStrategy(WeightingStrategy):
    """모멘텀 투자 전략"""
    def __init__(self, tickers: List[str]):
        self.tickers = tickers
        self.investment_universe = ['SPY', 'QQQ', 'GLD']
    
    def calculate_weights(self, prices: pd.DataFrame,
                        current_date: pd.Timestamp,
                        lookback_date: pd.Timestamp) -> pd.Series:
        """
        모멘텀 기반 비중 계산
        
        Notes:
            1. TIP의 수익률이 음수이면 BIL 100%
            2. TIP의 수익률이 양수이면 SPY, QQQ, GLD 중 상위 2개에 각각 50% 배분
        """
        # 기본 비중을 0으로 초기화
        weights = pd.Series(0.0, index=self.tickers)
        
        # 모멘텀 수익률 계산
        momentum_returns = (prices.loc[current_date] / prices.loc[lookback_date] - 1)
        
        # TIP의 수익률이 음수인 경우 BIL에 100% 배분
        if momentum_returns.get('TIP', 0) < 0:
            weights['BIL'] = 1.0
            return weights
        
        # SPY, QQQ, GLD 중에서 상위 2개 선택
        returns_universe = momentum_returns[self.investment_universe]
        top_2_assets = returns_universe.nlargest(2).index
        
        # 선택된 자산에 50%씩 배분
        weights[top_2_assets] = 0.5
        
        return weights 