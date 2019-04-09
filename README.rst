|logo|

netwulf
=======

This package provides an interface between
`networkx <https://networkx.github.io/>`__ Graph objects and `Ulf
Aslak's interactive web
app <https://github.com/ulfaslak/network_styling_with_d3>`__ for simple
and better network visualizations.

Install
-------

.. code:: bash

    pip install netwulf

Beware: ``netwulf`` only works with Python 3!

Example
-------

Standard
~~~~~~~~

Create a network and look at it

.. code:: python

    import networkx as nx
    from netwulf import visualize

    G = nx.barabasi_albert_graph(100,m=1)
    visualize(G)

|visualization example0|

When the visualization was posted to Python in the Browser, the function
actually returns a dictionary containing all style information of the
stylized network. For instance,

.. code:: python

    import networkx as nx
    from netwulf import visualize

    G = nx.barabasi_albert_graph(5,m=1)
    # the following only works if the user clicked "Post to Python" in the visualization.
    network_properties, config = visualize(G)
    print(network_properties)

A possible result from this code is

.. code:: python

    {   'height': 919,
        'linkAlpha': 0.5,
        'linkColor': '#7c7c7c',
        'links': [   {'link': [0, 1], 'width': 2},
                     {'link': [0, 2], 'width': 2},
                     {'link': [0, 3], 'width': 2},
                     {'link': [2, 4], 'width': 2}],
        'nodeStrokeColor': '#000000',
        'nodeStrokeWidth': 0.5,
        'nodes': [   {   'color': '#16a085',
                         'id': 0,
                         'pos': [442.2593240813363, 454.37557840980224],
                         'radius': 5.632111911473014},
                     {   'color': '#16a085',
                         'id': 1,
                         'pos': [481.8171665449027, 438.58151881303337],
                         'radius': 5.632111911473014},
                     {   'color': '#16a085',
                         'id': 2,
                         'pos': [446.98116529402097, 495.93002968604276],
                         'radius': 5.632111911473014},
                     {   'color': '#16a085',
                         'id': 3,
                         'pos': [437.9340114428489, 414.42238247014905],
                         'radius': 5.632111911473014},
                     {   'color': '#16a085',
                         'id': 4,
                         'pos': [488.5033653510982, 494.1926029578719],
                         'radius': 5.632111911473014}],
        'width': 919
    }

Config
~~~~~~

It's possible to change the default settings which are

.. code:: python

    default_config = {
      'Apply heat (wiggle)': False,
      'Charge strength': -10,
      'Center gravity': 0.1,
      'Link distance': 10,
      'Link width': 2,
      'Link alpha': 0.5,
      'Node size': 10, 
      'Node stroke size': 0.5,
      'Node size exponent': 0.5,
      'Link strength exponent': 0.1,
      'Link width exponent': 0.5,
      'Collision': False,
      'Node fill': '#16a085',
      'Node stroke': '#000000',
      'Link stroke': '#7c7c7c',
      'Label stroke': '#000000',
      'Show labels': False,
      'Zoom': 1.5,
      'Min. link weight %': 0,
      'Max. link weight %': 100
    }

It's done like so:

.. code:: python

    import networkx as nx
    from netwulf import visualize

    G = nx.barabasi_albert_graph(5000,m=1)
    visualize(G,config={
            'Node size': 11,
            'Charge strength' : -0.8,
            'Link distance' : 10,
            'Link width' : 1,
            'Collision' : True,
        })

|visualization example1|

Attributes
~~~~~~~~~~

Node attributes such as 'group' or 'size' that you define in your
``networkx.Graph`` are automatically visualized.

.. code:: Python

    import networkx as nx
    import community
    from netwulf import visualize

    G = nx.random_partition_graph([10,10,10],.25,.01)
    bb = community.best_partition(G)  # dict of node-community pairs
    nx.set_node_attributes(G, bb, 'group')

    visualize(G)

|visualization example2|

Dev notes
---------

The JS base code in ``/netwulf/js/`` is a fork of `Ulf Aslak's
interactive web
app <https://github.com/ulfaslak/network_styling_with_d3>`__. If this
repository is updated, change to ``/netwulf/js/``, then do

.. code:: bash

    git fetch upstream
    git merge upstream/master
    git commit -m "merged"
    git push

If you want to upload to PyPI, first convert the new ``README.md`` to
``README.rst``

.. code:: bash

    make readme

It will give you warnings about bad ``.rst``-syntax. Fix those errors in
``README.rst``. Then wrap the whole thing

.. code:: bash

    make pypi

It will probably give you more warnings about ``.rst``-syntax. Fix those
until the warnings disappear. Then do

.. code:: bash

    make upload

.. |logo| image:: https://github.com/benmaier/netwulf/raw/master/img/logo_small.png
.. |visualization example0| image:: https://github.com/benmaier/netwulf/raw/master/img/BA_1.png
.. |visualization example1| image:: https://github.com/benmaier/netwulf/raw/master/img/BA_2.png
.. |visualization example2| image:: https://github.com/benmaier/netwulf/raw/master/img/attributes_1.png
