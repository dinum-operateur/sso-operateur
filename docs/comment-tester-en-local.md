# Comment tester en local

## Lancer le pad en local via docker

`git clone https://github.com/betagouv/pad.numerique.gouv.fr.git`

Copier le docker-compose-pad.yaml.example de docs dans le dossier du pad
Renseigner `CMD_OAUTH2_CLIENT_ID` et `CMD_OAUTH2_CLIENT_SECRET` récupérés depuis Django admin. 

Dans le dossier du pad, lancer docker avec `docker compose up`.

## Test manuel du flux OIDC 

Il peut être utile de lancer manuellement les requêtes du flux OIDC pour tester ou pour y voir plus clair.

### Endpoint "authorize"

C'est le point d'interface vers lequelle le service redirige l'usager afin de lui demander l'autorisation d'utiliser ses données (et pour l'authentifier, aussi).

http://localhost:1234/openid/authorize?response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Foauth%2Fcallback&state=babidibou&client_id=135810&scope=openid%20profile%20email


Pour fabriquer soi-même son URI, il faut récupérer (dans l'admin Django) les données suivantes sur un client :

- `scope` (par exemple `openid profile email`)
- `client_id`
- `redirect_uri`

Le paramètre `response_type`, quant à lui, vaut toujours `code`.

:warning: Après avoir authentifié votre usager, vous pouvez récupérer le `code` dans l'URL vers laquelle vous redirige le navigateur.

### Endpoint `token`

Celui-ci est normalement un appel serveur-à-serveur, il permet au service de récupérer un jetons d'accès aux infos de l'usager.

Dans votre terminal préféré, remplissez ces quelques variables : 

```
CODE=récupéré à l'étape précédente
CLIENT_ID=à chercher dans l'admin
CLIENT_SECRET=idem
```


```bash
curl -X POST http://localhost:3000/oauth/token -u "$CLIENT_ID:$CLIENT_SECRET" -d "grant_type=authorization_code&redirect_uri=http%3A//localhost%3A3001/users/auth/api_gouv/callback&code=$CODE"
```

Avec [httpie](https://httpie.io/cli) pour avoir un retour plus lisible :

```
http --form \
-a $CLIENT_ID:$CLIENT_SECRET \
POST http://localhost:1234/openid/token \
grant_type='authorization_code' \
redirect_uri='http://localhost:3000/oauth/callback' \
code=$CODE
```

Cette requête vous retourne un paramètre `access_token` qui servira à récupérer les infos utilisateur dans l'endpoint suivant.

## Endpoint `userinfo`

Ici, vous allez enfin pouvoir récupérer les infos de l'usager.

Toujours dans le terminal :

```
ACCESSTOKEN=recuperez moi à l'étape précédente
```

```
curl -X GET http://localhost:1234/openid/userinfo -H "Authorization: Bearer $ACCESSTOKEN"
```

Avec HTTPIE:

```
http GET http://localhost:1234/openid/userinfo \
Authorization:'Bearer $ACCESSTOKEN'
```
