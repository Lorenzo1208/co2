import os
from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Charger les modèles et les scalers
model_emission = joblib.load('modelemission.pkl')
scaler_emission = joblib.load('scaleremission.pkl')

model_energy = joblib.load('modelenergy.pkl')
scaler_energy = joblib.load('scalerenergy.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_emission', methods=['GET'])
def predict_emission():
    # Récupérer le paramètre depuis l'URL
    param1 = float(request.args.get('param1'))
    # Mettre à l'échelle le paramètre à l'aide du scaler entrainé
    scaled_param1 = scaler_emission.transform(np.array([[param1]]))
    # Faire une prédiction
    prediction = model_emission.predict(scaled_param1)
    # Retourner la prédiction
    return f"Prédiction des émissions de CO2: {prediction[0]}"

@app.route('/predict_energy', methods=['GET'])
def predict_energy():
    # Récupérer le paramètre depuis l'URL
    param2 = float(request.args.get('param2'))
    # Mettre à l'échelle le paramètre à l'aide du scaler entrainé
    scaled_param2 = scaler_energy.transform(np.array([[param2]]))
    # Faire une prédiction
    prediction = model_energy.predict(scaled_param2)
    # Retourner la prédiction
    return f"Prédiction de la consommation d'énergie: {prediction[0]}"

if __name__ == "__main__":
    print("Starting the app...")
    app.run(debug=True, port=8000)  # Run the app on port 8000
