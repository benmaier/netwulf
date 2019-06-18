Simplest use case
-----------------

Given a *networkx.Graph* object, you can launch netwulf like so:

.. code:: python

	import networkx as nx
	import netwulf as wulf

	G = nx.barabasi_albert_graph(100, 2)

	wulf.visualize(G)  # <-- THIS IS IT

Alternatively, *netwulf.visualize* can accept a node-link dictionary object `formatted like this <https://gist.githubusercontent.com/ulfaslak/6be66de1ac3288d5c1d9452570cbba5a/raw/4cab5036464800e51ce59fc088688e9821795efb/miserables.json>`_.


Node and link attributes
------------------------

Netwulf recognizes node attributes 'group' and 'size', and link attribute 'weight'.
Users can create a *networkx.Graph* object with node and link data:

.. code:: python

    list(G.nodes(data=True))[:3]
    # [(0, {'group': 0, 'size': 0.20982489558943607}),
    #  (1, {'group': 0, 'size': 0.7118952904573288}),
    #  (2, {'group': 0, 'size': 0.8785902846905586})]

    list(G.edges(data=True))[:3]
    # [(0, 5, {'weight': 0.8917083938103719}),
    #  (0, 9, {'weight': 0.29583879684946757}),
    #  (0, 12, {'weight': 0.36847140599448236})]

Example:

.. code:: python

    import numpy as np
    import networkx as nx
    import netwulf as wulf

    # Create a network
    G = nx.random_partition_graph([10, 10, 10], .25, .01)

    # Change 'block' node attribute to 'group'
    for k, v in G.nodes(data=True):
        v['group'] = v['block']; del v['block']

    # Or detect communities and encode them in 'group' attribute
    # import community
    # bb = community.best_partition(G)
    # nx.set_node_attributes(G, bb, 'group')

    # Set node 'size' attributes
    for n, data in G.nodes(data=True):
        data['size'] = np.random.random()

    # Set link 'weight' attributes
    for n1, n2, data in G.edges(data=True):
        data['weight'] = np.random.random()

    wulf.visualize(G)


.. figure:: img/random_partition_graph.png

Note: If 'group' is not a color (like "red" or "#4fba21") the group colors are assigned randomly.


Initial node positions
----------------------

A network can be launched with initial node positions.
If netwulf sees node-attributes 'x' and 'y' like:

.. code:: python

    list(G.nodes(data=True))[:3]
    # [(0, {'x': 600, 'y': 400}),
    #  (1, {'x': 550, 'y': 450}),
    #  (2, {'x': 500, 'y': 500})]

it freezes the nodes in these positions at launch.
Nodes can be moved around in their frozen states.
Positions are relaxed upon untoggling "Freeze", toggling "Wiggle" or changing any of the physics parameters.



Save as PDF
-----------

.. code:: python

    import networkx as nx
    import netwulf as wulf
    import matplotlib.pyplot as plt
    
    G = nx.barabasi_albert_graph(100, 2)
    
    network, config = wulf.visualize(G, plot_in_cell_below=False)
    
    fig, ax = wulf.draw_netwulf(network, figsize=(10,10))
    plt.savefig("myfigure.pdf")


Labels and node positions
-------------------------

.. code:: python

    import networkx as nx
    import netwulf as wulf
    import matplotlib.pyplot as plt

    G = nx.Graph()
    G.add_nodes_from([0,1,2,'a','b','c'])
    G.add_edges_from([(0,1),('a','b')])

    network, config = wulf.visualize(G,config={'zoom':3})

    # draw links only at first
    fig, ax = wulf.draw_netwulf(network,draw_nodes=False)

    # get positions of two unconnected nodes to draw a link anyway
    v0 = wulf.node_pos(network, 'c')
    v1 = wulf.node_pos(network, 2)
    ax.plot([v0[0],v1[0]],[v0[1],v1[1]],c='#d95f02')

    # draw nodes now
    wulf.draw_netwulf(network,fig,ax,draw_links=False)

    # add labels to a node and an edge
    wulf.add_node_label(ax,network,'c')
    wulf.add_edge_label(ax,network,('a','b'))
    
.. figure:: img/labeled_graph.png
