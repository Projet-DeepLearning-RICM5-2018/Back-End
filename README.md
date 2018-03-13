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

/*TODO*/

## Lancement

/*TODO*/

## Déploiement

1. Changer les identifiant dans le dossier SmartRecruiting_BackEnd/data/database.py
2. (Optionnel) Changer le port de lancement du serveur(runserver.py)
3. (Optionnel) Si un model a déjà été génré copier le model dans le dossier data
4. Lancer le serveur


:::danger
Wifi campus n'autorise que le port 80 et 8080. Ainis si le back tourne sur le port 5555 il est inacessible depuis ce réseaux et l'application ne fonctionne pas.

Solution 1 : lancer la front et le back sur deux machines différentes

:::
