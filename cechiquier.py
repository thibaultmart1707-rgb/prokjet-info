# -*- coding: utf-8 -*-
"""

@author: Gaudin Timothé & Martin thibault
"""
from cpiece import *
from cpiece import PieceFactory




class Echiquier:
    def __init__(self):
        self.grille = [[None for _ in range(8)] for _ in range(8)]
        self.tour = "blanc"
    def deplacer_piece(self, depart, arrivee):
        piece = self.grille[depart[0]][depart[1]]

        if piece is None:
            return False

    # tour de jeu
        if piece.couleur != self.tour:
            print(f"ce n'est pas le tour des {piece.couleur}s")
            return False

    # mouvement légal
        if arrivee not in piece.mouvements_possibles(self):
            return False

    #  simulation du coup
        sauvegarde = self.grille[arrivee[0]][arrivee[1]]

        self.grille[arrivee[0]][arrivee[1]] = piece
        self.grille[depart[0]][depart[1]] = None
        ancienne_pos = piece.position
        piece.position = arrivee

    #si roi en échec → on annule
        if self.roi_en_echec(piece.couleur):
            self.grille[depart[0]][depart[1]] = piece
            self.grille[arrivee[0]][arrivee[1]] = sauvegarde
            piece.position = ancienne_pos
            return False

    #  coup accepté → changement de tour
        self.tour = "noir" if self.tour == "blanc" else "blanc"
        adversaire = self.tour
        
        if self.est_echec_et_mat(adversaire):
            print(f"ÉCHEC ET MAT ! {piece.couleur} gagne !")
        return True
        
    
    def trouver_roi(self, couleur):
            for l in range(8):
                for c in range(8):
                    piece = self.grille[l][c]
                    if isinstance(piece, Roi) and piece.couleur == couleur:
                        return (l, c)
            return None
    def case_attaquee(self, ligne, col, couleur_adverse):
        for l in range(8):
            for c in range(8):
                piece = self.grille[l][c]
    
                if piece is not None and piece.couleur == couleur_adverse:
                    if (ligne, col) in piece.mouvements_possibles(self):
                        return True

    
    def roi_en_echec(self, couleur):
        roi_pos = self.trouver_roi(couleur)
        if roi_pos is None:
            print('échec')
            return False
    
        ligne, col = roi_pos
        adversaire = "noir" if couleur == "blanc" else "blanc"
    
        return self.case_attaquee(ligne, col, adversaire)
    
    
    def coups_possibles(self, couleur):
        coups = []
    
        for l in range(8):
            for c in range(8):
                piece = self.grille[l][c]
    
                if piece is not None and piece.couleur == couleur:
                    depart = (l, c)
    
                    for arrivee in piece.mouvements_possibles(self):
                        # simulation
                        sauvegarde = self.grille[arrivee[0]][arrivee[1]]
                        ancienne_pos = piece.position
    
                        self.grille[arrivee[0]][arrivee[1]] = piece
                        self.grille[l][c] = None
                        piece.position = arrivee
    
                        en_echec = self.roi_en_echec(couleur)
    
                        # annulation
                        self.grille[l][c] = piece
                        self.grille[arrivee[0]][arrivee[1]] = sauvegarde
                        piece.position = ancienne_pos
    
                        if not en_echec:
                            coups.append((depart, arrivee))
    
        return coups
    def est_echec_et_mat(self, couleur):
        if not self.roi_en_echec(couleur):
            return False
    
        return len(self.coups_possibles(couleur)) == 0
    
    def exporter_etat(self):
        """Exporte l'état du plateau sous forme de dictionnaire pour la sauvegarde JSON."""
        etat = []
        for l in range(8):
            for c in range(8):
                piece = self.grille[l][c]
                if piece:
                    etat.append({
                        "type": type(piece).__name__,
                        "couleur": piece.couleur,
                        "position": [l, c]
                    })
        return etat

    def importer_etat(self, data):
        """Reconstruit le plateau depuis un dictionnaire JSON via le pattern Factory."""
        self.grille = [[None for _ in range(8)] for _ in range(8)]
        self.tour = data.get("tour", "blanc")
        for p_data in data.get("grille", []):
            l, c = p_data["position"]
            piece = PieceFactory.creer_piece(p_data["type"], p_data["couleur"], (l, c))
            self.grille[l][c] = piece
    