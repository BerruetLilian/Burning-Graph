from networkx.classes import neighbors
from networkx.algorithms.centrality import betweenness_centrality

"""
Retourne le noeud avec la plus grande
centralité d'intermédiarité.
La méthode de centralité de networkx peut avoir en temps d'exécution conséquent 
dans le cas de grand graphe.
"""
def max_centrality(G) :
    centrality = betweenness_centrality(G)
    return  max(centrality.keys(), key=(lambda k: centrality[k]))
    
"""
Brûle le graphe et renvoie sa burning_sequence.
"""   
def burn(graph) :
    tmp_graph = graph.copy()
    # step 0: choosing first activator
    next_node = max_centrality(tmp_graph)
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
        next_node = max_centrality(tmp_graph)
        # and next burn neighbors of PREVIOUSLY burned nodes
        previous_step={v for v in to_burn if v in tmp_graph.nodes()}    
        previous_step.add(next_node)
        burning_sequence.append(next_node)
    return burning_sequence