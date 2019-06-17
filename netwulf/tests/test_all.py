import unittest

import numpy as np
import matplotlib.pyplot as pl
import networkx as nx

from netwulf.tools import bind_properties_to_network, get_filtered_network, draw_netwulf, node_pos, add_node_label, add_edge_label
from netwulf import visualize

def _get_test_network():
    G = nx.Graph()
    G.add_nodes_from(range(2))
    G.add_nodes_from("ab")
    G.add_edges_from([("a","b")])
    G.add_edges_from([("a",0)])

    return G

def _get_test_config():
    return {'node_size':2,'link_width':2,'zoom':3}

def _drastically_round_positions(props,nprec=-1):

    for i, n in enumerate(props['nodes']):
        props['nodes'][i]['x'] = np.around(props['nodes'][i]['x'],nprec)
        props['nodes'][i]['y'] = np.around(props['nodes'][i]['y'],nprec)
        props['nodes'][i]['x_canvas'] = np.around(props['nodes'][i]['x_canvas'],nprec)
        props['nodes'][i]['y_canvas'] = np.around(props['nodes'][i]['y_canvas'],nprec)

def _assert_positions_within_one_percent(props1,props2):

    for i, n in enumerate(props1['nodes']):
        assert(np.isclose(props1['nodes'][i]['x'], props2['nodes'][i]['x'],rtol=1e-2))
        assert(np.isclose(props1['nodes'][i]['y'], props2['nodes'][i]['y'],rtol=1e-2))
        assert(np.isclose(props1['nodes'][i]['x_canvas'], props2['nodes'][i]['x_canvas'],rtol=1e-2))
        assert(np.isclose(props1['nodes'][i]['y_canvas'], props2['nodes'][i]['y_canvas'],rtol=1e-2))


class Test(unittest.TestCase):

    maxDiff = None

    def test_posting(self):
        """Test whether results are sucessfully posted to Python."""
        G = _get_test_network()
        visualize(G,is_test=True,config=_get_test_config())

    def test_reproducibility(self):
        """Test whether a restarted network visualization with binded positions results in the same visualization."""
        G = _get_test_network()
        props, config = visualize(G,config=_get_test_config(),is_test=True)        

        bind_properties_to_network(G, props)
        newprops, newconfig = visualize(G, config=config,is_test=True)

        # test if node positions are close within 1% and subsequently 
        # round all positional values to the 2nd positon (e.g. 451 => 450)
        _assert_positions_within_one_percent(props,newprops)
        _drastically_round_positions(props)
        _drastically_round_positions(newprops)

        # the second visualization should have frozen the nodes
        assert(newconfig['freeze_nodes'])

        # change it so the dictionary-equal-assertion doesnt fail
        newconfig['freeze_nodes'] = False

        self.assertDictEqual(props, newprops)
        self.assertDictEqual(config, newconfig)
    
    def test_filtering(self):
        """Test whether filtering works the way it should."""

        G = _get_test_network()
        weights = [10,100]
        for e, (u, v) in enumerate(G.edges()):
            G[u][v]['foo'] = weights[e]
            G[u][v]['bar'] = weights[(e+1)%2]

        grp = {u: 'AB'[i%2]  for i, u in enumerate(G.nodes()) }

        new_G = get_filtered_network(G,edge_weight_key='foo')
        visualize(new_G,is_test=True,config=_get_test_config())

        nx.set_node_attributes(G, grp, 'wum')

        new_G = get_filtered_network(G,edge_weight_key='bar',node_group_key='wum')
        visualize(new_G,is_test=True,config=_get_test_config())

    def test_matplotlib(self):
        """Test how the produced figure looks"""
        stylized_network = {   'linkAlpha': 0.2,
            'linkColor': '#758000',
            'links': [   {'source': 0, 'target': 1, 'weight': 1, 'width': 40},
                         {'source': 0, 'target': 3, 'weight': 1, 'width': 40},
                         {'source': 1, 'target': 2, 'weight': 1, 'width': 40},
                         {'source': 1, 'target': 4, 'weight': 1, 'width': 40}],
            'nodeStrokeColor': '#ffffff',
            'nodeStrokeWidth': 4,
            'nodes': [   {   'color': '#79aa00',
                             'id': 0,
                             'radius': 28.577380332470412,
                             'x': 420.4774227636891,
                             'x_canvas': 444.34195934582385,
                             'y': 402.92277557839725,
                             'y_canvas': 321.45942904878075},
                         {   'color': '#79aa00',
                             'id': 1,
                             'radius': 35,
                             'x': 419.94297017162165,
                             'x_canvas': 440.6007912013515,
                             'y': 426.56813829452074,
                             'y_canvas': 486.9769680616455},
                         {   'color': '#79aa00',
                             'id': 2,
                             'radius': 20.207259421636905,
                             'x': 405.5333864027982,
                             'x_canvas': 339.73370481958773,
                             'y': 411.01250794520007,
                             'y_canvas': 378.08755561640055},
                         {   'color': '#79aa00',
                             'id': 3,
                             'radius': 20.207259421636905,
                             'x': 434.1529311105535,
                             'x_canvas': 540.0705177738741,
                             'y': 413.3758620827409,
                             'y_canvas': 394.6310345791867},
                         {   'color': '#79aa00',
                             'id': 4,
                             'radius': 20.207259421636905,
                             'x': 403.23992572436083,
                             'x_canvas': 323.67948007052564,
                             'y': 429.81017078651104,
                             'y_canvas': 509.67119550557754}],
            'xlim': [0, 833],
            'ylim': [0, 833]
            }


        fig, ax = draw_netwulf(stylized_network)

        add_node_label(ax, stylized_network, 0)
        add_edge_label(ax, stylized_network, (0,1))
        pl.show(block=False)
        pl.pause(5)
        pl.close()


    def test_config_adaption(self):
        """Test whether config values are properly adapted."""
        config = {
            # Input/output
            'zoom':4,
            # Physics
            'node_charge': -70,
            'node_gravity': 0.5,
            'link_distance': 15,
            'link_distance_variation': 2,
            'node_collision': True,
            'wiggle_nodes': True,
            'freeze_nodes': False,
            # Nodes
            'node_fill_color': '#79aa00',
            'node_stroke_color': '#ffffff',
            'node_label_color': '#888888',
            'display_node_labels': True,
            'scale_node_size_by_strength': True,
            'node_size': 5,
            'node_stroke_width': 1,
            'node_size_variation': 0.7,
            # Links
            'link_color': '#758000',
            'link_width': 10,
            'link_alpha': 0.2,
            'link_width_variation': 0.7,
            # Thresholding
            'display_singleton_nodes': False,
            'min_link_weight_percentile': 0.1,
            'max_link_weight_percentile': 0.9,
        }

        G = _get_test_network()
        _, newconfig = visualize(G,config=config,is_test=True)

        self.assertDictEqual(config, newconfig)



if __name__ == "__main__":


    T = Test()

    T.test_matplotlib()
    #T.test_config_adaption()
