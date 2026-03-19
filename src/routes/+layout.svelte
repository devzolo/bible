<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<svelte:head>
	<title>Bíblia — Original + Português</title>
</svelte:head>

{@render children()}
