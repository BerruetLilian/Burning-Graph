import init_graph as ig
import sys
import degree
import visual

graph = ig.init_graph(sys.argv[1])
giant_component = ig.reduce(graph)
burning_sequence = degree.burn(giant_component)
visual.draw(giant_component,burning_sequence)