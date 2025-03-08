"""
가격 데이터 Repository
"""
from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Float

from app.db.models import Price

class PriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_price(self, ticker: str, price_date: date, price: float) -> None:
        """
        가격 데이터를 저장합니다. 이미 존재하는 경우 업데이트합니다.
        
        Args:
            ticker (str): ETF 티커
            price_date (date): 가격 날짜
            price (float): 가격
        """
        # upsert (insert or update) 수행
        stmt = insert(Price).values(
            ticker=ticker,
            date=price_date,
            price=price
        )
        
        # 충돌 시 업데이트
        stmt = stmt.on_conflict_do_update(
            index_elements=['date', 'ticker'],
            set_=dict(price=stmt.excluded.price)
        )
        
        self.db.execute(stmt)
        self.db.commit()

    def get_prices(self, ticker: str, start_date: date, end_date: date) -> List[Price]:
        """
        특정 기간의 가격 데이터를 조회합니다.
        
        Args:
            ticker (str): ETF 티커
            start_date (date): 시작일
            end_date (date): 종료일
            
        Returns:
            List[Price]: 가격 데이터 리스트
        """
        # price를 float로 변환하여 조회
        return [
            Price(
                ticker=p.ticker,
                date=p.date,
                price=float(p.price)
            )
            for p in self.db.query(Price).filter(
                Price.ticker == ticker,
                Price.date >= start_date,
                Price.date <= end_date
            ).order_by(Price.date).all()
        ] 