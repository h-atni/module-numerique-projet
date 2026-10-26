# Module de calcul scientifique — TP + projet

Ce dépôt contient les deux parties demandées pour le module :

- `tp/` : solutions des travaux pratiques.
- `projet/` : projet personnel basé sur les notions vues en cours.

## Structure du dépôt

- `README.md` : présentation générale du dépôt.
- `tp/README.md` : présentation des TP.
- `tp/tp1_nombres_flottants.py` : solutions sur les entiers, les flottants, les boucles, les fonctions et Héron.
- `tp/tp2_arithmetique_nombres_premiers.py` : solutions sur les diviseurs, le PGCD, la primalité, le crible et la factorisation.
- `tp/tp3_polynomes_fonctions.py` : solutions sur les polynômes, la dérivation, la recherche de racines et l’intégration.
- `tp/tp4_matrices_systemes_lineaires.py` : solutions sur les matrices, le produit matriciel, le pivot de Gauss et les transformations géométriques.
- `tp/tp5_chiffrement_affine.py` : solutions sur le chiffrement affine, le déchiffrement, les clés inversibles et les attaques par force brute et par fréquence.
- `tp/tp6_geometrie_plan.py` : solutions sur les points, vecteurs, déterminants, intersections, aires, tests d’appartenance et géométrie algorithmique.
- `projet/README.md` : description du projet.
- `projet/newton_basins.py` : script principal du projet.
- `projet/requirements.txt` : dépendances Python.

## Projet retenu

Le projet porte sur les bassins d'attraction de Newton dans le plan complexe.

Le but est de visualiser, pour un polynôme complexe donné, les régions du plan qui convergent vers chaque racine lorsque la méthode de Newton est appliquée. Cela permet de relier :

- les flottants et les erreurs d'arrondi,
- la convergence d'une méthode itérative,
- la recherche de racines d'un polynôme,
- la géométrie du plan complexe,
- l'importance de la stabilité numérique.

Le cas choisi est le polynôme z^3 - 1, dont les racines sont simples et connues. Il suffit pour observer immédiatement les zones de convergence ainsi que les frontières très fines entre bassins.

## Notes pédagogiques

Les contenus TP sont présentés sous forme de scripts exécutables, avec des fonctions, des vérifications et quelques commentaires. Le projet est autonome, avec un README et un programme d'illustration.

## Usage de l'IA

Le dépôt a été rédigé dans un esprit d'apprentissage et de vérification manuelle. Les scripts restent lisibles, explicites et testables, plutôt que purement générés sans contrôle.
