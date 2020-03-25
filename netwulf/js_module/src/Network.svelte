<!-- SCRIPT -->
<!-- ------ -->

<script>

    // Load network
    import { onMount } from 'svelte';
    import Controls from './Controls.svelte';
    import Network from './network.js';
    import { validateData, scaleLinks, scaleNodes, recolorNodes, initialNodePositions } from './preprocessing.js';
    import { sleep } from './utils.js'

    // Preprocess data
    let isValid = validateData(data);
    let linkWeightOrder = scaleLinks(data);
    scaleNodes(data);
    let groupColors = recolorNodes(data);
    initialNodePositions(data, config);

    // Canvas and parameters
    let canvas; 
 
    // Layout
    let width = window.innerWidth;
    let height = window.innerHeight;

    // Network prototype, links and nodes
    let network, links, nodes;

    if (isValid) {

        $: links = data.links.map(d => Object.create(d));
        $: nodes = data.nodes.map(d => Object.create(d));

        // Launch visualization
        onMount(() => {
            network = new Network(canvas, width, height, nodes, links, groupColors);
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

<Controls {network} {groupColors} {linkWeightOrder}/>