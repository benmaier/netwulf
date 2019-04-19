About this project
==================

Netwulf is an interactive visualization tool for networkx_ Graph-objects,
that allows you to produce beautiful looking network visualizations. Simply
input a `networkx.Graph` object, style the network in the interactive console
and either download the result as a PNG or pipe the layout back to Python for
further processing. Netwulf is fast and relies on no crude dependencies.

Quick example
-------------

.. code:: python

    import networkx as nx
    from netwulf import visualize

    G = nx.barabasi_albert_graph(100,2)

    visualize(G)

.. figure:: img/simple_example.gif
    
    started visualization

Why should I use netwulf
------------------------

Pros
~~~~

- Interactive styling of network visualizations in the browser, started from Python
- No compiling needed
- No external program needed 
- Cross-platform
- Seamlessly use the inferred style back in Python
- Redraw the visualization in Python using matplotlib

Cons
~~~~

- No multiedges yet
- No rendering of directed edges


Install
-------

::

   pip install netwulf


Bug reports & contributing
--------------------------

You can contribute to the `public repository`_ and raise issues there.


.. _`public repository`: https://github.com/benmaier/netwulf
.. _networkx: https://networkx.github.io/

