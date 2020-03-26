<script>
	import Logo from './Logo.svelte';
	import Menu from './Menu.svelte';

</script>

<style>
	.flex {
		display: flex;
	}

	.header {
		justify-content: space-between;
		background-color: #000000;
		padding: 0.5rem;
		padding-bottom: 0.3rem;
		padding-left: 1rem;
		padding-right: 1rem;
		align-items: center;
		color: #718096;
		border-bottom-width: 2px;
		z-index: 1
	}

</style>

<header class="flex header">
	<Logo/>	
	<Menu/>
</header>
