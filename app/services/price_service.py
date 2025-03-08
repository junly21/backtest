"""
ETF 가격 관련 비즈니스 로직
"""
from datetime import date
from typing import Dict, List
from sqlalchemy.orm import Session

from app.core.constants import ETF_TICKERS
from app.crawlers.yahoo_finance import fetch_etf_price
from app.repositories.price_repository import PriceRepository

class PriceService:
    def __init__(self, db: Session):
        self.repository = PriceRepository(db)
        
    def update_etf_prices(self) -> List[Dict]:
        """
        모든 ETF의 가격 정보를 업데이트
        
        Returns:
            List[Dict]: 각 ETF의 업데이트 결과
            예: [
                {"ticker": "SPY", "success": True, "date": "2025-03-08", "price": 575.92},
                {"ticker": "QQQ", "success": False, "error": "가격 정보를 찾을 수 없습니다"}
            ]
        """
        results = []
        for ticker in ETF_TICKERS:
            result = self._update_single_etf_price(ticker)
            results.append(result)
        return results
            
    def _update_single_etf_price(self, ticker: str) -> Dict:
        """
        단일 ETF의 가격 정보 업데이트
        
        Args:
            ticker (str): ETF 티커
            
        Returns:
            Dict: 업데이트 결과
        """
        try:
            price_data = fetch_etf_price(ticker)
            if not price_data:
                return {
                    "ticker": ticker,
                    "success": False,
                    "error": "가격 데이터를 가져오지 못했습니다"
                }
                
            self.repository.save_price(
                ticker=ticker,
                price_date=price_data['date'],
                price=price_data['price']
            )
            
            return {
                "ticker": ticker,
                "success": True,
                "date": price_data['date'].isoformat(),
                "price": price_data['price']
            }
            
        except Exception as e:
            return {
                "ticker": ticker,
                "success": False,
                "error": str(e)
            } 