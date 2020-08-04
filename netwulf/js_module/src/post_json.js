import { getRadius, getNodeColor } from './utils.js'
import Swal from 'sweetalert2';

// Send an HTTP request to the server with POSTed json-data
// This is adapted from https://stackoverflow.com/questions/24468459/sending-a-json-to-server-and-retrieving-a-json-in-return-without-jquery
function post_json(network_data, config_data, canvas, callback) {
	let xhr = new XMLHttpRequest();
	let url = window.location.href;
	let img = canvas.toDataURL("image/png");
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			let response = xhr.responseText;
			if (callback !== null)
				callback();
		}
	};
	let joint_data = {'network': network_data, 'config': config_data, 'image':img};
	let data_str = JSON.stringify(joint_data);
	xhr.send(data_str);
}

function post_stop() {
	let xhr = new XMLHttpRequest();
	let url = window.location.href;
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			let response = xhr.responseText;
			window.close();
		}
	};
	xhr.send();
}

window.addEventListener("beforeunload", post_window_closed_stop);
function post_window_closed_stop() {
	let xhr = new XMLHttpRequest();
	let url = window.location.href;
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			let response = xhr.responseText;
		}
	};
	xhr.send();
}

// Get a JSON object containing all the drawn properties for replication
function get_network_properties(network) {
	let k = network.transform.k;
	let x = network.transform.x;
	let y = network.transform.y;
	// save all those things we wish to draw to a dict;
	let network_properties = {};
	network_properties.xlim = [ 0, network.width ];
	network_properties.ylim = [ 0, network.height ];
	network_properties.linkColor = config['link_color'];
	network_properties.linkAlpha = config['link_alpha'];
	network_properties.nodeStrokeColor = config['node_stroke_color'];
	network_properties.nodeStrokeWidth = config['node_stroke_width'] * k;
	network_properties.links = [];
	network_properties.nodes = [];
	network.links.forEach(function(d){
		network_properties.links.push({
		source: d.source.id,
		target: d.target.id,
		width: (d.weight ** config['link_width_variation']) * config['link_width'] * k,
		weight: d.weight
		});
	});
	network.nodes.forEach(function(d){
		network_properties.nodes.push({
		id: d.id,
		x: d.x,
		y: d.y,
		x_canvas: d.x * k + x,
		y_canvas: d.y * k + y, 
		radius: getRadius(d) * k, 
		color: getNodeColor(d, network.groupColors)
		});
	});
	return network_properties;
}

// Post data back to Python
export function postData(network) {
	
	// Get network properties (returned val 0)
	let network_data = get_network_properties(network);

	// Get config (returned val 1)
	let config_data = {};
	for (let prop in config){
		config_data[prop] = config[prop];
	}
	config_data['zoom'] = network.transform.k;
	config_data['xpan'] = network.transform.x;
	config_data['ypan'] = network.transform.y;

	// POST data
	let timerInterval, cropImage = false;
	post_json(network_data, config_data, network.canvas, () => {
		Swal.fire({
			title: "Success!",
			html: "Posting to Python in <b></b> seconds.",
			timer: 3000,
			timerProgressBar: true,
			showCancelButton: true,
			confirmButtonColor: '#3085d6',
			confirmButtonText: 'OK <span style="position:relative;bottom:1px"><kbd>[enter]</kbd></span>',
			cancelButtonColor: '#d33',
			cancelButtonText: 'Cancel <span style="position:relative;bottom:1px"><kbd>[esc]</kbd></span>',
			footer: '<input type="checkbox" id="cropImageCheckbox"><span style="position:relative;left:4px;bottom:3px">Crop image <kbd>[c]</kbd></span>',
			stopKeydownPropagation: false,
			onBeforeOpen: () => {
				timerInterval = setInterval(() => {
					const content = Swal.getContent();
					if (content) {
						const b = content.querySelector('b');
						if (b)
							b.textContent = Math.ceil(Swal.getTimerLeft()/1000);
					}
				}, 100);
			},
			onClose: () => {
				clearInterval(timerInterval)
			}
		}).then(result => {
			let checkbox = document.getElementById('cropImageCheckbox');
			cropImage = checkbox.checked;
			if (result.value || result.dismiss == Swal.DismissReason.timer) {
				post_stop();
			}
		});
	});
}