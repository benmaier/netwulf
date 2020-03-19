export default Network;

// Imports
// -------
import { scaleLinear, scaleOrdinal } from 'd3-scale';
import { zoom, zoomIdentity } from 'd3-zoom';
import { schemeCategory10 } from 'd3-scale-chromatic';
import { select, selectAll, mouse } from 'd3-selection';
import { drag } from 'd3-drag';
import { forceSimulation, forceLink, forceManyBody, forceCenter } from 'd3-force';
import {event as currentEvent} from 'd3-selection';

let d3 = {
    zoom, zoomIdentity, scaleLinear, scaleOrdinal, schemeCategory10, select,
    selectAll, mouse, drag,  forceSimulation, forceLink, forceManyBody, forceCenter
};


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

        // DEBUG
        this.nodeRadius = 10;

        // Retina rendering
        this.devicePixelRatio = window.devicePixelRatio || 1;
        d3.select(this.canvas)
            .attr("width", this.width * this.devicePixelRatio)
            .attr("height", this.height * this.devicePixelRatio)
            .style("width", this.width + "px")
            .style("height", this.height + "px").node()
        this.context.scale(this.devicePixelRatio, this.devicePixelRatio)

        // Transformations (dragging, panning, zooming)
        this.transform = d3.zoomIdentity;
        d3.select(this.canvas)
        .call(d3.drag()
            .container(this.canvas)
            .subject(this.toArrowFunc(this.dragsubject))
            .on("start", this.toArrowFunc(this.dragstarted))
            .on("drag", this.toArrowFunc(this.dragged))
            .on("end", this.toArrowFunc(this.dragended)))
        .call(d3.zoom()
            .scaleExtent([1 / 10, 8])
            .on('zoom', this.toArrowFunc(this.zoomed))
        );

        // Node titles
        d3.select(this.context.canvas)
            .on("mousemove", () => {
                const mouse = d3.mouse(this.context.canvas);
                const d = this.simulation.find(this.transform.invertX(mouse[0]), this.transform.invertY(mouse[1]), this.nodeRadius);
                if (d) 
                    this.context.canvas.title = d.id;
                else
                    this.context.canvas.title = '';
        });

    }

    simulate() {
        this.simulation = d3.forceSimulation(this.nodes)
            .force("link", d3.forceLink(this.links).id(d => d.id))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .on("tick", this.toArrowFunc(this.simulationUpdate));
    }

    zoomed() {
        this.transform = currentEvent.transform;
        this.simulationUpdate();
    }

    dragsubject() {
        const node = this.simulation.find(this.transform.invertX(currentEvent.x), this.transform.invertY(currentEvent.y), this.nodeRadius);
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

        this.links.forEach(d => {
            this.context.beginPath();
            this.context.moveTo(d.source.x, d.source.y);
            this.context.lineTo(d.target.x, d.target.y);
            this.context.globalAlpha = 0.6;
            this.context.strokeStyle = "#999";
            this.context.lineWidth = Math.sqrt(d.value);
            this.context.stroke();
            this.context.globalAlpha = 1;
        });
        
        this.nodes.forEach((d, i) => {
            this.context.beginPath();
            this.context.arc(d.x, d.y, this.nodeRadius, 0, 2*Math.PI);
            this.context.strokeStyle = "#fff";
            this.context.lineWidth = 1.5;
            this.context.stroke();
            this.context.fillStyle = '#000000'
            this.context.fill();
        });
        this.context.restore();
    }

    toArrowFunc(func) {
        // Takes any function and formats it as a arrow function expression, like `() => { ... }`
        // It is necessary to use this function to reformat all function that function as listeners
        // in `on` method calls for d3 objects. Reason: d3 invokes the listener within the `this`
        // context of the simulation, and class methods are in the class context so cannot  be passed.
        let func_as_string = '() => {' + func.toString().split('\n').splice(1).join('\n');
        return eval(func_as_string);
    }
}