'''
Contient la classe abstraite chargée de traiter, stocker et manipuler les informations liées aux variables.
'''
from abc import ABC, abstractmethod


class Variable(ABC):
    '''
    description
    '''

    @abstractmethod
    def __init__(self) -> None:
        pass
