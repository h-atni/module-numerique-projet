import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def f(z):
    return z ** 3 - 1.0


def df(z):
    return 3.0 * z ** 2


def newton_step(z):
    return z - f(z) / df(z)


def classify_point(z, tol=1e-6, max_iter=80):
    roots = [
        complex(1.0, 0.0),
        complex(-0.5, math.sqrt(3) / 2),
        complex(-0.5, -math.sqrt(3) / 2),
    ]
    for _ in range(max_iter):
        z = newton_step(z)
        for idx, r in enumerate(roots):
            if abs(z - r) < tol:
                return idx
    return -1

res = 600
x_min, x_max = -1.8, 1.8
y_min, y_max = -1.8, 1.8
xs = np.linspace(x_min, x_max, res)
ys = np.linspace(y_min, y_max, res)

image = np.empty((res, res), dtype=int)
for i, x in enumerate(xs):
    for j, y in enumerate(ys):
        z = complex(x, y)
        image[i, j] = classify_point(z)

plt.figure(figsize=(8, 8))
plt.imshow(np.flipud(image), cmap="tab10", extent=[x_min, x_max, y_min, y_max])
plt.title("Bassins d'attraction de Newton pour z^3 - 1")
plt.xlabel("Partie réelle")
plt.ylabel("Partie imaginaire")
plt.colorbar(label="Indice de la racine")
plt.tight_layout()

output = Path(__file__).with_name("newton_bassin.png")
plt.savefig(output, dpi=200)
print(f"Image sauvegardée dans : {output}")
