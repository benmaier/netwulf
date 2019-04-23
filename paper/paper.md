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

Network visualization is an effective way to illustrate properties of a complex system. It is an important tool for exploring and spotting patterns, and is used by researchers and practitioners across many fields and industries.
Currently, there exists a number of tools for visualizing networks. *networkx* [@networkx] is a popular Python package for network analysis which provides limited functionality for computing layouts and plotting networks statically. Layout computations are done in Python or using the php-based software *Graphviz* [@graphviz], which is slow. *Gephi* [@gephi] and *Cytoscape* [@cytoscape] are dedicated visualization and analysis software programs. They are both Java-based and runs desktop clients with a GUI, where users save and load networks as seperate files. *Webweb* [@webweb] enables interactive visualization for Python and Matlab networks using the d3.js [@d3] force layout. It's main purpose is exploration of network features and exporting one-time visualizations as SVG or HTML.

For many users, these tools, although occasionally inconvenient and cumbersome to use, offer the necessary functionality to visualize networks in most desired ways. However, since a growing population of network researchers and practitioners are becoming Python users [@developersurvey], it is increasingly pressing that a fast and intuitive tool for network visualization exists.

*Netwulf* is a light-weight Python library that provides an ultra simple API for interactively visualizing a network and returning the computed layout and style. It is build around the philosophy that network manipulation and preprocessing should be done programmatically, but that the efficient generation of a visually appealing network is best done interactively, without code. It allows users to:

1. create a network, `G`, in either dictionary or *networkx.Graph* format, then calling `netwulf.visualize(G)`, to
2. display it in a browser window as an interactive, manipulable, stylable network and 
   1. post the final style and computed node-positions back to Python in dictionary format, allowing further manipulation, or redrawing with matplotlib [@matplotlib], or
   2. saving the image directly to the desktop as a PNG file.

The visualization component is implemented in JavaScript, relies on d3.js [@d3] for computing layouts, and uses canvas for rendering, which makes it the fastest tool for networks visualization in Python. 


# Figures

![Interactive visualization of a modular network in Netwulf.](random_partition_graph.png)

# Acknowledgements

Both authors contributed equally to the software, documentation, and manuscript. B. F. M. is financially supported as an *Add-On Fellow for Interdisciplinary Life Science* by the Joachim Herz Stiftung.

# References

