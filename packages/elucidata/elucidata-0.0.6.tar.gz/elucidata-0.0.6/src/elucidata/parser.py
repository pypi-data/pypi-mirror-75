'''
Contient la classe principal de notre module et la fonction d'ajout de repertoire client.
'''
from typing import List

from elucidata.classes.client import Client


class Parser:
    '''
    description
    '''

    list_clients: List[Client] = []

    def __init__(self) -> None:
        '''
        Constructeur de la classe Parser
        '''

def parse(chemin_du_repertoire: str, nom_du_client: str = '', langage: str = 'sql') -> None:
    '''
    entrées:    - chemin_du_repertoire: str ->  chemin vers le repertoire contenant les scripts à parser.
                - nom_du_client: str ->         nom du client propriétaire des scripts à parser.
                - langage: str ->               langage principal des scripts du repertoire à parser.

    sortie:     None

    définition: Parse les scripts d'un repertoire passé en entré.
    '''

    Parser.list_clients.append( \
            Client(chemin_du_repertoire, str(len(Parser.list_clients) + 1), nom_du_client, langage) \
                            )
