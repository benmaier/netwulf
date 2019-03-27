Starting a visualization
------------------------

The interactive visualization is started from Python. 
In this module, we introduce the main functionalities 
supplied by the Python package.

A visualization is started as follows.

.. code:: python

    import networkx as nx
    from netwulf import visualize

    G = nx.barabasi_albert_graph(100,2)

    visualize(G)


A visualization window is opened and the network can be stylized.
