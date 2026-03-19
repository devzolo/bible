<script lang="ts">
	import { onMount } from 'svelte';
	import { bibleIndex, sidebarOpen, viewMode, fontSize, searchOpen } from '$lib/store';
	import {
		search,
		searchVerses,
		highlightMatch,
		type SearchResult,
		type SearchResultVerse
	} from '$lib/search';

	let isOpen = $derived($searchOpen);
	let query = $state('');
	let selectedIndex = $state(0);
	let inputEl: HTMLInputElement | undefined = $state();
	let listEl: HTMLElement | undefined = $state();

	// Sync results
	let syncResults = $derived.by(() => {
		if (!$bibleIndex || !query.trim()) {
			return { nav: null, books: [], actions: [] };
		}
		return search(query, $bibleIndex);
	});

	// Async verse results
	let verseResults: SearchResultVerse[] = $state([]);
	let verseLoading = $state(false);
	let abortController: AbortController | null = null;

	// Debounced verse search
	let debounceTimer: ReturnType<typeof setTimeout> | undefined;

	$effect(() => {
		const q = query;
		const idx = $bibleIndex;

		clearTimeout(debounceTimer);
		if (abortController) {
			abortController.abort();
			abortController = null;
		}

		if (!idx || !q.trim() || q.trim().length < 3) {
			verseResults = [];
			verseLoading = false;
			return;
		}

		verseLoading = true;
		debounceTimer = setTimeout(async () => {
			const controller = new AbortController();
			abortController = controller;
			try {
				const results = await searchVerses(q, idx, controller.signal);
				if (!controller.signal.aborted) {
					verseResults = results;
					verseLoading = false;
				}
			} catch {
				if (!controller.signal.aborted) {
					verseLoading = false;
				}
			}
		}, 200);
	});

	// Flat list of all results for keyboard nav
	let allResults = $derived.by((): SearchResult[] => {
		const results: SearchResult[] = [];
		if (syncResults.nav) results.push(syncResults.nav);
		results.push(...syncResults.books);
		results.push(...verseResults);
		if (query.trim()) {
			results.push(...syncResults.actions);
		} else {
			// Show actions when empty
			results.push(...syncResults.actions);
		}
		return results;
	});

	// Reset selection when results change
	$effect(() => {
		allResults; // track
		selectedIndex = 0;
	});

	// Scroll selected item into view
	$effect(() => {
		if (!listEl) return;
		const selected = listEl.querySelector('[data-selected="true"]');
		if (selected) {
			selected.scrollIntoView({ block: 'nearest' });
		}
	});

	// Watch store for external open triggers (e.g. toolbar button)
	$effect(() => {
		if ($searchOpen) {
			query = '';
			verseResults = [];
			selectedIndex = 0;
			requestAnimationFrame(() => inputEl?.focus());
		}
	});

	function close() {
		$searchOpen = false;
		query = '';
		verseResults = [];
	}

	function executeResult(result: SearchResult) {
		switch (result.type) {
			case 'nav':
				window.location.hash = `#/${result.bookId}/${result.chapter}`;
				break;
			case 'book':
				window.location.hash = `#/${result.book.id}/1`;
				break;
			case 'verse':
				window.location.hash = `#/${result.bookId}/${result.chapter}`;
				break;
			case 'action':
				executeAction(result.id);
				break;
		}
		close();
	}

	function executeAction(actionId: string) {
		switch (actionId) {
			case 'mode-side-by-side':
				$viewMode = 'side-by-side';
				break;
			case 'mode-interleaved':
				$viewMode = 'interleaved';
				break;
			case 'mode-original-only':
				$viewMode = 'original-only';
				break;
			case 'mode-translation-only':
				$viewMode = 'translation-only';
				break;
			case 'font-increase':
				$fontSize = Math.min(24, $fontSize + 1);
				break;
			case 'font-decrease':
				$fontSize = Math.max(12, $fontSize - 1);
				break;
			case 'sidebar-toggle':
				$sidebarOpen = !$sidebarOpen;
				break;
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (!isOpen) return;

		switch (e.key) {
			case 'ArrowDown':
				e.preventDefault();
				selectedIndex = Math.min(selectedIndex + 1, allResults.length - 1);
				break;
			case 'ArrowUp':
				e.preventDefault();
				selectedIndex = Math.max(selectedIndex - 1, 0);
				break;
			case 'Enter':
				e.preventDefault();
				if (allResults[selectedIndex]) {
					executeResult(allResults[selectedIndex]);
				}
				break;
			case 'Escape':
				e.preventDefault();
				close();
				break;
		}
	}

	function getTypeIcon(type: SearchResult['type'], result?: SearchResult): string {
		switch (type) {
			case 'nav': return '→';
			case 'book': return '📖';
			case 'verse': return '✦';
			case 'action': return (result as any)?.icon ?? '⚡';
		}
	}

	function getTypeLabel(type: SearchResult['type']): string {
		switch (type) {
			case 'nav': return 'Navegação';
			case 'book': return 'Livro';
			case 'verse': return 'Versículo';
			case 'action': return 'Ação';
		}
	}

	// Track current section for group headers
	function shouldShowHeader(index: number): boolean {
		if (index === 0) return true;
		return allResults[index].type !== allResults[index - 1].type;
	}

	onMount(() => {
		function handleGlobalKey(e: KeyboardEvent) {
			if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
				e.preventDefault();
				$searchOpen = !$searchOpen;
			}
		}
		window.addEventListener('keydown', handleGlobalKey);
		return () => window.removeEventListener('keydown', handleGlobalKey);
	});
</script>

{#if isOpen}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="palette-backdrop" onclick={close} onkeydown={handleKeydown}>
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div class="palette" onclick={(e) => e.stopPropagation()} onkeydown={handleKeydown}>
			<div class="palette-input-wrap">
				<span class="search-icon">⌘K</span>
				<input
					bind:this={inputEl}
					bind:value={query}
					type="text"
					placeholder="Buscar versículos, livros, ações..."
					spellcheck="false"
					autocomplete="off"
				/>
				<button class="esc-hint" onclick={close}>
					<kbd>Esc</kbd>
				</button>
			</div>

			<div class="palette-results" bind:this={listEl}>
				{#if allResults.length === 0 && !verseLoading}
					<div class="empty-state">
						{#if query.trim().length > 0 && query.trim().length < 3}
							<span class="empty-icon">⌨</span>
							<span>Digite pelo menos 3 caracteres para buscar versículos</span>
						{:else if query.trim().length >= 3}
							<span class="empty-icon">∅</span>
							<span>Nenhum resultado para "{query}"</span>
						{:else}
							<span class="empty-icon">✦</span>
							<span>Digite para buscar ou use referências como "Jo 3:16"</span>
						{/if}
					</div>
				{/if}

				{#each allResults as result, i}
					{#if shouldShowHeader(i)}
						<div class="group-header">
							{getTypeLabel(result.type)}
						</div>
					{/if}
					<button
						class="result-item"
						class:selected={selectedIndex === i}
						data-selected={selectedIndex === i}
						onmouseenter={() => (selectedIndex = i)}
						onclick={() => executeResult(result)}
					>
						<span class="result-icon" class:nav={result.type === 'nav'} class:action={result.type === 'action'}>
							{getTypeIcon(result.type, result)}
						</span>
						<div class="result-body">
							{#if result.type === 'verse'}
								<span class="result-label">{result.label}</span>
								<span class="result-text">
									{#each highlightMatch(result.text, query) as seg}
										{#if seg.highlight}
											<mark>{seg.text}</mark>
										{:else}
											{seg.text}
										{/if}
									{/each}
								</span>
							{:else}
								<span class="result-label">
									{#if result.type === 'book'}
										{#each highlightMatch(result.label, query) as seg}
											{#if seg.highlight}
												<mark>{seg.text}</mark>
											{:else}
												{seg.text}
											{/if}
										{/each}
									{:else}
										{result.label}
									{/if}
								</span>
								<span class="result-detail">{result.detail}</span>
							{/if}
						</div>
						{#if selectedIndex === i}
							<kbd class="enter-hint">↵</kbd>
						{/if}
					</button>
				{/each}

				{#if verseLoading}
					<div class="loading-indicator">
						<div class="loading-dots">
							<span></span><span></span><span></span>
						</div>
						<span>Buscando versículos...</span>
					</div>
				{/if}
			</div>

			<div class="palette-footer">
				<span><kbd>↑↓</kbd> navegar</span>
				<span><kbd>↵</kbd> selecionar</span>
				<span><kbd>esc</kbd> fechar</span>
			</div>
		</div>
	</div>
{/if}

<style>
	.palette-backdrop {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.6);
		backdrop-filter: blur(4px);
		z-index: 1000;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding-top: min(20vh, 120px);
		animation: fadeIn 0.12s ease-out;
	}

	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: scale(0.98) translateY(-8px);
		}
		to {
			opacity: 1;
			transform: scale(1) translateY(0);
		}
	}

	.palette {
		width: 580px;
		max-width: calc(100vw - 32px);
		max-height: min(480px, 70vh);
		background: var(--bg-surface);
		border: 1px solid var(--border-light);
		border-radius: 12px;
		box-shadow:
			0 0 0 1px rgba(255, 255, 255, 0.04),
			0 16px 40px rgba(0, 0, 0, 0.5),
			0 4px 12px rgba(0, 0, 0, 0.3);
		display: flex;
		flex-direction: column;
		overflow: hidden;
		animation: slideIn 0.15s ease-out;
	}

	.palette-input-wrap {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 14px 16px;
		border-bottom: 1px solid var(--border);
	}

	.search-icon {
		font-size: 0.65rem;
		color: var(--text-dim);
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		padding: 3px 6px;
		border-radius: 4px;
		font-family: var(--font-sans);
		white-space: nowrap;
		font-weight: 600;
	}

	.palette-input-wrap input {
		flex: 1;
		background: none;
		border: none;
		color: var(--text);
		font-size: 0.95rem;
		font-family: var(--font-sans);
		outline: none;
		min-width: 0;
	}

	.palette-input-wrap input::placeholder {
		color: var(--text-dim);
	}

	.esc-hint {
		background: none;
		border: none;
		cursor: pointer;
		padding: 0;
	}

	.esc-hint kbd {
		font-size: 0.6rem;
		color: var(--text-dim);
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		padding: 2px 6px;
		border-radius: 3px;
		font-family: var(--font-sans);
	}

	.palette-results {
		flex: 1;
		overflow-y: auto;
		padding: 6px 0;
	}

	.group-header {
		font-size: 0.65rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--text-dim);
		padding: 10px 16px 4px;
	}

	.result-item {
		display: flex;
		align-items: center;
		gap: 10px;
		width: 100%;
		padding: 8px 16px;
		background: none;
		border: none;
		color: var(--text);
		cursor: pointer;
		text-align: left;
		font-family: var(--font-sans);
		transition: background 0.06s;
	}

	.result-item:hover,
	.result-item.selected {
		background: var(--bg-surface-2);
	}

	.result-icon {
		width: 28px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 6px;
		font-size: 0.8rem;
		background: var(--bg-surface-3);
		color: var(--text-muted);
		flex-shrink: 0;
	}

	.result-icon.nav {
		background: rgba(201, 168, 76, 0.15);
		color: var(--accent);
	}

	.result-icon.action {
		background: rgba(168, 196, 212, 0.12);
		color: var(--greek);
	}

	.result-body {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
		gap: 1px;
	}

	.result-label {
		font-size: 0.85rem;
		font-weight: 500;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.result-detail {
		font-size: 0.72rem;
		color: var(--text-dim);
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.result-text {
		font-size: 0.75rem;
		color: var(--text-muted);
		line-height: 1.4;
		overflow: hidden;
		text-overflow: ellipsis;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
	}

	.result-text mark,
	.result-label mark {
		background: rgba(201, 168, 76, 0.25);
		color: var(--accent);
		border-radius: 2px;
		padding: 0 1px;
	}

	.enter-hint {
		font-size: 0.6rem;
		color: var(--text-dim);
		background: var(--bg-surface-3);
		border: 1px solid var(--border);
		padding: 2px 5px;
		border-radius: 3px;
		font-family: var(--font-sans);
		flex-shrink: 0;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
		padding: 32px 16px;
		color: var(--text-dim);
		font-size: 0.8rem;
		text-align: center;
	}

	.empty-icon {
		font-size: 1.3rem;
		opacity: 0.5;
	}

	.loading-indicator {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 12px 16px;
		color: var(--text-dim);
		font-size: 0.75rem;
	}

	.loading-dots {
		display: flex;
		gap: 3px;
	}

	.loading-dots span {
		width: 4px;
		height: 4px;
		background: var(--text-dim);
		border-radius: 50%;
		animation: dotPulse 1s ease-in-out infinite;
	}

	.loading-dots span:nth-child(2) {
		animation-delay: 0.15s;
	}

	.loading-dots span:nth-child(3) {
		animation-delay: 0.3s;
	}

	@keyframes dotPulse {
		0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
		40% { opacity: 1; transform: scale(1); }
	}

	.palette-footer {
		display: flex;
		gap: 16px;
		padding: 8px 16px;
		border-top: 1px solid var(--border);
		font-size: 0.65rem;
		color: var(--text-dim);
	}

	.palette-footer kbd {
		font-size: 0.6rem;
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		padding: 1px 4px;
		border-radius: 2px;
		font-family: var(--font-sans);
		margin-right: 3px;
	}

	@media (max-width: 600px) {
		.palette-backdrop {
			padding-top: 16px;
		}

		.palette {
			max-height: calc(100vh - 32px);
			border-radius: 10px;
		}

		.palette-footer {
			display: none;
		}
	}
</style>
