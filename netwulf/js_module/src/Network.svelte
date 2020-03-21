<!-- SCRIPT -->
<!-- ------ -->

<script>

    // Load network
    import { onMount } from 'svelte';
    import Network from './network.js'
    import { validateData, scaleLinks, scaleNodes, recolorNodes, initialNodePositions } from './preprocessing.js'

    // Data
    export let graph;
    export let config;

    // Preprocess data
    let isValid = validateData(graph);
    scaleLinks(graph);
    scaleNodes(graph);
    recolorNodes(graph);
    initialNodePositions(graph, config);

    // Canvas and parameters
    let canvas;
 
    // Layout
    let width = window.innerWidth;
    let height = window.innerHeight;

    // Network prototype, links and nodes
    let network, links, nodes;

    if (isValid) {

        $: links = graph.links.map(d => Object.create(d));
        $: nodes = graph.nodes.map(d => Object.create(d));

        // Launch visualization
        onMount(() => {
            network = new Network(canvas, width, height, nodes, links);
            network.simulate();
        });
    }

    // Handle resizing
    async function resize() {
        await sleep(1000)
        network.width = width;
        network.height = height;
        network.addRetinaRendering();
        network.simulation.restart();
    }

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

</script>


<!-- STYLE -->
<!-- ----- -->

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
<!-- ---- -->

<svelte:window bind:innerWidth={width} bind:innerHeight={height} on:resize={resize}/>
<div class='container'>
    <canvas bind:this={canvas} width={width} height={height}/>
</div>