from sqlalchemy import Column, Date, String, Numeric
from .database import Base

class Price(Base):
    __tablename__ = "prices"

    date = Column(Date, primary_key=True)
    ticker = Column(String(10), primary_key=True)
    price = Column(Numeric(13, 4)) 