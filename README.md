# About project📝
This project generates an array of exchange rates with values for currencies like Euros, Dollar, Yen and Pound.
For this project the language is python.
For the database we used sqLite.
To build the API we used [fastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/#install-sqlalchemy)

# Before starting the project 📋
<small>be at the root of the project</small>
python3 -m venv venv

<small>activated the environment</small>
source venv/bin/activated

<small>in environment do</small>
pip install -r requirements.txt

# Command for start project ▶️
<small>if there is a subfolder of the application</small>
uvicorn api_sql.main:app --reload

** or **

uvicorn main:app --reload
