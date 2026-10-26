import time

# -----------------------------------------------------------------------------
# 1. Diviseurs
# -----------------------------------------------------------------------------

def diviseurs(n):
    resultat = []
    for d in range(1, n + 1):
        if n % d == 0:
            resultat.append(d)
    return resultat


def est_parfait(n):
    return sum(d for d in range(1, n) if n % d == 0) == n

print("Diviseurs de 28 :", diviseurs(28))
print("97 est-il premier ?", len(diviseurs(97)) == 2)
print("Nombres parfaits < 10000 :", [n for n in range(2, 10000) if est_parfait(n)])

# -----------------------------------------------------------------------------
# 2. PGCD
# -----------------------------------------------------------------------------

def pgcd_naif(a, b):
    meilleur = 1
    for d in range(1, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            meilleur = d
    return meilleur


def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

print("PGCD(1071, 462) =", pgcd(1071, 462))
print("PGCD naïf =", pgcd_naif(1071, 462))

# -----------------------------------------------------------------------------
# 3. Test de primalité et mesure de temps
# -----------------------------------------------------------------------------

def est_premier_naif(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True


def est_premier(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def duree(fonction, argument):
    debut = time.perf_counter()
    fonction(argument)
    return time.perf_counter() - debut

for n in (2, 1, 91, 97, 100003):
    print(n, est_premier(n))

for n in (10_007, 100_003, 1_000_003):
    t_naif = duree(est_premier_naif, n)
    t_rac = duree(est_premier, n)
    print(f"{n:>9} : naif {t_naif:.5f} s | racine {t_rac:.6f} s")

# -----------------------------------------------------------------------------
# 4. Crible d'Ératosthène
# -----------------------------------------------------------------------------

def crible(limite):
    est_premier_tab = [True] * (limite + 1)
    est_premier_tab[0] = False
    if limite >= 1:
        est_premier_tab[1] = False
    d = 2
    while d * d <= limite:
        if est_premier_tab[d]:
            for multiple in range(d * d, limite + 1, d):
                est_premier_tab[multiple] = False
        d += 1
    return [n for n in range(limite + 1) if est_premier_tab[n]]

premiers = crible(100)
print("Premiers <= 100 :", premiers)
print("Nombre de premiers <= 100 :", len(premiers))

# -----------------------------------------------------------------------------
# 5. Décomposition en facteurs premiers
# -----------------------------------------------------------------------------

def facteurs(n):
    resultat = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            resultat.append(d)
            n //= d
        d += 1
    if n > 1:
        resultat.append(n)
    return resultat

n = 360
f = facteurs(n)
print("Facteurs de 360 :", f)
print("Produit des facteurs :", __import__('functools').reduce(lambda x, y: x * y, f, 1))

# -----------------------------------------------------------------------------
# 6. Fibonacci récursif
# -----------------------------------------------------------------------------

def fibonacci_recursif(n):
    if n < 2:
        return n
    return fibonacci_recursif(n - 1) + fibonacci_recursif(n - 2)

for n in (20, 25, 30):
    print(f"Fibonacci récursif({n}) en {duree(fibonacci_recursif, n):.4f} s")

# -----------------------------------------------------------------------------
# 7. Euclide étendu
# -----------------------------------------------------------------------------

def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    g, u, v = euclide_etendu(b, a % b)
    return g, v, u - (a // b) * v

print("Euclide étendu(1071, 462) :", euclide_etendu(1071, 462))

# -----------------------------------------------------------------------------
# 8. Exponentiation rapide modulo n
# -----------------------------------------------------------------------------

def puissance_mod_naive(a, e, n):
    resultat = 1
    for _ in range(e):
        resultat = (resultat * a) % n
    return resultat


def puissance_mod(a, e, n):
    resultat = 1
    a %= n
    while e > 0:
        if e % 2 == 1:
            resultat = (resultat * a) % n
        a = (a * a) % n
        e //= 2
    return resultat


a, e, n = 7, 10 ** 7, 1_000_003
print("Puissance mod naïve :", puissance_mod_naive(a, e, n))
print("Puissance mod rapide :", puissance_mod(a, e, n))
print("pow Python :", pow(a, e, n))

print("TP2 terminé.")
