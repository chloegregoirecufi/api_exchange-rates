from sqlalchemy import  Column, Float, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rate"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    currency = Column(String)
    rate = Column(Float)
