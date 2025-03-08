"""
거래일 처리 관련 클래스
"""
from datetime import date
import pandas as pd
from typing import List

class TradingDateHandler:
    """거래일 처리 클래스"""
    def generate_trading_dates(self,
                             start_year: int,
                             start_month: int,
                             trade_day: int) -> List[pd.Timestamp]:
        """거래일 생성"""
        start_date = pd.Timestamp(date(start_year, start_month, trade_day))
        end_date = pd.Timestamp(date.today())
        
        dates = []
        current_date = start_date
        
        while current_date <= end_date:
            dates.append(current_date)
            current_date = current_date + pd.DateOffset(months=1)
        
        return dates
    
    def get_lookback_date(self,
                         current_date: pd.Timestamp,
                         lookback_months: int,
                         prices_df: pd.DataFrame) -> pd.Timestamp:
        """과거 기준일 찾기"""
        target_date = current_date - pd.DateOffset(months=lookback_months)
        return self._find_closest_trading_day(target_date, prices_df)
    
    def get_actual_trade_date(self,
                            target_date: pd.Timestamp,
                            prices_df: pd.DataFrame) -> pd.Timestamp:
        """실제 매매일 찾기 (주말인 경우 이전 금요일)"""
        if target_date in prices_df.index:
            return target_date
        
        for days_back in range(1, 3):
            prev_date = target_date - pd.Timedelta(days=days_back)
            if prev_date in prices_df.index:
                return prev_date
        
        return self._find_closest_trading_day(target_date, prices_df)
    
    def _find_closest_trading_day(self,
                                target_date: pd.Timestamp,
                                prices_df: pd.DataFrame) -> pd.Timestamp:
        """가장 가까운 거래일 찾기"""
        if target_date in prices_df.index:
            return target_date
        
        available_dates = prices_df.index[prices_df.index <= target_date]
        if len(available_dates) > 0:
            return available_dates[-1]
        
        return prices_df.index[0] 