import { getRadius, getNodeColor, sleep } from './utils.js'
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
	let joint_data = {
		'network': network_data,
		'config': config_data,
		'image': img
	};
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

// Using the `rDown` variable to check if unload event is reload or not.
// It is a hack that will fail if the user actually clicks the reload button
// or for reasons that beta users will probably uncover. See this SO answer:
// https://stackoverflow.com/questions/568977/identifying-between-refresh-and-close-browser-actions/63272006#63272006
let rDown = false;
window.addEventListener("keydown", event => {
	if (event.key == 'r')
		rDown = true;
})
window.addEventListener("keyup", event => {
	if (event.key == 'r')
		rDown = false;
})

window.addEventListener("beforeunload", post_window_closed_stop);
function post_window_closed_stop() {
	console.log(rDown)
	if (!rDown) {
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
}

// Get a JSON object containing all the drawn properties for replication
function get_network_properties(network, scaling) {
	
	// unpack canvas scaling variables
	let {k, x, y} = scaling;

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
	network.links.forEach(d => {
		network_properties.links.push({
		source: d.source.id,
		target: d.target.id,
		width: (d.weight ** config['link_width_variation']) * config['link_width'] * k,
		weight: d.weight
		});
	});
	network.nodes.forEach(d => {
		network_properties.nodes.push({
			id: d.id,
			x: d.x,
			y: d.y,
			y_canvas: d.y * k + y,
			x_canvas: d.x * k + x,
			size: getRadius(d) * k,
			color: getNodeColor(d, network.groupColors)
		});
	});
	return network_properties;
}

function get_xlim_ylim(network) {
	let xlim = [Infinity, -Infinity],
		ylim = [Infinity, -Infinity];
	network.nodes.forEach(n => {
		let size = getRadius(n) + config.node_stroke_width;
		xlim[0] = n.x - size < xlim[0] ? n.x - size : xlim[0];  // left
		xlim[1] = n.x + size > xlim[1] ? n.x + size : xlim[1];  // right
		ylim[0] = n.y - size < ylim[0] ? n.y - size : ylim[0];  // bottom
		ylim[1] = n.y + size > ylim[1] ? n.y + size : ylim[1];  // top
	})
	return [xlim, ylim]
}

// Post data back to Python
export function postData(network) {
	alertActive = true;
	// POST data
	let timerInterval, stop;
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
		footer: '<input type="checkbox" id="fitImageCheckbox"><span style="position:relative;left:4px;bottom:3px">Crop to fit<kbd>[c]</kbd></span>',
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
		if (result.value || result.dismiss == Swal.DismissReason.timer) {
			let scaling;
			let checkbox = document.getElementById('fitImageCheckbox');
			if (checkbox.checked) {
				let [xlim, ylim] = get_xlim_ylim(network);
				scaling = {
					'k': 1,
					'x': -xlim[0],
					'y': -ylim[0]
				};
				network.width = xlim[1] - xlim[0];
				network.height = ylim[1] - ylim[0];
			} else {
				scaling = network.transform;
			}

			// Get network properties (returned val 0)
			let network_data = get_network_properties(network, scaling);

			// Get config (returned val 1)
			let config_data = {};
			for (let prop in config){
				config_data[prop] = config[prop];
			}
			config_data['zoom'] = scaling.k;
			config_data['xpan'] = scaling.x;
			config_data['ypan'] = scaling.y;

			// POST data
			post_json(network_data, config_data, network.canvas, post_stop);
		}
		alertActive = false;
	});
}

export function downloadImg(network) {
	let link = document.createElement('a');
	link.download = 'Untitled.png';
	link.href = network.canvas.toDataURL("image/png")
	link.click();
}