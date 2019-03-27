"""
Some useful things to tweak and reproduce the visualizations.
"""

import numpy as np
import networkx as nx

import matplotlib as mpl
import matplotlib.pyplot as pl
from matplotlib.collections import LineCollection

def bind_positions_to_network(network, network_properties):
    """
    Binds calculated positional values to the network as node attributes `x` and `y`.

    Parameters
    ----------
    network : networkx.Graph or something alike
        The network object to which the position should be bound
    network_properties : dict
        The network properties which are returned from the
        interactive visualization.
    """

    x =  { node['id']: node['pos'][0] for node in network_properties['nodes'] }
    y =  { node['id']: node['pos'][1] for node in network_properties['nodes'] }
    nx.set_node_attributes(network, x, 'x')
    nx.set_node_attributes(network, y, 'y')

def draw_netwulf(network_properties, fig = None, ax=None):
    """
    Redraw the visualization using matplotlib. Creates
    figure and axes if None provided.
    In order to add labels, do for instance

    .. code:: python
        ax.text(
                network_properties['nodes'][0]['pos'][0],
                network_properties['nodes'][0]['pos'][1],
                network_properties['nodes'][0]['id']
               )

    Parameters
    ----------
    network_properties : dict
        The network properties which are returned from the
        interactive visualization.
    fig : matplotlib.Figure, default : None
        The figure in which to draw
    ax : matplotlib.Axes, default : None
        The Axes in which to draw
    
    Returns
    -------
    fig : matplotlib.Figure, default : None
        Resulting figure
    ax : matplotlib.Axes, default : None
        Resulting axes
    """

    # if no figure given, create a square one
    if ax is None or fig is None:
        size = min(mpl.rcParams['figure.figsize'])
        fig, ax = pl.subplots(1,1,figsize=(size,size))


    # for conversion of inches to points
    # (important for markersize and linewidths)
    points_in_inches = 72

    # set everything square and get the axis size in points
    ax.axis('square')
    ax.axis('off')
    ax.margins(0)
    ax.set_xlim(network_properties['xlim'])
    ax.set_ylim(network_properties['ylim'])
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    axwidth, axheight = bbox.width*points_in_inches, bbox.height*points_in_inches



    # filter out node positions for links
    width = network_properties['xlim'][1] - network_properties['xlim'][0]
    pos = { node['id']: np.array(node['pos']) for node in network_properties['nodes'] }

    lines = []
    linewidths = []
    for link in network_properties['links']:
        u, v = link['link']
        lines.append([ 
                        [pos[u][0],pos[v][0]], 
                        [pos[u][1],pos[v][1]]
                     ])
        linewidths.append(link['width']/width*axwidth)

    # collapse to line segments
    lines = [list(zip(x, y)) for x, y in lines]

    # plot Lines
    alpha = network_properties['linkAlpha']
    color = network_properties['linkColor']
    ax.add_collection(LineCollection(lines, 
                                     color=color,
                                     alpha=alpha, 
                                     linewidths=linewidths,
                                     zorder=-1
                                     ))

    # compute node positions and properties
    X, Y = [], []
    size = []
    node_colors = []

    for node in network_properties['nodes']:
        X.append( node['pos'][0] )
        Y.append( node['pos'][1] )
        # size has to be given in points**2
        size.append( (node['radius'] / width*axwidth)**2 )
        node_colors.append(node['color'])



    # plot nodes
    ax.scatter(X,Y,
               s=size,
               c=node_colors,
               linewidth=network_properties['nodeStrokeWidth']/width*axwidth,
               edgecolor=network_properties['nodeStrokeColor']
               )

    return fig, ax



if __name__ == "__main__":
    import pprint 
    pp = pprint.PrettyPrinter(indent=4)

    G = nx.barabasi_albert_graph(10,1)

