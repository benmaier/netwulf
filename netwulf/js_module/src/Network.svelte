<!-- SCRIPT -->
<!-- ------ -->

<script>

    // Load network
    import { onMount } from 'svelte';
    import Canvas from './Canvas.svelte';
    import Controls from './Controls.svelte';
    import Navbar from './Navbar.svelte';
    import Network from './network.js';
    import { validateData, scaleLinks, scaleNodes, recolorNodes, initialNodePositions } from './preprocessing.js';
    import { sleep } from './utils.js'
    import { postData } from './post_json.js'

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

        // Crate network prototype
        network = new Network(canvas, width, height, nodes, links, groupColors);
        window.tmp = network;
    }



    // Handle resizing
    async function resize() {
        await sleep(1000)
        network.width = width;
        network.height = height;
        network.addRetinaRendering();
        network.simulation.restart();
    }

    // Handle keydown events
    window.alertActive = false;
    async function handleKeydown() {
        console.log(event)
        if (event.key == 'Enter') {
            if (!alertActive) {
                await sleep(100);  // sleep is a necessary hack to avoid immediate POST
                postData(network);
            }
        }

        if (event.key == 'c') {
            let checkbox = document.getElementById('fitImageCheckbox');
            if (checkbox !== null)
                checkbox.checked = !checkbox.checked;
        }
    }

</script>


<!-- HTML -->
<!-- ---- -->

<svelte:window bind:innerWidth={width} bind:innerHeight={height} on:resize={resize}  on:keydown={handleKeydown}/>

<Canvas {network} {canvas} {width} {height}/>

<Controls {network} {groupColors} {linkWeightOrder}/>

<Navbar {network}/>