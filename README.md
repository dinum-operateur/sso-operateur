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

### Initialisation de données de fonctionnement

Créez un utilisateur administrateur 🫅 (_superuser_) :

```
python manage.py createsuperuser
```

Et aussi, créez une clé RSA 🔑 pour le bon fonctionnement du module oidc_provider :

```
python manage.py creatersakey
```

## Configurer un client OIDC

### Installation

D'abord, rendez-vous dans l'admin Django, section OpenID Connect Provider, pour créer un Client avec les caractéristiques suivantes : 

- owner : l'id d'un user existant
- client type : confidential
- Response type : code
- Redirect URIs : une URL par ligne. Pour le pad `http://localhost:3000/auth/oauth2/callback`.
- JWT algorithm : RS256
- Scopes : `openid email profile`
- Require consent : peut être activé dans un premier temps pour bien voir le processus, mais il faudra le désactiver pour l'auto-login

Sauvegardez, puis notez le client ID + le client secret disponible dans l'objet que vous venez de créer.

Exemple de configuration Docker-compose pour que le pad discute avec votre sso-operateur (:warning: complétez `CMD_OAUTH2_CLIENT_ID` et `CMD_OAUTH2_CLIENT_SECRET`) : 

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
      - CMD_OAUTH2_BASEURL=http://localhost:8000
      - CMD_OAUTH2_USER_PROFILE_URL=http://host.docker.internal:8000/openid/userinfo
      - CMD_OAUTH2_USER_PROFILE_USERNAME_ATTR=preferred_username
      - CMD_OAUTH2_USER_PROFILE_DISPLAY_NAME_ATTR=email
      - CMD_OAUTH2_USER_PROFILE_EMAIL_ATTR=email
      - CMD_OAUTH2_TOKEN_URL=http://host.docker.internal:8000/openid/token
      - CMD_OAUTH2_AUTHORIZATION_URL=http://localhost:8000/openid/authorize
      - CMD_OAUTH2_CLIENT_ID=xxxxxxx
      - CMD_OAUTH2_CLIENT_SECRET=xxxxxxx
      - CMD_OAUTH2_SCOPE=openid profile email
      - NODE_TLS_REJECT_UNAUTHORIZED=0
```

### Ajout de la clé RSA

Il faut également ajouter une clé RSA au moyen de la commande suivante : 
`python manage.py creatersakey`

### Utilisation

- Connectez-vous à l'admin Django avec votre super user : cela ouvre une session Django qui est aussi valable pour le module oidc provider.
- Sur le pad, cliquez sur "se connecter"
- Comme il n'y a pas besoin de login, vous êtes redirigé·e vers la page de demande de consentement si elle a été activée.
- Et une fois que le consentement a été donné, vous êtes redirigé·e vers le pad, dorénavant connecté·e avec le même identifiant que votre super admin Django.
