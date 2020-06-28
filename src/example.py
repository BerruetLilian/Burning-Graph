import init_graph as ig
import sys
import degree
import visual
import visual_meta

graph = ig.init_graph(sys.argv[1])
giant_component = ig.reduce(graph)
burning_sequence = degree.burn(giant_component)
visual.draw(giant_component,burning_sequence)

#In the case of a graph with many nodes, it is advisable 
#to use the metagraph in order to obtain a readable visual.
"""
partition_vector = ig.louvain_community_vector(giant_component )
#a metragraph can be provided by using make_metagraph from init_graph
visual_meta.draw(giant_component ,burning_sequence,partition_vector)
"""