"""
백테스트 계산 서비스
"""
from datetime import date
import pandas as pd
from sqlalchemy.orm import Session

from app.models.backtest import BacktestInput, BacktestResult
from app.repositories.price_repository import PriceRepository
from app.core.constants import ETF_TICKERS
from app.trading.portfolio import Portfolio
from app.trading.nav import NavCalculator
from app.trading.strategy import MomentumStrategy
from app.trading.dates import TradingDateHandler

class BacktestService:
    """백테스트 서비스"""
    def __init__(self, db: Session):
        self.price_repository = PriceRepository(db)
        self.nav_calculator = NavCalculator()
        self.date_handler = TradingDateHandler()
        self.strategy = MomentumStrategy(ETF_TICKERS)
    
    def run_backtest(self, input_data: BacktestInput) -> BacktestResult:
        """백테스트 실행"""
        # 거래일 생성
        trading_dates = self.date_handler.generate_trading_dates(
            input_data.start_year,
            input_data.start_month,
            input_data.trade_day
        )
        
        # 가격 데이터 로드
        earliest_date = trading_dates[0] - pd.DateOffset(months=input_data.momentum_window)
        prices_df = self._load_price_data(earliest_date, pd.Timestamp(date.today()))
        if prices_df.empty:
            raise ValueError("가격 데이터가 없습니다.")
        
        # 포트폴리오 초기화
        portfolio = Portfolio()
        last_trade_date = None
        
        # 매월 리밸런싱 수행
        for target_date in trading_dates:
            # 실제 거래일 찾기
            trade_date = self.date_handler.get_actual_trade_date(target_date, prices_df)
            
            # 매매 전 NAV 계산
            pre_trade_nav = self.nav_calculator.calculate_pre_trade_nav(
                portfolio, prices_df, trade_date, last_trade_date
            )
            
            # 모멘텀 계산을 위한 과거 날짜 찾기
            lookback_date = self.date_handler.get_lookback_date(
                trade_date, input_data.momentum_window, prices_df
            )
            
            # 새로운 비중 계산
            new_weights = self.strategy.calculate_weights(
                prices_df, trade_date, lookback_date
            )
            
            # 매매 후 NAV 계산
            post_trade_nav = self.nav_calculator.calculate_post_trade_nav(
                pre_trade_nav, portfolio.weights, new_weights, input_data.fee_rate
            )
            
            # 포트폴리오 업데이트
            portfolio.update_nav(post_trade_nav)
            portfolio.update_weights(new_weights, target_date)
            last_trade_date = trade_date
        
        # 통계 계산
        stats = self.nav_calculator.calculate_statistics(portfolio)
        
        # 최종 투자금액 계산
        final_investment_value = round(
            (portfolio.nav / 1000.0) * input_data.initial_investment, 0
        )
        
        return BacktestResult(
            total_return=stats.total_return,
            cagr=stats.cagr,
            annual_volatility=stats.annual_volatility,
            sharpe_ratio=stats.sharpe_ratio,
            max_drawdown=stats.max_drawdown,
            last_weights=portfolio.get_last_weights(),
            final_investment_value=final_investment_value
        )
    
    def _load_price_data(self, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
        """가격 데이터 로드"""
        prices_dict = {}
        for ticker in ETF_TICKERS:
            prices = self.price_repository.get_prices(ticker, start_date.date(), end_date.date())
            if prices:
                prices_dict[ticker] = pd.Series(
                    [p.price for p in prices],
                    index=[pd.Timestamp(p.date) for p in prices]
                )
        
        return pd.DataFrame(prices_dict) 