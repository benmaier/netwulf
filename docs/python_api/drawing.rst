Reproducing the figure in Python
--------------------------------

Once retrieved, the stylized network data can be used
to reproduce the figure in Python. To this end you can use
the function :mod:`netwulf.tools.draw_netwulf`.

.. code:: python

    import networkx as nx
    import netwulf as wulf

    G = nx.barabasi_albert_graph(100,1)

    stylized_network, config = wulf.visualize(G)

    import matplotlib.pyplot as plt
    fig, ax = wulf.draw_netwulf(stylized_network)
    plt.show()


A visualization window is opened and the network can be stylized.
Once you're done, press the button `Post to Python`. Afterwards,
the figure will be redrawn in matplotlib and opened.

.. figure:: img/reproduced_figure.png

    Reproduced figure

In order to add labels, use netwulf's functions 
:mod:`netwulf.tools.add_edge_label` 
or
:mod:`netwulf.tools.add_node_label`.

.. code:: python

    add_edge_label(ax, stylized_network, (0,1))
    add_node_label(ax, stylized_network, 9)

This will add the node id and edge tuple to the figure. You can add an optional label string as 

.. code:: python

    add_edge_label(ax, stylized_network, (0,1), label='this edge')
    add_node_label(ax, stylized_network, 9, label='this node')

For additional styling options check out the respective functions docstrings at
:mod:`netwulf.tools.add_edge_label` 
or
:mod:`netwulf.tools.add_node_label`.
