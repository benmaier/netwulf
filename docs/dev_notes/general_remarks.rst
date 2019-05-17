General remarks
===============

Contributing
------------

You can contribute to the `public repository`_ and `raise issues`_ there. Please also make sure to follow the `code of conduct`_ and to read the `contributing notes`_. Make sure to also read about :ref:`testing` before you open a pull request.

Install dev version
-------------------

Clone and install this repository as

.. code:: bash

    git clone --recurse-submodules -j8 git@github.com:benmaier/netwulf.git
    make

Note that ``make`` per default lets ``pip`` install a development
version of the repository.

Update JS base
--------------

The JS base code in ``/netwulf/js/`` is a fork of `Ulf Aslak's
interactive web
app <https://github.com/ulfaslak/network_styling_with_d3>`__. If this
repository is updated, change to ``/netwulf/js/``, then do

.. code:: bash

    git fetch upstream
    git merge upstream/master
    git commit -m "merged"
    git push

Upload to PyPI
--------------

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

.. _`public repository`: https://github.com/benmaier/netwulf
.. _`raise issues`: https://github.com/benmaier/netwulf/issues/new
.. _`code of conduct`: https://github.com/benmaier/netwulf/blob/master/CODE_OF_CONDUCT.md
.. _`contributing notes`: https://github.com/benmaier/netwulf/blob/master/CONTRIBUTING.md

