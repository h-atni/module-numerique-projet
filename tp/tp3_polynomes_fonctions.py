import math

# -----------------------------------------------------------------------------
# 1. Évaluation d'un polynôme
# -----------------------------------------------------------------------------

def evaluer_naif(P, x):
    total = 0
    for i in range(len(P)):
        total += P[i] * x ** i
    return total


def evaluer(P, x):
    total = 0
    for coefficient in reversed(P):
        total = total * x + coefficient
    return total

P = [2, 3, 0, 5]
print("Évaluation naïve en x=2 :", evaluer_naif(P, 2))
print("Évaluation Horner en x=2 :", evaluer(P, 2))
for x in (-2, 0, 1, 2, 10):
    print(f"x={x} : {evaluer_naif(P, x)} | {evaluer(P, x)}")

# -----------------------------------------------------------------------------
# 2. Dérivation d'un polynôme
# -----------------------------------------------------------------------------

def deriver(P):
    if len(P) <= 1:
        return []
    return [i * P[i] for i in range(1, len(P))]

print("Dérivée de [2, 3, 0, 5] :", deriver(P))

# -----------------------------------------------------------------------------
# 3. Dichotomie
# -----------------------------------------------------------------------------

def dichotomie(f, a, b, tolerance=1e-12):
    fa, fb = f(a), f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("f(a) et f(b) doivent être de signes opposés")
    while b - a > tolerance:
        milieu = (a + b) / 2
        fm = f(milieu)
        if f(a) * fm <= 0:
            b = milieu
        else:
            a = milieu
    return (a + b) / 2


def carre_moins_deux(x):
    return x * x - 2

print("Racine de x^2 - 2 par dichotomie :", dichotomie(carre_moins_deux, 0, 2))

# -----------------------------------------------------------------------------
# 4. Méthode de Newton
# -----------------------------------------------------------------------------

def newton(P, depart, tolerance=1e-12, tours_max=100):
    derivee = deriver(P)
    x = float(depart)
    for tour in range(tours_max):
        valeur = evaluer(P, x)
        pente = evaluer(derivee, x)
        if pente == 0:
            raise ZeroDivisionError("Tangente horizontale")
        suivant = x - valeur / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            return suivant, tour + 1
        x = suivant
    raise RuntimeError(f"Pas de convergence en {tours_max} tours")

Q = [-5, -2, 0, 1]
print("Newton sur x^3 - 2x - 5 depuis 2 :", newton(Q, 2))

# -----------------------------------------------------------------------------
# 5. Somme et produit de polynômes
# -----------------------------------------------------------------------------

def somme(P, Q):
    n = max(len(P), len(Q))
    P = P + [0] * (n - len(P))
    Q = Q + [0] * (n - len(Q))
    return [P[i] + Q[i] for i in range(n)]


def produit_poly(P, Q):
    if not P or not Q:
        return []
    R = [0] * (len(P) + len(Q) - 1)
    for i in range(len(P)):
        for j in range(len(Q)):
            R[i + j] += P[i] * Q[j]
    return R

print("Somme de [1,2] et [0,0,3] :", somme([1, 2], [0, 0, 3]))
print("Produit (x+1)^2 :", produit_poly([1, 1], [1, 1]))

# -----------------------------------------------------------------------------
# 6. Dérivées numériques
# -----------------------------------------------------------------------------

def derivee_avant(f, x, h):
    return (f(x + h) - f(x)) / h


def derivee_centree(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

exacte = math.cos(1.0)
for h in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12):
    e_avant = abs(derivee_avant(math.sin, 1.0, h) - exacte)
    e_centree = abs(derivee_centree(math.sin, 1.0, h) - exacte)
    print(f"h = {h:.0e} : avant {e_avant:.1e} | centree {e_centree:.1e}")

# -----------------------------------------------------------------------------
# 7. Intégration numérique
# -----------------------------------------------------------------------------

def rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))


def trapezes(f, a, b, n):
    h = (b - a) / n
    interieur = sum(f(a + i * h) for i in range(1, n))
    return h * ((f(a) + f(b)) / 2 + interieur)


def simpson(f, a, b, n):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    impairs = sum(f(a + i * h) for i in range(1, n, 2))
    pairs = sum(f(a + i * h) for i in range(2, n, 2))
    return h / 3 * (f(a) + f(b) + 4 * impairs + 2 * pairs)


def carre(x):
    return x * x

for n in (10, 100, 1000):
    e_rect = abs(rectangles(carre, 0, 1, n) - 1 / 3)
    e_trap = abs(trapezes(carre, 0, 1, n) - 1 / 3)
    e_simp = abs(simpson(carre, 0, 1, n) - 1 / 3)
    print(f"n = {n:>4} : rectangles {e_rect:.1e} | trapezes {e_trap:.1e} | simpson {e_simp:.1e}")

print("TP3 terminé.")
