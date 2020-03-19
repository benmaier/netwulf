<script>
	import Explorer from './NetworkExplorer.svelte';
	import { json } from 'd3';
	
	let this_url = new URL(window.location.href);
	let this_data_path = this_url.searchParams.get("data");

	let data;
	// let promise = json(this_data_path).then(function(graph) {
	let promise = json('tmp.json').then(function(graph) {
		data = graph;
	});
</script>


<style>
</style>


{#await promise}
	<p>...loading data</p>
{:then value}
	<Explorer graph={data}/>
{/await}