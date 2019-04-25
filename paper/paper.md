---
title: Netwulf: Interactive visualization of networks in Python # maybe you have a better title
tags:
  - Python
  - JavaScript
  - networks
  - visualization
  - interactive
authors:
  - name: Ulf Aslak
    orcid: 0000-0003-4704-3609
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Benjamin F. Maier
    orcid: 0000-0001-7414-8823
    affiliation: "3, 4"
affiliations:
 - name : Center for Social Data Science, University of Copenhagen, DK-1353 København K
   index: 1
 - name : DTU Compute, Technical University of Denmark, DK-2800 Kgs. Lyngby
   index: 2
 - name: Robert Koch-Institute, Nordufer 20, D-13353 Berlin
   index: 3
 - name: Department of Physics, Humboldt-University of Berlin, Newtonstr. 15, D-12489 Berlin
   index: 4
date: 20 April 2018
bibliography: paper.bib
---

# Summary

Network visualization is an effective way to illustrate properties of a complex system. It is an important tool for exploring and finding patterns, and is used by researchers and practitioners across many fields and industries.
Currently, there exist a number of tools for visualizing networks. *Networkx* [@networkx] is a popular Python package for network analysis which provides limited functionality for computing layouts and plotting networks statically. Layout computations are done in Python or using the php-based software *Graphviz* [@graphviz], which is slow. Another Python package for network analysis and visualization is *graph-tool* [@graphtool], which relies on a high number of external C++-libraries for installation/compilation which can be overwhelming for beginners. Furthermore, its visualization functions are non-interactive, as well. *Gephi* [@gephi] and *Cytoscape* [@cytoscape] are dedicated interactive visualization and analysis software programs. They are both Java-based and run desktop clients with a GUI where users save and load networks as separate files. *Webweb* [@webweb] enables interactive visualization for Python and Matlab networks using the d3.js [@d3] force layout. Its main purpose, however, is exploration of network features and exporting one-time visualizations as SVG or HTML.

For many users, these tools offer the necessary functionality to visualize networks in most desired ways. However, since a growing population of network researchers and practitioners are relying on Python for doing network science [@developersurvey], it is increasingly pressing that a fast and intuitive Python tool for reproducible network visualization exists.

*Netwulf* is a light-weight Python library that provides a simple API for interactively visualizing a network and returning the computed layout and style. It is build around the philosophy that network manipulation and preprocessing should be done programmatically, but that the efficient generation of a visually appealing network is best done interactively, without code. Therefore, it offers no analysis functionality and only few exploration features, but instead focuses almost entirely on fast and intuitive layout manipulation and node/link styling. Interaction with Netwulf typically works as follows:

1. Users have a network object, `G`, in either dictionary or *networkx.Graph* format. They then launch a Netwulf visualization by calling `netwulf.visualize(G)`.
2. The command opens a new browser window containing `G` as an interactive, manipulable, stylable network. Here, the user can, for instance, explore how different configurations of physics parameters like *node charge* and *gravity* influence the layout, they can change properties like node color and link opacity, and even threshold the network data for weak or strong links. When the user has finalized the layouting process, they may either:
   1. Save the image directly from the interactive visualization as a PNG file.
   2. Post the style and computed node positions back to Python in a dictionary format, which allows for further manipulation in the Python backend. Moreover, using the function `netwulf.draw_netwulf`, the network can be redrawn using the common Python drawing library *matplotlib* [@matplotlib], which further enables saving the visualization in any format.

The interactive visualization is implemented in JavaScript, relies on d3.js [@d3] for computing layouts, and uses the HTML5-object `canvas` for rendering. This makes it, to our knowledge, the most performant tool for interactive network visualization in Python to date.


# Figures

![Interactive visualization of a modular network in Netwulf.](random_partition_graph.png)

# Acknowledgements

Both authors contributed equally to the software, documentation, and manuscript. B. F. M. is financially supported as an *Add-On Fellow for Interdisciplinary Life Science* by the Joachim Herz Stiftung.

# References

