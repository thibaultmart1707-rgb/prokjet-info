# -*- coding: utf-8 -*-
"""

@author: Gaudin Timothé & Martin thibault
"""


class Piece:
    def __init__(self, couleur, position):
        self.couleur = couleur
        self.position = position
        self.symbole = "?"

    def mouvements_possibles(self, echiquier):
        return []


class Roi(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position)
        self.symbole = "♔" if couleur == "blanc" else "♚"

    def mouvements_possibles(self, echiquier):
        mouvements = []
        ligne, col = self.position

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),            (0, 1),
            (1, -1),  (1, 0),   (1, 1)
        ]

        for dl, dc in directions:
            l = ligne + dl
            c = col + dc
            if 0 <= l < 8 and 0 <= c < 8:
                piece = echiquier.grille[l][c]
                if piece is None or piece.couleur != self.couleur:
                    mouvements.append((l, c))

        return mouvements


class Reine(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position)
        self.symbole = "♕" if couleur == "blanc" else "♛"

    def mouvements_possibles(self, echiquier):
        mouvements = []
        ligne, col = self.position

        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for dl, dc in directions:
            l, c = ligne + dl, col + dc
            while 0 <= l < 8 and 0 <= c < 8:
                piece = echiquier.grille[l][c]
                if piece is None:
                    mouvements.append((l, c))
                else:
                    if piece.couleur != self.couleur:
                        mouvements.append((l, c))
                    break
                l += dl
                c += dc

        return mouvements


class Tour(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position)
        self.symbole = "♖" if couleur == "blanc" else "♜"

    def mouvements_possibles(self, echiquier):
        mouvements = []
        ligne, col = self.position

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dl, dc in directions:
            l, c = ligne + dl, col + dc
            while 0 <= l < 8 and 0 <= c < 8:
                piece = echiquier.grille[l][c]
                if piece is None:
                    mouvements.append((l, c))
                else:
                    if piece.couleur != self.couleur:
                        mouvements.append((l, c))
                    break
                l += dl
                c += dc

        return mouvements


class Fou(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position)
        self.symbole = "♗" if couleur == "blanc" else "♝"

    def mouvements_possibles(self, echiquier):
        mouvements = []
        ligne, col = self.position

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dl, dc in directions:
            l, c = ligne + dl, col + dc
            while 0 <= l < 8 and 0 <= c < 8:
                piece = echiquier.grille[l][c]
                if piece is None:
                    mouvements.append((l, c))
                else:
                    if piece.couleur != self.couleur:
                        mouvements.append((l, c))
                    break
                l += dl
                c += dc

        return mouvements


class Cavalier(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position)
        self.symbole = "♘" if couleur == "blanc" else "♞"

    def mouvements_possibles(self, echiquier):
        mouvements = []
        ligne, col = self.position

        coups = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        for dl, dc in coups:
            l = ligne + dl
            c = col + dc
            if 0 <= l < 8 and 0 <= c < 8:
                piece = echiquier.grille[l][c]
                if piece is None or piece.couleur != self.couleur:
                    mouvements.append((l, c))

        return mouvements


class Pion(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position)
        self.symbole = "♙" if couleur == "blanc" else "♟"

    def mouvements_possibles(self, echiquier):
        mouvements = []
        ligne, col = self.position

        if self.couleur == "noir":
            direction = -1
            ligne_depart = 6
        else:
            direction = 1
            ligne_depart = 1

        # Avance d'une case
        l1 = ligne + direction
        if 0 <= l1 < 8 and echiquier.grille[l1][col] is None:
            mouvements.append((l1, col))

            # Avance de deux cases au départ
            l2 = ligne + 2 * direction
            if ligne == ligne_depart and 0 <= l2 < 8 and echiquier.grille[l2][col] is None:
                mouvements.append((l2, col))

        # Prises en diagonale
        for dc in [-1, 1]:
            l = ligne + direction
            c = col + dc
            if 0 <= l < 8 and 0 <= c < 8:
                piece = echiquier.grille[l][c]
                if piece is not None and piece.couleur != self.couleur:
                    mouvements.append((l, c))

        return mouvements
    
    
    
    

class PieceFactory:
    """
    Design Pattern Factory : Centralise la création des objets pièces.
    Très utile pour recréer le plateau depuis une sauvegarde JSON.
    """
    @staticmethod
    def creer_piece(type_piece, couleur, position):
        pieces_disponibles = {
            "Pion": Pion,
            "Tour": Tour,
            "Cavalier": Cavalier,
            "Fou": Fou,
            "Reine": Reine,
            "Roi": Roi
        }
        if type_piece in pieces_disponibles:
            return pieces_disponibles[type_piece](couleur, position)
        return None
