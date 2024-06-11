from sqlalchemy.orm import Session

from . import models

def get_exchange_rate(db: Session, exchangeRate_id: int):
    return db.query(models.exchangeRate).filter(models.exchangeRate.id == exchangeRate_id).first()


def get_exchange_rates(db: Session, skip: int = 0, limit: int = 7):
    return db.query(models.exchangeRate).offset(skip).limit(limit).all()

