import networkx as nx
from netwulf import visualize
import json 

G = nx.barabasi_albert_graph(1000,2)

props, config = visualize(G,config={'Node size by strength':True,'Collision':True,'Node size': 25})
with open('BA_network_properties.json', 'w') as outfile:
    json.dump(props, outfile)

