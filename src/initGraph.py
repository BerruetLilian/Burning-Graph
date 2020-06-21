# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np
import time
from networkx.algorithms.shortest_paths import all_pairs_shortest_path_length
from networkx.relabel import relabel_nodes
from community import community_louvain

"""
Initialise un graphe networkx à partir du chemin
d'un fichier sous le format noeud_source [espace] noeud_cible.
Les noeuds sont de type entier.
"""
def init_graph(fichier_data) :
    return nx.read_edgelist(fichier_data,nodetype=int)

"""
Retour le composant convexe le plus grand du graphe
et réindexe les noeuds.
"""     
def reduce(G) :
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    giant = G.subgraph(Gcc[0])
    dico = dict()
    ind = 0
    for node in G :
        if node in giant :  
            dico[node]=ind
            ind=ind+1
    return relabel_nodes(giant,dico)

"""
Retourne un dictionnaire qui associe un noeud à sa communauté 
selon la méthode Louvain.
/!\ renvoie une partition différente à chaque appel.
"""
def louvain_community(G) :
    return community_louvain.best_partition(G)

"""
Retourne une séquence qui associe un noeud à sa communauté 
selon la méthode Louvain. 
/!\ renvoie une partition différente à chaque appel.
/!\ Le graphe doit avoir des neouds de type entier.
"""
def louvain_community_vector(G) :
    return list(louvain_community(G).values())

"""
Retourne une matrice numpy qui associe un noeud à un noeud au plus court chemin qui les relies.
{ noeud_source : { neoud_cible : [plus_court_chemin] } }
"""
def make_matrix_SP(G) :
    print("Création d'une matrice des plus courts chemins...")
    start_time_all = time.time()
    
    SP = np.zeros((len(G),len(G)))
    generateur = all_pairs_shortest_path_length(G)

    for node_src,dico in generateur :
        for node_tar in dico :
            SP[node_src,node_tar]=dico[node_tar]
            SP[node_tar,node_src]=dico[node_tar]
            
    print("Temps d'éxecution : ",round((time.time()-start_time_all),2))       
    return SP

"""
Retourne le graphe réduit à son composant convexe le plus grand.
Retourne le métagraphe du dit composant.
Retourne la séquence qui associe un noeud à sa commuanuté utiliser
/!\ le métagraphe et la séquence sera différente à chaque appel.
"""
def start_with_MetaGraph(fichier_data) :
    print("Création du Métagraphe...")
    start_time_all = time.time()
    
    start_time = time.time()
    G = init_graph(fichier_data)
    print("Réduction en composant convexe...")
    giant = reduce(G)
    print("Temps d'éxecution : ",round((time.time()-start_time),2))    
    
    start_time = time.time()
    print("Calcul des communautés...")
    partition_vector = louvain_community_vector(giant)
    print("Temps d'éxecution : ",round((time.time()-start_time),2))  
    
    Meta = nx.Graph()
    for edge in giant.edges() :
        com_1 = partition_vector[edge[0]]
        com_2 = partition_vector[edge[1]]
        if com_1 not in Meta.nodes() :
            Meta.add_node(com_1)
        if com_2 not in Meta.nodes() :
            Meta.add_node(com_2)
        if com_1 != com_2 :
            if Meta.has_edge(com_1,com_2) :
                Meta[com_1][com_2]['weight'] += 1
            else :
                Meta.add_edge(com_1,com_2,weight=1)
    print("Métagraphe finis.") 
    print("Temps d'éxecution : ",round((time.time()-start_time_all),2))  
    return (giant,Meta,partition_vector)


