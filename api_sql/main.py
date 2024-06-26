import select
from fastapi.responses import HTMLResponse
import pandas as pd
import os
import httpx
from fastapi import FastAPI, HTTPException, Request,  BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models
from .database import SessionLocal, engine
from datetime import datetime, timedelta
from .models import ExchangeRate
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = ["http://127.0.0.1:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"]
    )
   

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../app_exchange_rate/templates'))

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), '../app_exchange_rate/static')), name="static")

API_KEY="b4f0e87676794055821cdf83f5944ece"
BASE_URL = f'https://openexchangerates.org/api/latest.json?api_id={API_KEY}&symbols=EUR,USD,JPY,GBP'
currencies = ['EUR', 'USD', 'JPY', 'GBP']

async def fetch_latest_exchange_rates():
    params = {
        "app_id": API_KEY,
        "symbols": ",".join(currencies)
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()


def store_daily_exchange_rates(db: Session):
    data = httpx.get(BASE_URL, params={"app_id": API_KEY, "symbols": ",".join(currencies)}).json()
    rates = data.get("rates", {})
    date = datetime.now().date()

    for currency, rate in rates.items():
        db_rate = ExchangeRate(date=date, currency=currency, rate=rate)
        db.merge(db_rate)  # Use merge to insert or update
    db.commit()


#verifie si les résultats sont disponible pour chaque date demandée. Si les résultats existent, 
#ils sont ajoutés à la,list "exchange_data"
#si aucune donnée n'est trouvée =, une error HTTP 404 est levé


async def get_data():
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    exchange_data = []

    db = SessionLocal()
    try:
        for date in dates:
            query = select(ExchangeRate).filter(ExchangeRate.date == date)
            result = db.execute(query).scalars().all()
            if result:
                rates = {'date': date}  # Initialisation du dictionnaire avec la date
                for record in result:
                    rates[record.currency] = record.rate  # Ajout de chaque devise avec son taux
                exchange_data.append(rates) 
                # rates = {record.currency: record.rate for record in result}
                # date_obj = datetime.strptime(date, '%Y-%m-%d') 
                # rates['date'] = date_obj.strftime('%Y-%m-%d')
                # exchange_data.append(rates)
    finally:
        db.close()

    if not exchange_data:
        raise HTTPException(status_code=404, detail="No exchange rate data available")

    df = pd.DataFrame(exchange_data)
    print(f"DataFrame structure:\n{df}")
    return df



#BackgroundTasks est use for execut funtction 'store_daily_exchange_rates en tache de fond
# lorsque la route est appelé. Cela permet d'exécuter la maj des taux de change en arrière plan
#sans bloquer la réponse de la route
@app.get('/home')
async def index(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(store_daily_exchange_rates, SessionLocal())
    df = await get_data() 

     # Extraction des données pour le message
    message_data = {key: value for key, value in df.to_dict(orient='records')[0].items() if key != 'date'}
    message = ", ".join([f"{currency}: {rate}" for currency, rate in message_data.items()])
    
    # Conversion du DataFrame en table HTML
    tables = [df.to_html(classes='data')]
    
    return templates.TemplateResponse('index.html', {
        "request": request,
        "tables": tables,
        "result": df,  # Pass the DataFrame result
        "titles": df.columns.values,
        "message": message
    })
    # data_dict = df.to_dict(orient='records')
    
    # return {"data": data_dict}


@app.get('/search', response_class=HTMLResponse)
async def search(request: Request):
    date = request.query_params.get('date')
    df = await get_data()
    print(f"DataFrame before filtering:\n{df}")  
    print(f"Searching for date: {date}")  
    
    if 'date' in df.columns.values:
        result = df[df['date'] == date]
        print(f"Search result:\n{result}")  
        
        if not result.empty:
            # Extract data related to the date for the message
            message_data = {key: value for key, value in result.to_dict(orient='records')[0].items() if key != 'date'}
            message = ", ".join([f"{currency}: {rate}" for currency, rate in message_data.items()])
            tables = [df.to_html(classes='data')]
            return templates.TemplateResponse('index.html', {
                "request": request,
                "tables": tables,
                "result": result,  # Pass the result DataFrame
                "titles": result.columns.values,
                "message": message
        }) 
    message = "No data found for the given date." if 'date' in df.columns.values else "Data does not contain 'date' column." 
    return templates.TemplateResponse('index.html', {"request": request, "tables": None, "message": message,"titles": []})

