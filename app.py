import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, select

app = Flask(__name__)
database_uri = os.getenv('DATABASE_URI')
if not database_uri:
    raise RuntimeError("DATABASE_URI not set in environment")
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

db = SQLAlchemy(app)
meta = MetaData()

Co2 = None  # Declare Co2 here

@app.before_request
def load_table():
    global Co2  # Use the global Co2 variable
    if Co2 is None:
        print("Loading table 'co2'...")
        # Reflect your existing database into a new model
        Co2 = Table('co2', meta, autoload_with=db.engine)
        print("Table 'co2' loaded successfully.")

@app.route('/')
def index():
    print("Processing request for index...")
    stmt = select(Co2)  # construct the SELECT * FROM co2 query
    with db.engine.begin() as connection:
        result = connection.execute(stmt)  # execute the query
        data = result.fetchall()  # fetch all rows from the result
    return render_template('index.html', data=data)

if __name__ == "__main__":
    print("Starting the app...")
    app.run(debug=True, port=8000)  # Run the app on port 8000
