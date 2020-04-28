"""Quoridor - module quoridor"""
import unittest
import copy
import random
import itertools
import networkx as nx


class QuoridorError(Exception):
    """
    Classe pour gérer les exceptions s
    """

def graphe_helper(murs_horizontaux, murs_verticaux):
    """la fonction construire_graphe
   
    """
    graphe = nx.DiGraph()
    for x in range(1, 10):
        for y in range(1, 10):
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))
    return graphe

def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.
    """
    graphe = graphe_helper(murs_horizontaux, murs_verticaux)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)
        def ajouter_lien_sauteur(noeud, voisin):
            """
            fonction ajouter_lien_sauteur
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]
            if saut in graphe.successors(voisin):
                graphe.add_edge(noeud, saut)
            else:
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)
        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')
    return graphe


def check_type(t, variable, message):
    """fonction pour vérifier le type d'une variable
    """
    if not isinstance(variable, t):
        raise QuoridorError(message)


def check_iterable(j):
    """fonction pour alléger le nombre
    """
    try:
        iter(j)
    except TypeError:
        raise QuoridorError("joueurs n'est pas iterable!")
    if len(j) != 2:
        raise QuoridorError("Il n'y a pas exactement 2 joueurs!")


def check_total_murs(joueurs, murs):
    """Fonction check_total_murs
    """
    murh = 0
    murv = 0
    murj1 = 0
    murj2 = 0
    if murs:
        check_type(dict, murs, "murs n'est pas un dictionnaire!")
        murh = len(murs['horizontaux'])
        murv = len(murs['verticaux'])
    check_iterable(joueurs)
    if isinstance(joueurs[0], dict):
        for joueur in joueurs:
            if  not 0 <= joueur['murs'] <= 10:
                raise QuoridorError("mauvais nombre de murs!")
        murj1 = joueurs[0]['murs']
        murj2 = joueurs[1]['murs']
    elif isinstance(joueurs[0], str):
        murj1 = 10
        murj2 = 10
    else:
        raise QuoridorError("joueurs n'est ni des dictionnaires ni des string!")
    if (murh + murv + murj1 + murj2) != 20:
        print("\nmauvaise qt de murs:")
        raise QuoridorError("mauvaise quantité totale de murs!")


class Quoridor:
    """Class quoridor"""
    def __init__(self, joueurs, murs=None):
        """
        Initialisation de la classe Quoridor
        """
        self.joueurs = [{'nom':'', 'murs': 0, 'pos':(0, 0)},
                        {'nom':'', 'murs': 0, 'pos':(0, 0)}]
        self.murh = []
        self.murv = []
        self.gameid = ''

        starting_position = [(5, 1), (5, 9)]
        cjoueurs = copy.deepcopy(joueurs)
        cmurs = copy.deepcopy(murs)
        check_total_murs(cjoueurs, cmurs)
        if murs:
            check_type(dict, cmurs, "murs n'est pas un dictionnaire!")
            for mur in cmurs['horizontaux']:
                if not 1 <= mur[0] <= 8 or not 2 <= mur[1] <= 9:
                    raise QuoridorError("position du mur non-valide!")
                self.murh += [tuple(mur)]
            for mur in cmurs['verticaux']:
                if not 2 <= mur[0] <= 9 or not 1 <= mur[1] <= 8:
                    raise QuoridorError("position du mur non-valide!")
                self.murv += [tuple(mur)]
        check_iterable(cjoueurs)
        for numero, joueur in enumerate(cjoueurs):
            if isinstance(joueur, str):
                self.joueurs[numero]['nom'] = joueur
                self.joueurs[numero]['murs'] = 10
                self.joueurs[numero]['pos'] = starting_position[numero]
            else:
                if  not 0 <= joueur['murs'] <= 10:
                    raise QuoridorError("mauvais nombre de murs!")
                if not 1 <= joueur['pos'][0] <= 9 or not 1 <= joueur['pos'][1] <= 9:
                    raise QuoridorError("position du joueur invalide!")
                self.joueurs[numero] = joueur
                self.joueurs[numero]['pos'] = tuple(self.joueurs[numero]['pos'])

    def __str__(self):
        """
        Produit la représentation en art ascii
        """
        board_positions = 9
        spacing_horizontal = ((board_positions * 4) - 1)
        game_pos_x = range(1, (board_positions * 4), 4)
        game_pos_y = range(((board_positions - 1) * 2), -1, -2)
        board = [
            "légende: 1={} 2={}\n".format(self.joueurs[0]['nom'], self.joueurs[1]['nom']) +
            (' ' * 3) + ('-' * spacing_horizontal) + '\n'
        ]
        for i in reversed(range((board_positions * 2) - 1)):
            if (i % 2) == 0:
                board += ["{}{}|".format((((i + 1) // 2) + 1),
                                         (' ' * (1 - ((((i + 1) // 2) + 1) // 10))))]
                board += [' ', '.']
                board += ([' ', ' ', ' ', '.'] * (board_positions - 1))
                board += [' ', '|\n']
            else:
                board += ["  |"]
                board += ([' '] * spacing_horizontal)
                board += ['|\n']
        board += "--|" + ('-' * spacing_horizontal) + '\n'
        board += (' ' * 2) + '| '
        for i in range(1, board_positions):
            board += str(i) + (' ')
            board += (' ' * (2 - (i // 10)))
        board += "{}\n".format(board_positions)
        for num, joueur in enumerate(self.joueurs):
            position = joueur["pos"]
            if ((0 > position[0] > board_positions) or
                    (0 > position[1] > board_positions)):
                raise IndexError("Adresse du joueur invalide!")
            indice = (game_pos_x[(position[0] - 1)] +
                      (game_pos_y[(position[1] - 1)] * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            board[indice] = str(num + 1)
        for murh in self.murh:
            if ((1 > murh[0] > (board_positions - 1)) or
                    (2 > murh[1] > board_positions)):
                raise IndexError("Position du mur horizontal invalide!")
            indice = ((game_pos_x[(murh[0] - 1)] - 1) +
                      ((game_pos_y[(murh[1] - 1)] + 1) * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            for i in range(7):
                board[(indice + i)] = '-'
        for murv in self.murv:
            if (2 > murv[0] > board_positions) or (1 > murv[1] > board_positions):
                raise IndexError("Position du mur vertical invalide!")
            indice = ((game_pos_x[(murv[0] - 1)] - 2) +
                      (game_pos_y[(murv[1] - 1)] * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            for i in range(3):
                board[(indice - (i * (spacing_horizontal + 2)))] = '|'
        return ''.join(board)

    def déplacer_jeton(self, joueur, position):
        """
        déplacer_jeton
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée
        Arguments:
            joueur (int): 1 ou 2
            position (tuple):
                Le tuple (x, y) de la position où déplacer le jeton
        Return: None
        """
        # Vérifier que le joueur est valide
        if joueur not in (1, 2):
            raise QuoridorError("joueur invalide!")
        # Vérifier que la position du joueur est valide
        if not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9:
            raise QuoridorError("position invalide!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        # vérifier si le mouvement est valide
        if tuple(position) not in list(graphe.successors(tuple(self.joueurs[(joueur - 1)]['pos']))):
            raise QuoridorError("mouvement invalide!")
        # Changer la position du joueur
        self.joueurs[(joueur - 1)]['pos'] = position

    def état_partie(self):
        """
        état_partie
        Produit l'état actuel du jeu sous la forme d'un dictionnaire
        Arguments: None
        Return:
            une copie de l'état actuel du jeu sous la forme d'un dictionnaire
            {
                'joueurs': [
                    {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                    {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                ]
                'Murs': {
                    'horizontaux': [...],
                    'verticaux': [...],
                }
            }
        """
        return {"joueurs": self.joueurs,
                "murs":{
                    "horizontaux": self.murh,
                    "verticaux": self.murv
                    }}

    def switch_mur(self, joueur, pos, sens):
        """Simple fonction pour alléger auto_placer_mur
        Vérifie que le coup peut être joué et agence les datas dans la réponse
        Returns:
            [list] -- le coup à jouer, agencé dans le bon ordre
        """
        self.placer_mur(joueur, pos, sens)
        if sens == 'horizontal':
            return ('MH', pos[0], pos[1])
        return ('MV', pos[0], pos[1])

    def auto_placer_mur(self, joueur, chemin1, chemin2, attempts):
        """fonction pour assister jouer_coup
        Place un mur automatiquement dans le chemin du joueur adverse
        en fonction de son shortest_path
        Arguments:
            joueur {int} -- int (1 ou 2) du joueur pour lequel on joue le coup
            chemin1 {list} -- shortest_path du joueur qui place un mur
            chemin2 {list} -- shortest_path du joueur adverse
            attempts {int} -- nombre d'essai ayant été effectuées
        Returns:
            bool -- True si on a bien reussi a placer un mur. False sinon
        """
        # comparer le chemin le plus cours de notre joueur avec
        # celui de l'adversaire
        # si le plus cours chemin de l'adversaire est plus cours,
        # placer un mur pour lui barrer le chemin
        if attempts >= 2:
            return False

        try:
            # objectifs
            objectifs = ['B1', 'B2']
            adversaire = 1
            if adversaire == joueur:
                adversaire = 2
            # Itérer le long du chemin le plus court de l'adversaire
            for c, sens in itertools.product(chemin2[1:-1], ['horizontal', 'vertical']):
                # Itérer sur les 4 positions possibles où placer un mur
                for pos in [((c[0] - 1), c[1]),
                            ((c[0] + 1), (c[1])),
                            (c[0], (c[1] - 1)),
                            (c[0], (c[1] + 1))]:
                    try:
                        # Dresser un tableau avec le mur ajoué
                        graphe = ''
                        if sens == 'horizontal':
                            graphe = construire_graphe([joueur['pos'] for
                                                        joueur in self.joueurs],
                                                       (self.murh + [pos]),
                                                       self.murv
                                                      )
                        else:
                            graphe = construire_graphe([joueur['pos'] for
                                                        joueur in self.joueurs],
                                                       self.murh,
                                                       (self.murv + [pos])
                                                      )
                        # dresser les chemin avec le nouveau tableau
                        chem1 = nx.shortest_path(graphe,
                                                 tuple(self.joueurs[(joueur - 1)]['pos']),
                                                 objectifs[(joueur - 1)])
                        chem2 = nx.shortest_path(graphe,
                                                 tuple(self.joueurs[(adversaire - 1)]['pos']),
                                                 objectifs[(adversaire - 1)])
                        # comparer les nouveau chemins à ceux de départ
                        if len(chem2) > len(chemin2) and len(chem1) <= len(chemin1):
                            return self.switch_mur(joueur, pos, sens)
                    # Si le mur ne peut pas être placé, essayer le prochain
                    except nx.exception.NetworkXError:
                        continue
            return False
        # Si le mur ne peut pas être placé, essayer avec la prochaine position
        except (QuoridorError,
                nx.exception.NetworkXError,
                nx.exception.NetworkXNoPath):
            return self.auto_placer_mur(joueur,
                                        chemin1[attempts:],
                                        chemin2[attempts:],
                                        (attempts + 1))

    def jouer_coup(self, joueur):
        """
        jouer_coup
        Pour le joueur spécifié, jouer automatiquement son meilleur
        coup pour l'état actuel de la partie. Ce coup est soit le déplacement de son jeton,
        soit le placement d'un mur horizontal ou vertical.
        Arguments:
            joueur {int} -- un entier spécifiant le numéro du joueur (1 ou 2)
        Return: None
        """
        # objectifs
        objectifs = ['B1', 'B2']
        # identifiant de l'adversaire
        adversaire = 1
        if adversaire == joueur:
            adversaire = 2
        # Vérifier que le joueur est valide
        if joueur not in (1, 2):
            raise QuoridorError("joueur invalide!")
        # Vérifier si la partie est déjà terminée
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        # Dresser le tableau du shortest_path pour chaque joueur
        chemin1 = nx.shortest_path(graphe,
                                   tuple(self.joueurs[(joueur - 1)]['pos']),
                                   objectifs[(joueur - 1)])
        chemin2 = nx.shortest_path(graphe,
                                   tuple(self.joueurs[(adversaire - 1)]['pos']),
                                   objectifs[(adversaire - 1)])
        # utiliser le hasard pour déterminer si on deplace le jeton ou place un mur
        dice = random.choices([True, False], weights=[10, self.joueurs[(joueur-1)]['murs']], k=1)
        # varier le choix en fonction du nombre de murs qu'il reste à placer
        # compager si le chemin le plus rapide de l'adversaire est plus cours que celui du joueur
        if ((dice == [True]) or
                (len(chemin2) < len(chemin1) <= 3) or
                (len(chemin2) < (len(chemin1) - 2))):
            result = self.auto_placer_mur(joueur, chemin1, chemin2, 1)
            if result:
                return result

        # Sinon, bouger le joueur selon le plus court chemin
        self.déplacer_jeton(joueur, chemin1[1])
        return ('D', chemin1[1][0], chemin1[1][1])

    def partie_terminée(self):
        """
        partie_terminée
        Évalue si la partie est terminée
        Arguments: None
        Return: le nom du joueur si un joueur a gagné. Sinon False
        """
        # definir les conditions de victoire
        condition_de_victoire = [9, 1]
        # itérer sur chaque joueurs
        for numero, joueur in enumerate(self.joueurs):
            # Vérifier si le joueur rempli les conditions de victoires
            if joueur['pos'][1] == condition_de_victoire[(numero)]:
                # Retourner le nom du joueur gagnant
                return joueur['nom']
        return False

    def check_positionh(self, position):
        """simple fonction pour alléger le nombre
        de branches dans placer_mur
        """
        # vérifier si les positions sont dans les limites du jeu
        if not 1 <= position[0] <= 8 or not 2 <= position[1] <= 9:
            raise QuoridorError("position du mur invalide!")
        # vérifier si l'emplacement est déjà occupé par un mur horizontal
        if (position[0], position[1]) in self.murh:
            raise QuoridorError("Il y a déjà un mur!")
        if [position[0], position[1]] in self.murh:
            raise QuoridorError("Il y a déjà un mur!")
        # Prendre en compte le décalage des murs horizontaux
        if ((position[0] - 1), position[1]) in self.murh:
            raise QuoridorError("Il y a déjà un mur!")
        if [(position[0] - 1), position[1]] in self.murh:
            raise QuoridorError("Il y a déjà un mur!")
        # vérifier si l'emplacement est déjà occupé par un mur vertical
        if ((position[0] + 1), (position[1] - 1)) in self.murv:
            raise QuoridorError("Il y a déjà un mur!")
        if [(position[0] + 1), (position[1] - 1)] in self.murv:
            raise QuoridorError("Il y a déjà un mur!")

    def check_positionv(self, position):
        """Simple fonction pour alléger le nombre de
        branches dans placer_mur
        """
        if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
            raise QuoridorError("position du mur invalide!")
        # vérifier si l'emplacement est déjà occupé
        if (position[0], position[1]) in self.murv:
            raise QuoridorError("Il y a déjà un mur!")
        if [position[0], position[1]] in self.murv:
            raise QuoridorError("Il y a déjà un mur!")
        # Prendre en compte le décalage des murs
        if (position[0], (position[1] - 1)) in self.murv:
            raise QuoridorError("Il y a déjà un mur!")
        if [position[0], (position[1] - 1)] in self.murv:
            raise QuoridorError("Il y a déjà un mur!")
        # Vérifier si l'enplacement est déjà occupé par un mur horizontal
        if ((position[0] - 1), (position[1] + 1)) in self.murh:
            raise QuoridorError("Il y a déjà un mur!")
        if [(position[0] - 1), (position[1] + 1)] in self.murh:
            raise QuoridorError("Il y a déjà un mur!")

    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        """
        placer_mur
        pour le joueur spécifié, placer un mur à la position spécifiée
        Arguments:
            joueur {int} -- Le numéro du joueur (1 ou 2)
            position {tuple} -- le tuple (x, y) de la position du mur
            orientation {str} -- l'orientation du mur: 'horizontal' ou 'vertical'
        Return: None
        """
        # définir les objectifs de chaque joueurs
        objectif = ['B1', 'B2']
        # Vérifier que le joueur est valide
        if joueur not in (1, 2):
            raise QuoridorError("joueur invalide!")
        # Vérifier si le joueur ne peut plus placer de murs
        if self.joueurs[(joueur - 1)]['murs'] <= 0:
            raise QuoridorError("le joueur ne peut plus placer de murs!")
        # Si la position est invalide (B1 ou B2)
        if not isinstance(position[0], int) or not isinstance(position[1], int):
            raise QuoridorError("position invalide!")
        # Si le mur est horizontal
        if orientation == 'horizontal':
            self.check_positionh(position)
            # créer un graphe des mouvements possible à jouer avec le mur ajouté
            graphe = construire_graphe(
                [joueur['pos'] for joueur in self.joueurs],
                (self.murh + [position]),
                self.murv
            )

            # vérifier si placer ce mur enfermerais un joueur
            for i in range(2):
                if not nx.has_path(graphe, (tuple(self.joueurs[i]['pos'])), objectif[i]):
                    raise QuoridorError("ce coup enfermerait un joueur")
            # placer le mur
            self.murh += [position]
            # retirer un mur des murs plaçables du joueurs
            self.joueurs[(joueur - 1)]['murs'] -= 1
        # Si c'est un mur vertical
        elif orientation == 'vertical':
            self.check_positionv(position)
            # créer un graphe des mouvements possible à jouer avec le mur ajouté
            graphe = construire_graphe(
                [joueur['pos'] for joueur in self.joueurs],
                self.murh,
                (self.murv + [position])
            )
            # vérifier si placer ce mur enfermerais le joueur
            for i in range(2):
                if not nx.has_path(graphe, (tuple(self.joueurs[i]['pos'])), objectif[i]):
                    raise QuoridorError("ce coup enfermerait un joueur")
            # placer le mur
            self.murv += [position]
            # retirer un mur des murs plaçables du joueurs
            self.joueurs[(joueur - 1)]['murs'] -= 1
        # Si l'orientation n'est ni horizontal ni vertical, soulever une exception
        else:
            raise QuoridorError("orientation invalide!")


#Lancer la batterie de tests unitaires l'orsque ce module est lancé en tant que main (pas importé)
if __name__ == '__main__':
    import testquoridor
    unittest.main(module=testquoridor.__name__, argv=[''], verbosity=2, exit=False)