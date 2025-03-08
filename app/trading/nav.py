"""
NAV 계산 관련 클래스
"""
import pandas as pd
import numpy as np
from typing import Dict
from .portfolio import Portfolio, PortfolioStats

class NavCalculator:
    """NAV 계산기"""
    def calculate_pre_trade_nav(self, 
                              portfolio: Portfolio,
                              prices: pd.DataFrame,
                              current_date: pd.Timestamp,
                              last_date: pd.Timestamp | None) -> float:
        """매매 전 NAV 계산"""
        if last_date is None:
            return portfolio.nav
        
        period_returns = prices.loc[current_date] / prices.loc[last_date]
        return portfolio.nav * (period_returns * portfolio.weights).sum()
    
    def calculate_post_trade_nav(self,
                               pre_trade_nav: float,
                               old_weights: pd.Series,
                               new_weights: pd.Series,
                               fee_rate: float) -> float:
        """매매 후 NAV 계산 (수수료 차감)"""
        # 비중 변화에 따른 수수료 계산
        weight_changes = abs(new_weights - old_weights)
        total_fee = pre_trade_nav * weight_changes.sum() * fee_rate
        
        return pre_trade_nav - total_fee
    
    def calculate_statistics(self, portfolio: Portfolio) -> PortfolioStats:
        """포트폴리오 통계 계산"""
        nav_series = portfolio.get_nav_series()
        daily_returns = nav_series.pct_change().dropna()
        
        # 전체 기간 수익률
        total_return = (nav_series.iloc[-1] / nav_series.iloc[0]) - 1
        
        # 연환산수익률 (CAGR)
        years = (nav_series.index[-1] - nav_series.index[0]).days / 365
        cagr = (1 + total_return) ** (1/years) - 1
        
        # 연 변동성
        annual_volatility = daily_returns.std() * np.sqrt(252)
        
        # 샤프 지수 (무위험 수익률은 0으로 가정)
        sharpe_ratio = cagr / annual_volatility if annual_volatility != 0 else 0
        
        # 최대 손실폭 (MDD)
        cummax = nav_series.cummax()
        drawdown = (nav_series - cummax) / cummax
        max_drawdown = drawdown.min()
        
        return PortfolioStats(
            total_return=total_return,
            cagr=cagr,
            annual_volatility=annual_volatility,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown
        ) 