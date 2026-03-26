<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { theme } from '$lib/store';

	let { children } = $props();

	// Apply theme to document root so CSS vars cascade properly
	$effect(() => {
		document.documentElement.setAttribute('data-theme', $theme);
	});

	onMount(() => {
		if ('serviceWorker' in navigator) {
			navigator.serviceWorker.register('/sw.js').catch(() => {});
		}
	});
</script>

<svelte:head>
	<title>Biblia — Original + Portugues</title>
	<meta name="description" content="Leia a Biblia com texto original em Hebraico e Grego lado a lado com a traducao em Portugues (ACF). 66 livros completos." />
</svelte:head>

{@render children()}
