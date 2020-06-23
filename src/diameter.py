from networkx.classes import neighbors
from networkx.algorithms.shortest_paths import shortest_path
import init_graph as ig
import random
import math
import numpy as np

"""
Retourne le plus long des plus courts chemin du graphe.
"""
def longest_shortest_path_graph(graph,shortest_paths_matrix) :
    maxi = -1
    for i in range(0,shortest_paths_matrix.shape[0]):
     for j in range(0,shortest_paths_matrix.shape[1]):
             if maxi < shortest_paths_matrix[i,j] and i in graph and j in graph :
                 maxi = shortest_paths_matrix[i,j]
                 max_src = i
                 max_tar = j
    return shortest_path(graph,max_src,max_tar)

"""
Vérifie que le plus long des plus courts chemin n'est toujours pas brûlé.
"""
def still_not_burn(sequence_longest_shortest_path,tmp_graph) :
    for elt in sequence_longest_shortest_path :
        if elt in tmp_graph :
            return True
    return False

"""
Peut prendre en paramètre la matrice des plus courts chemins.
Brûle le graphe et renvoie sa burning_sequence.
"""
def burn(graph,shortest_paths_matrix=None) :
    if shortest_paths_matrix is None :
        shortest_paths_matrix = ig.make_matrix_of_shortest_paths(graph)
    sequence_longest_shortest_path = longest_shortest_path_graph(graph,shortest_paths_matrix)
    
    tmp_graph = graph.copy()
    len_diameter = len(sequence_longest_shortest_path)
    square_diameter = int(np.ceil(math.sqrt(len_diameter)))
    step = square_diameter-1
    # step 0: choosing first activator
    if len_diameter < step * step + square_diameter :
        next_node = sequence_longest_shortest_path[0]
    else : 
        next_node =  sequence_longest_shortest_path[(len_diameter - (step*step) - step )-1]
    step -= 1    
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
        if still_not_burn(sequence_longest_shortest_path,tmp_graph) :
            next_node =  sequence_longest_shortest_path[(len_diameter - (step*step) - step )-1]
            step -= 1
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