from sqlalchemy.orm import Session

from . import models, schemas

def get_exchangeRate(db: Session, exchangeRate_id: int):
    return db.query(models.exchangeRate).filter(models.exchangeRate.id == exchangeRate_id).first()


def get_exchangeRates(db: Session, skip: int = 0, limit: int = 7):
    return db.query(models.exchangeRate).offset(skip).limit(limit).all()