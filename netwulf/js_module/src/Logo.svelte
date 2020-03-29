<style>
	.navbar-element {
		display: none;
		color: #cccccc;
		text-transform: uppercase;
		font-weight: 700;
		display: block;
		width: 400;
		transition: 0.05s;
	}
	.inline-flex {
		display: inline-flex;
	}
	a:hover {
		color: #a0aec0;
		text-decoration: none;
	}
	.fill-current {
		filter: invert(1);
	}
	.w-4 {
		width: 2.2rem;
	}
	.h-4 {
		height: 2.2rem;
	}
	.leftdiv {
		position: relative;
	}
	.rightdiv {
		position: relative;
		padding-top: 0.5rem;
		padding-left: 0.5rem;
	}
</style>

<nav class="inline-flex">
	<div class="leftdiv">
		<img class="fill-current w-4 h-4" src="logo.png">
	</div>
	<div class="rightdiv">
		<a href="https://netwulf.readthedocs.io/en/latest/" class="navbar-element">NETWULF</a>
	</div>
</nav>