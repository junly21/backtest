"""
포트폴리오 관리 클래스
"""
from typing import List, Dict, Tuple
import pandas as pd
from dataclasses import dataclass

@dataclass
class PortfolioStats:
    """포트폴리오 통계 데이터"""
    total_return: float
    cagr: float
    annual_volatility: float
    sharpe_ratio: float
    max_drawdown: float

class Portfolio:
    """포트폴리오 클래스"""
    def __init__(self, initial_nav: float = 1000.0):
        self.nav = initial_nav
        self.weights = pd.Series()
        self.nav_history: List[float] = []
        self.nav_dates: List[pd.Timestamp] = []
        self.weight_history: List[Dict[str, float]] = []
    
    def update_nav(self, new_nav: float) -> None:
        """NAV 업데이트"""
        self.nav = new_nav
        self.nav_history.append(new_nav)
    
    def update_weights(self, new_weights: pd.Series, date: pd.Timestamp) -> None:
        """비중 업데이트"""
        self.weights = new_weights
        self.weight_history.append(dict(new_weights))
        self.nav_dates.append(date)
    
    def get_nav_series(self) -> pd.Series:
        """NAV 시계열 데이터 반환"""
        return pd.Series(self.nav_history, index=self.nav_dates)
    
    def get_last_weights(self) -> List[Tuple[str, float]]:
        """마지막 리밸런싱 비중 반환"""
        if not self.weight_history:
            return []
        return list(self.weights.items())
    
    def get_weight_history(self) -> List[Dict[str, float]]:
        """전체 리밸런싱 비중 히스토리 반환"""
        return self.weight_history 