from flask import Flask
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import json
import requests

app = Flask(__name__)

models.Base.metadata.create_all(bind=engine)

API_KEY= 'b4f0e87676794055821cdf83f5944ece'
URL_API=f'https://openexchangerates.org/api/latest.json?app_id={API_KEY}&symbols=EUR,USD,JPY,GBP'
currencies = ['EUR','USD','JPY','GBP']

def get_exchange_rates():
    response = requests.get(URL_API)
    if response.status_code == 200:
        data = response.json()
        return data.get('conversion_rates', {})
    else:
        return {}

@app.route('/')
def index():
    return get_exchange_rates()

if __name__ == '__main__':
    app.run(debug=True)
# class TestPrice(BaseModel):
#     currency: str
#     price: str

# def get_db(): 
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]

# @app.post("/price/", status_code=status.HTTP_201_CREATED)
# async def create_price(price: TestPrice, db: db_dependency):
#     db_price = models.Price(**price.dict())
#     db.add(db_price)
#     db.commit