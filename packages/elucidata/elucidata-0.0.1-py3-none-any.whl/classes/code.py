'''
Contient la classe abstraite chargée de traiter, stocker et manipuler les informations liées aux blocs de code.
'''
from abc import abstractmethod
from typing import List

from elucidata.classes.bloc import Bloc
from elucidata.classes.variable import Variable

class Code(Bloc):
    '''
    description
    '''

    @abstractmethod
    def __init__(self, texte: str, debut: int, fin: int, id_: str) -> None:
        '''
        description
        '''

        Bloc.__init__(self, texte, debut, fin, id_)
        self.var_utilise: List[Variable] = []
        self.var_declare: List[Variable] = []

    def imbrication_max(self) -> int:
        '''
        description
        '''

        # à renseigner
        return 6  # temporaire

    def imbrication_nb(self) -> int:
        '''
        description
        '''

        # à renseigner
        return 6  # temporaire

    def imbrication_moyenne(self) -> int:
        '''
        description
        '''

        # à renseigner
        return 6  # temporaire
