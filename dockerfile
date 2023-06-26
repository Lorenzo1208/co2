# Utilisez une image Python officielle comme image de base
FROM python:3.8-slim-buster

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers requirements.txt dans le répertoire de travail
COPY requirements.txt ./

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste de votre code de l'application dans le répertoire de travail
COPY . .

# Exposez le port sur lequel l'application s'exécute
EXPOSE 8000

# Lancez l'application
CMD ["python", "your_flask_app.py"]
