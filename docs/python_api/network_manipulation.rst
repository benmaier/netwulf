Network manipulation
--------------------

Filtering
~~~~~~~~~

Sometimes you have multiple edge or node attributes which can be
used to style your network. Using :mod:`netwulf.tools.get_filtered_network`
you can get a filtered network, where ``edge_weight_key`` is the name
of the edge attribute which will be used as the weight in the visualization
and ``node_group_key`` is the node attributed following which the nodes
will be grouped and colored in the visualization. Here's an example

.. code:: python

    import networkx as nx
    import netwulf as wulf

    import numpy as np

    G = nx.barabasi_albert_graph(100,1)

    for u, v in G.edges():
        # assign two random edge values to the network
        G[u][v]['foo'] = np.random.rand()
        G[u][v]['bar'] = np.random.rand()

    # assign node attributes according to some generic grouping 
    grp = {u: 'ABCDE'[u%5]  for u in G.nodes() }
    nx.set_node_attributes(G, grp, 'wum')

    # filter the Graph to visualize one where the weight is determined by 'foo'
    new_G = wulf.get_filtered_network(G,edge_weight_key='foo')
    wulf.visualize(new_G)

    # filter the Graph to visualize one where the weight is determined by 'bar'
    # and the node group (coloring) is determined by the node attribute 'wum'
    new_G = wulf.get_filtered_network(G,edge_weight_key='bar',node_group_key='wum')
    wulf.visualize(new_G)

Binding positions
~~~~~~~~~~~~~~~~~

If the network has node attributes ``'x'`` and ``'y'``, those will be used as default
values in the visualization. In order to reproduce a visualization or continue
where you left off last time, you can bind the positions to the network

.. code:: python

    wulf.bind_positions_to_network(G, stylized_network)

There's no return value and the positions are directly written to the Graph-object ``G``.


