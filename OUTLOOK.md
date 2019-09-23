# Outlook

This is a place to collect ideas on how to further improve the network visualization process.

## Directed and curved edges

This is a crucial functionality for a lot of network scientists. We plan to [incorporate this functionality soon](ulfaslak/network_styling_with_d3#3), in fact we already [started working on it](benmaier/curved-edges).

## Tree styling

d3 provides a great [API for tree styling](https://github.com/d3/d3-hierarchy/blob/master/README.md). We should build an addition tree styling function.

## Hierarchically clustered networks

Networks are often inferred to be hierarchically clustered. Different visualizations could be used to visually cluster these networks in a way that does not rely on a force-layout, e.g. with something like a [Pack](https://github.com/d3/d3-hierarchy/blob/master/README.md#pack), see [also here](https://observablehq.com/@d3/zoomable-circle-packing) or with [hierarchical edge bundling](https://observablehq.com/@d3/hierarchical-edge-bundling).
