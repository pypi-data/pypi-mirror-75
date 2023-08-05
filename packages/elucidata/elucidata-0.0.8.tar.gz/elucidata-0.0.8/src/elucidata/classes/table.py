'''
Contient la classe chargée de traiter, stocker et manipuler les informations liées aux tables.
'''

from elucidata.classes.variable import Variable


class Table(Variable):
    '''
    description
    '''

    def __init__(self, nom: str = "", alias: str = "", type_table: str = "", tmp_table=None) -> None:
        Variable.__init__(self)
        self.nom = nom
        self.alias = alias
        self.type_table = type_table
        self.lien_table = tmp_table
