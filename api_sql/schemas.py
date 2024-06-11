from pydantic import BaseModel
from datetime import date

class exchangeRateBase(BaseModel):
    date: date
    currency: str
    rate: float

class exchangeRate(exchangeRateBase):
    id: int

    class Config:
        from_attributes = True
