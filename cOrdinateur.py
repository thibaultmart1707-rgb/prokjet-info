# -*- coding: utf-8 -*-
"""
@author: Gaudin Timothé & Martin thibault
"""
from cpiece import Pion, Cavalier, Fou, Tour, Reine, Roi

class IA:
    # Dictionnaire des valeurs des pièces en attribut de classe
    VALEURS = {Pion: 10, Cavalier: 30, Fou: 30, Tour: 50, Reine: 90, Roi: 900}

    def __init__(self, couleur="noir", profondeur=3):
        self.couleur = couleur
        self.profondeur = profondeur

    def evaluer_plateau(self, echiquier):
        """Évalue le score du plateau actuel du point de vue de l'IA."""
        score = 0
        for l in range(8):
            for c in range(8):
                piece = echiquier.grille[l][c]
                if piece:
                    val = self.VALEURS.get(type(piece), 0)
                    if piece.couleur == self.couleur:
                        score += val
                    else:
                        score -= val
        return score

    def minimax(self, echiquier, profondeur, alpha, beta, maximisant):
        """
        Figures : 
        - Fonction récursive (appel de soi-même).
        - Algorithme d'optimisation (Élagage Alpha-Beta pour couper les branches inutiles).
        """
        if profondeur == 0:
            return self.evaluer_plateau(echiquier), None

        meilleur_coup = None
        
        if maximisant:
            max_eval = -float('inf')
            for coup in echiquier.coups_possibles("noir"):
                dep, arr = coup
                p_dep = echiquier.grille[dep[0]][dep[1]]
                p_arr = echiquier.grille[arr[0]][arr[1]]
                
                # Simulation
                echiquier.grille[arr[0]][arr[1]], echiquier.grille[dep[0]][dep[1]] = p_dep, None
                p_dep.position = arr
                
                evaluation = self.minimax(echiquier, profondeur - 1, alpha, beta, False)[0]
                
                # Annulation
                echiquier.grille[dep[0]][dep[1]], echiquier.grille[arr[0]][arr[1]] = p_dep, p_arr
                p_dep.position = dep
                
                if evaluation > max_eval:
                    max_eval = evaluation
                    meilleur_coup = coup
                
                # OPTIMISATION ALPHA-BETA
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break # Élagage de la branche
                    
            return max_eval, meilleur_coup
            
        else:
            min_eval = float('inf')
            for coup in echiquier.coups_possibles("blanc"):
                dep, arr = coup
                p_dep = echiquier.grille[dep[0]][dep[1]]
                p_arr = echiquier.grille[arr[0]][arr[1]]
                
                echiquier.grille[arr[0]][arr[1]], echiquier.grille[dep[0]][dep[1]] = p_dep, None
                p_dep.position = arr
                
                evaluation = self.minimax(echiquier, profondeur - 1, alpha, beta, True)[0]
                
                echiquier.grille[dep[0]][dep[1]], echiquier.grille[arr[0]][arr[1]] = p_dep, p_arr
                p_dep.position = dep
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    meilleur_coup = coup
                
                # OPTIMISATION ALPHA-BETA
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break # Élagage de la branche
               
            return min_eval, meilleur_coup

    def choisir_coup(self, echiquier):
        maximisant = (self.couleur == "noir")
        # Ajout des valeurs initiales -infini et +infini pour alpha et beta
        score, coup = self.minimax(echiquier, self.profondeur, -float('inf'), float('inf'), maximisant)
        return coup
