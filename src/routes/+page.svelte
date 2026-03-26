<script lang="ts">
	import { onMount } from 'svelte';
	import { loadIndex, loadBook, preloadAdjacentChapters } from '$lib/api';
	import {
		bibleIndex,
		currentBook,
		currentChapter,
		currentBookMeta,
		sidebarOpen,
		lastPosition,
		addToHistory,
		trackReading,
		fullscreen,
		activeSearchHighlight,
		translation
	} from '$lib/store';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import Toolbar from '$lib/components/Toolbar.svelte';
	import ChapterNav from '$lib/components/ChapterNav.svelte';
	import VerseReader from '$lib/components/VerseReader.svelte';
	import SearchPalette from '$lib/components/SearchPalette.svelte';
	import BookmarksPanel from '$lib/components/BookmarksPanel.svelte';
	import WordStudy from '$lib/components/WordStudy.svelte';

	let loading = $state(true);
	let error = $state('');
	let contentEl: HTMLElement | undefined = $state();
	let transitioning = $state(false);
	let touchStartX = $state(0);
	let touchStartY = $state(0);
	let showBookmarks = $state(false);

	async function handleRoute() {
		const hash = window.location.hash || '';
		const match = hash.match(/^#\/([^/]+)\/(\d+)(?::(\d+))?$/);
		if (match && $bibleIndex) {
			const bookId = match[1];
			const chapter = parseInt(match[2]);
			const verse = match[3] ? parseInt(match[3]) : undefined;
			const meta = $bibleIndex.books.find((b) => b.id === bookId);
			if (meta) {
				$currentBookMeta = meta;
				// Transition animation
				transitioning = true;
				try {
					const bookData = await loadBook(bookId, $translation);
					$currentBook = bookData;
					$currentChapter = Math.min(Math.max(1, chapter), bookData.chapters.length);
					// Save position
					$lastPosition = { bookId, chapter: $currentChapter };
					// Add to history & track reading stats
					addToHistory({ bookId, bookName: meta.name, chapter: $currentChapter });
					trackReading();
					// Preload adjacent chapters
					preloadAdjacentChapters(bookId, $currentChapter, bookData.chapters.length, $bibleIndex, $translation);

					await new Promise(r => setTimeout(r, 50));
					transitioning = false;

					// Scroll to verse or top
					if (verse && contentEl) {
						requestAnimationFrame(() => {
							const el = contentEl?.querySelector(`#v${verse}`);
							if (el) {
								el.scrollIntoView({ behavior: 'smooth', block: 'center' });
								el.classList.add('highlight-verse');
								setTimeout(() => el.classList.remove('highlight-verse'), 2000);
							}
						});
					} else if (contentEl) {
						contentEl.scrollTop = 0;
					}
					error = '';
				} catch (e) {
					console.error('Failed to load book:', e);
					error = 'Falha ao carregar o livro. Verifique sua conexão.';
					transitioning = false;
				}
			}
		}
	}

	function navigateChapter(delta: number) {
		if (!$currentBook || !$currentBookMeta) return;
		const next = $currentChapter + delta;
		if (next >= 1 && next <= $currentBook.chapters.length) {
			window.location.hash = `#/${$currentBook.id}/${next}`;
		} else if (delta > 0 && $bibleIndex) {
			// Go to next book
			const idx = $bibleIndex.books.findIndex(b => b.id === $currentBookMeta!.id);
			if (idx < $bibleIndex.books.length - 1) {
				window.location.hash = `#/${$bibleIndex.books[idx + 1].id}/1`;
			}
		} else if (delta < 0 && $bibleIndex) {
			// Go to previous book, last chapter
			const idx = $bibleIndex.books.findIndex(b => b.id === $currentBookMeta!.id);
			if (idx > 0) {
				const prevBook = $bibleIndex.books[idx - 1];
				window.location.hash = `#/${prevBook.id}/${prevBook.chapters}`;
			}
		}
	}

	onMount(async () => {
		try {
			const idx = await loadIndex();
			$bibleIndex = idx;

			if (!window.location.hash) {
				// Restore last position or default to Genesis 1
				const last = $lastPosition;
				if (last) {
					window.location.hash = `#/${last.bookId}/${last.chapter}`;
				} else {
					window.location.hash = '#/genesis/1';
				}
			}

			await handleRoute();
		} catch (e) {
			console.error('Failed to load index:', e);
			error = 'Falha ao carregar o índice. Verifique sua conexão.';
		} finally {
			loading = false;
		}

		window.addEventListener('hashchange', handleRoute);
		return () => window.removeEventListener('hashchange', handleRoute);
	});

	// Keyboard shortcuts
	function handleKeydown(e: KeyboardEvent) {
		// Don't intercept when typing in inputs
		if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

		switch (e.key) {
			case 'ArrowLeft':
				if (!e.ctrlKey && !e.metaKey) {
					e.preventDefault();
					navigateChapter(-1);
				}
				break;
			case 'ArrowRight':
				if (!e.ctrlKey && !e.metaKey) {
					e.preventDefault();
					navigateChapter(1);
				}
				break;
			case 'Escape':
				if ($fullscreen) {
					$fullscreen = false;
				} else if ($sidebarOpen && window.innerWidth < 768) {
					$sidebarOpen = false;
				}
				break;
			case 'f':
				if (!e.ctrlKey && !e.metaKey) {
					$fullscreen = !$fullscreen;
				}
				break;
			case 'b':
				if (!e.ctrlKey && !e.metaKey) {
					showBookmarks = !showBookmarks;
				}
				break;
			case 's':
				if (!e.ctrlKey && !e.metaKey) {
					$sidebarOpen = !$sidebarOpen;
				}
				break;
		}
	}

	// Swipe gestures for mobile
	function handleTouchStart(e: TouchEvent) {
		touchStartX = e.touches[0].clientX;
		touchStartY = e.touches[0].clientY;
	}

	function handleTouchEnd(e: TouchEvent) {
		const dx = e.changedTouches[0].clientX - touchStartX;
		const dy = e.changedTouches[0].clientY - touchStartY;
		// Only horizontal swipes (more horizontal than vertical, min 80px)
		if (Math.abs(dx) > 80 && Math.abs(dx) > Math.abs(dy) * 1.5) {
			if (dx > 0) {
				navigateChapter(-1);
			} else {
				navigateChapter(1);
			}
		}
	}

	function retryLoad() {
		error = '';
		loading = true;
		location.reload();
	}

	let isOpen = $derived($sidebarOpen);
	let isFullscreen = $derived($fullscreen);

	// Reload book when translation changes
	let prevTranslation = $state($translation);
	$effect(() => {
		const t = $translation;
		if (t !== prevTranslation) {
			prevTranslation = t;
			handleRoute();
		}
	});
</script>

<svelte:window onkeydown={handleKeydown} />

<SearchPalette />
<WordStudy />

{#if showBookmarks}
	<BookmarksPanel onclose={() => showBookmarks = false} />
{/if}

<div
	class="app-layout"
	class:fullscreen={isFullscreen}
	ontouchstart={handleTouchStart}
	ontouchend={handleTouchEnd}
>
	{#if !isFullscreen}
		<Sidebar />
	{/if}

	{#if isOpen && !isFullscreen}
		<button class="overlay" aria-label="Fechar sidebar" onclick={() => ($sidebarOpen = false)}></button>
	{/if}

	<main class="main-content" class:sidebar-open={isOpen && !isFullscreen}>
		{#if loading}
			<div class="loading">
				<div class="spinner"></div>
				<p>Carregando escrituras...</p>
			</div>
		{:else if error}
			<div class="error-state">
				<div class="error-icon">!</div>
				<p>{error}</p>
				<button class="retry-btn" onclick={retryLoad}>Tentar novamente</button>
			</div>
		{:else}
			{#if !isFullscreen}
				<Toolbar ontogglebookmarks={() => showBookmarks = !showBookmarks} />
			{/if}
			<ChapterNav />
			<div
				class="scroll-area"
				class:transitioning
				bind:this={contentEl}
			>
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
		transition: opacity 0.15s ease;
	}

	.scroll-area.transitioning {
		opacity: 0.3;
	}

	.overlay {
		display: none;
	}

	/* Loading */
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
		to { transform: rotate(360deg); }
	}

	/* Error state */
	.error-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		gap: 16px;
		color: var(--text-muted);
		text-align: center;
		padding: 24px;
	}

	.error-icon {
		width: 48px;
		height: 48px;
		border-radius: 50%;
		background: rgba(220, 80, 80, 0.15);
		color: #dc5050;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.5rem;
		font-weight: 700;
	}

	.retry-btn {
		padding: 8px 20px;
		background: var(--accent);
		color: var(--bg);
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-family: var(--font-sans);
		font-size: 0.85rem;
		font-weight: 600;
		transition: opacity 0.15s;
	}

	.retry-btn:hover {
		opacity: 0.9;
	}

	/* Fullscreen */
	.fullscreen .main-content {
		margin-left: 0 !important;
	}

	/* Verse highlight animation */
	:global(.highlight-verse) {
		background: rgba(201, 168, 76, 0.15) !important;
		border-radius: 4px;
		transition: background 0.3s ease;
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
