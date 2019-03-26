"""
Some useful things to tweak and reproduce the visualizations.
"""

import numpy as np
import networkx as nx

def bind_positions_to_network(network, network_properties):
    """
    Binds calculated positional values to the network as node attributes `x` and `y`.

    Parameters
    ==========
    network : networkx.Graph or something alike
        The network object to which the position should be bound
    network_properties : dict
        The network properties which are returned from the
        interactive visualization.
    """

    x =  { node['id']: node['pos'][0] for node in network_properties['nodes'] }
    y =  { node['id']: node['pos'][1] for node in network_properties['nodes'] }
    nx.set_node_attributes(network, x, 'x')
    nx.set_node_attributes(network, y, 'y')


if __name__ == "__main__":
    import pprint 
    pp = pprint.PrettyPrinter(indent=4)

    G = nx.Graph()
    G.add_nodes_from(range(10))
    G.add_nodes_from("abcde")

    from netwulf import visualize
    props, config = visualize(G)

    pp.pprint(props)
    bind_positions_to_network(G, props)
    visualize(G, config=config)
