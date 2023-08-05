'''
Ce fichier a pour objectif de regrouper les fonctions realisant des tâches automatisé.
Rendre l'outil accessible à un grand nombre de profils.
'''

import os
import pandas as pd
from graphviz import Digraph
from elucidata.parser import Parser, parse

def carto_tab(path : str, id_client : str):
    parse(path)
    script = Parser.list_clients[int(id_client)].list_scripts[0]
    script.script_to_excel()

def carto(path, id_client, Drop=True, view=True):

    carto_tab(path, id_client)
    # Importation du fichier excel en dataframe
    df = pd.read_excel("cartographie.xlsx", header=[0, 1])

    # Suppression des alias dans la colonne source de la carto tabulaire
    for i in range(len(df['Source']['Table'])):
        try:
            df.iloc[i, 1] = df['Source']['Table'][i].split(' ')[0]
        except:
            pass

    # Creation des dictionnaires utilisés pour grahviz
    df_no_create = df.where(df['Lien']['Type de lien'] != 'CREATE').dropna(how='all').reset_index(drop=True)
    df_create = df.where(df['Lien']['Type de lien'] == 'CREATE').dropna(how='all').reset_index(drop=True)

    # dictionnaire des tables sources
    source_dico = {}
    for i, j in enumerate(df_no_create.iloc[:, 1].dropna().drop_duplicates().tolist()):
        source_dico[j] = i + 1

    # dictionnaire des tables créées
    create_dico = {}
    for i, j in enumerate(df_create.iloc[:, 7].drop_duplicates().tolist()):
        create_dico[j] = i + 1 + len(source_dico)

    # dictionnaire des tables cibles
    cible_dico = {}
    for i, j in enumerate(df_no_create.iloc[:, 7].dropna().drop_duplicates().tolist()):
        if j not in source_dico and j not in create_dico:
            cible_dico[j] = i + 1 + len(source_dico) + len(create_dico)

    # Debut du Graph
    if Drop == True:
        global dot
        dot = Digraph(comment='Carto_graph')
    # Param par defaut
    dot.edge_attr.update(arrowhead='none')
    dot.node_attr.update(shape='box')

    # Relation entre les elements du tableau
    for i in source_dico:
        dot.node(str(source_dico[i]), i, style='filled', fillcolor='red')

    for i in cible_dico:
        dot.node(str(cible_dico[i]), i, style='filled, dashed', fillcolor='blue')

    for i in create_dico:
        dot.node(str(create_dico[i]), i, style='filled', fillcolor='yellow')

    for i in range(len(df_no_create)):
        try:
            dot.edge(str(source_dico[df_no_create.iloc[i, 1]]), str(cible_dico[df_no_create.iloc[i, 7]]))
        except:
            pass

    for i in list(create_dico.keys()):
        data = df.where(df['Cible']['Table'] == i).dropna(how='all')
        for j in range(len(data)):
            try:
                dot.edge(str(source_dico[data.iloc[j, 1]]), str(create_dico[data.iloc[j, 7]]))
            except:
                pass

    # Sortie PDF
    dot.render('Carto_graph.gv', view=view)
