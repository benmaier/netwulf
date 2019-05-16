About this project
==================

Netwulf is an interactive visualization tool for networkx_ Graph-objects,
that allows you to produce beautifully looking network visualizations. Simply
input a `networkx.Graph` object, style the network in the interactive console
and either download the result as a PNG or pipe the layout back to Python for
further processing. Netwulf is fast and relies on no crude dependencies.
It is build around the philosophy that network manipulation and preprocessing 
should be done programmatically, but that the efficient generation of a visually 
appealing network is best done interactively, without code.

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

Make sure to read the ``README.md`` in the `public repository`_ for notes on dependencies and installation.

``netwulf`` directly depends on the following packages which will be
installed by ``pip`` during the installation process

-  ``networkx>=2.0``
-  ``numpy>=0.14``
-  ``matplotlib>=3.0``
-  ``simplejson>=3.0``


Bug reports & contributing
--------------------------

You can contribute to the `public repository`_ and `raise issues`_ there. Please also make sure to follow the `code of conduct`_ and to read the `contributing notes`_.


.. _`public repository`: https://github.com/benmaier/netwulf
.. _networkx: https://networkx.github.io/
.. _`raise issues`: https://github.com/benmaier/netwulf/issues/new
.. _`code of conduct`: https://github.com/benmaier/netwulf/blob/master/CODE_OF_CONDUCT.md
.. _`contributing notes`: https://github.com/benmaier/netwulf/blob/master/CONTRIBUTING.md

