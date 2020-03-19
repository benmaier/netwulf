<script>
	import Network from './Network.svelte';
	import { json } from 'd3';
	
	let this_url = new URL(window.location.href);
	let data_path = this_url.searchParams.get("data");
	let config_path = this_url.searchParams.get("config");

	// let data, promise;
	window.data = undefined;
	window.config = undefined;

	// let promise_data = json(data_path).then(function(d) {
	let promise_data = json('tmp.json').then(function(d) {
		data = d;
	});
	// let promise_config = json(config_path).then(function(d) {
	let promise_config = json('config_tmp.json').then(function(d) {
		config = d;
	});

	let promise = Promise.all([promise_data, promise_config]);
</script>


<style>
</style>


{#await promise}
	<p>...loading data</p>
{:then value}
	<Network graph={data} config={config}/>
{/await}