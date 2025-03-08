"""
가격 데이터 Repository
"""
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

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