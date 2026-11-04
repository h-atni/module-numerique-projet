"""Bassins d'attraction de Newton dans le plan complexe.

  python newton_basins.py             calcul complet
  python newton_basins.py --rapide    résolutions réduites, pour tester
  python newton_basins.py --afficher  ouvre aussi les figures

Sorties : bassins.png, comptage_boites.png, resultats.txt
"""

import sys
import time
from pathlib import Path

import matplotlib

AFFICHER = "--afficher" in sys.argv
if not AFFICHER:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DOSSIER = Path(__file__).parent

RAPIDE = "--rapide" in sys.argv
RES = 300 if RAPIDE else 600
RES_FIN = 512 if RAPIDE else 2048
MAX_ITER = 1000
SEUILS = (30, 60, 200, 1000)
MAX_AFFICHAGE = 60

# P[i] = coefficient de x^i (convention du TP3)
POLYNOMES = {
    "z^3 - 1": [-1, 0, 0, 1],
    "z^4 - 1": [-1, 0, 0, 0, 1],
    "z^3 - 2z + 2": [2, -2, 0, 1],
}


def evaluer(P, x):
    total = 0
    for coefficient in reversed(P):
        total = total * x + coefficient
    return total


def deriver(P):
    if len(P) <= 1:
        return []
    return [i * P[i] for i in range(1, len(P))]


def racines_reference(P):
    return np.roots(P[::-1])


def grille(demi_largeur=2.0, res=600):
    x = np.linspace(-demi_largeur, demi_largeur, res)
    return x[None, :] + 1j * x[:, None]


def newton_plan(P, z0, tol=1e-8, max_iter=60):
    """Renvoie (indice de racine, itérations, racines) ; indice = -1 si non convergé."""
    dP = deriver(P)
    racines = racines_reference(P)
    forme = z0.shape
    indice = np.full(z0.size, -1, dtype=int)
    iterations = np.full(z0.size, max_iter, dtype=int)
    actifs = np.arange(z0.size)
    z = z0.ravel().astype(complex)

    with np.errstate(all="ignore"):
        for k in range(1, max_iter + 1):
            z = z - evaluer(P, z) / evaluer(dP, z)
            fini = ~np.isfinite(z)
            for i, r in enumerate(racines):
                proche = (np.abs(z - r) < tol) & ~fini
                indice[actifs[proche]] = i
                iterations[actifs[proche]] = k
                fini |= proche
            actifs, z = actifs[~fini], z[~fini]
            if actifs.size == 0:
                break
    return indice.reshape(forme), iterations.reshape(forme), racines


def frontiere(indice):
    f = np.zeros(indice.shape, dtype=bool)
    haut_bas = indice[:-1, :] != indice[1:, :]
    gauche_droite = indice[:, :-1] != indice[:, 1:]
    f[:-1, :] |= haut_bas
    f[1:, :] |= haut_bas
    f[:, :-1] |= gauche_droite
    f[:, 1:] |= gauche_droite
    return f


def dimension_boites(masque):
    """Dimension de la frontière : pente de log N(s) en fonction de log(1/s)."""
    n = masque.shape[0]
    kmax = int(np.log2(n)) - 5
    tailles = [2 ** k for k in range(2, kmax + 1)]
    comptes = []
    for s in tailles:
        m = (n // s) * s
        blocs = masque[:m, :m].reshape(m // s, s, m // s, s).any(axis=(1, 3))
        comptes.append(int(blocs.sum()))
    pente, _ = np.polyfit(np.log(1.0 / np.array(tailles)), np.log(comptes), 1)
    return pente, tailles, comptes


def newton(P, depart, tolerance=1e-12, tours_max=100):
    derivee = deriver(P)
    x = float(depart)
    for tour in range(tours_max):
        valeur = evaluer(P, x)
        pente = evaluer(derivee, x)
        if pente == 0:
            raise ZeroDivisionError("tangente horizontale")
        suivant = x - valeur / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            return suivant, tour + 1
        x = suivant
    raise RuntimeError(f"pas de convergence en {tours_max} tours (cycle ?)")


def dichotomie(f, a, b, tolerance=1e-12):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) et f(b) doivent être de signes opposés")
    tours = 0
    while b - a > tolerance:
        tours += 1
        milieu = (a + b) / 2
        fm = f(milieu)
        if fa * fm <= 0:
            b = milieu
        else:
            a, fa = milieu, fm
    return (a + b) / 2, tours


def comparer(nom, P, x0, a, b):
    try:
        xn, kn = newton(P, x0)
        texte_newton = f"Newton depuis x0={x0} -> {xn:.8f} en {kn} itérations"
    except (ZeroDivisionError, RuntimeError) as erreur:
        texte_newton = f"Newton depuis x0={x0} -> ECHEC ({erreur})"
    xd, kd = dichotomie(lambda x: evaluer(P, x), a, b)
    return (f"{nom} : {texte_newton} ; "
            f"dichotomie sur [{a}, {b}] -> {xd:.8f} en {kd} itérations")


def main():
    lignes = []

    def log(texte=""):
        print(texte, flush=True)
        lignes.append(texte)

    debut_total = time.perf_counter()
    log(f"Mode {'rapide' if RAPIDE else 'complet'} : "
        f"images {RES}x{RES}, frontière {RES_FIN}x{RES_FIN}")
    log()

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    bilan_frontiere = {}
    ext = [-2, 2, -2, 2]
    cmap_bassins = plt.get_cmap("viridis").copy()
    cmap_bassins.set_bad("black")

    for col, (nom, P) in enumerate(POLYNOMES.items()):
        t0 = time.perf_counter()

        # un seul calcul à max_iter=1000 ; les autres seuils s'en déduisent
        indice, iters, racines = newton_plan(P, grille(2.0, RES), max_iter=MAX_ITER)
        converge = (indice >= 0) & (iters <= MAX_AFFICHAGE)
        indice_aff = np.where(converge, indice, -1)
        iters_aff = np.minimum(iters, MAX_AFFICHAGE)

        axes[0, col].imshow(np.ma.masked_where(indice_aff < 0, indice_aff),
                            origin="lower", extent=ext, cmap=cmap_bassins)
        axes[0, col].set_title(f"Bassins : {nom}")
        im = axes[1, col].imshow(iters_aff, origin="lower", extent=ext, cmap="magma")
        axes[1, col].set_title("Itérations avant convergence")
        fig.colorbar(im, ax=axes[1, col], shrink=0.8)

        log(f"== {nom} ==")
        log(f"racines (référence) : {np.round(racines, 4)}")
        log(f"points non convergés (max_iter={MAX_AFFICHAGE}) : "
            f"{100 * np.mean(~converge):.2f} %")
        log(f"itérations moyennes (points convergés) : {iters[converge].mean():.2f}")

        for mi in SEUILS:
            non_conv = np.mean(~((indice >= 0) & (iters <= mi)))
            log(f"  max_iter={mi:4d} -> non convergés : {100 * non_conv:.2f} %")

        ind_fin, _, _ = newton_plan(P, grille(2.0, RES_FIN), max_iter=MAX_AFFICHAGE)
        dim, tailles, comptes = dimension_boites(frontiere(ind_fin))
        bilan_frontiere[nom] = (tailles, comptes)
        log(f"dimension estimée de la frontière (comptage de boîtes) : {dim:.3f}")
        log(f"(durée : {time.perf_counter() - t0:.1f} s)")
        log()

    for ax in axes.ravel():
        ax.set_xlabel("Re")
        ax.set_ylabel("Im")
    fig.tight_layout()
    fig.savefig(DOSSIER / "bassins.png", dpi=130)

    fig2, ax = plt.subplots(figsize=(6, 5))
    for nom, (tailles, comptes) in bilan_frontiere.items():
        ax.loglog(1 / np.array(tailles), comptes, "o-", label=nom)
    ax.set_xlabel("1 / taille de boîte")
    ax.set_ylabel("N(boîtes touchant la frontière)")
    ax.set_title("Comptage de boîtes")
    ax.legend()
    fig2.tight_layout()
    fig2.savefig(DOSSIER / "comptage_boites.png", dpi=130)

    log("== Newton contre dichotomie (droite réelle) ==")
    log(comparer("z^3 - 1", POLYNOMES["z^3 - 1"], 0.5, 0.0, 2.0))
    log(comparer("z^3 - 2z + 2", POLYNOMES["z^3 - 2z + 2"], -2.0, -3.0, 0.0))
    log(comparer("z^3 - 2z + 2", POLYNOMES["z^3 - 2z + 2"], 0.0, -3.0, 0.0))
    log()
    log(f"Durée totale : {time.perf_counter() - debut_total:.1f} s")

    (DOSSIER / "resultats.txt").write_text("\n".join(lignes), encoding="utf-8")

    if AFFICHER:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main()
