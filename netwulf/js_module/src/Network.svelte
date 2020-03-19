<!-- SCRIPT -->
<!-- ------ -->

<script>

    // Load network
    import { onMount } from 'svelte';
    import Network from './network.js'
    import { scaleNodes, scaleLinks, recolorNodes, recolorLinks, inferMode } from './preprocessing.js'

    // Data
    export let graph;
    export let config;

    console.log(config)

    // Preprocess data
    scaleNodes(graph);
    scaleLinks(graph);
    recolorNodes(graph);
    recolorLinks(graph);
    inferMode(graph);

    // Canvas and parameters
    let canvas;
 
    // Layout
    let width = window.innerWidth;
    let height = window.innerHeight;

    // Links and nodes
    let network;
    $: links = graph.links.map(d => Object.create(d));
    $: nodes = graph.nodes.map(d => Object.create(d));

    // Launch visualization
    onMount(() => {
        network = new Network(canvas, width, height, nodes, links);
        network.simulate();
    });

    // Handle resizing
    async function resize() {
        await sleep(1000)
        network.width = width;
        network.height = height;
        network.addRetinaRendering();
        network.simulate(); 
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