from sqlalchemy import Column, Date, String, Integer
from database import Base

class Date(Base):
    __tablename__ = 'date'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)

class Price(Base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String(3))
    price = Column(String(10))
