from networkx.classes import neighbors
from networkx.algorithms import center
import init_graph as ig
import random
import numpy as np

"""
Retourne une liste des noeuds avec un time_to_burn égal
au time_to_burn maximal -1.
"""
def next_node_to_burn(graph,tmp_graph,shortest_paths_matrix) :
    burned_nodes = []
    for node in graph.nodes() :
        if node not in tmp_graph :
            burned_nodes.append(node)         
    maxi = -1
    dico=dict()
    for node in graph.nodes() :
        if node in tmp_graph :
            mini = int(np.min(shortest_paths_matrix[node,burned_nodes]))
            if mini > maxi :
                maxi = mini
            dico[node]=mini
    sequence=[]
    for node in dico.keys() :
        if dico[node]==maxi-1:
            sequence.append(node)
    return sequence

"""
Peut prendre en paramètre la matrice des plus courts chemins.
Brûle le graphe et renvoie sa burning_sequence.
/!\ Attention, la matrice des plus courts chemins est une matrice numpy 
de nombre de noeuds * nombre de noeuds. La RAM peut donc être très vite surcahrgé 
sur de grand graphe.
"""
def burn(graph,shortest_paths_matrix=None) :
    #initialize variables needed
    if shortest_paths_matrix is None :
        shortest_paths_matrix=ig.make_matrix_of_shortest_paths(graph)
        
    tmp_graph = graph.copy()
    # step 0: choosing first activator
    next_node = center(graph)[0]
    burning_sequence = []
    burning_sequence.append(next_node)
    # the set of burned nodes at the previous step 
    previous_step = {next_node}
    while len(tmp_graph)>0 :
        # remembering the nodes whose neighbors must burn
        # this set contains neighbors of every previously burned nodes, if they still belong to tmp_graph
        to_burn=set(neighbor for v in previous_step for neighbor in neighbors(tmp_graph,v))
        # and removing them from the graph
        tmp_graph.remove_nodes_from(previous_step)
        # the process stops if the tmp_graph is empty
        if len(tmp_graph)==0 :
            break
        # step i: we choose a non-burned activator
        sequence_next_nodes = next_node_to_burn(graph,tmp_graph,shortest_paths_matrix)
        if sequence_next_nodes :
            next_node = random.choice(sequence_next_nodes)
        else :
            sequence_random = []
            for node in tmp_graph.nodes() :
                sequence_random.append(node)
            next_node = random.choice(sequence_random)    
        # and next burn neighbors of PREVIOUSLY burned nodes
        previous_step={v for v in to_burn if v in tmp_graph.nodes()}    
        previous_step.add(next_node)
        burning_sequence.append(next_node)
    return burning_sequence