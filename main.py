"""Quoridor - module main"""
# pylint: disable=no-member
import argparse
import re
import time
import turtle

import api
from quoridor import Quoridor
from quoridorx import QuoridorX


def analyser_commande():
    """Traite les options passées en ligne de commande."""
    parser = argparse.ArgumentParser(description="Jeu Quoridor")

    parser.add_argument("-l", "--lister", action="store_true",
                        help="Lister les identifiants des 20 dernières parties")

    parser.add_argument("-a", dest="mode_auto", action="store_true",
                        help="Jouer contre le serveur en mode automatique")

    parser.add_argument("-x", dest="mode_graphique", action="store_true",
                        help="Jouer contre le serveur avec affichage graphique")

    parser.add_argument("idul", help="IDUL du joueur")  # , nargs='?', default="phcas16")

    return parser.parse_args()


def jouer_coup(args, q, id_partie):
    """Boucle de saisie."""
    if args.mode_auto:
        return api.jouer_coup(id_partie, q.type_coup.upper(), q.pos_coup)

    capture = None
    titre = "C'est votre tour!"
    question = "Entrez votre prochain coup sous la forme (D|MH|MV) x y :"

    while not capture:
        if args.mode_graphique:
            entree = turtle.textinput(titre, question)
            if entree is None:  # bouton Cancel ou X
                turtle.mainloop()  # pause sur damier
                raise RuntimeError("Fenêtre fermée par le joueur")
        else:
            print(question, end=" ")
            entree = input()

        capture = re.search(r'^(D|MH|MV)\s+(\d)\s+(\d)$', entree.strip(), re.IGNORECASE)

        if capture:
            entrees = capture.groups()

            try:
                return api.jouer_coup(id_partie, entrees[0].upper(),
                                      (int(entrees[1]), int(entrees[2])))
            # except StopIteration as gagnant:
            #    gagnant = str(gagnant)
            except RuntimeError as message:
                titre = str(message)
                capture = None
                if not args.mode_graphique:
                    print(titre)
        else:
            titre = "Erreur de syntaxe, veuillez réessayer."
            if not args.mode_graphique:
                print(titre)


def main():
    """Boucle principale."""
    args = analyser_commande()

    if args.lister:
        for partie in api.lister_parties(args.idul):
            print(partie["id"])
        return

    id_partie, partie = api.débuter_partie(args.idul)
    gagnant = False
    q = None

    while not gagnant:
        if args.mode_graphique:
            q = QuoridorX(partie["joueurs"], partie["murs"])
        else:
            q = Quoridor(partie["joueurs"], partie["murs"])

        gagnant = q.partie_terminée()
        if gagnant:
            break

        if args.mode_auto:
            time.sleep(0.25)
            q.jouer_coup(1)

        if args.mode_graphique:
            q.afficher()
        else:
            print("", q, sep="\n")

        partie = jouer_coup(args, q, id_partie)

    if args.mode_graphique:
        turtle.mainloop()  # pause sur damier
    else:
        print("", q, "", f'{gagnant} a gagné la partie!', "", sep="\n")


if __name__ == "__main__":
    main()