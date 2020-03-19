<!-- SCRIPT -->
<!-- ------ -->

<script>

    // Load network
    import { onMount } from 'svelte';
    import Network from './network.js'

    // Data
    export let graph;

    // Canvas and parameters
    let canvas;
 
    // Layout
    let width = window.innerWidth;
    let height = window.innerHeight;

    // Links and nodes
    $: links = graph.links.map(d => Object.create(d));
    $: nodes = graph.nodes.map(d => Object.create(d));

    // Launch visualization
    onMount(() => {
        let network = new Network(canvas, width, height, nodes, links);
        network.simulate();
    });

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

<svelte:window bind:innerWidth={width} bind:innerHeight={height}/>
<div class='container'>
    <canvas bind:this={canvas} width={width} height={height}/>
</div>