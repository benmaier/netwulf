import networkx as nx
from netwulf import visualize

G = nx.barabasi_albert_graph(100,2)

visualize(G)
