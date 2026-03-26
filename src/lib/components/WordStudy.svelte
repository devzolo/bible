<script lang="ts">
	import { wordStudyQuery, wordStudyOpen, bibleIndex } from '$lib/store';
	import { searchVerses, type SearchResultVerse } from '$lib/search';

	let query = $derived($wordStudyQuery);
	let isOpen = $derived($wordStudyOpen);
	let results: SearchResultVerse[] = $state([]);
	let loading = $state(false);

	$effect(() => {
		if (!isOpen || !query || !$bibleIndex) {
			results = [];
			return;
		}
		loading = true;
		const controller = new AbortController();
		searchVerses(query, $bibleIndex, controller.signal).then(r => {
			if (!controller.signal.aborted) {
				results = r;
				loading = false;
			}
		}).catch(() => { loading = false; });

		return () => controller.abort();
	});

	function close() {
		$wordStudyOpen = false;
		$wordStudyQuery = '';
	}

	function goTo(r: SearchResultVerse) {
		window.location.hash = `#/${r.bookId}/${r.chapter}`;
		close();
	}
</script>

{#if isOpen && query}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="ws-backdrop" onclick={close} onkeydown={(e) => e.key === 'Escape' && close()}>
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div class="ws-panel" onclick={(e) => e.stopPropagation()}>
			<div class="ws-header">
				<div class="ws-title">
					<span class="ws-icon">🔤</span>
					<span>Estudo de palavra: <strong>"{query}"</strong></span>
				</div>
				<button class="ws-close" onclick={close}>✕</button>
			</div>

			<div class="ws-body">
				{#if loading}
					<div class="ws-loading">Buscando em toda a Biblia...</div>
				{:else if results.length === 0}
					<div class="ws-empty">Nenhuma ocorrencia encontrada.</div>
				{:else}
					<div class="ws-count">{results.length} ocorrencia{results.length > 1 ? 's' : ''} encontrada{results.length > 1 ? 's' : ''}</div>
					{#each results as r}
						<button class="ws-result" onclick={() => goTo(r)}>
							<span class="ws-ref">{r.label}</span>
							<span class="ws-text">{r.text}</span>
						</button>
					{/each}
				{/if}
			</div>
		</div>
	</div>
{/if}

<style>
	.ws-backdrop {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(2px);
		z-index: 950;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding-top: min(12vh, 80px);
		animation: fadeIn 0.1s ease-out;
	}

	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	.ws-panel {
		width: 520px;
		max-width: calc(100vw - 32px);
		max-height: min(500px, 70vh);
		background: var(--bg-surface);
		border: 1px solid var(--border-light);
		border-radius: 12px;
		box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.ws-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 14px 16px;
		border-bottom: 1px solid var(--border);
	}

	.ws-title {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.85rem;
		color: var(--text);
	}

	.ws-icon {
		font-size: 1rem;
	}

	.ws-title strong {
		color: var(--accent);
	}

	.ws-close {
		background: none;
		border: none;
		color: var(--text-dim);
		cursor: pointer;
		padding: 4px 8px;
		border-radius: 4px;
		font-size: 0.9rem;
	}

	.ws-close:hover {
		background: var(--bg-hover);
		color: var(--text);
	}

	.ws-body {
		flex: 1;
		overflow-y: auto;
		padding: 4px 0;
	}

	.ws-count {
		padding: 8px 16px 4px;
		font-size: 0.7rem;
		color: var(--text-dim);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.ws-result {
		display: flex;
		flex-direction: column;
		gap: 2px;
		width: 100%;
		padding: 10px 16px;
		background: none;
		border: none;
		text-align: left;
		cursor: pointer;
		font-family: var(--font-sans);
		color: var(--text);
		transition: background 0.1s;
	}

	.ws-result:hover {
		background: var(--bg-surface-2);
	}

	.ws-ref {
		font-size: 0.78rem;
		font-weight: 600;
		color: var(--accent);
	}

	.ws-text {
		font-size: 0.75rem;
		color: var(--text-muted);
		line-height: 1.4;
		overflow: hidden;
		text-overflow: ellipsis;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
	}

	.ws-loading, .ws-empty {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 32px 16px;
		color: var(--text-dim);
		font-size: 0.82rem;
	}
</style>
