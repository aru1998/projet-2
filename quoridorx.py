"""Quoridor - module quoridorx"""
# pylint: disable=no-member
import turtle
from quoridor import Quoridor


class QuoridorX(Quoridor):
    """Classe QuoridorX"""
    TAILLE_CASE = 30
    MARGE_CASE = 20
    NB_RANGEES = 9
    XY_OFFSET = - (TAILLE_CASE * NB_RANGEES + MARGE_CASE * (NB_RANGEES - 1)) / 2 \
                - TAILLE_CASE - MARGE_CASE
    XY_INCR = TAILLE_CASE + MARGE_CASE
    TAILLE_POLICE = 18
    LONGUEUR_MUR = TAILLE_CASE * 2.4 + MARGE_CASE
    RECUL_MUR = TAILLE_CASE * 0.2
    OFFSET_MUR = MARGE_CASE / 2
    OFFSET_PION = TAILLE_CASE / 2
    TAILLE_PION = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.afficher()

    def _pos_damier(self, num_case):
        return num_case * self.XY_INCR + self.XY_OFFSET

    def afficher(self):
        """Afficher le damier dans une fenêtre Turtle"""
        # config damier

        turtle.Screen().tracer(0, 0)  # gèle fenêtre
        turtle.clear()
        turtle.penup()

        # dessin damier

        turtle.color("lightgray")
        turtle.pensize(5)
        turtle.setheading(90)

        for x in range(1, self.NB_RANGEES + 1):
            for y in range(1, self.NB_RANGEES + 1):
                turtle.setpos(self._pos_damier(x), self._pos_damier(y))
                turtle.pendown()
                turtle.begin_fill()

                for _ in range(4):
                    turtle.forward(self.TAILLE_CASE)
                    turtle.right(90)

                turtle.end_fill()
                turtle.penup()

        # config murs

        turtle.color("black")

        # dessin murs h

        turtle.setheading(0)

        for mur_h in self.etat.get("murs")["horizontaux"]:
            turtle.setpos(self._pos_damier(mur_h[0]) - self.RECUL_MUR,
                          self._pos_damier(mur_h[1]) - self.OFFSET_MUR)
            turtle.pendown()
            turtle.forward(self.LONGUEUR_MUR)
            turtle.penup()

        # dessin murs v

        turtle.setheading(90)

        for mur_v in self.etat.get("murs")["verticaux"]:
            turtle.setpos(self._pos_damier(mur_v[0]) - self.OFFSET_MUR,
                          self._pos_damier(mur_v[1]) - self.RECUL_MUR)
            turtle.pendown()
            turtle.forward(self.LONGUEUR_MUR)
            turtle.penup()

        # dessin pions

        turtle.color("white")

        for i, joueur in enumerate(self.etat["joueurs"]):
            turtle.setpos(self._pos_damier(joueur["pos"][0]) + self.OFFSET_PION,
                          self._pos_damier(joueur["pos"][1]) + self.OFFSET_PION)
            turtle.dot(self.TAILLE_PION, "forestgreen" if i == 0 else "firebrick")
            turtle.setpos(self._pos_damier(joueur["pos"][0]) + self.OFFSET_PION,
                          self._pos_damier(joueur["pos"][1]))
            turtle.write(str(i+1), font=("", self.TAILLE_POLICE), align="center")

        # dessin nombres

        turtle.color("black")

        for i in range(1, self.NB_RANGEES+1):
            turtle.setpos(self._pos_damier(i) + self.OFFSET_PION,
                          self._pos_damier(0) + self.OFFSET_PION)  # hor
            turtle.write(str(i), font=("", self.TAILLE_POLICE), align="center")
            turtle.setpos(self._pos_damier(0) + self.TAILLE_CASE,
                          self._pos_damier(i))  # ver
            turtle.write(str(i), font=("", self.TAILLE_POLICE), align="center")

        # dessin légende

        id_joueurs = [f'{i+1}={joueur["nom"]}' for i, joueur in enumerate(self.etat["joueurs"])]
        turtle.setpos(self._pos_damier(1), self._pos_damier(10) - self.MARGE_CASE/2)
        turtle.write("Légende: " + ", ".join(id_joueurs), font=("", 14))

        # plaçage des pions

        for i, joueur in enumerate(self.etat["joueurs"]):
            id_joueur = str(i + 1)
            id_joueurs.append(f'{id_joueur}={joueur["nom"]}')

        # affichage

        turtle.hideturtle()

        gagnant = self.partie_terminée()
        if gagnant:
            turtle.title(f'QuoridorX - {gagnant} a gagné la partie!')
            turtle.bgcolor("forestgreen"
                           if gagnant == self.etat["joueurs"][0]["nom"] else
                           "firebrick")
        else:
            turtle.title("QuoridorX")

        turtle.update()  # dégèle fenêtre


# test
if __name__ == "__main__":
    QuoridorX(joueurs=[
        {"nom": "henri", "murs": 0, "pos": (5, 1)},
        {"nom": "robot", "murs": 0, "pos": (5, 9)}
    ], murs={
        "horizontaux": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                        (2, 7), (2, 8), (2, 9), (4, 2), (4, 3)],
        "verticaux": [(2, 2), (2, 4), (2, 6), (2, 8), (4, 2),
                      (4, 4), (4, 6), (4, 8), (6, 2), (6, 4)]
    })
    turtle.mainloop()