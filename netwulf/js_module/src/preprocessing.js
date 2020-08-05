import { DefaultDict, removeConsecutiveDuplicates } from './utils.js'
import Swal from 'sweetalert2';
import chroma from 'chroma-js'

/**
 * Check that input data is valid.
 *
 * @param {Object}  data  Data object exported from Python
 *
 * @yield {boolean}		Declaring if input is valid
 */
export function validateData(data) {

	let errors = []
	let warnings = []

	// Nodes and links
	if (!data.nodes)
	{
		errors.push("• &nbsp Missing key: 'nodes'")
	} else
	{	
		if (data.nodes.length == 0)
			errors.push("• &nbsp Found 0 nodes")

		for (let d of data.nodes) {
			if (!('id' in d)) {
				errors.push("• &nbsp Found nodes without 'id' key");
				break;
		}
	}
	}
	if (!data.links)
	{
		errors.push("Missing key: 'links'")
	} else
	{
		if (data.links.length == 0)
			warnings.push("• &nbsp Found 0 links")

		for (let d of data.links) {
			if (!('source' in d && 'target' in d)) {
				errors.push("• &nbsp Found links without 'source' and/or 'target' key");
				break;
			}
		}
	}

	if (data.nodes && data.links){

		// Check that nodes references in links exist in list of nodes
		let nodesSet = new Set(data.nodes.map(d => { return d.id }));
		nodesSet.delete(undefined);
		
		let linksSet = new Set()
		data.links.forEach(l => { linksSet.add(l.source); linksSet.add(l.target); });
		linksSet.delete(undefined);

		let intersection = [...nodesSet].filter(x => linksSet.has(x))
		if (intersection.length < linksSet.size) {
			errors.push("• &nbsp Found nodes that don't exist, but are referenced in links")
		}

		// Sum occurances of each node and link attribute (AC = AttributeCounts)
		let nodeAC = new DefaultDict(Number)
		data.nodes.forEach(d => {
			Object.keys(d).forEach(k => {
				nodeAC[k] += 1;
			})
		})
		let linkAC = new DefaultDict(Number)
		data.links.forEach(d => {
			Object.keys(d).forEach(k => {
				linkAC[k] += 1;
			})
		})

		// Check that node and link attributes are consistent
		if (0 < nodeAC['group'] && nodeAC['group'] < data.nodes.length) {
			errors.push("• &nbsp Found nodes with and nodes without 'group' attribute")
		}
		if (0 < nodeAC['size'] && nodeAC['size'] < data.nodes.length) {
			errors.push("• &nbsp Found nodes with and nodes without 'size' attribute")
		}
		if (0 < nodeAC['color'] && nodeAC['color'] < data.nodes.length) {
			errors.push("• &nbsp Found nodes with and nodes without 'color' attribute")
		}
		if (0 < linkAC['weight'] && linkAC['weight'] < data.links.length) {
		  	errors.push("• &nbsp Found links with and links without 'weight' attribute")
		}
		if (0 < linkAC['color'] && linkAC['color'] < data.links.length) {
		  	errors.push("• &nbsp Found links with and links without 'color' attribute")
		}

		// Check that nodes only has one of 'group' and 'color' attributes
		if (nodeAC['group'] > 0 && nodeAC['color'] > 0) {
			warnings.push("• &nbsp Nodes have both 'group' and 'color' attributes. Ignoring 'group' attribute.")
		}

		// Check that 'group' attribute does not hold a color
		if (nodeAC['group'] == data.nodes.length) {
			for (let d of data.nodes) {
				if (chroma.valid(d.group.toString())) {
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
		let recognizedNodeAttributes = ['id', 'size', 'color', 'group', 'x', 'y', 'x_canvas', 'y_canvas']
		let unrecognizedNodeAttributes = Object.keys(nodeAC).filter(k => !recognizedNodeAttributes.includes(k))
		if (unrecognizedNodeAttributes.length > 0) {
			warnings.push("• &nbsp Found unrecognized attribute(s) <em>" + unrecognizedNodeAttributes.join(", ") + "</em> on nodes.")
			data.nodes.forEach(d => {
				unrecognizedNodeAttributes.forEach(k => { delete d[k] })
			});
		}

		let recognizedLinkAttributes = ['source', 'target', 'color', 'weight', 'width']
		let unrecognizedLinkAttributes = Object.keys(linkAC).filter(k => !recognizedLinkAttributes.includes(k))
		if (unrecognizedLinkAttributes.length > 0) {
			warnings.push("• &nbsp Found unrecognized attribute(s) <em>" + unrecognizedLinkAttributes.join(", ") + "</em> on links.")
			data.links.forEach(d => {
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
 * @param {Object}  data  Data object exported from Python
 */
export function scaleLinks(data) {
	// Get max weight
	let maxWeight = Math.max(...data.links.map(d => d.weight));

	// Normalize link weights
	if (maxWeight > 0)
		data.links.forEach(d => { d['weight'] = d.weight / maxWeight });
	else
		data.links.forEach(d => { d['weight'] = 1 });

	let linkWeightOrder = removeConsecutiveDuplicates(
		data.links.map(d => d.weight).sort((a, b) => a - b)
	);

	return linkWeightOrder;
}


/**
 * Rescale node sizes (normalize by max size) and add normalized degree
 *
 * @param {Object}  data  Data object exported from Python
 */
export function scaleNodes(data) {
	// Estimate degree
	let nodeDegrees = new DefaultDict(Number)
	data.links.forEach(d => {
		nodeDegrees[d.source] += d.weight;
		nodeDegrees[d.target] += d.weight;
	});

	// Get max size and degree, used for normalizing
	let maxSize = Math.max(...data.nodes.map(d => d.size));
	let maxDegree = Math.max(...Object.values(nodeDegrees));

	// Rescale size and degree
	data.nodes.forEach(d => {
		d['size'] = (maxSize > 0) ? d.size / maxSize : 1; 
		d['degree'] = nodeDegrees[d.id];
		d['degree_normed'] = nodeDegrees[d.id] / maxDegree;
	})
}


/**
 * If nodes have a group attribute, color nodes accordingly.
 *
 * @param {Object}  data  Data object exported from Python
 */
export function recolorNodes(data) {
	let nodeGroups = new Set(data.nodes.map(d => { return d.group }));
	let nodeColors = new Set(data.nodes.map(d => { return d.color }));
	nodeGroups.delete(undefined);
	nodeColors.delete(undefined);

	let groupColors = {};

	if (nodeGroups.size > 0 && nodeColors.size == 0) {
		// Cases where the user has created a 'group' attribute and nodes are
		// not colored
		for (let group of nodeGroups) {
			let color = chroma.random().hex();
			groupColors[group] = {'reference': color, 'active': color};
		}
	} else if (nodeColors.size > 0) {
		// If nodes are colored, 'group' is ignored
		for (let color of nodeColors) {
			groupColors[color] = {'reference': color, 'active': color};
		}

		data.nodes.forEach(d => {
			d['group'] = groupColors[d.color]['reference'];
			delete d['color'];
		})
	}

	return groupColors;
}


/**
 * If nodes have 'x' and 'y' attributes, rescale them to fit canvas and
 * set `config['freeze_nodes']` to `true`.
 *
 * @param {Object}  data   Data object exported from Python
 * @param {Object}  config  Network config exported from Python
 */
export function initialNodePositions(data, config) {

	// Check if any node does not have 'x' and 'y'
	let nodesHavePosition = true;
	for (let d of data.nodes) {
		if (!('x' in d) && !('y' in d)) {
			nodesHavePosition = false;
			break;
		}
	}

	// Rescale node positions to fit nicely inside of canvas depending on xlim or rescale properties.
	if (nodesHavePosition && (data.rescale || !('xlim' in data))) {
		// Get visualization width and height
		let width = window.innerWidth;
		let height = window.innerHeight;

		// Get lists for x and y positions (to compute bounds)
		let xVals = [];
		let yVals = [];
		data.nodes.forEach(d => { xVals.push(d.x); yVals.push(d.y) })

		// Scaling functions for repositioning
		let scaleX = d3.scaleLinear()
			.domain([d3.min(xVals), d3.max(xVals)])
			.range([width * 0.15, width * (1 - 0.15)])
		let scaleY = d3.scaleLinear()
			.domain([d3.min(yVals), d3.max(yVals)])
			.range([width * 0.15, width * (1 - 0.15)])

		// Rescale positions
		data.nodes.forEach((d, i) => {
			d['x'] = scaleX(d.x)
			d['y'] = scaleY(d.y)
		})
	}
	
	// Update config
	if (nodesHavePosition)
		config['freeze_nodes'] = true;
}