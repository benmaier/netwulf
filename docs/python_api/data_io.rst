Data I/O
--------

It's not too hard to dump the returned visualization session to a json-file 
to restore it easily, but we wrote a wrapper for that nevertheless.

Start a visualization like this

.. code:: python

    import networkx as nx
    import netwulf as wulf

    G = nx.barabasi_albert_graph(100,2)

    stylized_network, config = wulf.visualize(G)

You can either save/load the stylized network only

.. code:: python

    wulf.save("BA.json", stylized_network, config)
    stylized_network, config, _ = wulf.load("BA.json")
    wulf.draw_netwulf(stylized_network, config)


.. figure:: img/post_to_python.png
    :width: 500

Or you can save/load with the respective ``networkx.Graph``-object
in order to replicate some other features.

.. code:: python

    wulf.save("BA.json", stylized_network, config, G)
    stylized_network, config, G = wulf.load("BA.json")

