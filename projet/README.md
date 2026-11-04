# Projet : bassins d'attraction de Newton dans le plan complexe

## Question posée

La méthode de Newton permet de trouver, à partir d'un point de départ, une racine d'un polynôme. Dans le plan complexe, ce point de départ décide de la racine atteinte. Que devient ce partage du plan quand on change de polynôme, et que peut-on mesurer sur la frontière entre les bassins ?

## Ce que fait le programme

`newton_basins.py` écrit à la main Newton, Horner et la dérivée ; `np.roots` ne sert que de racines de référence pour classer les points. Le script :

- calcule, pour 3 polynômes (`z^3 - 1`, `z^4 - 1`, `z^3 - 2z + 2`), la racine atteinte et le nombre d'itérations depuis chaque point d'une grille 600 x 600 ;
- repère les points qui ne convergent pas (en noir sur les images) ;
- mesure l'effet du nombre maximal d'itérations sur ces points ;
- estime la dimension de la frontière entre bassins par comptage de boîtes, sur des grilles de 512, 1024 et 2048 pixels de côté ;
- teste la sensibilité de la classification à la tolérance de convergence ;
- compare Newton et dichotomie sur la droite réelle, dont un cas où Newton échoue.

## Lancer le projet

```bash
cd projet
python3 -m pip install -r requirements.txt
python3 newton_basins.py             # calcul complet, environ 15 s
python3 newton_basins.py --rapide    # résolutions réduites, pour tester
python3 newton_basins.py --afficher  # ouvre aussi les figures dans une fenêtre
```

Le temps du calcul complet dépend de la machine. Le script écrit `bassins.png`, `comptage_boites.png` et `resultats.txt` dans `projet/`.

## Résultats mesurés (voir `resultats.txt`)

| Polynôme | Points non convergés (60 it.) | Dimension de la frontière (estimée) |
|---|---|---|
| z^3 - 1 | 0,00 % | 1,457 |
| z^4 - 1 | 0,36 % | 1,574 |
| z^3 - 2z + 2 | 1,07 % | 1,399 |

- **Effet de la résolution.** La dimension estimée se stabilise quand la grille s'affine :

| Polynôme | 512 x 512 | 1024 x 1024 | 2048 x 2048 |
|---|---|---|---|
| z^3 - 1 | 1,461 | 1,457 | 1,457 |
| z^4 - 1 | 1,599 | 1,578 | 1,574 |
| z^3 - 2z + 2 | 1,418 | 1,406 | 1,399 |

  L'écart entre 1024 et 2048 est d'au plus 0,007, donc la valeur à 2048 est fiable à quelques millièmes près ; à 512, elle est surestimée de 0,004 à 0,025 selon le polynôme.
- **Effet de la tolérance.** Passer de la tolérance 1e-8 à 1e-4 ne change la racine atteinte d'aucun pixel (0,000 % pour les trois polynômes) : le critère de convergence n'influence pas le classement des bassins.
- Pour `z^3 - 2z + 2`, 1,07 % des points ne convergent jamais, même avec 1000 itérations : ce sont les zones noires bien visibles sur `bassins.png`. Augmenter `max_iter` n'y change rien, ce qui colle avec des cycles attractifs plutôt qu'avec un simple manque d'itérations.
- Pour `z^4 - 1`, passer de 30 à 60 itérations fait tomber les points non convergés de 1,48 % à 0,36 %, puis la valeur se stabilise à 0,26 %.
- Sur la droite réelle, pour `z^3 - 1`, Newton converge en 8 itérations contre 41 pour la dichotomie. Pour `z^3 - 2z + 2` depuis x0 = -2, Newton converge en 5 itérations. Depuis x0 = 0, Newton échoue (cycle 0 <-> 1) alors que la dichotomie trouve la racine -1,7693 en 42 itérations.
- La carte du nombre d'itérations montre que les points lents se concentrent sur la frontière entre bassins.

## Limites du travail

- La dimension de la frontière est une estimation : comptage de boîtes de 4 à 64 pixels sur une image de 2048 pixels, frontière détectée par différence entre pixels voisins (donc épaisse d'environ deux pixels). À lire comme des ordres de grandeur, pas comme des valeurs exactes.
- Seuls 3 polynômes sont étudiés, sur le carré [-2, 2] x [-2, 2].
- La classification utilise `np.roots` comme référence ; le critère de convergence est |z - racine| < 1e-8.
- Je n'ai pas testé la sensibilité à la précision flottante (float32 contre float64), et la fenêtre reste fixée à [-2, 2] x [-2, 2].

## Observations et interprétation

Je m'attendais à trois grandes zones bien séparées. En zoomant sur la frontière, j'ai vu que les trois couleurs s'y mélangent à toutes les échelles : entre deux bassins, on retrouve toujours le troisième.

Les points les plus lents sont sur la frontière. Mon explication : près de la frontière, un point de départ très proche d'un autre peut finir sur une racine différente, donc Newton met plus de temps à se décider.

Pour `z^3 - 2z + 2`, environ 1 % des points ne convergent jamais, même avec 1000 itérations. Pour `z^4 - 1`, au contraire, le pourcentage baisse quand on augmente `max_iter` puis se stabilise. Pour `z^3 - 2z + 2`, ce n'est donc pas un manque d'itérations : sur la droite réelle, en partant de 0, Newton tourne entre 0 et 1 (f(0) = 2 et f'(0) = -2 donnent 1, puis f(1) = 1 et f'(1) = 1 redonnent 0).

Quand il marche, Newton est bien plus rapide que la dichotomie (8 itérations contre 41 pour `z^3 - 1`), mais il peut échouer, alors que la dichotomie converge toujours si l'intervalle contient un changement de signe. Il faut donc connaître le polynôme avant de choisir la méthode.

Le test de résolution me rassure : la dimension varie très peu entre 1024 et 2048 pixels, donc ce n'est pas un artefact de la grille. De même, la tolérance de convergence ne change le bassin d'aucun pixel.

La dimension estimée de la frontière tombe entre 1,40 et 1,57, donc entre une ligne (1) et une surface (2), ce qui correspond à l'idée d'une frontière fractale. Je reste prudent : c'est une estimation par comptage de boîtes, pas une valeur exacte.

## Usage de l'IA

Je me suis aidé de claude afin de voir comment utiliser certaines partie du code afin de l'appliquer à mon projet, optimiser le code avec numpy et relire le README.
