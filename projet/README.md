# Projet : bassins d'attraction de Newton dans le plan complexe

## Question posée

La méthode de Newton permet de trouver, à partir d'un point de départ, une racine d'un polynôme. Dans le plan complexe, ce point de départ décide de la racine atteinte. **Que devient ce partage du plan quand on change de polynôme, et que peut-on mesurer sur la frontière entre les bassins ?**

## Ce que fait le programme

`newton_basins.py` écrit à la main Newton, Horner et la dérivée ; `np.roots` ne sert que de racines de référence pour classer les points. Le script :

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

- Pour `z^3 - 2z + 2`, 1,07 % des points ne convergent jamais, même avec 1000 itérations : ce sont les zones noires bien visibles sur `bassins.png`. Augmenter `max_iter` n'y change rien, ce qui colle avec des cycles attractifs plutôt qu'avec un simple manque d'itérations.
- Pour `z^4 - 1`, passer de 30 à 60 itérations fait tomber les points non convergés de 1,48 % à 0,36 %, puis la valeur se stabilise à 0,26 %.
- Sur la droite réelle, pour `z^3 - 1`, Newton converge en 7 itérations contre 35 pour la dichotomie. Pour `z^3 - 2z + 2` depuis x0 = 0, Newton échoue (cycle 0 <-> 1) alors que la dichotomie trouve la racine -1,7693 en 35 itérations.
- La carte du nombre d'itérations montre que les points lents se concentrent sur la frontière entre bassins.

## Limites du travail

- La dimension de la frontière est une **estimation** : comptage de boîtes de 2 à 64 pixels sur une image de 2048 pixels, frontière détectée par différence entre pixels voisins (donc épaisse d'un pixel). À lire comme des ordres de grandeur, pas comme des valeurs exactes.
- Seuls 3 polynômes sont étudiés, sur le carré [-2, 2] x [-2, 2].
- La classification utilise `np.roots` comme référence ; le critère de convergence est `|z - racine| < 1e-8`.
- Je n'ai testé ni la sensibilité à la précision flottante ni celle à la résolution de la grille.

## Observations et interprétation

Je m'attendais à trois grandes zones bien séparées. En zoomant sur la frontière, j'ai vu que les trois couleurs s'y mélangent à toutes les échelles : entre deux bassins, on retrouve toujours le troisième.

Les points les plus lents sont sur la frontière. Mon explication : près de la frontière, un point de départ très proche d'un autre peut finir sur une racine différente, donc Newton met plus de temps à se décider.

Pour `z^3 - 2z + 2`, environ 1 % des points ne convergent jamais, même avec 1000 itérations. Pour `z^4 - 1`, au contraire, le pourcentage baisse quand on augmente `max_iter` puis se stabilise. Pour `z^3 - 2z + 2`, ce n'est donc pas un manque d'itérations : sur la droite réelle, en partant de 0, Newton tourne entre 0 et 1 (f(0)=2 et f'(0)=-2 donnent 1, puis f(1)=1 et f'(1)=1 redonnent 0).

Quand il marche, Newton est bien plus rapide que la dichotomie (7 itérations contre 35 pour `z^3 - 1`), mais il peut échouer, alors que la dichotomie converge toujours si l'intervalle contient un changement de signe. Il faut donc connaître le polynôme avant de choisir la méthode.

La dimension estimée de la frontière tombe entre 1,41 et 1,58, donc entre une ligne (1) et une surface (2), ce qui correspond à l'idée d'une frontière fractale. Je reste prudent : c'est une estimation par comptage de boîtes, pas une valeur exacte.

## Usage de l'IA

Je me suis aidé de claude afin de voir comment utiliser certaines partie du code afin de l'appliquer à mon projet.
