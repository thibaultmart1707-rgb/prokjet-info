# -*- coding: utf-8 -*-
"""
@author: Gaudin Timothé & Martin thibault
"""
import tkinter as tk
from cpiece import *
from cechiquier import *
from cia import IA  # Importation de votre nouvelle classe IA
import json


class InterfaceEchecs:
    def __init__(self, echiquier):
        self.echiquier = echiquier
        self.selection = None
        self.mouvements_valides = []
        
        # Initialisation de l'IA (Couleur noire, profondeur 3)
        self.ia = IA(couleur="noir", profondeur=3)

        self.fenetre = tk.Tk()
        self.fenetre.title("Jeu d'échecs")
        
        frame_boutons = tk.Frame(self.fenetre)
        frame_boutons.pack(pady=5)
        
        tk.Button(frame_boutons, text="Sauvegarder", command=self.sauvegarder_partie).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_boutons, text="Charger", command=self.charger_partie).pack(side=tk.LEFT, padx=5)

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
        self.fenetre.mainloop()

    def dessiner_plateau(self):
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
        # Mise à jour du label en dehors de la boucle des cases pour éviter les rafraîchissements inutiles
        self.label_tour.config(text=f"Tour : {self.echiquier.tour}")

    def clic(self, event):
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
            
            # Laisse un court instant au plateau pour se rafraîchir avant le coup de l'IA
            self.fenetre.after(100, self.tour_ia)
    
    def tour_ia(self):
        # On vérifie si c'est bien au tour de l'IA de jouer
        if self.echiquier.tour == self.ia.couleur:
            coup = self.ia.choisir_coup(self.echiquier)
            if coup:
                self.echiquier.deplacer_piece(coup[0], coup[1])
                self.dessiner_plateau()
            else:
                print("Échec et mat ou Pat !")
                
    def sauvegarder_partie(self):
        """Figure: Stockage de données (JSON)."""
        data = {
            "tour": self.echiquier.tour,
            "grille": self.echiquier.exporter_etat()
        }
        with open("sauvegarde_echecs.json", "w") as f:
            json.dump(data, f)
        self.label_tour.config(text="Partie sauvegardée !")

    def charger_partie(self):
        """Figure: Stockage de données (JSON)."""
        try:
            with open("sauvegarde_echecs.json", "r") as f:
                data = json.load(f)
            self.echiquier.importer_etat(data)
            self.dessiner_plateau()
        except FileNotFoundError:
            self.label_tour.config(text="Aucune sauvegarde trouvée.")