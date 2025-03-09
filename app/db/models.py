"""데이터베이스 모델"""
from sqlalchemy import Column, Integer, Float, Date, String, JSON
from app.db.database import Base

class Price(Base):
    """가격 데이터 모델"""
    __tablename__ = "prices"

    date = Column(Date, primary_key=True)
    ticker = Column(String, primary_key=True)
    price = Column(Float, nullable=False)

class Backtest(Base):
    """백테스트 결과 모델"""
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True)
    start_year = Column(Integer, nullable=False)
    start_month = Column(Integer, nullable=False)
    initial_investment = Column(Float, nullable=False)
    trade_day = Column(Integer, nullable=False)
    fee_rate = Column(Float, nullable=False)
    momentum_window = Column(Integer, nullable=False)
    nav_history = Column(JSON, nullable=False)
    weight_history = Column(JSON, nullable=False) 
    