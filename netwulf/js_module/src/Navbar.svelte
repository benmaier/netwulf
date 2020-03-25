<script>
	import Logo from './Logo.svelte';
	import Menu from './Menu.svelte';

</script>

<style>
	.flex {
		display: flex;
		z-index: 1;
	}

	.header {
		justify-content: space-between;
		background-color: #000;
		padding: 0.5rem;
		align-items: center;
		color: #718096;
		border-bottom-width: 2px;
	}

</style>

<div class="flex header">
	<nav class="flex">
		<Logo/>	
	</nav>
	<Menu/>
</div>
