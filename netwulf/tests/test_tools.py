from netwulf.tools import bind_positions_to_network
from netwulf import visualize
import networkx as nx

import numpy as np

from copy import deepcopy

import unittest

def _get_test_network():
    G = nx.Graph()
    G.add_nodes_from(range(2))
    G.add_nodes_from("ab")
    G.add_edges_from([("a","b")])

    return G

def _round_positions(props):

    for i, n in enumerate(props['nodes']):
        props['nodes'][i]['x'] = np.around(props['nodes'][i]['x'],3)
        props['nodes'][i]['y'] = np.around(props['nodes'][i]['y'],3)

class Test(unittest.TestCase):

    maxDiff = None

    def test_posting(self):
        """Test whether results are sucessfully posted to Python"""
        G = _get_test_network()
        visualize(G,is_test=True)

    def test_reproducibility(self):
        """Test whether a restarted network visualization with binded positions results in the same visualization"""
        G = _get_test_network()
        props, config = visualize(G,is_test=True)        

        bind_positions_to_network(G, props)
        newprops, newconfig = visualize(G, config=config,is_test=True)

        # round all positional values to their third decimal place
        _round_positions(props)
        _round_positions(newprops)

        # the second visualization should have frozen the nodes
        assert(newconfig['freeze_nodes'] == True)

        # change it so the dictionary-equal-assertion doesnt fail
        newconfig['freeze_nodes'] = False

        self.assertDictEqual(props, newprops)
        self.assertDictEqual(config, newconfig)

    def 
