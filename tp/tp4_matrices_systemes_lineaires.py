import random
import time
import numpy as np

# -----------------------------------------------------------------------------
# 1. Représentation des matrices
# -----------------------------------------------------------------------------

A = [[1, 2, 2],
     [1, 3, -2],
     [3, 5, 8]]

print("A[0] =", A[0])
print("A[0][2] =", A[0][2])


def transposee(A):
    lignes = len(A)
    colonnes = len(A[0])
    return [[A[i][j] for i in range(lignes)] for j in range(colonnes)]

print("Transposée de A :")
for ligne in transposee(A):
    print(ligne)

# -----------------------------------------------------------------------------
# 2. Produit matriciel en Python pur
# -----------------------------------------------------------------------------

def produit(A, B):
    n, p = len(A), len(A[0])
    if len(B) != p:
        raise ValueError("dimensions incompatibles")
    q = len(B[0])
    C = [[0] * q for _ in range(n)]
    for i in range(n):
        for j in range(q):
            somme = 0
            for k in range(p):
                somme += A[i][k] * B[k][j]
            C[i][j] = somme
    return C

identite = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
print("A * I =", produit(A, identite))


def matrice_aleatoire(n):
    return [[random.random() for _ in range(n)] for _ in range(n)]

for n in (40, 80, 120):
    M1 = matrice_aleatoire(n)
    M2 = matrice_aleatoire(n)
    debut = time.perf_counter()
    produit(M1, M2)
    print(f"n = {n:>3} : {time.perf_counter() - debut:.4f} s")

# -----------------------------------------------------------------------------
# 3. NumPy
# -----------------------------------------------------------------------------

A_np = np.array([[1.0, 2.0, 2.0],
                 [1.0, 3.0, -2.0],
                 [3.0, 5.0, 8.0]])
b = np.array([2.0, -1.0, 8.0])
print("A_np.shape =", A_np.shape)
print("A_np.T =\n", A_np.T)
print("A_np @ A_np =\n", A_np @ A_np)
print("A_np * A_np =\n", A_np * A_np)

# -----------------------------------------------------------------------------
# 4. Pivot de Gauss avec pivot partiel
# -----------------------------------------------------------------------------

def resoudre(A, b, tolerance=1e-14):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]

    for k in range(n):
        meilleure = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[meilleure][k]) <= tolerance:
            raise ValueError("système singulier ou mal posé")
        M[k], M[meilleure] = M[meilleure], M[k]

        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] = M[i][j] - facteur * M[k][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        somme = M[i][n]
        for j in range(i + 1, n):
            somme = somme - M[i][j] * x[j]
        x[i] = somme / M[i][i]
    return x

A_systeme = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
b_systeme = [2, -1, 8]
print("Solution du système =", resoudre(A_systeme, b_systeme))

# -----------------------------------------------------------------------------
# 5. Pourquoi on n'inverse jamais une matrice
# -----------------------------------------------------------------------------

def hilbert(n):
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])

n = 12
H = hilbert(n)
x_vrai = np.ones(n)
b = H @ x_vrai
x_solve = np.linalg.solve(H, b)
x_inverse = np.linalg.inv(H) @ b
print("erreur solve :", float(np.max(np.abs(x_solve - x_vrai))))
print("erreur inv @ b :", float(np.max(np.abs(x_inverse - x_vrai))))
print("conditionnement :", float(np.linalg.cond(H)))

# -----------------------------------------------------------------------------
# 6. Géométrie : transformation plane
# -----------------------------------------------------------------------------

def rotation(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]])

maison = np.array([[0, 0], [2, 0], [2, 1.5], [1, 2.5], [0, 1.5], [0, 0]]).T
print("Maison :\n", maison)

# -----------------------------------------------------------------------------
# 7. Déterminant par Gauss
# -----------------------------------------------------------------------------

def determinant(A):
    n = len(A)
    M = [list(ligne) for ligne in A]
    det = 1.0
    for k in range(n):
        meilleure = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[meilleure][k]) < 1e-14:
            return 0.0
        if meilleure != k:
            M[k], M[meilleure] = M[meilleure], M[k]
            det = -det
        det *= M[k][k]
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] = M[i][j] - facteur * M[k][j]
    return det

print("Déterminant(A) =", determinant(A_systeme))
print("np.linalg.det(A) =", float(np.linalg.det(np.array(A_systeme, dtype=float))))

print("TP4 terminé.")
