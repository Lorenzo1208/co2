import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{database}'

db = SQLAlchemy(app)

class Co2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ajoutez d'autres attributs selon la structure de votre table 'co2'

@app.route('/')
def index():
    data = Co2.query.all()
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)

#
