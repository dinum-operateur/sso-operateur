# SSO opérateur

## Introduction

Ce produit vise à connecter automatiquement les utilisateurs de la suite numérique collaborative de la DINUM.

## Démarrage rapide après installation

```bash
. venv/bin/activate
python manage.py runserver
```

## Installation

### Installer l'environnement

Création d'un venv et installation des dépendances : 

```
cp .env.example .env
python -m venv venv 
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Configurer la base de données

Installer PostgreSQL en fonction de votre OS : https://www.postgresql.org/download/

Puis lancez l'invite de commande PostgreSQL :

```
psql
```

Dans l'invite de commande psql, vous pouvez à présent créer la base de données et l'utilisateur :

```sql
CREATE USER sso_team PASSWORD 'sso_pwd';
CREATE DATABASE sso_db OWNER sso_team;
ALTER USER sso_team CREATEDB;
```

Vous pouvez à présent quitter l'invite de commande psql.

Pour finir, lancez les migrations pour initialiser la base de données :

```bash
python manage.py migrate
```

### Installation de pre-commit

[Pre-commit](https://pre-commit.com/) permet de linter et formatter votre code avant chaque commit. Par défaut ici, il exécute :

- [black](https://github.com/psf/black) pour formatter automatiquement vos fichiers .py en conformité avec la PEP 8 (gestion des espaces, longueur des lignes, etc)
- [flake8](https://github.com/pycqa/flake8) pour soulever les "infractions" restantes (import non utilisés, etc)
- [isort](https://github.com/pycqa/isort) pour ordonner vos imports

Pour l'installer :

```bash
pre-commit install
```

Vous pouvez effectuer un premier passage sur tous les fichiers du repo avec :

```bash
pre-commit run --all-files
```

### Exécuter les tests manuellement

```bash
python manage.py test
```

## Configurer un client OIDC

D'abord, rendez-vous dans l'admin Django, section OpenID Connect Provider, pour créer un Client avec les caractéristiques suivantes : 

- client type : confidential
- Response type : code
- Redirect URIs : une URL par ligne. Pour le pad `http://localhost:3000/auth/oauth2/callback`.
- JWT algorithm : RS256
- Scopes : `openid email profile`

Sauvegardez, puis notez le client ID + le client secret que vous donne la page.

Exemple de configuration Docker-compose pour que le pad discute avec votre sso-operateur (:warning: complétez le client ID et le client secret) : 

```yaml
version: '3'
services:
  app:
    image: betagouv-hedgedoc
    build: .
    environment:
      - CMD_DB_URL=postgres://hedgedoc:password@db:5432/hedgedoc
      - CMD_DOMAIN=localhost
      - CMD_URL_ADDPORT=true
      - CMD_OAUTH2_BASEURL=http://localhost:1234
      - CMD_OAUTH2_USER_PROFILE_URL=http://host.docker.internal:1234/openid/userinfo
      - CMD_OAUTH2_USER_PROFILE_USERNAME_ATTR=id
      - CMD_OAUTH2_USER_PROFILE_DISPLAY_NAME_ATTR=username
      - CMD_OAUTH2_USER_PROFILE_EMAIL_ATTR=email
      - CMD_OAUTH2_TOKEN_URL=http://host.docker.internal:1234/openid/token
      - CMD_OAUTH2_AUTHORIZATION_URL=http://localhost:1234/openid/authorize
      - CMD_OAUTH2_CLIENT_ID=xxxxxxx
      - CMD_OAUTH2_CLIENT_SECRET=xxxxxxxx
      - NODE_TLS_REJECT_UNAUTHORIZED=0
```
