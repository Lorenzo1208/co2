import pandas as pd
import yaml
from numpy import nan
from sodapy import Socrata
from psycopg2 import sql
import psycopg2

# Importer les configurations à partir du fichier config.yaml
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Importer le schéma de la base de données à partir du fichier schema.yaml
with open("schema.yaml", "r", encoding="utf-8") as file:
    schema = yaml.safe_load(file)

# Connexion à la base de données
conn = psycopg2.connect(
    host=config['host'],
    port=config['port'],
    database=config['database'],
    user=config['user'],
    password=config['password']
)

cursor = conn.cursor()

# Création des colonnes
for table in schema["tables"]:
    table_name = table["name"]
    columns = []
    for column in table["columns"]:
        column_name = column["name"]
        column_type = column["type"].upper()
        columns.append(f"{column_name} {column_type}")

    columns_query = ', '.join(columns)

    # Création de la table si elle n'existe pas
    create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
        sql.Identifier(table_name),
        sql.SQL(columns_query)
    )
    cursor.execute(create_table_query)

# Récupération des données depuis l'API
client = Socrata("data.seattle.gov", None)
results = client.get("2bpz-gwpy", limit=5000)
api_df = pd.DataFrame.from_records(results)

# Nettoyage des données
api_df.replace(["NULL", ""], nan, inplace=True)

# Chargement des données dans la base de données
for index, row in api_df.iterrows():
    columns_str = ", ".join(row.keys())
    values_str = ", ".join("'{}'".format(str(value).replace("'", "''")) if pd.notnull(value) else 'NULL' for value in row)
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
        sql.Identifier(table_name),
        sql.SQL(columns_str),
        sql.SQL(values_str)
    )
    cursor.execute(insert_query)

conn.commit()
cursor.close()
conn.close()
