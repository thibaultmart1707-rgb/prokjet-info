# -*- coding: utf-8 -*-
"""
@author: Gaudin Timothé & Martin thibault
"""
from cpiece import Pion, Cavalier, Fou, Tour, Reine, Roi

class ORDI: #@author: Timothé Gaudin
    """Classe responsable de l’ordinateur qui affronte le joueur. Chaque type de pièce se voit attribuer une valeur en points. Lorsqu’un coup est simulé, le score du plateau résultant est évalué à partir de ces valeurs, ce qui permet de comparer et de classer les différents coups possibles.
    Plus précisément, l’algorithme anticipe plusieurs coups à l’avance. Avec une profondeur de recherche de 1, l’ordinateur teste tous les coups légaux, évalue le score obtenu pour chacun d’eux et choisit celui qui lui est le plus favorable.
    Avec une profondeur de 2, pour chaque coup envisagé par l’ordinateur, on considère ensuite toutes les réponses possibles du joueur. On suppose alors que le joueur choisira le coup qui maximise son propre avantage. Le score associé à un coup de l’ordinateur n’est donc plus simplement celui du plateau obtenu après ce coup, mais celui du plateau résultant après la meilleure réponse possible du joueur.
    Ce principe est ensuite appliqué récursivement pour des profondeurs de 3, 4 coups ou davantage : chaque joueur est supposé jouer le meilleur coup disponible à son tour. L’ensemble de cette démarche repose ainsi sur une fonction récursive permettant d’explorer l’arbre des coups possibles et d’évaluer leur pertinence.
    """
        
    # Dictionnaire des valeurs des pièces pour l'ordi
    VALEURS = {Pion: 10, Cavalier: 30, Fou: 30, Tour: 50, Reine: 90, Roi: 900}

    def __init__(self, couleur, profondeur): #@author: Timothé Gaudin
        """
        Initialise l'ordinateur avec sa couleur et sa profondeur de calcul.
        -param couleur: str ("blanc" ou "noir") représentant le camp de l'IA.
        -param profondeur: int, nombre de coups d'avance simulés par l'algorithme.
        -return: None
        """
        self.couleur = couleur
        self.profondeur = profondeur

    def evaluer_plateau(self, echiquier): #@author: Timothé Gaudin
        """
        Évalue le score du plateau actuel du point de vue de l'ORDI.
        -param echiquier: Instance de la classe Echiquier.
        -return: int, score du plateau (positif si avantageux pour l'ordi, négatif si désavantageux).
        """
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

    def minimax(self, echiquier, profondeur, alpha, beta, maximisant): #@author: Timothé Gaudin
        """
        Fonction récursive permettant de déterminer le meilleur coup à jouer pour l’ordinateur en explorant l’arbre des possibilités jusqu’à une profondeur donnée. Afin de réduire le temps de calcul, l’algorithme utilise l’élagage alpha-bêta, une optimisation qui évite d’explorer certaines branches de l’arbre lorsque celles-ci ne peuvent plus influencer la décision finale.
        Le système d’évaluation attribue un score à chaque position : un score élevé correspond à une situation favorable à l’ordinateur, tandis qu’un score faible, voire négatif, indique un avantage pour le joueur adverse.
        Le coefficient alpha représente le meilleur score que le joueur maximisant (l’ordinateur) est déjà assuré d’obtenir. Il est initialisé à −∞. À l’inverse, le coefficient bêta représente le meilleur score que le joueur minimisant (l’adversaire) peut encore tolérer pour l’ordinateur. Il est initialisé à +∞.
        Au cours de l’exploration de l’arbre, ces deux bornes sont progressivement mises à jour en fonction des positions évaluées. Lorsqu’une branche conduit à une situation qui est déjà moins intéressante qu’une alternative précédemment analysée, il devient inutile de poursuivre son exploration. Par exemple, à une profondeur de 2, si l’on constate que l’adversaire dispose d’une réponse lui procurant un avantage supérieur à celui obtenu dans une autre branche déjà étudiée, alors les autres réponses associées au coup actuellement examiné ne pourront pas conduire à une meilleure décision pour l’ordinateur. La branche est donc abandonnée, ce qui permet de réduire considérablement le nombre de positions à analyser sans modifier le résultat final de l’algorithme.
        -param echiquier: Instance de la classe Echiquier.
        -param profondeur: int, profondeur actuelle restante de l'arbre de recherche.
        -param alpha: float, la meilleure valeur que le joueur maximisant peut garantir à ce niveau ou au-dessus.
        -param beta: float, la meilleure valeur que le joueur minimisant peut garantir à ce niveau ou au-dessus.
        -param maximisant: bool, True si l'algorithme est dans la phase d'évaluation maximisante (tour de l'IA), False sinon.
        -return: tuple (score, meilleur_coup) où meilleur_coup est structuré comme ((l_dep, c_dep), (l_arr, c_arr)).
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
                
                # optimisation
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break 
                    
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
                
                # OPTIMISATION 
                beta = min(beta, evaluation)
                if beta < alpha:
                    break 
               
            return min_eval, meilleur_coup

    def choisir_coup(self, echiquier): #@author: Timothé Gaudin
        """
        Permet d'appeler la méthode minimax avec les paramètres d'initialisation corrects.
        -param echiquier: Instance de la classe Echiquier.
        -return: tuple ((l_dep, c_dep), (l_arr, c_arr)) correspondant au meilleur coup trouvé, ou None.
        """
        maximisant = (self.couleur == "noir")
        # Ajout des valeurs initiales -infini et +infini pour alpha et beta
        score, coup = self.minimax(echiquier, self.profondeur, -float('inf'), float('inf'), maximisant)
        return coup
