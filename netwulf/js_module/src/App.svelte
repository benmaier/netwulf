<script>
	import Explorer from './NetworkExplorer.svelte';
	import data from './data.js';
</script>

<style>
	.chart {
		width: 100%;
		max-width: 640px;
		height: 100%;
		min-height: 280px;
		max-height: 480px;
		margin: 0 auto;
	}
</style>

<main class="chart">
	<Explorer graph={data}/>
</main>