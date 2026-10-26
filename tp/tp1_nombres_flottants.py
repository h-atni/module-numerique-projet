import math
import sys
from fractions import Fraction

# -----------------------------------------------------------------------------
# 1. Entiers
# -----------------------------------------------------------------------------

quotient, reste = divmod(2026, 7)
print("Exercice 1.1")
print("quotient =", quotient)
print("reste =", reste)
print("Vérification :", quotient * 7 + reste == 2026)

n = 123456789
print("Exercice 1.2")
print("dernier chiffre =", n % 10)
print("sans dernier chiffre =", n // 10)

# -----------------------------------------------------------------------------
# 2. Flottants
# -----------------------------------------------------------------------------

s = 0.0
for _ in range(1000):
    s += 0.1
print("Exercice 2.1")
print("somme =", s)
print("écart avec 100 =", abs(s - 100.0))


def presque_egaux(a, b, tol=1e-9):
    return abs(a - b) <= tol

print("Exercice 2.2")
print("0.1 + 0.2 == 0.3 ?", (0.1 + 0.2) == 0.3)
print("presque_egaux(0.1 + 0.2, 0.3) =", presque_egaux(0.1 + 0.2, 0.3))

# -----------------------------------------------------------------------------
# 3. Conditions et boucles
# -----------------------------------------------------------------------------

print("Exercice 3.1")
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")

somme_boucle = 0
for i in range(1, 101):
    somme_boucle += i
print("Exercice 3.2")
print("somme_boucle =", somme_boucle)
print("formule =", 100 * 101 // 2)

# -----------------------------------------------------------------------------
# 4. Fonctions
# -----------------------------------------------------------------------------

def nombre_de_chiffres(n):
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    if n == 0:
        return 1
    c = 0
    while n > 0:
        n //= 10
        c += 1
    return c

print("Exercice 4.1")
print("nombre_de_chiffres(2026) =", nombre_de_chiffres(2026))
print("nombre_de_chiffres(7) =", nombre_de_chiffres(7))

# -----------------------------------------------------------------------------
# 5. Méthode de Héron
# -----------------------------------------------------------------------------

def heron(a, tol=1e-12, max_iter=50):
    x = a if a > 1 else 1.0
    for _ in range(max_iter):
        x_suivant = 0.5 * (x + a / x)
        if abs(x_suivant - x) < tol:
            return x_suivant
        x = x_suivant
    return x

print("Exercice 5.1")
print("heron(2) =", heron(2))
print("math.sqrt(2) =", math.sqrt(2))
print("écart =", abs(heron(2) - math.sqrt(2)))

# -----------------------------------------------------------------------------
# 6. Écriture binaire d'un entier
# -----------------------------------------------------------------------------

def vers_binaire(n):
    if n == 0:
        return "0"
    bits = []
    while n > 0:
        bits.append(str(n % 2))
        n //= 2
    return "".join(reversed(bits))

print("Exercice 6.1")
print("vers_binaire(37) =", vers_binaire(37))
print("vers_binaire(0) =", vers_binaire(0))

eps = 1.0
while 1.0 + eps / 2.0 != 1.0:
    eps /= 2.0
print("Exercice 6.2")
print("epsilon approximé =", eps)
print("sys.float_info.epsilon =", sys.float_info.epsilon)

# -----------------------------------------------------------------------------
# 7. Élimination catastrophique
# -----------------------------------------------------------------------------

def racines_naif(a, b, c):
    delta = b * b - 4 * a * c
    x1 = (-b + math.sqrt(delta)) / (2 * a)
    x2 = (-b - math.sqrt(delta)) / (2 * a)
    return x1, x2

print("Exercice 7.1")
a, b, c = 1.0, 1e8, 1.0
r1, r2 = racines_naif(a, b, c)
print("racines_naif =", r1, r2)
print("produit =", r1 * r2)


def racines_stables(a, b, c):
    delta = b * b - 4 * a * c
    sqrt_delta = math.sqrt(delta)
    x1 = (-b - sqrt_delta) / (2 * a)
    x2 = c / (a * x1)
    return x1, x2

print("Exercice 7.2")
print("racines_stables =", racines_stables(a, b, c))
print("Fraction(1,10) + Fraction(2,10) == Fraction(3,10) ?",
      Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))
print("Fraction(1,10) * 1000 =", sum(Fraction(1, 10) for _ in range(1000)))
