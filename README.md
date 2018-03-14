# Back-End
## Fonctionnalités implémentées
### Back 

* API fonctionnelle (cf document des routes)
* Possibilité de lancer l'apprentissage au démarrage du serveur
* Possibilité de remplir automatiquement la base de données au démarrage du serveur

### Deeplearning
* Mise en place de l'algorithme de deeplearning de word2Vector
* Mise en place de l'algorithme de deeplearning CNN pour générer le model de prediction
* Possibilité d'évaluer une offre en fonction d'un model de prédiction 

## Fonctionnalité interesante à mettre en place

* Transformer l'algorithme de prédiction CNN pour prédire des équipes et non une fillère

## Installation

* Installer mysql-server et le lancer (pour le choix du nom d'utilisateur et du mot de passe il faut que ça corresponde avec le fichier SmartRecruiting_BackEnd/data/database.py
* Pas besoin de créer les tables, elles seront crées automatiquement en lançant l'application
* Installer Python 3 et pip
* Installer les packages nécessaires : pip install -r requirements.txt

## Lancement

* Pour lancer le serveur : python runserver.py
* Paramètres à ajouter :
  * -i, --init : initialiser le modèle et la base de données
  * -r, --reinit : réinitialiser le modèle à partir de la base de données

## Déploiement

1. Changer les identifiant dans le dossier SmartRecruiting_BackEnd/data/database.py
2. (Optionnel) Changer le port de lancement du serveur(runserver.py)
3. (Optionnel) Si un model a déjà été génré copier le model dans le dossier data
4. Lancer le serveur


:::danger
Wifi campus n'autorise que le port 80 et 8080. Ainis si le back tourne sur le port 5555 il est inacessible depuis ce réseaux et l'application ne fonctionne pas.

Solution 1 : lancer la front et le back sur deux machines différentes

:::

## Ajout des données

* Pour l'initialisation il faut ajouter 3 fichiers dans le dossier data :
  * offers.csv
  * fields.csv
  * contacts.csv
* Les fichiers doivent être encodés en UTF-8 et les champs doivent être séparés par des virgules
* Les différents champs des fichiers sont :
  * offers.csv : Formation,Offre initiale
  * fields.csv : name,description,website
  * contacts.csv : name,surname,role,email,phone,field
* La première ligne des fichiers doit comporter le nom des champs

## Tests unitaires

* Pour lancer un script de tests en particulier : python SmartRecruiting_BackEnd/tests/script_test.py
* Pour lancer tous les tests unitaires : nose2
