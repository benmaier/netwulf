Use network style in Python
---------------------------

The network data tuned by the visualization can be posted back
to Python. The visualization function can actually return 
two dictionaries, the first containing information about the stylized
network, the second containing information about the 
visualization control configuration.

Start a visualization like this

.. code:: python

    import networkx as nx
    import netwulf as wulf

    G = nx.barabasi_albert_graph(100,2)

    stylized_network, config = wulf.visualize(G)


A visualization window is opened and the network can be stylized.
Once you're done, press the button `Post to Python`.

.. figure:: img/post_to_python.png

    Post to Python

Pressing this button will lead the data to be posted back to Python. 
Subsequently the browser window will be closed. The Python kernel will
not be responding until either the `Post to Python`-button is pressed
or the ``KeyboardInterrupt`` signal is send (manually or using the `Stop`-Button 
in a Jupyter notebook).

The returned stylized network dictionary will contain all the necessary information
to reproduce the figure. It will look something like this.

.. code:: python

    stylized_network = {
         'xlim': [0, 833],
         'ylim': [0, 833],
         'linkColor': '#7c7c7c',
         'linkAlpha': 0.5,
         'nodeStrokeColor': '#000000',
         'nodeStrokeWidth': 0.75,
         'links': [{'link': [0, 2], 'width': 3},
          {'link': [0, 3], 'width': 3},
          {'link': [0, 4], 'width': 3},
          {'link': [1, 2], 'width': 3},
          {'link': [1, 3], 'width': 3},
          {'link': [1, 4], 'width': 3}],
         'nodes': [{'id': 0,
           'pos': [436.0933431058901, 431.72418500564186],
           'radius': 20,
           'color': '#16a085'},
          {'id': 1,
           'pos': [404.62184898400426, 394.8158724310507],
           'radius': 20,
           'color': '#16a085'},
          {'id': 2,
           'pos': [409.15148692745356, 438.08415417584683],
           'radius': 20,
           'color': '#16a085'},
          {'id': 3,
           'pos': [439.27989436871223, 397.14932001193233],
           'radius': 20,
           'color': '#16a085'},
          {'id': 4,
           'pos': [393.4680683212157, 420.63184247673917],
           'radius': 20,
           'color': '#16a085'}]
          }


Furthermore, the configuration
which was used to generate this figure will resemble

.. code:: python

    config = {
         'Apply heat (wiggle)': False,
         'Charge strength': -30,
         'Center gravity': 0.1,
         'Link distance': 10,
         'Link width': 2,
         'Link alpha': 0.5,
         'Node size': 10,
         'Node stroke size': 0.5,
         'Node size exponent': 0.5,
         'Link width exponent': 0.5,
         'Collision': False,
         'Node fill': '#16a085',
         'Node stroke': '#000000',
         'Link stroke': '#7c7c7c',
         'Label stroke': '#000000',
         'Show labels': False,
         'Show singleton nodes': False,
         'Node size by strength': False,
         'Zoom': 1.5,
         'Min. link weight %': 0,
         'Max. link weight %': 100
         }

If the visualization was started from a Jupyter notebook, a picture of the stylized
network will appear additionally

.. figure:: img/figure_in_jupyter.png

    Stylized network in a Jupyter notebook.

In order to reproduce this visualization, you may want to call the visualization function
again with, passing the produced configuration.

.. code:: python

    wulf.visualize(G, config=config)
