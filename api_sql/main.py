from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from .database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/exchange_rates/{rate_id}", response_model=schemas.exchangeRate)
def read_exchange_rate(exchangeRate_id: int, db: Session = Depends(get_db)):
    db_rate = crud.get_exchange_rate(db, exchangeRate_id)
    if db_rate is None:
        raise HTTPException(status_code=404, detail="Exchange rate not found")
    return db_rate

@app.get("/exchange_rates/", response_model=List[schemas.exchangeRate])
def read_exchange_rates(skip: int = 0, limit: int = 7, db: Session = Depends(get_db)):
    exchange_rates = crud.get_exchange_rates(db, skip=skip, limit=limit)
    return exchange_rates

