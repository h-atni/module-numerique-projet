# Projet : bassins d'attraction de Newton dans le plan complexe

## Idée générale

La méthode de Newton permet de chercher des racines d'une fonction. En appliquant cette méthode à un polynôme complexe, chaque point du plan peut converger vers une racine différente. En colorant le plan selon la racine atteinte, on obtient des bassins d'attraction.

## Polynôme étudié

On considère le polynôme z^3 - 1. Ses racines sont :

- 1
- exp(2iπ/3)
- exp(4iπ/3)

## Concepts mobilisés

- flottants et précision numérique,
- convergence de méthodes itératives,
- recherche de racines de polynômes,
- géométrie du plan complexe,
- interprétation de résultats et limites de la méthode.

## Lancer le projet

```bash
cd projet
python3 -m pip install -r requirements.txt
python3 newton_basins.py
```

Le script produit une image `newton_bassin.png` dans le dossier `projet/`.

## Observation attendue

Les couleurs du plan indiquent vers quelle racine la méthode converge. Au niveau visuel, les frontières entre bassins sont très fines et donnent une structure fractale.
