<!-- SCRIPT -->
<script>
    // Load network
    import { onMount } from 'svelte';
    import Network from './network.js';

    // D3
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

    // Data    
    export let graph;

    // Canvas and parameters
    let canvas;
    window.devicePixelRatio = window.devicePixelRatio || 1;
 
    // Layout
    let width = window.innerWidth;
    let height = window.innerHeight;
    
    const nodeRadius = 15;

    // Links and nodes
    $: links = graph.links.map(d => Object.create(d));
    $: nodes = graph.nodes.map(d => Object.create(d));  

    // Colors
    const groupColour = d3.scaleOrdinal(d3.schemeCategory10);

    // Simulation
    let transform = d3.zoomIdentity;
    let simulation, context;
    
    onMount(visualize);

    function visualize() {
        context = canvas.getContext('2d');
        
        // Retina
        d3.select(canvas)
            .attr("width", width * devicePixelRatio)
            .attr("height", height * devicePixelRatio)
            .style("width", width + "px")
            .style("height", height + "px").node()
        context.scale(devicePixelRatio, devicePixelRatio)

        // Simulation
        simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2))
            .on("tick", simulationUpdate);

        // title
        d3.select(context.canvas)
            .on("mousemove", () => {
                const mouse = d3.mouse(context.canvas);
                const d = simulation.find(transform.invertX(mouse[0]), transform.invertY(mouse[1]), nodeRadius);
                if (d) 
                    context.canvas.title = d.id;
                else
                    context.canvas.title = '';
        });

        d3.select(canvas)
        .call(d3.drag()
            .container(canvas)
            .subject(dragsubject)
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))
        .call(d3.zoom()
          .scaleExtent([1 / 10, 8])
          .on('zoom', zoomed));
    }

    function simulationUpdate () {
        context.save();
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);
        context.translate(transform.x, transform.y);
        context.scale(transform.k, transform.k);

        links.forEach(d => {
            context.beginPath();
            context.moveTo(d.source.x, d.source.y);
            context.lineTo(d.target.x, d.target.y);
            context.globalAlpha = 0.6;
            context.strokeStyle = "#999";
            context.lineWidth = Math.sqrt(d.value);
            context.stroke();
            context.globalAlpha = 1;
        });
        
        nodes.forEach((d, i) => {
            context.beginPath();
            context.arc(d.x, d.y, nodeRadius, 0, 2*Math.PI);
            context.strokeStyle = "#fff";
            context.lineWidth = 1.5;
            context.stroke();
            context.fillStyle = groupColour(d.group);
            context.fill();
        });
        context.restore();
    }

    function zoomed() {
        transform = currentEvent.transform;
        simulationUpdate();
    }

    // Use the d3-force simulation to locate the node
    function dragsubject() {
        const node = simulation.find(transform.invertX(currentEvent.x), transform.invertY(currentEvent.y), nodeRadius);
        if (node) {
            node.x = transform.applyX(node.x);
            node.y = transform.applyY(node.y);
        }
        return node;
    }

    function dragstarted() {
        if (!currentEvent.active) simulation.alphaTarget(0.3).restart();
        currentEvent.subject.fx = transform.invertX(currentEvent.subject.x);
        currentEvent.subject.fy = transform.invertY(currentEvent.subject.y);
    }

    function dragged() {
        currentEvent.subject.fx = transform.invertX(currentEvent.x);
        currentEvent.subject.fy = transform.invertY(currentEvent.y);
    }

    function dragended() {
        if (!currentEvent.active) simulation.alphaTarget(0);
        currentEvent.subject.fx = null;
        currentEvent.subject.fy = null;
    }

    async function resize() {
        await sleep(1000);
        visualize()
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

</script>

<!-- STYLE -->
<style>
    .container {
        position: absolute;
        margin: auto;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
    }
</style>

<!-- HTML -->

<svelte:window bind:innerWidth={width} bind:innerHeight={height} on:resize={resize}/>
<div class='container'>
    <canvas bind:this={canvas} width={width} height={height}/>
</div>