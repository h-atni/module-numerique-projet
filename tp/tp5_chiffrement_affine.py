import random
import unicodedata
from collections import Counter

# -----------------------------------------------------------------------------
# 1. Des lettres aux nombres et retour
# -----------------------------------------------------------------------------

def lettre_vers_nombre(c):
    """Numéro de 0 à 25 d'une lettre majuscule."""
    return ord(c) - ord("A")


def nombre_vers_lettre(n):
    """Lettre majuscule correspondant à un numéro de 0 à 25."""
    return chr(n % 26 + ord("A"))


def nettoyer(texte):
    """Majuscules sans accents, lettres A-Z uniquement."""
    sans_accent = unicodedata.normalize("NFD", texte)
    sans_accent = "".join(c for c in sans_accent if unicodedata.category(c) != "Mn")
    return "".join(c for c in sans_accent.upper() if "A" <= c <= "Z")

print("Conversion C ->", lettre_vers_nombre("C"))
print("Conversion 2 ->", nombre_vers_lettre(2))
print("Nettoyage :", nettoyer("Été, à Paris !"))

# -----------------------------------------------------------------------------
# 2. Chiffrement affine
# -----------------------------------------------------------------------------

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def chiffrer(texte, a, b):
    """Chiffrement affine de texte avec la clé (a, b)."""
    resultat = []
    for c in nettoyer(texte):
        x = lettre_vers_nombre(c)
        resultat.append(nombre_vers_lettre((a * x + b) % 26))
    return "".join(resultat)

message = "ATTAQUEALAUBE"
print("Chiffrement affine :", chiffrer(message, 5, 8))
print("Chiffre de César :", chiffrer(message, 1, 3))

# -----------------------------------------------------------------------------
# 3. Clés valides et inverse modulaire
# -----------------------------------------------------------------------------

valides = [a for a in range(1, 26) if pgcd(a, 26) == 1]
print("Clés utilisables modulo 26 :", valides)
print("Nombre de clés valides :", len(valides))


def inverse_modulaire(a, n):
    """Inverse de a modulo n, par recherche exhaustive."""
    a = a % n
    for candidat in range(1, n):
        if (a * candidat) % n == 1:
            return candidat
    raise ValueError(f"{a} n'est pas inversible modulo {n}")

print("Inverse de 5 modulo 26 :", inverse_modulaire(5, 26))
print("(5 * 21) % 26 =", (5 * 21) % 26)

# -----------------------------------------------------------------------------
# 4. Déchiffrement affine
# -----------------------------------------------------------------------------

def dechiffrer(texte, a, b):
    """Déchiffrement affine. Lève une erreur si la clé n'est pas inversible."""
    a_inverse = inverse_modulaire(a, 26)
    resultat = []
    for c in nettoyer(texte):
        y = lettre_vers_nombre(c)
        resultat.append(nombre_vers_lettre(a_inverse * (y - b) % 26))
    return "".join(resultat)

message_nettoye = nettoyer("Attaque a l aube")
secret = chiffrer(message_nettoye, 5, 8)
print("Message chiffré :", secret)
print("Message déchiffré :", dechiffrer(secret, 5, 8))
print("Aller-retour :", dechiffrer(secret, 5, 8) == message_nettoye)

try:
    dechiffrer(secret, 4, 7)
except ValueError as erreur:
    print("Clé invalide refusée :", erreur)

# -----------------------------------------------------------------------------
# 5. Force brute
# -----------------------------------------------------------------------------

def toutes_les_clefs(secret):
    """Tous les déchiffrements possibles, sous forme de triplets (a, b, texte)."""
    resultats = []
    for a in valides:
        for b in range(26):
            resultats.append((a, b, dechiffrer(secret, a, b)))
    return resultats

essais = toutes_les_clefs(secret)
print("Nombre de clés essayées :", len(essais))
print("Bonne clé trouvée :", next((e for e in essais if e[2] == message_nettoye), None))

# -----------------------------------------------------------------------------
# 6. Analyse de fréquences
# -----------------------------------------------------------------------------

def indice_coincidence(texte):
    """Probabilité que deux lettres tirées au hasard dans le texte coïncident."""
    N = len(texte)
    if N <= 1:
        return 0.0
    comptes = Counter(texte)
    return sum(n * (n - 1) for n in comptes.values()) / (N * (N - 1))


texte_long = nettoyer(
    "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
    "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
    "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
    "le code sans essayer toutes les clefs possibles."
)
secret_long = chiffrer(texte_long, 7, 12)
comptes = Counter(secret_long)
lettre_frequente = comptes.most_common(1)[0][0]
print("Lettre la plus fréquente du chiffré :", lettre_frequente)

cible = lettre_vers_nombre(lettre_frequente)
candidats = []
for a in valides:
    b = (cible - 4 * a) % 26
    candidats.append((a, b, dechiffrer(secret_long, a, b)))
print("Nombre de candidats :", len(candidats))
for a, b, texte in candidats:
    if texte.startswith("LECHIFFREMENT"):
        print("Candidat trouvé via fréquence :", a, b)
        print(texte[:60])
        break

# -----------------------------------------------------------------------------
# 7. Indice de coïncidence
# -----------------------------------------------------------------------------

random.seed(1)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
hasard = "".join(random.choice(alphabet) for _ in range(len(texte_long)))
print(f"Indice de coïncidence du texte clair : {indice_coincidence(texte_long):.4f}")
print(f"Indice de coïncidence du texte chiffré : {indice_coincidence(secret_long):.4f}")
print(f"Indice de coïncidence d'un texte aléatoire : {indice_coincidence(hasard):.4f}")

# -----------------------------------------------------------------------------
# 8. Chiffre de Vigenère
# -----------------------------------------------------------------------------

def vigenere(texte, cle):
    """Chiffre de Vigenère : chaque lettre est décalée par la lettre de la clé en face."""
    resultat = []
    for i, c in enumerate(nettoyer(texte)):
        decalage = lettre_vers_nombre(cle[i % len(cle)])
        resultat.append(nombre_vers_lettre(lettre_vers_nombre(c) + decalage))
    return "".join(resultat)

secret_vigenere = vigenere(texte_long, "CLE")
print("Vigenère (début) :", secret_vigenere[:40])
print(f"Indice de coïncidence Vigenère : {indice_coincidence(secret_vigenere):.4f}")

# Séparation en colonnes pour retrouver la longueur de la clé
for L in range(1, 8):
    colonnes = [secret_vigenere[i::L] for i in range(L)]
    moyenne = sum(indice_coincidence(col) for col in colonnes) / L
    print(f"Longueur L = {L} : indice moyen {moyenne:.4f}")

print("TP5 terminé.")
