'''
Contient la classe chargée de traiter, stocker et manipuler les informations liées aux repertoires clients.
'''

import os
from typing import List

from elucidata.classes.script import Script


class Client:
    '''
    description
    '''
    def __init__(self, chemin_du_repertoire: str, id_: str, nom_du_client: str, langage: str) -> None:
        '''
        description
        '''
        self.nom: str = nom_du_client  # temporairement déclaratif
        self.id: str = id_
        self.langage: str = langage  # temporairement déclaratif
        self.chemin: str = chemin_du_repertoire

        self.list_scripts: List[Script] = []
        list_chemin_scripts: List[str] = os.listdir(chemin_du_repertoire)
        for chemin in list_chemin_scripts:
            self.list_scripts.append( \
                    Script(chemin_du_repertoire + '/' + chemin, self.id + '.' + str(len(self.list_scripts) + 1)) \
                    )

    def nb_scripts(self) -> int:
        '''
        définition: Renvoie le nombre de scripts du client.
        '''
        return len(self.list_scripts)

    def nb_blocs(self) -> int:
        '''
        définition: Renvoie le nombre de blocs contenus dans les scripts du client.
        '''
        acc = 0
        for script in self.list_scripts:
            acc += script.nb_blocs()
        return acc

    def nb_requetes(self) -> int:
        '''
        définition: Renvoie le nombre de requêtes contenues dans les scripts du client.
        '''
        acc = 0
        for script in self.list_scripts:
            acc += script.nb_requetes()
        return acc

    def nb_commentaires(self) -> int:
        '''
        définition: Renvoie le nombre de commentaires contenus dans les scripts du client.
        '''
        acc = 0
        for script in self.list_scripts:
            acc += script.nb_commentaires()
        return acc

    def nb_lignes(self) -> int:
        '''
        définition: Renvoie la somme du nombre de lignes des scripts du client.
        '''
        acc = 0
        for script in self.list_scripts:
            acc += script.nb_lignes()
        return acc

    def nb_caracteres(self) -> int:
        '''
        définition: Renvoie la somme du nombre de caractères des scripts du client.
        '''
        acc = 0
        for script in self.list_scripts:
            acc += script.nb_caracteres()
        return acc
