"""
Some useful things to tweak and reproduce the visualizations.
"""

import numpy as np
import networkx as nx

import matplotlib as mpl
import matplotlib.pyplot as pl
from matplotlib.collections import LineCollection, EllipseCollection

def node_pos(network_properties,node_id):
    """
    Get the node's position in matplotlib data coordinates.
    
    Parameters
    ----------
    network_properties : dict
        The network properties which are returned from the
        interactive visualization.

    Returns
    -------
    x : float
        The x-position in matplotlib data coordinates
    y : float
        The y-position in matplotlib data coordinates

    Example
    -------
        >>> props, _ = visualize(G)
        >>> node_pos(props, 0)
    """

    height = network_properties['ylim'][1] - network_properties['ylim'][0]
    node = network_properties['nodes'][node_id]

    return node['x_canvas'], height - node['y_canvas']

def add_node_label(ax,
                   network_properties,
                   node_id,
                   label=None,
                   dx=0,
                   dy=0,
                   ha='center',
                   va='center',
                   **kwargs):
    """
    Add a label to a node in the drawn matplotlib axis

    Parameters
    ----------
    ax : matplotlib.Axis
        The Axis object which has been used to draw the network
    network_properties : dict
        The network properties which are returned from the
        interactive visualization.
    node_id : str or int
        The focal node's id in the `network_properties` dict
    label : str, default : None
        The text to write at the node's position
        If `None`, the value of `node_id` will be put there.
    dx : float, default : 0.0
        Label offset in x-direction
    dy : float, default : 0.0
        Label offset in y-direction
    ha : str, default : 'center'
        Horizontal anchor orientation of the text
    va : str, default : 'center'
        Vertical anchor orientation of the text
    **kwargs : dict
        Additional styling arguments forwarded to Axis.text


    Example
    -------
        >>> netw, _ = netwulf.visualize(G)
        >>> fig, ax = netwulf.draw_netwulf(netw)
        >>> netwulf.add_node_label(ax,netw,0)
    """

    pos = node_pos(network_properties, node_id)

    if label is None:
        label = str(node_id)
    
    ax.text(pos[0]+dx,pos[1]+dy,label,ha=ha,va=va,**kwargs)

def add_edge_label(ax,
                   network_properties,
                   edge,
                   label=None,
                   dscale=0.5,
                   dx=0,
                   dy=0,
                   ha='center',
                   va='center',
                   **kwargs):
    """
    Add a label to an edge in the drawn matplotlib axis

    Parameters
    ----------
    ax : matplotlib.Axis
        The Axis object which has been used to draw the network
    edge : 2-tuple of str or int
        The edge's node ids
    network_properties : dict
        The network properties which are returned from the
        interactive visualization.
    label : str, default : None
        The text to write at the node's position
        If `None`, the tuple of node ids in `edge` will be put there.
    dscale : float, default : 0.5
        At which position between the two nodes to put the label
        (``dscale = 0.0`` refers to the position of node ``edge[0]``
        and ``dscale = 1.0`` refers to the position of node ``edge[1]``,
        so use any number between 0.0 and 1.0).
    dx : float, default : 0.0
        Additional label offset in x-direction
    dy : float, default : 0.0
        Additional label offset in y-direction
    ha : str, default : 'center'
        Horizontal anchor orientation of the text
    va : str, default : 'center'
        Vertical anchor orientation of the text
    **kwargs : dict
        Additional styling arguments forwarded to Axis.text


    Example
    -------
        >>> netw, _ = netwulf.visualize(G)
        >>> fig, ax = netwulf.draw_netwulf(netw)
        >>> netwulf.add_node_label(ax,netw,0)
    """

    v0 = np.array(node_pos(network_properties, edge[0]))
    v1 = np.array(node_pos(network_properties, edge[1]))
    e = (v1-v0)

    if label is None:
        label = str("("+str(edge[0])+", "+str(edge[1])+")")
    
    pos = v0 + dscale * e 
    ax.text(pos[0]+dx,pos[1]+dy,label,ha=ha,va=va,**kwargs)

def bind_properties_to_network(network,
                               network_properties,
                               bind_node_positions=True,
                               bind_node_color=True,
                               bind_node_radius=True,
                               bind_node_stroke_color=True,
                               bind_node_stroke_width=True,
                               bind_link_width=True,
                               bind_link_color=True,
                               bind_link_alpha=True):
    """
    Binds calculated positional values to the network as node attributes `x` and `y`.

    Parameters
    ----------
    network : networkx.Graph or something alike
        The network object to which the position should be bound
    network_properties : dict
        The network properties which are returned from the
        interactive visualization.
    bind_node_positions : bool (default: True)
    bind_node_color : bool (default: True)
    bind_node_radius : bool (default: True)
    bind_node_stroke_color : bool (default: True)
    bind_node_stroke_width : bool (default: True)
    bind_link_width : bool (default: True)
    bind_link_color : bool (default: True)
    bind_link_alpha : bool (default: True)

    Example
    -------
        >>> props, _ = netwulf.visualize(G)
        >>> netwulf.bind_properties_to_network(G, props)
    """
    # Add individial node attributes
    if bind_node_positions:
        x = { node['id']: node['x'] for node in network_properties['nodes'] }
        y = { node['id']: node['y'] for node in network_properties['nodes'] }
        nx.set_node_attributes(network, x, 'x')
        nx.set_node_attributes(network, y, 'y')
        network.graph['rescale'] = False
    if bind_node_color:
        color = { node['id']: node['color'] for node in network_properties['nodes'] }
        nx.set_node_attributes(network, color, 'color')
    if bind_node_radius:
        radius = { node['id']: node['radius'] for node in network_properties['nodes'] }
        nx.set_node_attributes(network, radius, 'radius')

    # Add individual link attributes
    if bind_link_width:
        width = { (link['source'], link['target']): link['width'] for link in network_properties['links'] }
        nx.set_edge_attributes(network, width, 'width')

    # Add global style properties
    if bind_node_stroke_color:
        network.graph['nodeStrokeColor'] = network_properties['nodeStrokeColor']
    if bind_node_stroke_width:
        network.graph['nodeStrokeWidth'] = network_properties['nodeStrokeWidth']
    if bind_link_color:
        network.graph['linkColor'] = network_properties['linkColor']
    if bind_link_alpha:
        network.graph['linkAlpha'] = network_properties['linkAlpha']

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
    In order to add labels, check out 
    :mod:`netwulf.tools.add_node_label`
    and
    :mod:`netwulf.tools.add_edge_label`

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
    # (important for markersize and linewidths).
    # Apparently matplotlib uses 72 dpi internally for conversions in all figures even for those
    # which do not follow dpi = 72 which is freaking weird but hey why not.
    dpi = 72

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
    pos = { node['id']: np.array([node['x_canvas'], height - node['y_canvas']]) for node in network_properties['nodes'] }

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
        XY.append([node['x_canvas'], height - node['y_canvas']])
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


