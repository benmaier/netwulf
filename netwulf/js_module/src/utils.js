import * as _ from 'lodash';

export function toArrowFuncString(func) {
	// Takes any function and formats it as a arrow function expression, like `() => { ... }`
	// It is necessary to use this function to reformat all function that function as listeners
	// in `on` method calls for d3 objects. Reason: d3 invokes the listener within the `this`
	// context of the simulation, and class methods are in the class context so cannot  be passed.
	return '() => {' + func.toString().split('\n').splice(1).join('\n');
}

export function valIfValid(v, alt) {
	// Use this instead of (v || alt) which won't work when v is 0
	if (typeof(v) == "number") return v;
	if (typeof(v) == "string") return v;
	return alt;
}

export class DefaultDict {
	constructor(defaultInit) {
		return new Proxy({}, {
			get: (target, name) => name in target ?
				target[name] :
				(target[name] = typeof defaultInit === 'function' ?
					new defaultInit().valueOf() :
					defaultInit)
		})
	}
}

export function getRadius(d) {
	let nodeSize = config['scale_node_size_by_strength'] ? d['degree_normed'] : d['size'];
	nodeSize = nodeSize ** config['node_size_variation'];
	return nodeSize * config['node_size'];
}

export function getNodeColor(d, groupColors) {
	if (_.default.isEmpty(groupColors)) {
		return config['node_fill_color'];
	} else {
		return groupColors[d.group]['active'];
	}
}

export function toHex(v) {
	let hv = v.toString(16)
	if (hv.length == 1)
		hv = "0" + hv;
	return hv;
}

export function hexToInt(hex) {
	return parseInt(hex, 16)
}

export function bounceModulus(v, lower, upper) {
	if (lower <= v & v <= upper)
		return v;
	if (v < lower)
		return bounceModulus(lower + (lower - v), lower, upper);
	if (v > upper)
		return bounceModulus(upper - (v - upper), lower, upper);
}

export function clip(val, lower, upper) {
	if (val < lower) {
		return lower
	} else if (val > upper) {
		return upper
	} else {
		return val
	}
}

export function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export function getPercentile(val, sortedArr) {
	let length = sortedArr.length
	return sortedArr.indexOf(val) / length * (length / (length-1))
}

export function removeConsecutiveDuplicates(a) {
	return a.filter((item, pos, arr) => pos === 0 || item !== arr[pos-1])
}

export function findNode(data, d_id) {
	for (let d of data.nodes) {
		if (d.id == d_id)
			return d;
	}
	return undefined;
}