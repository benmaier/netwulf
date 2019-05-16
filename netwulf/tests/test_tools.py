from netwulf.tools import bind_positions_to_network
from netwulf import visualize
import networkx as nx

def test_binding():

    G = nx.Graph()
    G.add_nodes_from(range(10))
    G.add_nodes_from("abcde")
    G.add_edges_from([("a","b")])

    props, config = visualize(G,is_test=True)

    bind_positions_to_network(G, props)
    newprops, newconfig = visualize(G, config=config,is_test=True)
    
def test_posting():
    G = nx.Graph()
    G.add_nodes_from(range(10))
    G.add_nodes_from("abcde")
    G.add_edges_from([("a","b")])
    visualize(G,is_test=True)

