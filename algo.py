from typing import Final
import numpy as np


class Demoucron:
    def __init__(self, matrice: np.ndarray, choix: str):
        self._origin = np.copy(matrice)
        self._matrice = matrice
        self.choix = choix
        self.calculer()

    def entrer(self, k):
        """
        Récupération des indices de la colonne k
        """
        return [i for i, elem in enumerate(self._matrice[:, k]) if not np.isnan(elem)]

    def sortir(self, k):
        """
        Récupération des indices de la ligne k
        """
        return [i for i, elem in enumerate(self._matrice[k]) if not np.isnan(elem)]

    def calculer(self):
        for k in range(1, self.sommets-1):
            entrees = self.entrer(k)
            sorties = self.sortir(k)
            items = []
            for entree in entrees:
                self.set_items(k, entree, sorties, items)
            self.set_matrice(items)

    def set_matrice(self, items: list[tuple[int, int, int]]):
        for item in items:
            entree, sortie, distance = item
            self._matrice[entree, sortie] = distance

    def set_items(self, k: int, entree: np.float64, sorties: list[np.float64], items: list[tuple[int, int, int]]):
        entree_to_k = self._matrice[entree, k]
        for sortie in sorties:
            k_to_sortie = self._matrice[k, sortie]
            vecteur = self._matrice[entree, sortie]
            distance = self.distance(vecteur, entree_to_k, k_to_sortie)
            items.append((entree, sortie, distance))

    def distance(self, vecteur: np.float64, entree_to_k: np.float64, k_to_sortie: np.float64):
        somme = entree_to_k + k_to_sortie
        return somme if np.isnan(vecteur) else min(somme, vecteur)

    @property
    def minimiser(self):
        """
        Récupérer le tableau T de la colonne de line.
        Changer la valeur de line avec l'indice où
        est le plus petit valeur de la colonne du tableau T
        """
        line = self.sommets-1
        paths: list[int] = []
        paths.append(line)
        while line > 0:
            line = np.nanargmin(self._matrice[:, line])
            paths.append(int(line))
        paths.reverse()
        return paths
    
    @property
    def sommets(self):
        return self._matrice.shape[0]


matrix = np.array(
    [
    [None, 10, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 15, 8, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, 1, None, None, None, None, 16, None, None, None, None, None],
    [None, None, 8, None, 6, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, 1, None, None, None, None, None, None, None],
    [None, None, None, None, 5, None, 4, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, 1, None, None, 8, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, 3, None, 4, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, 7, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, 6, 12, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, 9, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, 3, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 3],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, 5, None, 6],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
], dtype=np.float64
)

expected_output = [0, 1, 3, 4, 8, 9, 11, 14, 15]
# Expected Distance parcourue : 51
# Result got : 57
demoucron = Demoucron(matrix, 'minimiser')
print(demoucron.minimiser == expected_output)