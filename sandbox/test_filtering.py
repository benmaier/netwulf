import networkx as nx
from netwulf import visualize
from netwulf import get_filtered_network

import numpy as np

G = nx.barabasi_albert_graph(100,2)

for u, v in G.edges():
    G[u][v]['foo'] = np.random.rand()
    G[u][v]['bar'] = np.random.rand()

grp = {u: 'ABCDE'[u%5]  for u in G.nodes() }

nx.set_node_attributes(G, grp, 'wum')

new_G = get_filtered_network(G,edge_weight_key='foo')
visualize(new_G)

new_G = get_filtered_network(G,edge_weight_key='bar',node_group_key='wum')
visualize(new_G)

