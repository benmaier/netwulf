import unittest

import numpy as np
import matplotlib.pyplot as pl
import networkx as nx

from netwulf.tools import bind_positions_to_network, get_filtered_network, draw_netwulf
from netwulf import visualize

def _get_test_network():
    G = nx.Graph()
    G.add_nodes_from(range(2))
    G.add_nodes_from("ab")
    G.add_edges_from([("a","b")])

    return G

def _round_positions(props):

    for i, n in enumerate(props['nodes']):
        props['nodes'][i]['x'] = np.around(props['nodes'][i]['x'],2)
        props['nodes'][i]['y'] = np.around(props['nodes'][i]['y'],2)

class Test(unittest.TestCase):

    maxDiff = None

    def test_posting(self):
        """Test whether results are sucessfully posted to Python."""
        G = _get_test_network()
        visualize(G,is_test=True)

    def test_reproducibility(self):
        """Test whether a restarted network visualization with binded positions results in the same visualization."""
        G = _get_test_network()
        props, config = visualize(G,is_test=True)        

        bind_positions_to_network(G, props)
        newprops, newconfig = visualize(G, config=config,is_test=True)

        # round all positional values to their 4th decimal place
        _round_positions(props)
        _round_positions(newprops)

        # the second visualization should have frozen the nodes
        assert(newconfig['freeze_nodes'] == True)

        # change it so the dictionary-equal-assertion doesnt fail
        newconfig['freeze_nodes'] = False

        self.assertDictEqual(props, newprops)
        self.assertDictEqual(config, newconfig)
    
    def test_filtering(self):
        """Test whether filtering works the way it should."""

        G = _get_test_network()
        for u, v in G.edges():
            G[u][v]['foo'] = np.random.rand()
            G[u][v]['bar'] = np.random.rand()

        grp = {u: 'AB'[i%2]  for i, u in enumerate(G.nodes()) }

        new_G = get_filtered_network(G,edge_weight_key='foo')
        visualize(new_G,is_test=True)

        nx.set_node_attributes(G, grp, 'wum')

        new_G = get_filtered_network(G,edge_weight_key='bar',node_group_key='wum')
        visualize(new_G,is_test=True)

    def test_matplotlib(self):
        stylized_network = {   'linkAlpha': 0.5,
                               'linkColor': '#7c7c7c',
                               'links': [   {'source': 0, 'target': 1, 'width': 8.067180430164552},
                                            {'source': 0, 'target': 2, 'width': 8.067180430164552},
                                            {'source': 0, 'target': 4, 'width': 8.067180430164552},
                                            {'source': 0, 'target': 6, 'width': 8.067180430164552},
                                            {'source': 1, 'target': 3, 'width': 8.067180430164552},
                                            {'source': 1, 'target': 7, 'width': 8.067180430164552},
                                            {'source': 4, 'target': 5, 'width': 8.067180430164552},
                                            {'source': 4, 'target': 9, 'width': 8.067180430164552},
                                            {'source': 6, 'target': 8, 'width': 8.067180430164552}],
                               'nodeStrokeColor': '#000000',
                               'nodeStrokeWidth': 2.898890104734921,
                               'nodes': [   {   'color': '#16a085',
                                                'id': 0,
                                                'radius': 27.71774321528189,
                                                'x': 425.30610641802105,
                                                'y': 408.2306291226664},
                                            {   'color': '#16a085',
                                                'id': 1,
                                                'radius': 24.004269760007883,
                                                'x': 396.4745121676665,
                                                'y': 501.4049104000019},
                                            {   'color': '#16a085',
                                                'id': 2,
                                                'radius': 13.858871607640944,
                                                'x': 473.08739238768067,
                                                'y': 351.91545364057833},
                                            {   'color': '#16a085',
                                                'id': 3,
                                                'radius': 13.858871607640944,
                                                'x': 419.7726184875137,
                                                'y': 569.8869495527006},
                                            {   'color': '#16a085',
                                                'id': 4,
                                                'radius': 24.004269760007883,
                                                'x': 357.7122249241811,
                                                'y': 329.38938497349545},
                                            {   'color': '#16a085',
                                                'id': 5,
                                                'radius': 13.858871607640944,
                                                'x': 374.1221609268641,
                                                'y': 257.68914701013045},
                                            {   'color': '#16a085',
                                                'id': 6,
                                                'radius': 19.599404186713244,
                                                'x': 516.4329698471261,
                                                'y': 437.85889577403395},
                                            {   'color': '#16a085',
                                                'id': 7,
                                                'radius': 13.858871607640944,
                                                'x': 329.1977725136212,
                                                'y': 531.0354125644326},
                                            {   'color': '#16a085',
                                                'id': 8,
                                                'radius': 13.858871607640944,
                                                'x': 586.3601749401209,
                                                'y': 457.9664495383031},
                                            {   'color': '#16a085',
                                                'id': 9,
                                                'radius': 13.858871607640944,
                                                'x': 286.53060275648363,
                                                'y': 319.624522724607}],
                               'xlim': [0, 833],
                               'ylim': [0, 833]
                               }


        draw_netwulf(stylized_network)
        pl.show()


if __name__ == "__main__":


    T = Test()

    T.test_matplotlib()
