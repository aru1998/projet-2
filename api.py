"""Quoridor - module api"""
import requests


def lister_parties(idul):
    """Retourne en sortie la liste des parties reçus du serveur."""
    url_req = "https://python.gel.ulaval.ca/quoridor/api/lister/"
    rep = requests.get(url_req, params={"idul": idul})

    if rep.status_code != 200:
        raise RuntimeError(f"Le GET sur {url_req} a produit le code d'erreur {rep.status_code}.")

    rep = rep.json()

    if "message" in rep.keys():
        raise RuntimeError(rep["message"])

    return rep["parties"]


def débuter_partie(idul):
    """Retourne en sortie un tuple constitué de l'identifiant de la partie et de l'état du jeu."""
    url_req = "https://python.gel.ulaval.ca/quoridor/api/débuter/"
    rep = requests.post(url_req, data={"idul": idul})

    if rep.status_code != 200:
        raise RuntimeError(f"Le POST sur {url_req} a produit le code d'erreur {rep.status_code}.")

    rep = rep.json()

    if "message" in rep.keys():
        raise RuntimeError(rep["message"])

    return rep["id"], rep["état"]


def jouer_coup(id_partie, type_coup, position):
    """Retourne en sortie l'état actuel du jeu."""
    url_req = "https://python.gel.ulaval.ca/quoridor/api/jouer/"
    rep = requests.post(url_req, data={"id": id_partie, "type": type_coup, "pos": position})

    if rep.status_code != 200:
        raise RuntimeError(f"Le POST sur {url_req} a produit le code d'erreur {rep.status_code}.")

    rep = rep.json()

    if "message" in rep.keys():
        raise RuntimeError(rep["message"])
    # if "gagnant" in rep.keys():
    #     raise StopIteration(rep["gagnant"])

    return rep["état"]
