"""Bassins d'attraction de Newton dans le plan complexe.

Le script :
  1. calcule, pour plusieurs polynômes, la racine atteinte et le nombre
     d'itérations nécessaires depuis chaque point du plan ;
  2. repère les points qui ne convergent pas (cycles, divergence) ;
  3. mesure l'effet du nombre maximal d'itérations sur ces points ;
  4. estime la dimension de la frontière entre bassins (comptage de boîtes) ;
  5. compare Newton et dichotomie sur la droite réelle.

Lancement :  python3 newton_basins.py
Sorties   :  images .png et fichier resultats.txt dans le dossier projet/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DOSSIER = Path(__file__).parent

# Polynômes étudiés : coefficients par degré décroissant (convention de Horner).
POLYNOMES = {
    "z^3 - 1": [1, 0, 0, -1],
    "z^4 - 1": [1, 0, 0, 0, -1],
    "z^3 - 2z + 2": [1, 0, -2, 2],
}


# ---------------------------------------------------------------------------
# Polynômes : Horner et dérivée (écrits à la main, comme en TP3)
# ---------------------------------------------------------------------------

def horner(coeffs, z):
    """Évalue le polynôme en z (z peut être un tableau numpy complexe)."""
    resultat = np.zeros_like(z, dtype=complex)
    for c in coeffs:
        resultat = resultat * z + c
    return resultat


def derivee(coeffs):
    """Coefficients de la dérivée."""
    n = len(coeffs) - 1
    return [c * (n - i) for i, c in enumerate(coeffs[:-1])]


def racines_reference(coeffs):
    """Racines de référence, uniquement pour classer les points.

    On utilise np.roots comme point de comparaison, pas comme moteur de
    la recherche : les itérations de Newton sont faites ci-dessous.
    """
    return np.roots(coeffs)


# ---------------------------------------------------------------------------
# Itération de Newton vectorisée
# ---------------------------------------------------------------------------

def grille(demi_largeur=2.0, res=600, centre=0j):
    x = np.linspace(centre.real - demi_largeur, centre.real + demi_largeur, res)
    y = np.linspace(centre.imag - demi_largeur, centre.imag + demi_largeur, res)
    return x[None, :] + 1j * y[:, None]


def newton_plan(coeffs, z0, tol=1e-8, max_iter=60):
    """Applique Newton à tous les points z0 en même temps.

    Renvoie (indice de racine, nombre d'itérations) ; indice = -1 si le
    point n'a pas convergé après max_iter itérations.
    """
    p = coeffs
    dp = derivee(coeffs)
    racines = racines_reference(coeffs)
    z = z0.copy()
    indice = -np.ones(z.shape, dtype=int)
    iterations = np.full(z.shape, max_iter, dtype=int)
    actif = np.ones(z.shape, dtype=bool)

    with np.errstate(all="ignore"):
        for k in range(1, max_iter + 1):
            d = horner(dp, z[actif])
            z[actif] = z[actif] - horner(p, z[actif]) / d
            # on classe les points qui viennent d'arriver près d'une racine
            for i, r in enumerate(racines):
                proche = actif & (np.abs(z - r) < tol)
                indice[proche] = i
                iterations[proche] = k
                actif &= ~proche
            # les points devenus nan/inf (dérivée nulle) sont abandonnés
            actif &= np.isfinite(z)
            if not actif.any():
                break
    return indice, iterations, racines


# ---------------------------------------------------------------------------
# Frontière et comptage de boîtes
# ---------------------------------------------------------------------------

def frontiere(indice):
    """Pixels dont au moins un voisin (4-connexité) est dans un autre bassin."""
    f = np.zeros(indice.shape, dtype=bool)
    f[:-1, :] |= indice[:-1, :] != indice[1:, :]
    f[1:, :] |= indice[:-1, :] != indice[1:, :]
    f[:, :-1] |= indice[:, :-1] != indice[:, 1:]
    f[:, 1:] |= indice[:, :-1] != indice[:, 1:]
    return f


def dimension_boites(masque, tailles=(2, 4, 8, 16, 32, 64)):
    """Estime la dimension de la frontière par comptage de boîtes.

    Pour chaque taille s, on compte N(s) boîtes s x s contenant au moins
    un pixel de frontière. La pente de log N(s) en fonction de log(1/s)
    estime la dimension. Renvoie (dimension, tailles, comptes).
    """
    n = masque.shape[0]
    comptes = []
    for s in tailles:
        m = (n // s) * s
        blocs = masque[:m, :m].reshape(m // s, s, m // s, s).any(axis=(1, 3))
        comptes.append(blocs.sum())
    pente, _ = np.polyfit(np.log(1.0 / np.array(tailles)), np.log(comptes), 1)
    return pente, tailles, comptes


# ---------------------------------------------------------------------------
# Newton contre dichotomie sur la droite réelle
# ---------------------------------------------------------------------------

def newton_reel(coeffs, x0, tol=1e-10, max_iter=100):
    """Newton réel. Renvoie (x, nb d'itérations, convergé ?)."""
    dp = derivee(coeffs)
    x = complex(x0)
    for k in range(1, max_iter + 1):
        d = horner(dp, np.array(x))
        if d == 0:
            return x.real, k, False
        x_new = x - horner(coeffs, np.array(x)) / d
        if abs(x_new - x) < tol:
            return x_new.real, k, True
        x = x_new
    return x.real, max_iter, False


def dichotomie(coeffs, a, b, tol=1e-10):
    """Dichotomie sur [a, b] ; suppose un changement de signe."""
    fa = horner(coeffs, np.array(a)).real
    k = 0
    while b - a > tol:
        k += 1
        m = (a + b) / 2
        fm = horner(coeffs, np.array(m)).real
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return (a + b) / 2, k


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------

def main():
    lignes = []

    def log(texte=""):
        print(texte)
        lignes.append(texte)

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    bilan_frontiere = {}

    for col, (nom, coeffs) in enumerate(POLYNOMES.items()):
        z0 = grille(2.0, 600)
        indice, iters, racines = newton_plan(coeffs, z0)
        ext = [-2, 2, -2, 2]

        # Ligne 1 : bassins (couleur = racine, -1 en noir)
        couleurs = np.where(indice < 0, np.nan, indice)
        axes[0, col].imshow(couleurs, origin="lower", extent=ext, cmap="viridis")
        axes[0, col].imshow(np.where(indice < 0, 1.0, np.nan), origin="lower",
                            extent=ext, cmap="gray_r", vmin=0, vmax=1)
        axes[0, col].set_title(f"Bassins : {nom}")
        # Ligne 2 : nombre d'itérations
        im = axes[1, col].imshow(iters, origin="lower", extent=ext, cmap="magma")
        axes[1, col].set_title("Itérations avant convergence")
        fig.colorbar(im, ax=axes[1, col], shrink=0.8)

        non_conv = np.mean(indice < 0)
        log(f"== {nom} ==")
        log(f"racines (référence) : {np.round(racines, 4)}")
        log(f"points non convergés : {100 * non_conv:.2f} %")
        log(f"itérations moyennes (points convergés) : "
            f"{iters[indice >= 0].mean():.2f}")

        # Effet du nombre maximal d'itérations sur les points non convergés
        for mi in (30, 60, 200, 1000):
            ind_m, _, _ = newton_plan(coeffs, z0, max_iter=mi)
            log(f"  max_iter={mi:4d} -> non convergés : {100 * np.mean(ind_m < 0):.2f} %")

        # Dimension de la frontière (résolution plus fine)
        z_fin = grille(2.0, 2048)
        ind_fin, _, _ = newton_plan(coeffs, z_fin)
        dim, tailles, comptes = dimension_boites(frontiere(ind_fin))
        bilan_frontiere[nom] = (tailles, comptes)
        log(f"dimension estimée de la frontière (comptage de boîtes) : {dim:.3f}")
        log()

    for ax in axes.ravel():
        ax.set_xlabel("Re")
        ax.set_ylabel("Im")
    fig.tight_layout()
    fig.savefig(DOSSIER / "bassins.png", dpi=130)
    plt.close(fig)

    # Droite log-log du comptage de boîtes
    fig, ax = plt.subplots(figsize=(6, 5))
    for nom, (tailles, comptes) in bilan_frontiere.items():
        ax.loglog(1 / np.array(tailles), comptes, "o-", label=nom)
    ax.set_xlabel("1 / taille de boîte")
    ax.set_ylabel("N(boîtes touchant la frontière)")
    ax.set_title("Comptage de boîtes")
    ax.legend()
    fig.tight_layout()
    fig.savefig(DOSSIER / "comptage_boites.png", dpi=130)
    plt.close(fig)

    # Newton contre dichotomie : cas favorable puis cas où Newton échoue
    log("== Newton contre dichotomie (droite réelle) ==")
    cas = [
        ("z^3 - 1", [1, 0, 0, -1], 0.5, (0.0, 2.0)),
        ("z^3 - 2z + 2", [1, 0, -2, 2], 0.0, (-3.0, 0.0)),
    ]
    for nom, coeffs, x0, (a, b) in cas:
        xn, kn, ok = newton_reel(coeffs, x0)
        xd, kd = dichotomie(coeffs, a, b)
        etat = "converge" if ok else "ECHEC (cycle ou dérivée nulle)"
        log(f"{nom} : Newton depuis x0={x0} -> {etat} en {kn} itérations ; "
            f"dichotomie sur [{a}, {b}] -> {xd:.8f} en {kd} itérations")
    log()

    (DOSSIER / "resultats.txt").write_text("\n".join(lignes), encoding="utf-8")


if __name__ == "__main__":
    main()
