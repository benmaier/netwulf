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
    orcid: 0000-0000-0000-0000
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Benjamin F. Maier
    orcid: 0000-0001-7414-8823
    affiliation: "3, 4"
affiliations:
 - name : Centre for Social Data Science, University of Copenhagen, DK-1353 København K
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

I'm just collecting some thoughts here

* visualizing networks is an important part of communicating their structure
* there already exist several tools to explore/visualize networks and their structure and properties.
* "networkx" [@networkx] is the most commonly used Python package for network analysis
* it provides visualization functions which are either slow or inconvenient as they
  rely on third-party dependencies like "graphviz" [@graphviz], and use a
  a variety of parameters. These parameters then have to be manually scanned, 
  reproducing a new visualization for every changed parameter.
* Gephi [@gephi] is mostly focused on both interactive analysis and visualization.
  However, networks must be saved and loaded as separate files. Java has to be installed.
  an automated view of a network which was previously manipulated in Python is not possbile
* Webweb [@webweb] provides an interactive visualization for Python network objects based
  on the force layout of d3.js [@d3], however
  its main purpose is exploration of network features
  and single-time visualizations:
  the stylized network and visualization parameters may not be saved to reproduce
  Further, a variety of styling parameters are only accessible through its API
  which again may provide difficulties when trying to find the optimal visualization.
* Netwulf provides a simple interactive interface to stylize a network which was previously
  manipulated in Python. 
* Its philosophy is that network manipulation should be done programmatically (i.e. in Python)
  but the efficient generation of a visually pleasing network representation should be
  done manually
* Its main purpose is to easily generate both a network visualization
  and find the optimal visualization parameters to reproduce the visualization. To this end, both are 
  saved to objects in the Python instance running Netwulf.
* It further provides functionality to
  redraw the visualization in Python using matplotlib [@matplotlib] to save it as a vector graphic
  or image in arbitrary resolution.
* more description


# Figures

![Interactive visualization of a modular network in Netwulf.](random_partition_graph.png)

# Acknowledgements

Both authors contributed equally to the software, documentation, and manuscript. B. F. M. is financially supported as an *Add-On Fellow for Interdisciplinary Life Science* by the Joachim Herz Stiftung.

# References
