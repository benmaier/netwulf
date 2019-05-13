"""
Some useful things to tweak and reproduce the visualizations.
"""

import numpy as np
import networkx as nx

import matplotlib as mpl
import matplotlib.pyplot as pl
from matplotlib.collections import LineCollection, EllipseCollection

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

    x = { node['id']: node['x'] for node in network_properties['nodes'] }
    y = { node['id']: node['y'] for node in network_properties['nodes'] }
    nx.set_node_attributes(network, x, 'x')
    nx.set_node_attributes(network, y, 'y')

def get_filtered_network(network,edge_weight_key=None,node_group_key=None):
    """
    Get a copy of a network where the edge attribute ``'weight'`` is
    set to the attribute given by the keyword ``edge_weight_key`` and the
    nodes are regrouped according to their node attribute provided by
    ``node_group_key``. 

    Parameters
    ----------
    network : networkx.Graph or alike
        The network object which is about to be filtered
    edge_weight_key : str, default : None
        If provided, set the edge weight to the edge attribute
        given by ``edge_weight_key`` and delete all other edge attributes
    node_group_key : str, default : None
        If provided, set the node ``'group'`` attribute according to a
        new grouping provided by the node attribute ``node_group_key``.

    Returns
    -------
    G : networkx.Graph or alike
        A filtered copy of the original network.
    """

    G = network.copy()

    if edge_weight_key is not None:
        for u, v, d in G.edges(data=True):
            keep_value = d[edge_weight_key]
            d.clear()
            G[u][v]['weight'] = keep_value

    if node_group_key is not None:
        groups = { node[1][node_group_key] for node in network.nodes(data=True) }
        groups_enum = {v: k for k,v in enumerate(groups)}
        for u in network.nodes():
            grp = G.node[u].pop(node_group_key)
            keep_value = groups_enum[grp]
            G.node[u]['group'] = keep_value

    return G

def draw_netwulf(network_properties, fig=None, ax=None, figsize=None):
    """
    Redraw the visualization using matplotlib. Creates
    figure and axes if None provided.
    In order to add labels, do for instance

    .. code:: python

        ax.text(
                network_properties['nodes'][0]['x'],
                network_properties['nodes'][0]['y'],
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
    figsize : float, default : None
        the size of the figure in inches (sidelength of a square)
        if None, will be taken as the minimum of the values in 
        ``matplotlib.rcParams['figure.figsize']``.
    
    Returns
    -------
    fig : matplotlib.Figure, default : None
        Resulting figure
    ax : matplotlib.Axes, default : None
        Resulting axes
    """

    # if no figure given, create a square one
    if ax is None or fig is None:
        if figsize is None:
            size = min(mpl.rcParams['figure.figsize'])
        else:
            size = figsize

        fig = pl.figure(figsize=(size,size))
        ax = fig.add_axes([0, 0, 1, 1])
        # Customize the axis
        # remove top and right spines
        ax.spines['right'].set_color('none')
        ax.spines['left'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        # turn off ticks
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])


    # for conversion of inches to points
    # (important for markersize and linewidths)
    dpi = fig.dpi

    # set everything square and get the axis size in points
    ax.axis('square')
    ax.axis('off')
    ax.margins(0)
    ax.set_xlim(network_properties['xlim'])
    ax.set_ylim(network_properties['ylim'])
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    axwidth, axheight = bbox.width*dpi, bbox.height*dpi



    # filter out node positions for links
    width = network_properties['xlim'][1] - network_properties['xlim'][0]
    height = network_properties['ylim'][1] - network_properties['ylim'][0]
    pos = { node['id']: np.array([node['x'], height - node['y']]) for node in network_properties['nodes'] }

    lines = []
    linewidths = []
    for link in network_properties['links']:
        u, v = link['source'], link['target']
        lines.append([ 
            [pos[u][0], pos[v][0]], 
            [pos[u][1], pos[v][1]]
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
    XY = []
    size = []
    node_colors = []

    for node in network_properties['nodes']:
        XY.append([node['x'], height - node['y']])
        # size has to be given in points*2
        size.append( 2*node['radius'] )
        node_colors.append(node['color'])

    XY = np.array(XY)
    size = np.array(size)
    circles = EllipseCollection(size,size,np.zeros_like(size),
                                offsets=XY,
                                units='x',
                                transOffset=ax.transData,
                                facecolors=node_colors,
                                linewidths=network_properties['nodeStrokeWidth']/width*axwidth,
                                edgecolors=network_properties['nodeStrokeColor'],
                                )
    ax.add_collection(circles)

    return fig, ax



if __name__ == "__main__":
    import pprint 
    pp = pprint.PrettyPrinter(indent=4)

    G = nx.barabasi_albert_graph(10,1)

