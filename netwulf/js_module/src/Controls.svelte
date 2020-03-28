<script>

	import { onMount } from 'svelte';
	import { getRadius, toHex, hexToInt, bounceModulus, getPercentile, findNode } from './utils.js';
	import * as dat from 'dat.gui';
	import * as _ from 'lodash';

	// Component data
	export let network;
	export let groupColors;
	export let linkWeightOrder;

	// Div that dat.gui controls elements binds to
	let configDiv;

	// Default config for reference and restoration
	const configInit = _.default.cloneDeep(config)

	// Hack to enable titles (https://stackoverflow.com/a/29563786/3986879)
	function eachController(fnc) {
		for (let controllerName in dat.controllers) {
			if (dat.controllers.hasOwnProperty(controllerName)) {
				fnc(dat.controllers[controllerName]);
			}
		}
	}

	function setTitle(v) {
		// __li is the root dom element of each controller
		if (v) {
			this.__li.setAttribute('title', v);
		} else {
			this.__li.removeAttribute('title')
		}
		return this;
	};

	eachController(function(controller) {
		if (!controller.prototype.hasOwnProperty('title')) {
			controller.prototype.title = setTitle;
		}
	});

	// Control titles to appear on hover
	let title1_1 = "Charge: Each node has negative charge and thus repel one another (like electrons). The more negative this charge is, the greater the repulsion"
	let title1_2 = "Gravity: Push the nodes more or less towards the center of the canvas"
	let title1_3 = "Link distance: The optimal link distance that the force layout algorithm will try to achieve for each link"
	let title1_4 = "Collision: Make it harder for nodes to overlap"
	let title1_5 = "Wiggle: Increase the force layout algorithm temperature to make the nodes wiggle. Useful for big networks that need some time for the nodes to settle in the right positions"
	let title1_6 = "Freeze: Set force layout algorithm temperature to zero, causing the nodes to freeze in their position."
	let title2_1 = 'Fill: Node color(s). If nodes have "group" attributes (unless groups are named after colors) each group is given a random color. Changing "Fill color" will continuously change the color of all groups'
	let title2_2 = "Stroke: The color of the ring around nodes"
	let title2_3 = "Label color: The color of node labels"
	let title2_4 = "Display labels: Whether to show labels or not"
	let title2_5 = "Size by strength: Rescale the size of each node relative to their strength (weighted degree)"
	let title2_6 = "Size: Change the size of all nodes"
	let title2_7 = "Stroke width: Change the width of the ring around nodes"
	let title2_8 = "Size variation: Tweak the node size scaling function. Increase to make big nodes bigger and small nodes smaller. Useful for highlighting densely connected nodes."
	let title3_1 = "Color: The color of links"
	let title3_2 = "Width: Change the width of all links"
	let title3_3 = "Alpha: How transparent links should be. Useful in large dense networks"
	let title3_4 = "Width variation: Tweak the link width scaling function. Increase to make wide links wider and narrow links narrower. Useful for highlighting strong connections"
	let title4_1 = "Singleton nodes: Whether or not to show nodes with zero degree"
	let title4_2 = "Min. link percentile: Lower percentile threshold on link weight"

	// Create controls on mount
	onMount(() => {

		let gui = new dat.GUI({ autoPlace: false });
		configDiv.appendChild(gui.domElement);
		gui.closed = false;

		let f1 = gui.addFolder('Physics'); f1.open();
		f1.add(config, 'node_charge', -100, 0).name('Charge').onChange(function(v) { chargeChanged(v) }).title(title1_1);
		f1.add(config, 'node_gravity', 0, 1).name('Gravity').onChange(function(v) { gravityChanged(v) }).title(title1_2);
		f1.add(config, 'link_distance', 0.1, 50).name('Link distance').onChange(function(v) { distanceChanged(v) }).title(title1_3);
		f1.add(config, 'node_collision', false).name('Collision').onChange(function(v) { collisionChanged(v) }).title(title1_4);
		f1.add(config, 'wiggle_nodes', false).name('Wiggle').onChange(function(v) { wiggleChanged(v) }).listen().title(title1_5);
		f1.add(config, 'freeze_nodes', false).name('Freeze').onChange(function(v) { freezeChanged(v) }).listen().title(title1_6);

		let f2 = gui.addFolder('Nodes'); f2.open();
		f2.addColor(config, 'node_fill_color', config['node_fill_color']).name('Fill').onChange(function(v) { nodeFillChanged(v) }).title(title2_1);
		f2.addColor(config, 'node_stroke_color', config['node_stroke_color']).name('Stroke').onChange(function(v) { stylingChanged(v) }).title(title2_2);
		f2.addColor(config, 'node_label_color', config['node_label_color']).name('Label color').onChange(function(v) { stylingChanged(v) }).title(title2_3);
		f2.add(config, 'node_size', 0, 50).name('Size').onChange(function(v) { nodeSizeChanged(v) }).title(title2_6);
		f2.add(config, 'node_stroke_width', 0, 10).name('Stroke width').onChange(function(v) { stylingChanged(v) }).title(title2_7);
		f2.add(config, 'node_size_variation', 0., 3.).name('Size variation').onChange(function(v) { nodeSizeChanged(v) }).title(title2_8);
		f2.add(config, 'display_node_labels', false).name('Display labels').onChange(function(v) { stylingChanged(v) }).title(title2_4);
		f2.add(config, 'scale_node_size_by_strength', false).name('Size by strength').onChange(function(v) { nodeSizeChanged(v) }).title(title2_5);

		let f3 = gui.addFolder('Links'); f3.open();
		f3.addColor(config, 'link_color', config['link_color']).name('Color').onChange(function(v) { stylingChanged(v) }).title(title3_1);
		f3.add(config, 'link_width', 0.01, 30).name('Width').onChange(function(v) { stylingChanged(v) }).title(title3_2);
		f3.add(config, 'link_alpha', 0, 1).name('Alpha').onChange(function(v) { stylingChanged(v) }).title(title3_3);
		f3.add(config, 'link_width_variation', 0., 3.).name('Width variation').onChange(function(v) { stylingChanged(v) }).title(title3_4);

		let f4 = gui.addFolder('Thresholding'); f4.open();
		f4.add(config, 'display_singleton_nodes', true).name('Singleton nodes').onChange(function(v) { singletonNodesChanged(v) }).title(title4_1);
		f4.add(config, 'min_link_weight_percentile', 0, 1.0).name('Min. link percentile').step(0.01).onChange(function(v) { minLinkChanged(v) }).listen().title(title4_2);

	})

	
	// Event handlers //
	// -------------- //

	// Physics
	function chargeChanged(v) {
		network.simulation.force("charge").strength(+v);
		network.simulation.alpha(1).restart();
		if (config['freeze_nodes'])
			config['freeze_nodes'] = false;
	}

	function gravityChanged(v) {
		network.simulation.force("x").strength(+v);
		network.simulation.force("y").strength(+v);
		network.simulation.alpha(1).restart();
		if (config['freeze_nodes'])
			config['freeze_nodes'] = false;
	}

	function distanceChanged(v) {
		network.simulation.force("link").distance(v);
		network.simulation.alpha(1).restart();
		if (config['freeze_nodes'])
			config['freeze_nodes'] = false;
	}

	function collisionChanged(v) {
		network.simulation.force("collide").radius(function(d) {
			return config['node_collision'] * getRadius(d, config)
		});
		if (!config['freeze_nodes'])
			network.simulation.alpha(1)
		simulationSoftRestart();
	}

	function wiggleChanged(v) {
		network.simulation.alpha(0.5);
		network.simulation.alphaTarget(v).restart();
		if (v) config['freeze_nodes'] = !v;
	}

	let lastAlpha = 1;
	function freezeChanged(v) {
		if (v) {
			lastAlpha = network.simulation.alpha();
			config['wiggle_nodes'] = false;
			network.simulation.alphaTarget(0).alpha(0);
		} else {
			let alpha = Math.max(0.05, lastAlpha)
			network.simulation.alpha(alpha).alphaTarget(0).restart();
		}
	}

	// Styling
	function nodeFillChanged(v) {
		let dr = hexToInt(v.slice(1, 3)) - hexToInt(configInit['node_fill_color'].slice(1, 3))
		let dg = hexToInt(v.slice(3, 5)) - hexToInt(configInit['node_fill_color'].slice(3, 5))
		let db = hexToInt(v.slice(5, 7)) - hexToInt(configInit['node_fill_color'].slice(5, 7))

		for (let g of Object.keys(groupColors)) {
			let r_ = bounceModulus(parseInt(groupColors[g]['reference'].slice(1, 3), 16) + dr, 0, 255);
			let g_ = bounceModulus(parseInt(groupColors[g]['reference'].slice(3, 5), 16) + dg, 0, 255);
			let b_ = bounceModulus(parseInt(groupColors[g]['reference'].slice(5, 7), 16) + db, 0, 255);
			groupColors[g]['active'] = '#' + toHex(r_) + toHex(g_) + toHex(b_);
		}
		simulationSoftRestart();
	}

	function stylingChanged(v) {
		simulationSoftRestart();	
	}

	function nodeSizeChanged(v) {
		if (config['node_collision']) {
			network.simulation.force("collide").radius(function(d) { return getRadius(d, config) })
			if (!config['freeze_nodes'])
				network.simulation.alpha(1);
		}
		simulationSoftRestart();
	} 

	// Adding/removing nodes
	let negativeNetwork = {'nodes': [], 'links': []};
	function singletonNodesChanged(v) {
		if (v) {
			network['nodes'].push(...negativeNetwork.nodes);
			negativeNetwork['nodes'] = [];
		} else {
			network.nodes = network.nodes.filter(d => {
				let keepNode = d.degree > 1e-10;
				if (!keepNode)
					negativeNetwork['nodes'].push(d);
				return keepNode;
			})
		}
		network.reset();
		network.simulation.alpha(1).restart();
	}

	let vPrev = 0;
	let dv = 0;
	function minLinkChanged(v) {
		
		// Compute change (to figure out if slider is moving left or right)
		dv = v - vPrev;
		vPrev = v;
		
		// SLIDER MOVES RIGHT
		if (dv > 0) {

			// Remove links and decrement node 'degree' values
			network.links = network.links.filter(d => {
				let keepLink = v < getPercentile(d.weight, linkWeightOrder);
				if (!keepLink) {
					let d_source = findNode(data, d.source.id)
					let d_target = findNode(data, d.target.id)
					d_source['degree'] -= d.weight;
					d_target['degree'] -= d.weight;
					negativeNetwork['links'].push(d);
				}
				return keepLink;
			})

			// Remove singleton nodes
			if (!config['display_singleton_nodes']) {
				network.nodes = network.nodes.filter(d => {
					let keepNode = d.degree > 1e-10;
					if (!keepNode)
						negativeNetwork.nodes.push(d);
					return keepNode;
				})
			}
		}

		// SLIDER MOVES LEFT
		if (dv < 0) {

			// Add back links and increment node 'degree' values
			negativeNetwork.links = negativeNetwork.links.filter(d => {
				let addBackLink = v <= getPercentile(d.weight, linkWeightOrder)
				if (addBackLink) {
					let d_source = findNode(data, d.source.id)
					let d_target = findNode(data, d.target.id)
					d_source['degree'] += d.weight;
					d_target['degree'] += d.weight;
					network.links.push(d)
				}
				return !addBackLink
			})

			// Add back nodes
			if (!config['display_singleton_nodes']) {
				negativeNetwork['nodes'] = negativeNetwork.nodes.filter(d => {
					let addBackNode = d.degree >= 1e-10;
					if (addBackNode) {
						network.nodes.push(d)
					}
					return !addBackNode;
				})
			}
		}

		network.reset();
		network.simulation.alpha(1).restart();
	}

	// Handle restart (respecting frozen state)
	function simulationSoftRestart() {
		if (!config['freeze_nodes']){
			network.simulation.restart();
		} else {
			network.simulationUpdate();
		}
	}
</script>

<style>
	.topleftcorner{
		position: absolute;
		top: 70px;
		left: 15px;
	}
</style>

<div class="topleftcorner" bind:this={configDiv}>
</div>







