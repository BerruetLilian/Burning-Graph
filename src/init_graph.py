import networkx as nx
import numpy as np
from networkx.algorithms.shortest_paths import all_pairs_shortest_path_length
from networkx.relabel import relabel_nodes
from community import community_louvain

"""
Initialise un graphe networkx à partir du chemin
d'un fichier sous le format noeud_source [espace] noeud_cible.
Les noeuds sont de type entier.
"""
def init_graph(data_file) :
    return nx.read_edgelist(data_file,nodetype=int)

"""
Retour le composant convexe le plus grand du graphe
et réindexe les noeuds.
"""     
def reduce(graph) :
    connected_component = sorted(nx.connected_components(graph), key=len, reverse=True)
    giant = graph.subgraph(connected_component[0])
    dico = dict()
    ind = 0
    for node in graph :
        if node in giant :  
            dico[node]=ind
            ind=ind+1
    return relabel_nodes(giant,dico)

"""
Retourne un dictionnaire qui associe un noeud à sa communauté 
selon la méthode Louvain.
/!\ renvoie une partition différente à chaque appel.
"""
def louvain_community(graph) :
    return community_louvain.best_partition(graph)

"""
Retourne une séquence qui associe un noeud à sa communauté 
selon la méthode Louvain. 
/!\ renvoie une partition différente à chaque appel.
/!\ Le graphe doit avoir des neouds de type entier.
"""
def louvain_community_vector(graph) :
    return list(louvain_community(graph).values())

"""
Retourne une matrice numpy qui associe un noeud à un noeud au plus court chemin qui les relies.
{ noeud_source : { neoud_cible : [plus_court_chemin] } }
"""
def make_matrix_of_shortest_paths(graph) :
    shortest_paths_matrix = np.zeros((len(graph),len(graph)))
    generator = all_pairs_shortest_path_length(graph)
    for node_src,dico in generator :
        for node_tar in dico :
            shortest_paths_matrix[node_src,node_tar]=dico[node_tar]
            shortest_paths_matrix[node_tar,node_src]=dico[node_tar]
    return shortest_paths_matrix

"""
Retourne le métagraphe du graphe selon sa partition de communauté.
"""
def make_metagraph(graph,partition_vector) :
    metagraph = nx.Graph()
    for edge in graph.edges() :
        com_1 = partition_vector[edge[0]]
        com_2 = partition_vector[edge[1]]
        if com_1 not in metagraph.nodes() :
            metagraph.add_node(com_1)
        if com_2 not in metagraph.nodes() :
            metagraph.add_node(com_2)
        if com_1 != com_2 :
            if metagraph.has_edge(com_1,com_2) :
                metagraph[com_1][com_2]['weight'] += 1
            else :
                metagraph.add_edge(com_1,com_2,weight=1) 
    return metagraph