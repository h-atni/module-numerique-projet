# Module de calcul scientifique : TP et projet personnel

Ce dépôt rassemble les deux éléments demandés pour le module : les solutions des travaux pratiques dans `tp/`, et un projet personnel dans `projet/`, cohérent avec ce qui a été vu en cours. Le README principal, à la racine, présente l'ensemble.

## Structure du dépôt

- `README.md` : présentation générale.
- `tp/tp1_nombres_flottants.py` : entiers, flottants, boucles, fonctions, comparaison avec tolérance, Héron.
- `tp/tp2_arithmetique_nombres_premiers.py` : diviseurs, PGCD, primalité, crible d'Ératosthène, factorisation, coût des algorithmes.
- `tp/tp3_polynomes_fonctions.py` : représentation des polynômes, Horner, dérivation, dichotomie, Newton, intégration numérique.
- `tp/tp4_matrices_systemes_lineaires.py` : matrices, transposition, produit matriciel, pivot de Gauss, résolution de systèmes, numpy.
- `tp/tp5_chiffrement_affine.py` : arithmétique modulaire, clés inversibles, chiffrement affine, force brute, analyse de fréquence.
- `tp/tp6_geometrie_plan.py` : points, vecteurs, déterminant, aires orientées, intersection de segments, point dans un polygone.
- `projet/newton_basins.py` : programme principal du projet (bassins de Newton, frontière, comparaison avec la dichotomie).
- `projet/README.md` : question posée, résultats mesurés, limites.
- `projet/requirements.txt` : dépendances Python du projet.

## Projet personnel

Le projet porte sur les **bassins d'attraction de Newton dans le plan complexe**.

On applique la méthode de Newton à un polynôme complexe. Pour chaque point du plan, on itère

```
z_{n+1} = z_n - f(z_n) / f'(z_n)
```

et on regarde vers quelle racine la suite converge. En colorant le plan selon la racine atteinte, on fait apparaître les bassins d'attraction : des figures fractales, belles à regarder et pratiques pour montrer comment se comporte la convergence d'une méthode itérative.

Le projet mobilise :

- les flottants et les erreurs d'arrondi,
- le calcul numérique et la convergence,
- la recherche de racines,
- les polynômes et la dérivation,
- la géométrie du plan complexe,
- la visualisation et l'interprétation des résultats.

### Lancer le projet

```bash
cd projet
python3 -m pip install -r requirements.txt
python3 newton_basins.py
```

Le script écrit `bassins.png`, `comptage_boites.png` et `resultats.txt` dans `projet/`. Il tourne en une minute environ.

## Pédagogie du dépôt

Les exercices sont des scripts Python exécutables et commentés. Ils montrent la compréhension des notions, le raisonnement derrière chaque algorithme, les vérifications effectuées et l'interprétation des résultats. Le but n'est pas d'avoir un code parfait du premier coup, mais de rendre visible le travail réel mené sur les notions du module.

## Remarque sur l'IA

Je me suis aidé de l'intelligence artificielle pour obtenir des exemples d'utilisation de certaines parties du code, afin de les réutiliser correctement dans mon projet

## Conclusion

Ce dépôt contient les travaux pratiques du module et un projet personnel cohérent avec le semestre. La partie projet pèse le plus dans l'évaluation : elle montre qu'on sait exploiter les méthodes numériques de façon concrète, critique et structurée.
