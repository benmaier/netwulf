[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](code-of-conduct.md)

![logo](https://github.com/benmaier/netwulf/raw/master/img/logo_small.png)

## About

**Simple and interactive network visualization in Python.** Network visualization is an indispensable tool for exploring and communicating patterns in complex systems. Netwulf offers an ultra-simple API for **reproducible interactive visualization** of networks directly from a Python prompt or Jupyter notebook. As a research tool, its purpose is to allow hassle-free quick exploration of networks, and enable interactive layouting and styling for communication purposes.

![example](https://github.com/benmaier/netwulf/raw/master/img/simple_example.gif)


## Install

    pip install netwulf

`netwulf` was developed and tested for 

* Python 3.5
* Python 3.6
* Python 3.7

## Dependencies

`netwulf` directly depends on the following packages which will be installed by `pip` during the installation process

* `networkx>=2.0`
* `numpy>=0.14`
* `matplotlib>=3.0`
* `simplejson>=3.0`

## Documentation

The full documentation is available at https://netwulf.rtfd.io .

## Example

Create a network and look at it

```python
import networkx as nx
from netwulf import visualize

G = nx.barabasi_albert_graph(100,m=1)
visualize(G)
```

![visualization example0](https://github.com/benmaier/netwulf/raw/master/img/BA_1.png)

## Contributing

If you want to contribute to this project, please make sure to read the [code of conduct](https://github.com/benmaier/netwulf/raw/master/CONDE_OF_CONDUCT.md) and the [contributing guidelines](https://github.com/benmaier/netwulf/raw/master/CONTRIBUTING.md).

## Dev notes

The JS base code in `/netwulf/js/` is a fork of [Ulf Aslak's interactive web app](https://github.com/ulfaslak/network_styling_with_d3). If this repository is updated, change to `/netwulf/js/`, then do

```bash
git fetch upstream
git merge upstream/master
git commit -m "merged"
git push
```

If you want to upload to PyPI, first convert the new `README.md` to `README.rst`

```bash
make readme
```

It will give you warnings about bad `.rst`-syntax. Fix those errors in `README.rst`. Then wrap the whole thing 

```bash
make pypi
```

It will probably give you more warnings about `.rst`-syntax. Fix those until the warnings disappear. Then do

```bash
make upload
```
