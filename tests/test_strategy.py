import pytest
import pandas as pd
from app.trading.strategy import MomentumStrategy

def test_momentum_strategy_risk_off():
    """위험회피 시기(TIP 음수)의 자산 배분 테스트"""
    # 전략 초기화
    strategy = MomentumStrategy(['SPY', 'QQQ', 'GLD', 'BIL', 'TIP'])
    
    # 테스트 데이터 준비 (TIP 수익률 음수)
    prices = pd.DataFrame({
        'SPY': [100.0, 105.0],  # +5%
        'QQQ': [200.0, 220.0],  # +10%
        'GLD': [150.0, 157.5],  # +5%
        'BIL': [100.0, 100.1],  # +0.1%
        'TIP': [100.0, 99.0],   # -1% (음수)
    })
    prices.index = [pd.Timestamp('2024-01-01'), pd.Timestamp('2024-02-01')]
    
    # 비중 계산
    weights = strategy.calculate_weights(
        prices,
        current_date=pd.Timestamp('2024-02-01'),
        lookback_date=pd.Timestamp('2024-01-01')
    )
    
    # TIP이 음수이므로 BIL에 100% 배분되어야 함
    assert weights['BIL'] == 1.0
    assert weights['SPY'] == 0.0
    assert weights['QQQ'] == 0.0
    assert weights['GLD'] == 0.0
    assert weights['TIP'] == 0.0 