# -*- coding: utf-8 -*-
"""
@author: Gaudin Timothé & Martin thibault
"""
import tkinter as tk
from cpiece import *
from cechiquier import *
from cordi import ORDI  
import json
from cmemen import *
    
class InterfaceEchecs: #@author: Timothé Gaudin
    """permet de gérer l'affichage du jeu ainsi que l'interaction utilisateur, on a dans les variables d'instance, l'échiquier, les paramètres de l'ordi, la fenêtre d'affichage etc"""
    def __init__(self, echiquier):
        """
        Initialise l'interface graphique, demande les modes et lance la boucle principale de Tkinter.
        -param echiquier: Instance de la classe Echiquier associée au jeu.
        -return: None
        """
        self.echiquier = echiquier
        self.selection = None
        self.mouvements_valides = []
        
        # Initialisation de l'ordi (Couleur noir, profondeur 3)
        
        self.mode_jeu = "ordi"
        self.profondeur_ordi = 0
        self.couleur_ordi = 'noir'

        self.fenetre = tk.Tk()
        self.fenetre.title("Jeu d'échecs")
        
        frame_boutons = tk.Frame(self.fenetre)
        frame_boutons.pack(pady=5)
        
        self.demander_mode_jeu()
        if self.mode_jeu == "ordi":
            self.demander_difficulte()
            
        self.ordi = ORDI(couleur=self.couleur_ordi, profondeur=self.profondeur_ordi)
        
        tk.Button(frame_boutons, text="Sauvegarder", command=self.sauvegarder_partie).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_boutons, text="Charger", command=self.charger_partie).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_boutons, text="Annuler Coup (Undo)", command=self.annuler_dernier_coup, bg="#e0a6ae").pack(side=tk.LEFT, padx=5)

        self.taille_case = 70
        self.canvas = tk.Canvas(
            self.fenetre,
            width=8 * self.taille_case,
            height=8 * self.taille_case
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.clic)
        self.label_tour = tk.Label(self.fenetre, text="")
        self.label_tour.pack() # Sert par la suite pour afficher le tour
        self.dessiner_plateau()
        if self.mode_jeu == "ordi": #on le met au cas où on souhaite jouer avec les noirs et donc l'ordi avec les blancs, mais les paramètres par défauts font que normalement on en a pas besoin à moins de modifier directement dans le code python la couleur de l'ia.
            self.fenetre.after(100, self.tour_ordi)
        self.fenetre.mainloop()
        
     
    
    def demander_mode_jeu(self): #@author: Timothé Gaudin
        """
        Pour choisir le mode de jeu (2 joueurs ou contre l'ordi) au démarrage via une pop-up.
        -return: None
        """
        popup = tk.Toplevel(self.fenetre)
        popup.title("Choix du mode")
        popup.geometry("300x160")
        popup.grab_set()  # Bloque l'interaction avec la fenêtre principale tant qu'on n'a pas choisi
        popup.transient(self.fenetre)  # Garde la pop-up au premier plan
        
        label = tk.Label(popup, text="Choisissez votre mode de jeu :", font=("Arial", 12, "bold"))
        label.pack(pady=15)
        
        def choisir_ordi():
            self.mode_jeu = "ordi"
            popup.destroy()
            
        def choisir_pvp():
            self.mode_jeu = "pvp"
            popup.destroy()
            
        btn_ordi = tk.Button(popup, text="Contre l'ordinateur", command=choisir_ordi, width=22, bg="#B58863", fg="white")
        btn_ordi.pack(pady=5)
        
        btn_pvp = tk.Button(popup, text="2 Joueurs", command=choisir_pvp, width=22, bg="#F0D9B5")
        btn_pvp.pack(pady=5)
        
        self.fenetre.wait_window(popup)  # Met le reste de l'initialisation en pause
        
        
    def demander_difficulte(self): #@author: Timothé Gaudin
        """
        Affiche une pop-up pour choisir le niveau de l'ordinateur (profondeur du Minimax).
        -return: None
        """
        popup = tk.Toplevel(self.fenetre)
        popup.title("Choix de la difficulté")
        popup.geometry("300x230")
        popup.grab_set()  # Bloque l'interaction avec la fenêtre principale
        popup.transient(self.fenetre)
        
        label = tk.Label(popup, text="Choisissez le niveau de l'ordi :", font=("Arial", 12, "bold"))
        label.pack(pady=10)
        
        # Liste des niveaux : (Nom du bouton, profondeur associée, couleur du bouton)
        niveaux = [
            ("Facile (Profondeur 1)", 1, "#85e3b3"),
            ("Moyen (Profondeur 2)", 2, "#f8d7da"),
            ("Difficile (Profondeur 3)", 3, "#f5c6cb"),
            ("Expert (Profondeur 4)", 4, "#e0a6ae")
        ]
        
        def configurer_niveau(prof): #@author: Timothé Gaudin
            self.profondeur_ordi = prof
            popup.destroy()
            
        # Création dynamique des boutons
        for texte, prof, couleur in niveaux:
            btn = tk.Button(
                popup, 
                text=texte, 
                command=lambda p=prof: configurer_niveau(p), 
                width=22, 
                bg=couleur
            )
            btn.pack(pady=4)
            
        self.fenetre.wait_window(popup)  # Met l'initialisation en pause tant que le choix n'est pas fait    

    def dessiner_plateau(self): #@author: Timothé Gaudin
        """
        Permet de dessiner le plateau graphique, les pièces et la surbrillance des sélections/mouvements valides.
        -return: None
        """
        self.canvas.delete("all")

        for ligne in range(8):
            for col in range(8):
                x1 = col * self.taille_case
                y1 = ligne * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case

                if (ligne + col) % 2 == 0:
                    couleur = "#F0D9B5"
                else:
                    couleur = "#B58863"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="black")

                if (ligne, col) in self.mouvements_valides:
                    self.canvas.create_rectangle(
                        x1 + 4, y1 + 4, x2 - 4, y2 - 4,
                        outline="green", width=3
                    )

                if self.selection == (ligne, col):
                    self.canvas.create_rectangle(
                        x1 + 3, y1 + 3, x2 - 3, y2 - 3,
                        outline="red", width=3
                    )

                piece = self.echiquier.grille[ligne][col]
                if piece is not None:
                    self.canvas.create_text(
                        x1 + self.taille_case / 2,
                        y1 + self.taille_case / 2,
                        text=piece.symbole,
                        font=("Arial", 30)
                    )
        
        
        mode_texte = "vs ORDI" if self.mode_jeu == "ordi" else "à 2"
        self.label_tour.config(text=f"Tour : {self.echiquier.tour} ({mode_texte})")

    def clic(self, event): #@author: Timothé Gaudin
        """
        Cette méthode est lancée dès qu'un clic est détecté. Gère la sélection de pièce ou le déplacement.
        -param event: Objet événement généré par Tkinter contenant les attributs x et y du clic.
        -return: None
        """
        col = event.x // self.taille_case
        ligne = event.y // self.taille_case

        if not (0 <= ligne < 8 and 0 <= col < 8):
            return

        if self.selection is None:
            piece = self.echiquier.grille[ligne][col]
            if piece is not None and piece.couleur == self.echiquier.tour:
                self.selection = (ligne, col)
                self.mouvements_valides = piece.mouvements_possibles(self.echiquier)
                self.dessiner_plateau()
        else:
            depart = self.selection
            arrivee = (ligne, col)

            self.echiquier.deplacer_piece(depart, arrivee)

            self.selection = None
            self.mouvements_valides = []
            self.dessiner_plateau()
            
            if self.mode_jeu == "ordi":
                self.fenetre.after(100, self.tour_ordi)
    
    def tour_ordi(self): #@author: Timothé Gaudin
        """
        Gère le tour de l'ordinateur en effectuant le coup choisi par l'algorithme Minimax ou par sécurité.
        -return: None
        """
        if self.echiquier.tour == self.ordi.couleur:
            coup = self.ordi.choisir_coup(self.echiquier)
            if coup:
                self.echiquier.deplacer_piece(coup[0], coup[1])
                self.dessiner_plateau()
            else:
                
                cp = self.echiquier.coups_possibles(self.ordi.couleur)
                if cp == []:
                    print("Échec et mat ou Pat !")
                else :# il peut arriver que l'ordi ne trouve pas de coup alors qu'il y en a si il y a par exemple echec et mat au coup suivant (dans ce cas l'evaluation du plateau par la classe ORDI renvoie -inf qui n'est pas supérieur à -inf -> pas de coup enregistrer)
                    self.echiquier.deplacer_piece(cp[0][0], cp[0][1])#dans ce cas, on prend un coup au hasard
                    self.dessiner_plateau()
                    
    def sauvegarder_partie(self): #@author: Thibault Martin
        """
        Stockage de données dans un fichier JSON pour sauvegarder l'état actuel.
        -return: None
        """
        data = {
            "tour": self.echiquier.tour,
            "grille": self.echiquier.exporter_etat()
        }
        with open("sauvegarde_echecs.json", "w") as f:
            json.dump(data, f)
        self.label_tour.config(text="Partie sauvegardée !")

    def charger_partie(self): #@author: Thibault Martin
        """
        Stockage de données (JSON) : lit le fichier de sauvegarde s'il existe et met à jour l'échiquier.
        -return: None
        """
        try:
            with open("sauvegarde_echecs.json", "r") as f:
                data = json.load(f)
            self.echiquier.importer_etat(data)
            self.dessiner_plateau()
        except FileNotFoundError:
            self.label_tour.config(text="Aucune sauvegarde trouvée.")
            
    def annuler_dernier_coup(self): #@author: Timothé Gaudin
        """Gère le retour en arrière."""
        # Si on joue contre l'ordinateur, il faut annuler DEUX coups (humain et ordi)
        if self.mode_jeu == "ordi":
            # Annule le coup de l'ordi
            if self.echiquier.restaurer_depuis_memento():
                # Annule ton propre coup
                self.echiquier.restaurer_depuis_memento()
        else:
            # En mode 2 joueurs, on annule juste un seul coup
            self.echiquier.restaurer_depuis_memento()
            
        self.selection = None
        self.mouvements_valides = []
        self.dessiner_plateau()
