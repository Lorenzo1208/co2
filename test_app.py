import os
import pytest
import pandas as pd
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_file_form(client):
    # Créer un fichier de test
    test_file_path = 'test_file.csv'
    test_data = "LargestPropertyUseTypeGFA;PrimaryPropertyType\n1000;Office\n2000;Retail"
    with open(test_file_path, 'w') as f:
        f.write(test_data)

    # Envoyer une requête POST avec le formulaire pour télécharger le fichier
    response = client.post('/upload', data={'csv_file': (open(test_file_path, 'rb'), 'test_file.csv')}, follow_redirects=True)

    # Vérifier la réponse
    assert response.status_code == 200
    assert [[-861523.9333982859, 20.417919796486416], [-774547.0714570917, 21.759107104223247]] == response.json

    # Supprimer le fichier de test
    os.remove(test_file_path)
