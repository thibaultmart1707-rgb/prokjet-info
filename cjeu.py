from cpiece import *
from cechiquier import *
from cinterface import *

def initialiser_plateau():
    """
    Initialise le plateau avec la position réglementaire des pièces au début d'une partie.
    -return: Instance de la classe Echiquier complètement initialisée.
    """
    plateau = Echiquier()

    plateau.grille[0][0] = Tour("blanc", (0, 0))
    plateau.grille[0][1] = Cavalier("blanc", (0, 1))
    plateau.grille[0][2] = Fou("blanc", (0, 2))
    plateau.grille[0][4] = Reine("blanc", (0, 4))
    plateau.grille[0][3] = Roi("blanc", (0, 3))
    plateau.grille[0][5] = Fou("blanc", (0, 5))
    plateau.grille[0][6] = Cavalier("blanc", (0, 6))
    plateau.grille[0][7] = Tour("blanc", (0, 7))

    for col in range(8):
        plateau.grille[1][col] = Pion("blanc", (1, col))
    
    plateau.grille[7][0] = Tour("noir", (7, 0))
    plateau.grille[7][1] = Cavalier("noir", (7, 1))
    plateau.grille[7][2] = Fou("noir", (7, 2))
    plateau.grille[7][4] = Reine("noir", (7, 4))
    plateau.grille[7][3] = Roi("noir", (7, 3))
    plateau.grille[7][5] = Fou("noir", (7, 5))
    plateau.grille[7][6] = Cavalier("noir", (7, 6))
    plateau.grille[7][7] = Tour("noir", (7, 7))

    for col in range(8):
        plateau.grille[6][col] = Pion("noir", (6, col))

    return plateau


if __name__ == "__main__":
    plateau = initialiser_plateau()
    InterfaceEchecs(plateau)# -*- coding: utf-8 -*-
"""

