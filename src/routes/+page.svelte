<script lang="ts">
	import { onMount } from 'svelte';
	import { loadIndex, loadBook } from '$lib/api';
	import {
		bibleIndex,
		currentBook,
		currentChapter,
		currentBookMeta,
		sidebarOpen
	} from '$lib/store';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import Toolbar from '$lib/components/Toolbar.svelte';
	import ChapterNav from '$lib/components/ChapterNav.svelte';
	import VerseReader from '$lib/components/VerseReader.svelte';
	import SearchPalette from '$lib/components/SearchPalette.svelte';

	let loading = $state(true);
	let contentEl: HTMLElement | undefined = $state();

	async function handleRoute() {
		const hash = window.location.hash || '';
		const match = hash.match(/^#\/([^/]+)\/(\d+)$/);
		if (match && $bibleIndex) {
			const bookId = match[1];
			const chapter = parseInt(match[2]);
			const meta = $bibleIndex.books.find((b) => b.id === bookId);
			if (meta) {
				$currentBookMeta = meta;
				try {
					const bookData = await loadBook(bookId);
					$currentBook = bookData;
					$currentChapter = Math.min(Math.max(1, chapter), bookData.chapters.length);
					// Scroll to top
					if (contentEl) contentEl.scrollTop = 0;
				} catch (e) {
					console.error('Failed to load book:', e);
				}
			}
		}
	}

	onMount(async () => {
		try {
			const idx = await loadIndex();
			$bibleIndex = idx;

			if (!window.location.hash) {
				window.location.hash = '#/genesis/1';
			}

			await handleRoute();
		} catch (e) {
			console.error('Failed to load index:', e);
		} finally {
			loading = false;
		}

		window.addEventListener('hashchange', handleRoute);
		return () => window.removeEventListener('hashchange', handleRoute);
	});

	let isOpen = $derived($sidebarOpen);
</script>

<SearchPalette />

<div class="app-layout">
	<Sidebar />

	{#if isOpen}
		<button class="overlay" onclick={() => ($sidebarOpen = false)}></button>
	{/if}

	<main class="main-content" class:sidebar-open={isOpen}>
		{#if loading}
			<div class="loading">
				<div class="spinner"></div>
				<p>Carregando escrituras...</p>
			</div>
		{:else}
			<Toolbar />
			<ChapterNav />
			<div class="scroll-area" bind:this={contentEl}>
				<VerseReader />
			</div>
		{/if}
	</main>
</div>

<style>
	.app-layout {
		display: flex;
		height: 100vh;
		overflow: hidden;
	}

	.main-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		height: 100vh;
		overflow: hidden;
		transition: margin-left 0.25s ease;
	}

	.scroll-area {
		flex: 1;
		overflow-y: auto;
	}

	.overlay {
		display: none;
	}

	.loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		gap: 16px;
		color: var(--text-muted);
	}

	.spinner {
		width: 32px;
		height: 32px;
		border: 2px solid var(--border);
		border-top-color: var(--accent);
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	@media (min-width: 768px) {
		.main-content.sidebar-open {
			margin-left: var(--sidebar-width);
		}
	}

	@media (max-width: 767px) {
		.overlay {
			display: block;
			position: fixed;
			inset: 0;
			background: rgba(0, 0, 0, 0.5);
			z-index: 50;
			border: none;
			cursor: default;
		}
	}
</style>
