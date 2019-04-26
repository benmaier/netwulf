![logo](https://github.com/benmaier/netwulf/raw/master/img/logo_small.png)

## About

**Simple and interactive network visualization in Python.** Network visualization is an indispensable tool for exploring and communicating patterns in complex systems. Netwulf offers an ultra-simple API for **reproducible interactive visualization** of networks directly from a Python prompt or Jupyter notebook. As a research tool, its purpose is to allow hassle-free quick exploration of networks, and enable interactive layouting and styling for communication purposes.

![example](https://github.com/benmaier/netwulf/raw/master/img/simple_example.gif)



## Install

    pip install netwulf

Beware: `netwulf` only works with Python 3!

## Documentation

The full documentation is available [here](https://netwulf.readthedocs.io/en/latest/python_api/start.html).

## Example

### Standard

Create a network and look at it

```python
import networkx as nx
from netwulf import visualize

G = nx.barabasi_albert_graph(100,m=1)
visualize(G)
```

![visualization example0](https://github.com/benmaier/netwulf/raw/master/img/BA_1.png)

When the visualization was posted to Python in the Browser, the function actually returns a dictionary containing all style information of the stylized network. For instance,

```python
import networkx as nx
from netwulf import visualize

G = nx.barabasi_albert_graph(5,m=1)
# the following only works if the user clicked "Post to Python" in the visualization.
network_properties, config = visualize(G)
print(network_properties)
```

A possible result from this code is

```python
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
```


### Config

It's possible to change the default settings which are

```python
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
```

It's done like so:

```python
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
```

![visualization example1](https://github.com/benmaier/netwulf/raw/master/img/BA_2.png)


### Attributes
Node attributes such as 'group' or 'size' that you define in your `networkx.Graph` are automatically visualized.

```Python
import networkx as nx
from netwulf import visualize

G = nx.random_partition_graph([10, 10, 10], .25, .01)
for k, v in G.nodes(data=True):
    v['group'] = v['block']; del v['block']

data = visualize(G)
```

![visualization example2](https://github.com/benmaier/netwulf/raw/master/img/attributes_1.png)

### Dev notes

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
