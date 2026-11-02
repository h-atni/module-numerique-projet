# Projet : bassins d'attraction de Newton dans le plan complexe

## Question posée

La méthode de Newton trouve une racine d'un polynôme à partir d'un point de départ. Dans le plan complexe, le point de départ décide de la racine atteinte. **Que devient ce partage du plan quand on change de polynôme, et que peut-on mesurer sur la frontière entre les bassins ?**

## Ce que fait le programme

`newton_basins.py` (Newton, Horner et dérivée sont écrits à la main ; `np.roots` ne sert que de racines de référence pour classer les points) :

1. calcule, pour 3 polynômes (`z^3 - 1`, `z^4 - 1`, `z^3 - 2z + 2`), la racine atteinte et le nombre d'itérations depuis chaque point d'une grille 600 x 600 ;
2. repère les points qui ne convergent pas (en noir sur les images) ;
3. mesure l'effet du nombre maximal d'itérations sur ces points ;
4. estime la dimension de la frontière entre bassins par comptage de boîtes (grille 2048 x 2048) ;
5. compare Newton et dichotomie sur la droite réelle, dont un cas où Newton échoue.

## Lancer le projet

```bash
cd projet
python3 -m pip install -r requirements.txt
python3 newton_basins.py
```

Compter environ une minute. Le script écrit `bassins.png`, `comptage_boites.png` et `resultats.txt` dans `projet/`.

## Résultats mesurés (voir `resultats.txt`)

| Polynôme | Points non convergés (60 it.) | Dimension de la frontière (estimée) |
|---|---|---|
| `z^3 - 1` | 0,00 % | 1,465 |
| `z^4 - 1` | 0,36 % | 1,579 |
| `z^3 - 2z + 2` | 1,07 % | 1,408 |

- Pour `z^3 - 2z + 2`, 1,07 % des points ne convergent jamais, même avec 1000 itérations : ce sont des zones noires bien visibles sur `bassins.png`. Augmenter `max_iter` n'y change rien, ce qui est cohérent avec des cycles attractifs et non un simple manque d'itérations.
- Pour `z^4 - 1`, passer de 30 à 60 itérations réduit les points non convergés de 1,48 % à 0,36 %, puis la valeur se stabilise à 0,26 %.
- Sur la droite réelle, pour `z^3 - 1`, Newton converge en 7 itérations contre 35 pour la dichotomie. Pour `z^3 - 2z + 2` depuis x0 = 0, Newton échoue (cycle 0 <-> 1) alors que la dichotomie trouve la racine -1,7693 en 35 itérations.
- La carte du nombre d'itérations montre que les points lents se concentrent sur la frontière entre bassins.

## Limites du travail

- La dimension de la frontière est une **estimation** : comptage de boîtes de 2 à 64 pixels sur une image de 2048 pixels, frontière détectée par différence entre pixels voisins (donc épaisse d'un pixel). Les valeurs sont à lire comme des ordres de grandeur, pas comme des valeurs exactes.
- Seuls 3 polynômes sont étudiés, sur le carré [-2, 2] x [-2, 2].
- La classification utilise `np.roots` comme référence ; le critère de convergence est `|z - racine| < 1e-8`.
- Je n'ai pas testé la sensibilité à la précision flottante ni à la résolution de la grille.

## Observations et interprétation (à compléter)

> **[À COMPLÉTER PAR MOI avant le rendu]** : ce que je comprends de ces résultats avec mes mots, une chose qui m'a surpris, une idée testée qui n'a pas marché.

## Usage de l'IA

J'ai utilisé l'assistant Claude (Anthropic) pour écrire le code de `newton_basins.py` et une première version de ce README, à partir de ma demande d'étudier la frontière entre bassins.
Ce que j'ai vérifié moi-même : **[À COMPLÉTER PAR MOI : par exemple relancé le script, relu le code, vérifié à la main un résultat comme le cas z^3 - 2z + 2 depuis x0 = 0]**.
