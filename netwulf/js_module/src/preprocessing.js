import { DefaultDict } from './utils.js'
import Swal from 'sweetalert2';
import chroma from 'chroma-js'

/**
 * Check that input data is valid.
 *
 * @param {Object}  graph  Data object exported from Python
 *
 * @yield {boolean}        Declaring if input is valid
 */
export function validateData(graph) {

    let errors = []
	let warnings = []

	// Nodes and links
    if (!graph.nodes)
    {
		errors.push("• &nbsp Missing key: 'nodes'")
    } else
    {	
    	if (graph.nodes.length == 0)
			errors.push("• &nbsp Found 0 nodes")

		for (let d of graph.nodes) {
	    	if (!('id' in d)) {
	    		errors.push("• &nbsp Found nodes without 'id' key");
	    		break;
    	}
    }
    }
    if (!graph.links)
    {
    	errors.push("Missing key: 'links'")
    } else
    {
    	if (graph.links.length == 0)
			warnings.push("• &nbsp Found 0 links")

		for (let d of graph.links) {
	    	if (!('source' in d && 'target' in d)) {
	    		errors.push("• &nbsp Found links without 'source' and/or 'target' key");
	    		break;
	    	}
	    }
    }

    if (graph.nodes && graph.links){

    	// Check that nodes references in links exist in list of nodes
	    let nodesSet = new Set(graph.nodes.map(d => { return d.id }));
	    nodesSet.delete(undefined);
	    
	    let linksSet = new Set()
	    graph.links.forEach(l => { linksSet.add(l.source); linksSet.add(l.target); });
	    linksSet.delete(undefined);

	    let intersection = [...nodesSet].filter(x => linksSet.has(x))
	    if (intersection.length < linksSet.size) {
	    	errors.push("• &nbsp Found nodes that don't exist, but are referenced in links")
	    }

	    // Sum occurances of each node and link attribute (AC = AttributeCounts)
	    let nodeAC = new DefaultDict(Number)
	    graph.nodes.forEach(d => {
	    	Object.keys(d).forEach(k => {
	    		nodeAC[k] += 1;
	    	})
	    })
	    let linkAC = new DefaultDict(Number)
	    graph.links.forEach(d => {
	    	Object.keys(d).forEach(k => {
	    		linkAC[k] += 1;
	    	})
	    })

	    // Check that node and link attributes are consistent
	    if (0 < nodeAC['group'] && nodeAC['group'] < graph.nodes.length) {
	    	errors.push("• &nbsp Found nodes with and nodes without 'group' attribute")
	    }
	    if (0 < nodeAC['size'] && nodeAC['size'] < graph.nodes.length) {
			errors.push("• &nbsp Found nodes with and nodes without 'size' attribute")
	    }
	    if (0 < nodeAC['color'] && nodeAC['color'] < graph.nodes.length) {
			errors.push("• &nbsp Found nodes with and nodes without 'color' attribute")
	    }
	    if (0 < linkAC['weight'] && linkAC['weight'] < graph.links.length) {
	      	errors.push("• &nbsp Found links with and links without 'weight' attribute")
	    }
	    if (0 < linkAC['color'] && linkAC['color'] < graph.links.length) {
	      	errors.push("• &nbsp Found links with and links without 'color' attribute")
	    }

	    // Check that nodes only has one of 'group' and 'color' attributes
	    if (nodeAC['group'] > 0 && nodeAC['color'] > 0) {
	    	warnings.push("• &nbsp Nodes have both 'group' and 'color' attributes. Ignoring 'group' attribute.")
	    }

	    // Check that 'group' attribute does not hold a color
	    if (nodeAC['group'] == graph.nodes.length) {
		    for (let d of graph.nodes) {
		    	if (chroma.valid(d.group)) {
		    		warnings.push(`
		    			• &nbsp Found nodes where 'group' attribute holds a valid color. User defined colors for
		    			this attribute are not reflected in the visualization, because the 'group' value is
		    			treated as a category. Instead, to control node colors give nodes a 'color' attribute
		    			`);
		    		break;
		    	}
		    }
	    }

	    // Check nodes and links for unrecognized attributes and clear if any exists
	    let recognizedNodeAttributes = ['id', 'size', 'color', 'group']
	    let unrecognizedNodeAttributes = Object.keys(nodeAC).filter(k => !recognizedNodeAttributes.includes(k))
	    if (unrecognizedNodeAttributes.length > 0) {
	    	warnings.push("• &nbsp Found unrecognized attribute(s) <em>" + unrecognizedNodeAttributes.join(", ") + "</em> on nodes.")
	    	graph.nodes.forEach(d => {
	    		unrecognizedNodeAttributes.forEach(k => { delete d[k] })
	    	});
	    }

	    let recognizedLinkAttributes = ['source', 'target', 'color', 'weight']
	    let unrecognizedLinkAttributes = Object.keys(linkAC).filter(k => !recognizedLinkAttributes.includes(k))
	    if (unrecognizedLinkAttributes.length > 0) {
	    	warnings.push("• &nbsp Found unrecognized attribute(s) <em>" + unrecognizedLinkAttributes.join(", ") + "</em> on links.")
	    	graph.links.forEach(d => {
	    		unrecognizedLinkAttributes.forEach(k => { delete d[k] })
	    	});
	    }
    }

    // Raise errors and warnings is any were caught
    if (errors.length > 0) {
    	Swal.fire({
    		'title': (errors.length > 1) ? 'Encountered ' + errors.length + ' errors in input data' : 'Encountered an error in input data',
    		'html': '<p align="left">' + errors.join('<br><br>') + '</p>',
    		'icon': 'error'
    	})
    	return false;
    }
    if (errors.length == 0 && warnings.length > 0) {
    	Swal.fire({
    		'title': (warnings.length > 1) ? 'Encountered ' + warnings.length + ' issues in input data' : 'Encountered an issue in input data',
    		'html': '<p align="left">' + warnings.join('<br><br>') + '</p>',
    		'icon': 'warning'
    	})
    }

    return true;
}


/**
 * Rescale link weights (normalize by max link weight)
 *
 * @param {Object}  graph  Data object exported from Python
 */
export function scaleLinks(graph) {
	// Get max weight
	let maxWeight = Math.max(...graph.links.map(d => d.weight));

	// Normalize link weights
	if (maxWeight > 0)
		graph.links.forEach(d => { d['weight'] = d.weight / maxWeight });
	else
		graph.links.forEach(d => { d['weight'] = 1 });
}


/**
 * Rescale node sizes (normalize by max size) and add normalized degree
 *
 * @param {Object}  graph  Data object exported from Python
 */
export function scaleNodes(graph) {
	// Estimate degree
	let nodeDegrees = new DefaultDict(Number)
	graph.links.forEach(d => {
		nodeDegrees[d.source] += d.weight;
		nodeDegrees[d.target] += d.weight;
    });

    // Get max size and degree, used for normalizing
    let maxSize = Math.max(...graph.nodes.map(d => d.size));
    let maxDegree = Math.max(...Object.values(nodeDegrees));

    // Rescale size and degree
	graph.nodes.forEach(d => {
		d['size'] = (maxSize > 0) ? d.size / maxSize : 1; 
		d['degree_normed'] = nodeDegrees[d.id] / maxDegree;
	})
}


/**
 * If nodes have a group attribute, color nodes accordingly.
 *
 * @param {Object}  graph  Data object exported from Python
 */
export function recolorNodes(graph) {
	let nodeGroups = new Set(graph.nodes.map(d => { return d.group }));
	nodeGroups.delete(undefined);
	let nodesHaveColor = 'color' in graph.nodes[0]

	if (nodeGroups.size > 0 && !nodesHaveColor) {
		// Cases where the user has created a 'group' attribute and nodes are
		// not colored. In case nodes are colored, 'group' is ignored
	    let groupColors = {};
	    for (let g of nodeGroups) {
	    	groupColors[g] = chroma.random().hex();
	    }

	    graph.nodes.forEach(d => {
	    	d['color'] = groupColors[d.group];
	    })
	}

}


/**
 * If nodes have 'x' and 'y' attributes, rescale them to fit canvas and
 * set `config['freeze_nodes']` to `true`.
 *
 * @param {Object}  graph   Data object exported from Python
 * @param {Object}  config  Network config exported from Python
 */
export function initialNodePositions(graph, config) {

	// Check if any node does not have 'x' and 'y'
    let nodesHavePosition = true;
    for (let d of graph.nodes) {
		if (!('x' in d) && !('y' in d)) {
			nodesHavePosition = false;
			break;
		}
    }

    // Rescale node positions to fit nicely inside of canvas depending on xlim or rescale properties.
    if (nodesHavePosition && (graph.rescale || !('xlim' in graph))) {
    	// Get visualization width and height
        let width = window.innerWidth;
    	let height = window.innerHeight;

    	// Get lists for x and y positions (to compute bounds)
        let xVals = [];
        let yVals = [];
        graph.nodes.forEach(d => { xVals.push(d.x); yVals.push(d.y) })

        // Scaling functions for repositioning
        let scaleX = d3.scaleLinear()
			.domain([d3.min(xVals), d3.max(xVals)])
			.range([width * 0.15, width * (1 - 0.15)])
        let scaleY = d3.scaleLinear()
			.domain([d3.min(yVals), d3.max(yVals)])
			.range([width * 0.15, width * (1 - 0.15)])

		// Rescale positions
        graph.nodes.forEach((d, i) => {
			d['x'] = scaleX(d.x)
			d['y'] = scaleY(d.y)
        })
    }
    
    // Update config
    if (nodesHavePosition)
    	config['freeze_nodes'] = true;
}