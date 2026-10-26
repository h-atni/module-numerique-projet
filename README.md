# Module de calcul scientifique — TP + projet personnel

Ce dépôt contient les deux éléments demandés pour le module :

- `tp/` : les solutions aux travaux pratiques.
- `projet/` : un projet personnel cohérent avec les notions vues en cours.

Le dépôt est organisé de façon simple et lisible, avec le README principal à la racine pour présenter le travail global.

## Structure du dépôt

- `README.md` : présentation générale du dépôt.
- `tp/tp1_nombres_flottants.py` : entiers, flottants, boucles, fonctions, comparaison avec tolérance, Héron.
- `tp/tp2_arithmetique_nombres_premiers.py` : diviseurs, PGCD, primalité, crible d’Ératosthène, factorisation, coût des algorithmes.
- `tp/tp3_polynomes_fonctions.py` : représentation des polynômes, Horner, dérivation, dichotomie, Newton, intégration numérique.
- `tp/tp4_matrices_systemes_lineaires.py` : matrices, transposition, produit matriciel, pivot de Gauss, résolution de systèmes, numpy.
- `tp/tp5_chiffrement_affine.py` : arithmétique modulaire, clés inversibles, chiffrement affine, force brute, analyse de fréquence.
- `tp/tp6_geometrie_plan.py` : points, vecteurs, déterminant, aires orientées, intersection de segments, point dans un polygone.
- `projet/newton_basins.py` : programme principal du projet.
- `projet/requirements.txt` : dépendances Python du projet.

## Projet personnel

Le projet choisi est : les bassins d'attraction de Newton dans le plan complexe.

### Idée

On applique la méthode de Newton à un polynôme complexe. À chaque point du plan, on suit la suite itérative

z_{n+1} = z_n - f(z_n) / f'(z_n)

et on détermine vers quelle racine la suite converge. En colorant le plan selon cette racine, on obtient des bassins d'attraction : des figures fractales de grande beauté et très utiles pour illustrer la convergence des méthodes itératives.

### Ce que le projet mobilise

- flottants et erreurs d'arrondi,
- calcul numérique et convergence,
- recherche de racines,
- polynômes et dérivation,
- géométrie du plan complexe,
- visualisation et interprétation des résultats.

### Lancer le projet

```bash
cd projet
python3 -m pip install -r requirements.txt
python3 newton_basins.py
```

Le script produit une image `newton_bassin.png` dans le dossier `projet/`.

## Pédagogie du dépôt

Les exercices sont écrits sous forme de scripts Python exécutables et commentés, afin de montrer à la fois :

- la compréhension des notions,
- le raisonnement derrière chaque algorithme,
- les vérifications effectuées,
- et l'interprétation des résultats.

L'objectif n'est pas d'obtenir un code parfait sans réflexion, mais de rendre visible le travail réel mené sur les notions du module.

## Remarque sur l'IA

L'usage de l'IA n'est ni obligatoire ni interdit. Ici, le dépôt a été pensé dans un esprit d'apprentissage et de vérification personnelle : les scripts ont été adaptés, adaptés, testés et expliqués pour rester lisibles et exploitables.

## Conclusion

Ce dépôt présente à la fois les travaux pratiques du module et un projet personnel cohérent avec les notions vues pendant le semestre. La partie projet est la plus importante pour l'évaluation, car elle montre la capacité à exploiter les méthodes numériques de manière concrète, critique et structurée.
