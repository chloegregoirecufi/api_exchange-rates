from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector

db_config = {
    'user':'root',
    'password':'Crevette66',
    'host':'localhost:3306',
    'database':'exchanges_schema'
}

# Création de l'URL de connexion
db_url = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
SessionLocal = SessionLocal()

Base = declarative_base()

def insert_rate(date, currency, rate):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Exécution de la requête d'insertion
        cursor.execute(
            "INSERT INTO rates (date, currency, rate) VALUES (%s, %s, %s)",
            (date, currency, rate)
        )
        
        # Validation de la transaction
        conn.commit()
        
        # Fermeture du curseur et de la connexion
        cursor.close()
        conn.close()
        
        # Message de confirmation
        print(f"Inserted {currency} rate for {date}: {rate}")
    except mysql.connector.Error as err:
        # Gestion des erreurs
        print(f"Error: {err}")

