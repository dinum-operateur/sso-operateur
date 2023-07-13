# On utilise une image Python 3.9 officielle
FROM python:3.9-slim-buster

# Pour utiliser la commande 'print' dans le Dockerfile
RUN apt-get update && apt-get install -y postgresql-client

# Répertoire de travail pour l'application
WORKDIR /usr/src/app

# Copier le fichier des dépendances dans le répertoire de travail
COPY requirements.txt ./

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le répertoire de travail
COPY . .

# Exposer le port sur lequel l'application sera exécutée
EXPOSE 8000
