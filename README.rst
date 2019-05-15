|logo|

About
-----

**Simple and interactive network visualization in Python.** Network
visualization is an indispensable tool for exploring and communicating
patterns in complex systems. Netwulf offers an ultra-simple API for
**reproducible interactive visualization** of networks directly from a
Python prompt or Jupyter notebook. As a research tool, its purpose is to
allow hassle-free quick interactive layouting/styling for communication
purposes.

The package is build around the philosophy that network manipulation and
preprocessing should be done programmatically, but that the efficient
generation of a visually appealing network is best done interactively,
without code.

|example|

Install
-------

.. code:: bash

    pip install netwulf

``netwulf`` was developed and tested for

-  Python 3.5
-  Python 3.6
-  Python 3.7

So far, the package's functionality was tested on Mac OS X, several
Linux distributions and Windows NT. Windows support cannot be guaranteed
as we do not have constant access to machines with this OS.

Dependencies
------------

``netwulf`` directly depends on the following packages which will be
installed by ``pip`` during the installation process

-  ``networkx>=2.0``
-  ``numpy>=0.14``
-  ``matplotlib>=3.0``
-  ``simplejson>=3.0``

Documentation
-------------

The full documentation is available at https://netwulf.rtfd.io.

Example
-------

Create a network and look at it

.. code:: python

    import networkx as nx
    from netwulf import visualize

    G = nx.barabasi_albert_graph(100,m=1)
    visualize(G)

|visualization example0|

Changelog
---------

Changes are logged in a `separate
file <https://github.com/benmaier/netwulf/blob/master/CHANGELOG.md>`__.

Contributing
------------

If you want to contribute to this project, please make sure to read the
`code of
conduct <https://github.com/benmaier/netwulf/blob/master/CODE_OF_CONDUCT.md>`__
and the `contributing
guidelines <https://github.com/benmaier/netwulf/blob/master/CONTRIBUTING.md>`__.

|Contributor Covenant|

License
-------

This project is licensed under the `MIT
License <https://github.com/benmaier/netwulf/blob/master/LICENSE>`__.

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
.. |example| image:: https://github.com/benmaier/netwulf/raw/master/img/simple_example.gif
.. |visualization example0| image:: https://github.com/benmaier/netwulf/raw/master/img/BA_1.png
.. |Contributor Covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg
   :target: code-of-conduct.md
