""" module quoridorX"""
#pylint:disable=E1101

import turtle
from quoridor import Quoridor


class QuoridorX(Quoridor):
    """
    Classe Quoridor
    """
    def __init__(self, joueurs, murs=None):
        super().__init__(joueurs, murs)
        self.fen = turtle.Screen()
        self.joe = turtle.Turtle()
        self.alex = turtle.Turtle()
        self.robot = turtle.Turtle()
        self.mure = turtle.Turtle()
        self.punto = turtle.Turtle()
        self.bord = ((0, 0), (0, 10), (600, 10), (600, 0), (0, 0))
        self.mur = ((0, 0), (0, 10), (-110, 10), (-110, 0), (0, 0))
        self.pion = ((-10, -10), (10, -10), (10, 10), (-10, 10), (-10, -10)
    
    def afficher(self):
        """
        Fonction pour afficher le jeu en mode graphique
        """
        # On crée la fenêtre
        self.fen.title("Jeu Quoridor")
        self.fen.setup(width=800, height=800)

        # On définie nos formes, les bords, les murs et les pions
        turtle.addshape('pion', self.pion)
        turtle.addshape('bord', self.bord)
        turtle.addshape('mur', self.mur)

        # On définie toutes nos turtles et on place leurs vitesses au max
        self.joe.speed(0)
        self.alex.speed(0)
        self.robot.speed(0)
        self.mure.speed(0)
        self.punto.speed(0)

        # On fait un cadrillage pour les positions de points

        self.punto.penup()
        self.punto.pencolor('black')
        self.punto.fillcolor('black')
        self.punto.backward(55)
        self.punto.left(90)
        self.punto.backward(280)

        for i in range(1, 10):
            for j in range(1, 10):
                x = (5 - i)*68 - 5
                y = (j - 1)*68 + 10
                self.punto.forward(y)
                self.punto.left(90)
                self.punto.forward(x)
                self.punto.dot(5)
                self.punto.backward(x)
                self.punto.right(90)
                self.punto.backward(y)

        # On trace les bords du plateau
        # On va ce placer dans le coin inférieur droit du plateau
        self.joe.penup()
        self.joe.backward(350)
        self.joe.left(90)
        self.joe.forward(300)
        self.joe.pendown()
        self.joe.shape('bord')
        self.joe.pencolor('black')
        self.joe.fillcolor('black')
        self.joe.stamp()

        # On fait tous les bords un par un
        self.joe.penup()
        self.joe.right(90)
        self.joe.forward(590)
        self.joe.pendown()
        self.joe.stamp()

        self.joe.penup()
        self.joe.right(90)
        self.joe.forward(590)
        self.joe.pendown()
        self.joe.stamp()

        self.joe.penup()
        self.joe.right(90)
        self.joe.forward(590)
        self.joe.pendown()
        self.joe.stamp()
        self.joe.penup()

        # On définie le pion du joueur 1 en rouge
        self.alex.shape('pion')
        self.alex.penup()
        self.alex.pencolor('red')
        self.alex.fillcolor('red')
        self.alex.backward(55)
        self.alex.left(90)
        self.alex.backward(280)

        # On définie le pion du joueur 2 en vert
        self.robot.shape('pion')
        self.robot.penup()
        self.robot.pencolor('green')
        self.robot.fillcolor('green')
        self.robot.backward(55)
        self.robot.left(90)
        self.robot.forward(290)
        # On place le pion du joueur 1 en fonction des coordonées
        x = (5 - self.etat["joueurs"][0]["pos"][0])*68 - 5
        y = (self.etat["joueurs"][0]["pos"][1] - 1)*68 + 10
        self.alex.forward(y)
        self.alex.left(90)
        self.alex.forward(x)

        # On place le pion du joueur 2 en fonction des coordonées
        x = (5 - self.etat["joueurs"][1]["pos"][0])*68 - 5
        y = (9 - self.etat["joueurs"][1]["pos"][1])*68 +16
        self.robot.backward(y)
        self.robot.right(90)
        self.robot.backward(x)

        # On place ce place à l'origine pour les murs

        # On définie la couleur des murs et sa position d'origines
        self.mure.shape('mur')
        self.mure.penup()
        self.mure.pencolor('blue')
        self.mure.fillcolor('blue')
        self.mure.backward(370)
        self.mure.right(90)
        self.mure.forward(300)
        self.mure.left(90)

        # On place d'abord tous les murs verticaux un par un en lisant la liste
        for liste in self.etat["murs"]["verticaux"]:
            print('Je suis dans la liste de V')
            x = (liste[0] - 1)*68 + 10
            y = (liste[1] - 1)*68 + 15
            self.mure.forward(x)
            self.mure.left(90)
            self.mure.forward(y)
            self.mure.right(90)
            self.mure.stamp()
            self.mure.left(90)
            self.mure.backward(y)
            self.mure.right(90)
            self.mure.backward(x)
        # On change le sens de la forme
        self.mure.right(90)

        # On place les murs horizontaux
        for liste in self.etat["murs"]["horizontaux"]:
            x = (liste[0] - 1)*68 + 30
            y = (liste[1] - 1)*68
            self.mure.backward(y)
            self.mure.left(90)
            self.mure.forward(x)
            self.mure.right(90)
            self.mure.stamp()
            self.mure.left(90)
            self.mure.backward(x)
            self.mure.right(90)
            self.mure.forward(y)
        # On cache le turtle des murs 
        self.mure.fillcolor('black')
        self.mure.pencolor('black')
        self.mure.left(90)
        self.mure.forward(10)
        self.mure.right(90)
        self.mure.backward(10)

        # On demande à l'utilisateur son prochain coup
        coup_invalide = True
        while coup_invalide:
            self.coup = self.fen.textinput("Vos coups", "Entrez votre type coups:")
            if self.coup in ["q", "Q"]:
                break
            print(self.coup)
            try:
                self.coup = self.coup.split(" ")
                if self.coup[0] not in ("D", "MH", "MV"):
                    raise ValueError
                self.coup = self.coup[0], [int(self.coup[1]), int(self.coup[2])]
                coup_invalide = False
            except:
                print("Mauvaise entrée. Réessayez")
                coup_invalide = True
        self.fen.clear()
