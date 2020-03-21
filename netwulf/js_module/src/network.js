// Exports
// -------
export default Network;

// Imports
// -------
import { scaleLinear, scaleOrdinal } from 'd3-scale';
import { zoom, zoomIdentity } from 'd3-zoom';
import { schemeCategory10 } from 'd3-scale-chromatic';
import { select, selectAll, mouse } from 'd3-selection';
import { drag } from 'd3-drag';
import { forceSimulation, forceLink, forceManyBody, forceCenter, forceX, forceY} from 'd3-force';
import { event as currentEvent } from 'd3-selection';
let d3 = {
    zoom, zoomIdentity, scaleLinear, scaleOrdinal, schemeCategory10, select,
    selectAll, mouse, drag,  forceSimulation, forceLink, forceManyBody, forceCenter,
    forceX, forceY
};

import { toArrowFuncString } from './utils.js'


// Network class
// -------------

let Network = class Network {

    constructor(canvas, width, height, nodes, links) {
        // Class variables
        this.canvas = canvas;
        this.context = canvas.getContext('2d');
        this.width = width;
        this.height = height;
        this.nodes = nodes;
        this.links = links;

        // Scale context if retina display
        this.addRetinaRendering();

        // Transformations (dragging, panning, zooming)
        this.addTransformations();

        // Node titles
        this.addNodeTitles();

    }

    addRetinaRendering() {
        this.devicePixelRatio = window.devicePixelRatio || 1;
        d3.select(this.canvas)
            .attr("width", this.width * this.devicePixelRatio)
            .attr("height", this.height * this.devicePixelRatio)
            .style("width", this.width + "px")
            .style("height", this.height + "px").node()
        this.context.scale(this.devicePixelRatio, this.devicePixelRatio)
    }

    addTransformations() {
        this.transform = d3.zoomIdentity;
        d3.select(this.canvas)
        .call(d3.drag()
            .container(this.canvas)
            .subject(eval(toArrowFuncString(this.dragsubject)))
            .on("start", eval(toArrowFuncString(this.dragstarted)))
            .on("drag", eval(toArrowFuncString(this.dragged)))
            .on("end", eval(toArrowFuncString(this.dragended))))
        .call(d3.zoom()
            .scaleExtent([1 / 10, 8])
            .on('zoom', eval(toArrowFuncString(this.zoomed)))
        );
    }

    addNodeTitles() {
        d3.select(this.context.canvas)
            .on("mousemove", () => {
                const mouse = d3.mouse(this.context.canvas);
                const d = this.simulation.find(this.transform.invertX(mouse[0]), this.transform.invertY(mouse[1]), config['node_size']);
                if (d) { this.context.canvas.title = d.id } 
                else   { this.context.canvas.title = '' };
        });
    }

    simulate() {
        this.simulation = d3.forceSimulation(this.nodes)
            .force("link", d3.forceLink(this.links).id(d => d.id).distance(config['link_distance']))
            .force("charge", d3.forceManyBody().strength(config['node_charge']))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .force("x", d3.forceX(this.width / 2)).force("y", d3.forceY(this.height / 2))
            .on("tick", eval(toArrowFuncString(this.simulationUpdate)));
        this.simulation.force("x").strength(config['node_gravity']);
        this.simulation.force("y").strength(config['node_gravity']);
    }

    zoomed() {
        this.transform = currentEvent.transform;
        this.simulationUpdate();
    }

    dragsubject() {
        const node = this.simulation.find(this.transform.invertX(currentEvent.x), this.transform.invertY(currentEvent.y), config['node_size']);
        if (node) {
            node.x = this.transform.applyX(node.x);
            node.y = this.transform.applyY(node.y);
        }
        return node;
    }

    dragstarted() {
        if (!currentEvent.active) this.simulation.alphaTarget(0.3).restart();
        currentEvent.subject.fx = this.transform.invertX(currentEvent.subject.x);
        currentEvent.subject.fy = this.transform.invertY(currentEvent.subject.y);
    }

    dragged() {
        currentEvent.subject.fx = this.transform.invertX(currentEvent.x);
        currentEvent.subject.fy = this.transform.invertY(currentEvent.y);
    }

    dragended() {
        if (!currentEvent.active) this.simulation.alphaTarget(0);
        currentEvent.subject.fx = null;
        currentEvent.subject.fy = null;
    }

    simulationUpdate() {
        this.context.save();
        this.context.clearRect(0, 0, this.context.canvas.width, this.context.canvas.height);
        this.context.translate(this.transform.x, this.transform.y);
        this.context.scale(this.transform.k, this.transform.k);

        this.context.globalAlpha = config['link_alpha'];
        this.context.strokeStyle = config['link_color'];
        this.context.globalCompositeOperation = "destination-over";
        this.links.forEach(d => {
            this.context.beginPath();
            this.context.moveTo(d.source.x, d.source.y);
            this.context.lineTo(d.target.x, d.target.y);
            this.context.lineWidth = d.weight * config['link_width'];
            this.context.stroke();
        });
        
        this.context.strokeStyle = config['node_stroke_color'];
        this.context.lineWidth = config['node_stroke_width'] < 1e-3 ? 1e-9 : config['node_stroke_width'];
        this.context.globalCompositeOperation = "source-over";
        this.context.globalAlpha = 1;
        this.nodes.forEach((d, i) => {
            this.context.beginPath();
            this.context.arc(
                d.x, d.y,
                (config['scale_node_size_by_strength'] ? d.degree_normed : d.size) * config['node_size'],
                0, 2*Math.PI
            );
            this.context.stroke();
            this.context.fillStyle = d.color || config['node_fill_color'];
            this.context.fill();
        });
        this.context.restore();
    }
}