'''
Contient la classe chargée de traiter, stocker et manipuler les informations liées aux commentaires.
'''

import re

from elucidata.classes.bloc import Bloc
from elucidata.const_regex import REG_w

class Commentaire(Bloc):
    '''
    description
    '''

    def __init__(self, texte: str, debut: int, fin: int, id_: str) -> None:
        '''
        description
        '''
        Bloc.__init__(self, texte, debut, fin, id_)
        self.explicatif: bool = est_explicatif(texte)

    def nb_caracteres(self) -> int:
        '''
        Renvoie la taille du commentaire en nombre de caractères
        '''
        acc = 0
        lignes = re.split('[ \t\n\r]', self.contenu)
        for i in lignes:
            acc += len(i)
        if lignes[0][0] == '/':
            return acc - 4

        if lignes[0][0] == '-':
            return acc - 2

        if lignes[0][0] == '#':
            return acc - 1  # doit etre améliorer pour identifier facilement le type de commentaire.

        return 0  # throw error ?


    def nb_lignes(self) -> int:
        '''
        Renvoie la taille du commentaire en nombre de ligne
        '''
        return 1 + self.ligne_fin - self.ligne_debut

def est_explicatif(texte: str) -> bool:
    '''
    description
    '''
    pattern = re.compile('.*?' + REG_w + '.*')
    if pattern.match(texte):
        return True
    return False
