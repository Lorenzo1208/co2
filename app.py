import os
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
import joblib
import numpy as np
import pandas as pd
import pickle
from flask import jsonify

app = Flask(__name__)

# Charger le modèle et le scaler
multi_model = joblib.load('multimodel.pkl')
multi_scaler = joblib.load('multiscaler.pkl')

# Charger les données pour obtenir les PrimaryPropertyType
df_train = pd.read_csv('column_list.csv')

primary_property_types = df_train.columns.tolist()

# Créer une dataframe vide avec les bonnes colonnes
df_predict = pd.DataFrame(columns=primary_property_types)


ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csv_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        df = pd.read_csv(file, delimiter=';')


        predictions = []
        for index, row in df.iterrows():
            primary_property_type = row['PrimaryPropertyType']
            largest_property_use_type_gfa = row['LargestPropertyUseTypeGFA']

            data = {col: [0] for col in primary_property_types}
            data['LargestPropertyUseTypeGFA'] = [largest_property_use_type_gfa]
            data[primary_property_type] = [1] 

            df_predict_request = pd.DataFrame(data)

            columns_order = ['LargestPropertyUseTypeGFA'] + [col for col in df_train.columns if col != 'LargestPropertyUseTypeGFA']
            df_predict_request = df_predict_request[columns_order]

            df_predict_request['LargestPropertyUseTypeGFA'] = multi_scaler.transform(df_predict_request[['LargestPropertyUseTypeGFA']])

            prediction = multi_model.predict(df_predict_request)
            predictions.append(prediction.flatten().tolist())

        return jsonify(predictions)
    else:
        return jsonify({'error': 'Allowed file types are .csv'}), 400


@app.route('/')
def index():
    return render_template('index.html', primary_property_types=primary_property_types[1:]) # ignore the first item which is 'LargestPropertyUseTypeGFA'

@app.route('/predict', methods=['GET'])
def predict():
    # Récupérer les paramètres depuis l'URL
    LargestPropertyUseTypeGFA = request.args.get('LargestPropertyUseTypeGFA')
    # print(f"LargestPropertyUseTypeGFA: {LargestPropertyUseTypeGFA}")  # Ajouté pour le débogage

    # Convertissez LargestPropertyUseTypeGFA en float
    LargestPropertyUseTypeGFA = float(LargestPropertyUseTypeGFA)

    PrimaryPropertyType = request.args.get('PrimaryPropertyType')
    # print(f"PrimaryPropertyType: {PrimaryPropertyType}")  # Ajouté pour le débogage

    # Créer une ligne de données avec la valeur pour LargestPropertyUseTypeGFA et des zéros pour les types de propriété
    data = {col: [0] for col in primary_property_types}
    data['LargestPropertyUseTypeGFA'] = [LargestPropertyUseTypeGFA]
    data[PrimaryPropertyType] = [1]  # mettre la valeur à 1 pour le type de propriété sélectionné

    # Imprimez les données pour le débogage
    # print(f"Data: {data}")

    # Créer un DataFrame à partir de ces données
    df_predict_request = pd.DataFrame(data)

    # Réorganiser les colonnes pour correspondre à l'ordre souhaité (LargestPropertyUseTypeGFA first)
    columns_order = ['LargestPropertyUseTypeGFA'] + [col for col in df_train.columns if col != 'LargestPropertyUseTypeGFA']
    df_predict_request = df_predict_request[columns_order]

    # Mettre à l'échelle uniquement la caractéristique LargestPropertyUseTypeGFA à l'aide du scaler entraîné
    df_predict_request['LargestPropertyUseTypeGFA'] = multi_scaler.transform(df_predict_request[['LargestPropertyUseTypeGFA']])

    # Faire une prédiction
    predictions = multi_model.predict(df_predict_request)

    # Retourner les prédictions
    return f"{predictions[0][0]} {predictions[0][1]}"

if __name__ == "__main__":
    print("Starting the app...")
    app.run(debug=True, port=8000)  # Run the app on port 8000