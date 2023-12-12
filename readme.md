# Projet NoSQL - Mounir MOUSTAPHA & Pierre LAURENT

## Lancer le projet

### Exécutez la commande suivante dans le répertoire du projet :

```bash
docker-compose up
```

### Vous pourrez accéder à l'application via le navigateur web à l'adresse :

http://localhost:8080/

## Se connecter aux systemes de persistance

### MongoDB :

```bash
# Se connecter à mongosh (le nom du conteneur peut être différent, vous pouvez le vérifier avec : docker ps)
docker exec -it ensiie_2a_projetnosql-mongodb-1 mongosh app
# Lister les collections
show collections
# Afficher le contenu d'une collection
db.matieres.find()
```

### PostgreSQL :

```bash
# Se connecter à psql (le nom du conteneur peut être différent, vous pouvez le vérifier avec : docker ps)
docker exec -it ensiie_2a_projetnosql-postgres-1 psql --username=admin app
# Lister les tables 
\dt
# Afficher le contenu d'une table
SELECT * FROM matieres;
```

## Se connecter à Adminer (PostgreSQL)

### Vous pourrez accéder à Adminer via le navigateur web à l'adresse :

http://localhost:8050/

### Informations à remplir dans le formulaire Adminer :

| Système       | Serveur       | Utilisateur   | Mot de passe	| Base de données |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| PostgreSQL    | postgres      | admin         | 123           | app           |