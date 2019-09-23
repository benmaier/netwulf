"""
A data input/output module for netwulf.
"""

import simplejson as json
import networkx as nx

def _write(f,stylized_network,config,G):
    """Internal function to write the everything to a json-file."""

    if G is not None:
        js_G = nx.node_link_data(G)
    else:
        js_G = None

    json.dump({
                'stylized_network' : stylized_network,
                'config' : config,
                'Graph' : js_G
              },
              f,
              separators=(',', ':'),
              )

def _read(f):
    """Internal function to read everything from a json-file."""

    data = json.load(f)
            
    stylized_network = data['stylized_network']
    config = data['config']
    G = data['Graph']
    if G is not None:
        G = nx.node_link_graph(data['Graph'])

    return stylized_network, config, G

def save(f,stylized_network,config,G=None):
    """
    Parameters
    ----------
    f : file-like object or str
        The file to which to write.
    stylized_network : dict
        dictionary returned by :mod:`netwulf.interactive.visualize`
    config : dict
        dictionary returned by :mod:`netwulf.interactive.visualize`
    G : networkx.Graph or similar, default : None
        Graph object from which the whole thing was generated.

    Example
    -------
        >>> G = networkx.fast_gnp_random_graph(10,0.3)
        >>> style_nw, cf = netwulf.visualize(G)
        >>> netwulf.save("ER.json",style_nw,cf,G)
    """

    if hasattr(f, 'write'):
        _write(f,stylized_network,config,G)
    else:
        with open(f,'w') as _f:
            _write(_f,stylized_network,config,G)

def load(f):
    """
    Parameters
    ----------
    f : file-like object or str
        The file to which to write.

    Returns
    -------
    stylized_network : dict
        dictionary returned by :mod:`netwulf.interactive.visualize`
    config : dict
        dictionary returned by :mod:`netwulf.interactive.visualize`
    G : networkx.Graph or similar, default : None
        Graph object from which the whole thing was generated.

    Example
    -------
        >>> G = networkx.fast_gnp_random_graph(10,0.3)
        >>> style_nw, cf = netwulf.visualize(G)
        >>> netwulf.save("ER.json",style_nw,cf,G)
        >>> style_nw,cf,G = netwulf.load("ER.json")
    """

    if hasattr(f, 'read'):
        return _read(f)
    else:
        with open(f,'r') as _f:
            return _read(_f)

