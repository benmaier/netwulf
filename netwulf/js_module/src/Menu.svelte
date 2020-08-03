<script>
	import { postData } from './post_json.js'

	export let network;
	function handlePostToPython() {
		postData(network);
	}
</script>

<style>
	a {
		color: #ffffff;
		text-decoration: none;
	}
	.fill-current {
		fill: currentColor;
	}
	.w-4 {
		width: 1rem;
	}
	.h-4 {
		height: 1rem;
	}
	.inline-flex {
		display: inline-flex;
	}
	.btn-dark {
		color: #fff;
		background-color: #343a40;
		border-color: #343a40;
	}
	.btn {
		padding: 0.25rem 1.65rem;
		font-size: 1.0rem;
		line-height: 1.5;
		border-radius: 0.3rem;
		z-index: 1;
	}
	.btn-dark {
		color: #fff;
		background-color: #1A1A1A;
		border-color: #000000;
	}
	.btn-dark:hover {
		color: #fff;
		background-color: #000000;
		border-color: #000000;
	}
</style>

<nav class="inline-flex">
	<button on:click={handlePostToPython} type="button" class="btn btn-dark">
		Post to Python
	</button>
	<button type="button" class="btn btn-dark">
		<svg class="fill-current w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z"/></svg>
	</button>
</nav>