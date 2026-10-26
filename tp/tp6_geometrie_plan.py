import math
import random

# -----------------------------------------------------------------------------
# 1. Points, vecteurs, produit scalaire, norme, angle
# -----------------------------------------------------------------------------

def vecteur(A, B):
    """Vecteur AB, de A vers B."""
    return (B[0] - A[0], B[1] - A[1])


def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]


def norme(u):
    return math.hypot(u[0], u[1])


def angle(u, v):
    """Angle non orienté entre u et v, en degrés."""
    cosinus = produit_scalaire(u, v) / (norme(u) * norme(v))
    cosinus = max(-1.0, min(1.0, cosinus))
    return math.degrees(math.acos(cosinus))


def determinant(u, v):
    """Déterminant de (u, v), aire orientée du parallélogramme."""
    return u[0] * v[1] - u[1] * v[0]


def distance_point_droite(P, A, B):
    AB = vecteur(A, B)
    AP = vecteur(A, P)
    return abs(determinant(AB, AP)) / norme(AB)

print("norme((3,4)) =", norme((3, 4)))
print("produit_scalaire((1,2),(3,4)) =", produit_scalaire((1, 2), (3, 4)))
print("angle((1,0),(1,1)) =", angle((1, 0), (1, 1)))
print("angle((1,0),(0,1)) =", angle((1, 0), (0, 1)))
print("distance du point (3,4) à l'axe x =", distance_point_droite((3, 4), (0, 0), (1, 0)))

# -----------------------------------------------------------------------------
# 2. Orientation et aire d'un polygone
# -----------------------------------------------------------------------------

def orientation(A, B, C):
    """1 si A -> B -> C tourne à gauche, -1 à droite, 0 si alignés."""
    d = determinant(vecteur(A, B), vecteur(A, C))
    if d > 0:
        return 1
    if d < 0:
        return -1
    return 0


def aire(polygone):
    """Aire d'un polygone simple donné par ses sommets dans l'ordre."""
    somme = 0
    n = len(polygone)
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        somme += x1 * y2 - x2 * y1
    return abs(somme) / 2

print("orientation((0,0),(1,0),(1,1)) =", orientation((0, 0), (1, 0), (1, 1)))
print("orientation((0,0),(1,0),(1,-1)) =", orientation((0, 0), (1, 0), (1, -1)))
print("orientation((0,0),(1,1),(2,2)) =", orientation((0, 0), (1, 1), (2, 2)))

carre = [(0, 0), (1, 0), (1, 1), (0, 1)]
triangle = [(0, 0), (4, 0), (0, 3)]
maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
print("aire(carre) =", aire(carre))
print("aire(triangle) =", aire(triangle))
print("aire(maison) =", aire(maison))

# -----------------------------------------------------------------------------
# 3. Intersection de segments
# -----------------------------------------------------------------------------

def se_coupent(A, B, C, D):
    """Vrai si les segments [AB] et [CD] se croisent franchement.

    Cas dégénérés (trois points alignés) -> False.
    """
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    return o1 * o2 < 0 and o3 * o4 < 0


def intersection(A, B, C, D):
    """Point d'intersection des segments [AB] et [CD], ou None."""
    AB = vecteur(A, B)
    CD = vecteur(C, D)
    denominateur = determinant(AB, CD)
    if abs(denominateur) < 1e-12:
        return None
    AC = vecteur(A, C)
    t = determinant(AC, CD) / denominateur
    u = determinant(AC, AB) / denominateur
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (A[0] + t * AB[0], A[1] + t * AB[1])
    return None

print("Diagonales du carré unité se coupent ?", se_coupent((0, 0), (1, 1), (0, 1), (1, 0)))
print("Point d'intersection :", intersection((0, 0), (2, 2), (0, 2), (2, 0)))

# -----------------------------------------------------------------------------
# 4. Point dans un polygone (lancer de rayon)
# -----------------------------------------------------------------------------

def dedans(P, polygone):
    """Vrai si P est à l'intérieur du polygone, par lancer de rayon horizontal."""
    x, y = P
    n = len(polygone)
    interieur = False
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_croisement:
                interieur = not interieur
    return interieur

maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
for P in ((1, 1), (1, 2.4), (3, 1), (0.2, 2.2)):
    print(P, "dans la maison ?", dedans(P, maison))

# -----------------------------------------------------------------------------
# 5. Estimation par Monte-Carlo
# -----------------------------------------------------------------------------

random.seed(0)
tirages = 200_000
touches = 0
for _ in range(tirages):
    P = (random.uniform(0, 2), random.uniform(0, 2.5))
    if dedans(P, maison):
        touches += 1

print("Estimation Monte-Carlo de l'aire de la maison :", (2 * 2.5) * touches / tirages)

# -----------------------------------------------------------------------------
# 6. Tracé simple (optionnel)
# -----------------------------------------------------------------------------

try:
    import matplotlib.pyplot as plt

    def tracer_polygone(polygone, points=()):
        xs = [s[0] for s in polygone] + [polygone[0][0]]
        ys = [s[1] for s in polygone] + [polygone[0][1]]
        plt.figure(figsize=(5, 5))
        plt.plot(xs, ys, color="black")
        for P in points:
            couleur = "green" if dedans(P, polygone) else "red"
            plt.scatter([P[0]], [P[1]], color=couleur)
        plt.axis("equal")
        plt.title("Vert : dedans, rouge : dehors")
        plt.show()

    random.seed(1)
    nuage = [(random.uniform(-0.5, 2.5), random.uniform(-0.5, 3)) for _ in range(60)]
    tracer_polygone(maison, nuage)
except Exception:
    pass

print("TP6 terminé.")
