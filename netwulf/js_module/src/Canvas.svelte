<script>
	import { onMount } from 'svelte'

	export let network;
	export let canvas;
	export let width;
	export let height;

	onMount(() => {
		network.canvas = canvas;
		network.startVisualization();
        network.simulate();
        if (config['freeze_nodes'])
			network.simulation.alpha(0).restart();
    });

</script>

<style>
    .container {
        position: absolute;
        margin: auto;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 0
    }
    #canvas {
    	position: absolute;
    }
</style>

<div class='container'>
    <canvas bind:this={canvas} width={width} height={height}/>
</div>