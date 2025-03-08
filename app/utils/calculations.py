"""
백테스트 계산 유틸리티 함수
"""
import numpy as np
from typing import Dict
import pandas as pd

def calculate_returns(prices: pd.Series) -> float:
    """수익률 계산"""
    return (prices.iloc[-1] / prices.iloc[0]) - 1

def calculate_momentum_weights(momentum_returns: pd.Series) -> pd.Series:
    """모멘텀 기반 비중 계산
    Args:
        momentum_returns: 각 자산의 momentum_window 기간 수익률
        
    Returns:
        각 자산의 목표 비중 (SPY, QQQ, GLD, BIL)
    
    Notes:
        1. TIP의 수익률이 음수이면 BIL 100%
        2. TIP의 수익률이 양수이면 SPY, QQQ, GLD 중 상위 2개에 각각 50% 배분
    """
    # 기본 비중을 0으로 초기화
    weights = pd.Series(0.0, index=['SPY', 'QQQ', 'GLD', 'BIL'])
    
    # TIP의 수익률이 음수인 경우 BIL에 100% 배분
    if momentum_returns.get('TIP', 0) < 0:
        weights['BIL'] = 1.0
        return weights
    
    # SPY, QQQ, GLD 중에서 상위 2개 선택
    investment_universe = ['SPY', 'QQQ', 'GLD']
    returns_universe = momentum_returns[investment_universe]
    top_2_assets = returns_universe.nlargest(2).index
    
    # 선택된 자산에 50%씩 배분
    weights[top_2_assets] = 0.5
    
    return weights

def calculate_nav_after_rebalancing(
    current_nav: float,
    old_weights: pd.Series,
    new_weights: pd.Series,
    fee_rate: float
) -> tuple[float, float]:
    """리밸런싱 후 NAV 계산
    Args:
        current_nav: 현재 NAV (매매 전)
        old_weights: 기존 비중
        new_weights: 새로운 비중
        fee_rate: 수수료율
    
    Returns:
        tuple[float, float]: (매매 전 NAV, 매매 후 NAV)
    
    Notes:
        - 목표NAV와 매매전NAV의 차이에 대해 수수료 계산
        - 비중이 증가하는 경우에만 수수료 계산
        - 소수점 8자리까지 유지
    """
    # 매매 전 NAV 계산
    pre_trade_nav = round(current_nav, 8)
    
    # 각 자산별 목표 NAV 계산
    target_nav = {ticker: pre_trade_nav * weight for ticker, weight in new_weights.items()}
    current_nav_by_asset = {ticker: pre_trade_nav * weight for ticker, weight in old_weights.items()}
    
    # 각 자산별 수수료 계산 (비중이 증가하는 경우에만)
    total_fee = 0.0
    for ticker in old_weights.index:
        weight_change = new_weights[ticker] - old_weights[ticker]
        if weight_change > 0:  # 비중이 증가하는 경우에만 수수료 계산
            nav_change = target_nav[ticker] - current_nav_by_asset[ticker]
            fee = nav_change * fee_rate
            total_fee += fee
    
    # 수수료를 차감한 NAV 반환
    post_trade_nav = round(pre_trade_nav - total_fee, 8)
    
    return pre_trade_nav, post_trade_nav

def calculate_statistics(nav_history: pd.Series) -> Dict:
    """백테스트 결과 통계 계산"""
    # 일간 수익률
    daily_returns = nav_history.pct_change().dropna()
    
    # 전체 기간 수익률
    total_return = (nav_history.iloc[-1] / nav_history.iloc[0]) - 1
    
    # 연환산수익률 (CAGR)
    years = (nav_history.index[-1] - nav_history.index[0]).days / 365
    cagr = (1 + total_return) ** (1/years) - 1
    
    # 연 변동성
    annual_volatility = daily_returns.std() * np.sqrt(252)
    
    # 샤프 지수 (무위험 수익률은 0으로 가정)
    sharpe_ratio = cagr / annual_volatility if annual_volatility != 0 else 0
    
    # 최대 손실폭 (MDD)
    cummax = nav_history.cummax()
    drawdown = (nav_history - cummax) / cummax
    max_drawdown = drawdown.min()
    
    return {
        "total_return": total_return,
        "cagr": cagr,
        "annual_volatility": annual_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown
    }

def is_trading_day(d: date) -> bool:
    """거래일 여부 확인 (주말 제외)"""
    return d.weekday() < 5  # 0=월요일, 5=토요일, 6=일요일

def get_next_trading_day(d: date) -> date:
    """다음 거래일 반환"""
    next_day = d + timedelta(days=1)
    while not is_trading_day(next_day):
        next_day += timedelta(days=1)
    return next_day 