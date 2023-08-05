'''
Contient la classe abstraite chargée de traiter, stocker et manipuler les informations liées aux blocs.
'''

import re

from abc import ABC

class Bloc(ABC):
    '''
    description
    '''

    def __init__(self, texte: str, debut: int, fin: int, id_) -> None:
        '''
        description
        '''

        self.contenu: str = texte
        self.ligne_debut: int = debut
        self.ligne_fin: int = fin
        self.id: str = id_

    def nb_lignes(self) -> int:
        '''
        Renvoie la taille du bloc en nombre de ligne
        '''
        lignes = re.split('[\n\r]', self.contenu)
        return len(lignes) - 1

    def nb_caracteres(self) -> int:
        '''
        Renvoie la taille du blocs en nombre de caractères
        '''
        acc = 0
        lignes = re.split('[ \t\n\r]', self.contenu)
        for i in lignes:
            acc += len(i)
        return acc
        