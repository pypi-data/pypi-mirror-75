'''
Fichier contenant des algorythmes utilitaires.
'''

import re
from typing import List, Tuple

from elucidata.const_regex import REGEX_INLINE, REGEX_MULTILIGNE

#typer en sortie ?
def recup_client(id_: str):
    '''
    entrées:    - id_: str ->   identifiant de la structure dont on cherche le client.

    sortie:     - Client ->     client de la structure portant l'id 'id_'.

    définition: Renvoie le client de la structure identifiée par 'id_'.
    '''
    from elucidata.classes.parser import Parser
    tmp = re.split('\\.', id_)
    return Parser.list_clients[int(tmp[0]) - 1]

def recup_script(id_: str):
    '''
    entrées:    - id_: str ->   identifiant de la structure dont on cherche le script.

    sortie:     - Script ->     script de la structure portant l'id 'id_'.

    définition: Renvoie le script de la structure identifiée par 'id_'.
    '''
    from elucidata.classes.parser import Parser
    tmp = re.split('\\.', id_)
    return Parser.list_clients[int(tmp[0]) - 1].list_scripts[int(tmp[1]) - 1]


def nb_lignes(multiligne: str) -> int:
    '''
    entrées:    - multiligne: str ->    texte dont on cherche le nombre de lignes.

    sortie:     - int ->                nombre de lignes dans le texte.

    définition: Renvoie le nombre de lignes du texte en entrée.
    '''
    return len(re.split('[\n\r]', multiligne))


def extraction_inligne(ligne: str) -> Tuple[str, str]:
    '''
    entrées:    - ligne: str ->     ligne contenant un commentaire inligne à extraire.

    sortie:     - str ->            composante non commentaire de la ligne.
                - str ->            composante commentaire de la ligne.

    définition: Extrait un commentaire inline d'une ligne et renvoie ses deux composantes (non commentaire/commentaire).
    '''
    tmp = re.split(REGEX_INLINE, ligne)
    return tmp[0] + '\n', tmp[1]


def extraction_multiligne(texte: str) -> Tuple[str, List[str]]:
    '''
    entrées:    - texte: str ->     texte contenant des commentaires multilignes à extraire.

    sortie:     - str ->            concaténation des composantes non commentaire du texte.
                - List[str] ->      liste des composantes commentaire du texte.

    définition: Extrait les commentaires multilignes d'un texte.
    '''
    ligne = ""
    comment = []
    pattern = re.compile(REGEX_MULTILIGNE)
    tmp = re.split(REGEX_MULTILIGNE, texte)

    i = 0
    while i < len(tmp):
        if pattern.match(tmp[i]):
            comment.append(tmp[i])
            if nb_lignes(tmp[i]) > 1:
                ligne += '\n'
            if i < (len(tmp) - 1):
                i += 1
        else:
            ligne += tmp[i]
        i += 1
    return ligne, comment
    