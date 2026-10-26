# Module de calcul scientifique — TP + projet

Ce dépôt contient les deux parties demandées pour le module :

- `tp/` : solutions des travaux pratiques.
- `projet/` : projet personnel axé sur les notions vues en cours.

## Structure du dépôt

- `README.md` : présentation générale du dépôt.
- `tp/README.md` : présentation du travail de TP.
- `tp/tp1_nombres_flottants.py` : solutions Python des exercices de base.
- `projet/README.md` : description du projet.
- `projet/newton_basins.py` : programme principal du projet.
- `projet/requirements.txt` : dépendances nécessaires.

## Projet retenu

Le projet porte sur les bassins d'attraction de Newton dans le plan complexe.

Le but est de visualiser, pour un polynôme complexe donné, les régions du plan qui convergent vers chaque racine lorsqu'on applique la méthode de Newton. Cela permet de relier :

- les flottants et les erreurs d'arrondi,
- la convergence d'une méthode itérative,
- la recherche de racines d'un polynôme,
- la géométrie du plan complexe,
- l'importance de la stabilité numérique.

Ce projet est volontairement limité à un cas simple mais exploitable : le polynôme z^3 - 1. Il suffit pour observer immédiatement le comportement fractal, ainsi que les zones de convergence et les frontières instables.

## Intention de travail

Les solutions TP sont présentées sous forme de script exécutable. Le projet est autonome, avec un README détaillé et un script d'illustration.

## Note sur l'usage de l'IA

Le dépôt a été rédigé avec une logique d'apprentissage et de vérification manuelle. Les scripts ont été pensés pour rester lisibles, testables et explicites, plutôt que purement générés de façon automatique.
