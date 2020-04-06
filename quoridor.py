"""module quoridor"""
import networkx as nx


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.
    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


class QuoridorError(Exception):
    """Classe implémentant l'exception QuoridorError"""


class Quoridor:
    """Classe implémentant le jeu Quoridor"""

    @staticmethod
    def pos_joueur_valide(pos_joueur):
        """Vérifie si la position pos_joueur est valide"""
        return isinstance(pos_joueur, (list, tuple)) and len(pos_joueur) == 2 and \
            all(isinstance(x, int) and 1 <= x <= 9 for x in pos_joueur)

    @staticmethod
    def pos_mur_h_valide(mur_h):
        """Vérifie si la position mur_h est valide"""
        return isinstance(mur_h, (list, tuple)) and len(mur_h) == 2 and \
            all(isinstance(x, int) for x in mur_h) and 1 <= mur_h[0] <= 8 and 2 <= mur_h[1] <= 9

    @staticmethod
    def pos_mur_v_valide(mur_v):
        """Vérifie si la position mur_v est valide"""
        return isinstance(mur_v, (list, tuple)) and len(mur_v) == 2 and \
            all(isinstance(x, int) for x in mur_v) and 2 <= mur_v[0] <= 9 and 1 <= mur_v[1] <= 8

    @classmethod
    def valider_murs(cls, murs_h, murs_v):
        """Vérifie si tous les murs sont valides"""
        for i, mur_h in enumerate(murs_h):
            if not cls.pos_mur_h_valide(mur_h):
                raise QuoridorError("La position d'un des murs horizontaux est invalide")

            if any(mur_h[1] == mur_h2[1] and mur_h[0] - 1 <= mur_h2[0] <= mur_h[0] + 1
                   for j, mur_h2 in enumerate(murs_h) if i != j):
                raise QuoridorError("Deux des murs horizontaux se chevauchent")

        for i, mur_v in enumerate(murs_v):
            if not cls.pos_mur_v_valide(mur_v):
                raise QuoridorError("La position d'un des murs verticaux est invalide")

            if any(mur_v[0] == mur_v2[0] and mur_v[1] - 1 <= mur_v2[1] <= mur_v[1] + 1
                   for j, mur_v2 in enumerate(murs_v) if i != j):
                raise QuoridorError("Deux des murs verticaux se chevauchent")

            if any(tuple(mur_h) == (mur_v[0] - 1, mur_v[1] + 1) for mur_h in murs_h):
                raise QuoridorError("Un des murs horizontaux et un des murs verticaux se "
                                    "chevauchent")

    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie.
        Cette représentation est la même que celle du TP précédent.
        :returns: la chaîne de caractères de la représentation.
        """
        patron_carres = list(" | .   .   .   .   .   .   .   .   . |")
        patron_murs = list("  |                                   |")
        plateau = []

        # génération du plateau vierge
        num_ligne = 9
        for i in range(17):
            if i % 2:
                plateau.append([*patron_murs])  # shallow copy du patron
            else:
                plateau.append([str(num_ligne)] + patron_carres)
                num_ligne -= 1

        id_joueurs = []

        # plaçage des pions
        for i, joueur in enumerate(self.etat["joueurs"]):
            id_joueur = str(i + 1)
            id_joueurs.append(f'{id_joueur}={joueur["nom"]}')
            ligne = -2 * joueur["pos"][1] + 1
            colonne = 4 * joueur["pos"][0]
            plateau[ligne][colonne] = id_joueur

        patron_mur_h = list("-------")

        # plaçage des murs horizontaux
        for mur_h in self.etat.get("murs")["horizontaux"]:
            ligne = -2 * mur_h[1] + 2
            colonne = 4 * mur_h[0] - 1
            plateau[ligne][colonne: colonne + len(patron_mur_h)] = patron_mur_h

        # plaçage des murs verticaux
        for mur_v in self.etat.get("murs")["verticaux"]:
            ligne = -2 * mur_v[1] + 1
            colonne = 4 * mur_v[0] - 2
            for i in range(ligne, ligne - 3, -1):
                plateau[i][colonne] = "|"

        # concaténation des morceaux du plateau
        return "\n".join(["Légende: " + ", ".join(id_joueurs),
                          "   -----------------------------------",
                          *["".join(ligne) for ligne in plateau],
                          "--|-----------------------------------",
                          "  | 1   2   3   4   5   6   7   8   9"])

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.
        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la position est invalide (en dehors du damier).
        :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
        """
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est invalide")

        if not self.pos_joueur_valide(position):
            raise QuoridorError("La position est invalide (en dehors du damier)")

        graphe = construire_graphe(
            [joueur["pos"] for joueur in self.etat["joueurs"]],
            self.etat.get("murs")["horizontaux"],
            self.etat.get("murs")["verticaux"]
        )

        dict_joueur = self.etat.get("joueurs")[int(joueur)-1]

        if position not in graphe.successors(tuple(dict_joueur["pos"])):
            raise QuoridorError("La position est invalide pour l'état actuel du jeu")

        dict_joueur["pos"] = position

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.
        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée")

        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est invalide")

        # joueur = int(joueur)
        adversaire = 1 if joueur == 2 else 2

        pos_joueur = tuple(self.etat.get("joueurs")[joueur-1]["pos"])
        pos_adversaire = tuple(self.etat.get("joueurs")[adversaire-1]["pos"])

        graphe = construire_graphe(
            [pos_joueur, pos_adversaire],
            self.etat.get("murs")["horizontaux"],
            self.etat.get("murs")["verticaux"]
        )

        chemin_joueur = nx.shortest_path(graphe, pos_joueur, f'B{joueur}')
        chemin_adversaire = nx.shortest_path(graphe, pos_adversaire, f'B{adversaire}')
        deplacer_joueur = False

        if len(chemin_joueur) <= len(chemin_adversaire) or \
                len(graphe.successors(pos_adversaire)) < 2:
            deplacer_joueur = True
        else:
            prochaine_pos_adversaire = chemin_adversaire[1]
            diff_x = prochaine_pos_adversaire[0] - pos_adversaire[0]
            diff_y = prochaine_pos_adversaire[1] - pos_adversaire[1]

            if diff_x != 0:  # tentative plaçage mur vertical
                mur_v = [prochaine_pos_adversaire[0] - min(diff_x, 0), prochaine_pos_adversaire[1]]
                try:
                    self.placer_mur(joueur, tuple(mur_v), "vertical")
                    self.type_coup = "MV"
                    self.pos_coup = tuple(mur_v)
                except QuoridorError:
                    mur_v[1] -= 1  # tentative plaçage mur vertical plus bas
                    try:
                        self.placer_mur(joueur, tuple(mur_v), "vertical")
                        self.type_coup = "MV"
                        self.pos_coup = tuple(mur_v)
                    except QuoridorError:
                        deplacer_joueur = True

            else:  # tentative plaçage mur horizontal
                mur_h = [prochaine_pos_adversaire[0], prochaine_pos_adversaire[1] - min(diff_y, 0)]
                try:
                    self.placer_mur(joueur, tuple(mur_h), "horizontal")
                    self.type_coup = "MH"
                    self.pos_coup = tuple(mur_h)
                except QuoridorError:
                    mur_h[0] -= 1  # tentative plaçage mur horizontal plus à gauche
                    try:
                        self.placer_mur(joueur, tuple(mur_h), "horizontal")
                        self.type_coup = "MH"
                        self.pos_coup = tuple(mur_h)
                    except QuoridorError:
                        deplacer_joueur = True

        if deplacer_joueur:
            self.déplacer_jeton(joueur, chemin_joueur[1])
            self.type_coup = "D"
            self.pos_coup = chemin_joueur[1]

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.
        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        joueur_1 = self.etat["joueurs"][0]
        joueur_2 = self.etat["joueurs"][1]

        if joueur_1.get("pos")[1] == 9:
            return joueur_1["nom"]
        if joueur_2.get("pos")[1] == 1:
            return joueur_2["nom"]
        return False

    def placer_mur(self, joueur, position, orientation):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.
        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si un mur occupe déjà cette position.
        :raises QuoridorError: si la position est invalide pour cette orientation.
        :raises QuoridorError: si le joueur a déjà placé tous ses murs.
        """
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est invalide")

        if orientation not in ("horizontal", "vertical"):
            raise QuoridorError("L'orientation du mur est invalide")

        if self.etat.get("joueurs")[int(joueur)-1]["murs"] == 0:
            raise QuoridorError("Aucun mur restant pour ce joueur")

        if orientation == "horizontal":
            if not self.pos_mur_h_valide(position):
                raise QuoridorError("La position de ce mur horizontal est invalide")
            murs_h = [position] + self.etat.get("murs")["horizontaux"]
            murs_v = self.etat.get("murs")["verticaux"]
        else:
            if not self.pos_mur_v_valide(position):
                raise QuoridorError("La position de ce mur vertical est invalide")
            murs_h = self.etat.get("murs")["horizontaux"]
            murs_v = [position] + self.etat.get("murs")["verticaux"]

        self.valider_murs(murs_h, murs_v)

        pos_joueurs = [joueur["pos"] for joueur in self.etat["joueurs"]]

        graphe = construire_graphe(
            pos_joueurs,
            murs_h,
            murs_v
        )

        if any(not nx.has_path(graphe, tuple(pos_joueur), f'B{i+1}')
               for i, pos_joueur in enumerate(pos_joueurs)):
            raise QuoridorError("Un des joueurs serait emprisonné par ce mur")

        if orientation == "horizontal":
            self.etat.get("murs")["horizontaux"].append(position)
        else:
            self.etat.get("murs")["verticaux"].append(position)