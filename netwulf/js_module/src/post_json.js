import { getRadius, getNodeColor } from './utils.js'
import Swal from 'sweetalert2';

// Send an HTTP request to the server with POSTed json-data
// This is adapted from https://stackoverflow.com/questions/24468459/sending-a-json-to-server-and-retrieving-a-json-in-return-without-jquery
export function post_json(network_data, config_data, canvas, callback) {
	let xhr = new XMLHttpRequest();
	let url = window.location.href;
	let img = canvas.toDataURL("image/png");
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			let response = xhr.responseText;
			console.log(response);
			if (callback !== null)
				callback();
		}
	};
	let joint_data = { 'network':network_data, 'config':config_data, 'image':img};
	let data_str = JSON.stringify(joint_data);
	xhr.send(data_str);
}

export function post_stop() {
	let xhr = new XMLHttpRequest();
	let url = window.location.href;
	let this_close_function = window.close;
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			let response = xhr.responseText;
			console.log(response);
			this_close_function();
		}
	};
	xhr.send();
}

window.addEventListener("unload", post_window_closed_stop);
export function post_window_closed_stop() {
	let xhr = new XMLHttpRequest();
	let url = window.location.href;
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			let response = xhr.responseText;
			console.log(response);
		}
	};
	xhr.send();
}

// Get a JSON object containing all the drawn properties for replication
export function get_network_properties(network) {
	// save all those things we wish to draw to a dict;
	let network_properties = {};
	network_properties.xlim = [ 0, network.width ];
	network_properties.ylim = [ 0, network.height ];
	network_properties.linkColor = config['link_color'];
	network_properties.linkAlpha = config['link_alpha'];
	network_properties.nodeStrokeColor = config['node_stroke_color'];
	network_properties.nodeStrokeWidth = config['node_stroke_width'];
	network_properties.links = [];
	network_properties.nodes = [];
	network.links.forEach(function(d){
		network_properties.links.push({
		source: d.source.id,
		target: d.target.id,
		width: (d.weight ** config['link_width_variation']) * config['link_width'],
		weight: d.weight
		});
	});
	network.nodes.forEach(function(d){
		let dSize = getRadius(d);
		network_properties.nodes.push({
		id: d.id,
		x: d.x,
		y: d.y,
		x_canvas: d.x,
		y_canvas: d.y, 
		radius: dSize,
		color: getNodeColor(d, network.groupColors)
		});
	});
	console.log(network)
	return network_properties;
}

// Post data back to Python
export function postData(network) {
	let nw_prop = get_network_properties(network);
	let config_copy = {};
	for (let prop in config){
		config_copy[prop] = config[prop];
	}

	post_json(nw_prop, config_copy, network.canvas, function(){
		Swal.fire({
			//type: "success",
			title: "Success!",
			text: "Closes automatically after 3 seconds.",
			type: "success",
			timer: 3000,
			showCancelButton: true,
			confirmButtonColor: '#3085d6',
			cancelButtonColor: '#d33',
			confirmButtonText: 'OK',
		}).then((willDelete) => {
				if (!willDelete) {
				} else {
					post_stop();
				}
		});
	});
}