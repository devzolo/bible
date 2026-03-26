<script lang="ts">
	import { bookmarks, removeBookmark, readingHistory, readingStats, highlights, annotations } from '$lib/store';

	let { onclose }: { onclose: () => void } = $props();
	let tab: 'bookmarks' | 'history' | 'stats' = $state('bookmarks');
	let stats = $derived($readingStats);

	function goTo(bookId: string, chapter: number, verse?: number) {
		window.location.hash = `#/${bookId}/${chapter}${verse ? `:${verse}` : ''}`;
		onclose();
	}

	function formatDate(ts: number): string {
		const d = new Date(ts);
		const now = new Date();
		const diff = now.getTime() - d.getTime();
		if (diff < 60000) return 'agora';
		if (diff < 3600000) return `${Math.floor(diff / 60000)}min`;
		if (diff < 86400000) return `${Math.floor(diff / 3600000)}h`;
		if (diff < 604800000) return `${Math.floor(diff / 86400000)}d`;
		return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' });
	}
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="panel-backdrop" onclick={onclose} onkeydown={(e) => e.key === 'Escape' && onclose()}>
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="panel" onclick={(e) => e.stopPropagation()}>
		<div class="panel-header">
			<div class="tabs">
				<button class="tab" class:active={tab === 'bookmarks'} onclick={() => tab = 'bookmarks'}>
					Favoritos
				</button>
				<button class="tab" class:active={tab === 'history'} onclick={() => tab = 'history'}>
					Historico
				</button>
				<button class="tab" class:active={tab === 'stats'} onclick={() => tab = 'stats'}>
					Stats
				</button>
			</div>
			<button class="close" onclick={onclose}>✕</button>
		</div>

		<div class="panel-body">
			{#if tab === 'bookmarks'}
				{#if $bookmarks.length === 0}
					<div class="empty">
						<span class="empty-icon">☆</span>
						<p>Nenhum favorito ainda.</p>
						<p class="hint">Clique no numero de um versiculo para marcar.</p>
					</div>
				{:else}
					{#each $bookmarks as bm}
						<div class="item">
							<button class="item-body" onclick={() => goTo(bm.bookId, bm.chapter, bm.verse)}>
								<span class="item-ref">{bm.bookName} {bm.chapter}:{bm.verse}</span>
								<span class="item-text">{bm.text}</span>
							</button>
							<button class="remove-btn" onclick={() => removeBookmark(bm.bookId, bm.chapter, bm.verse)} title="Remover">
								✕
							</button>
						</div>
					{/each}
				{/if}
			{:else}
				{#if $readingHistory.length === 0}
					<div class="empty">
						<span class="empty-icon">📖</span>
						<p>Nenhuma leitura recente.</p>
					</div>
				{:else}
					{#each $readingHistory as entry}
						<button class="item-body history-item" onclick={() => goTo(entry.bookId, entry.chapter)}>
							<span class="item-ref">{entry.bookName} {entry.chapter}</span>
							<span class="item-time">{formatDate(entry.visitedAt)}</span>
						</button>
					{/each}
				{/if}
			{:else if tab === 'stats'}
				<div class="stats-grid">
					<div class="stat-card">
						<span class="stat-value">{stats.streak}</span>
						<span class="stat-label">{stats.streak === 1 ? 'dia' : 'dias'} seguidos</span>
					</div>
					<div class="stat-card">
						<span class="stat-value">{stats.chaptersRead}</span>
						<span class="stat-label">capitulos lidos</span>
					</div>
					<div class="stat-card">
						<span class="stat-value">{stats.totalDays}</span>
						<span class="stat-label">dias de leitura</span>
					</div>
					<div class="stat-card">
						<span class="stat-value">{$highlights.length}</span>
						<span class="stat-label">versiculos marcados</span>
					</div>
					<div class="stat-card">
						<span class="stat-value">{$annotations.length}</span>
						<span class="stat-label">anotacoes</span>
					</div>
					<div class="stat-card">
						<span class="stat-value">{$bookmarks.length}</span>
						<span class="stat-label">favoritos</span>
					</div>
				</div>

				{#if stats.readDates.length > 0}
					<div class="streak-calendar">
						<span class="stats-section-title">Ultimos 30 dias</span>
						<div class="calendar-grid">
							{#each Array.from({ length: 30 }, (_, i) => {
								const d = new Date(Date.now() - (29 - i) * 86400000);
								return d.toISOString().slice(0, 10);
							}) as day}
								<div
									class="calendar-dot"
									class:active={stats.readDates.includes(day)}
									title={day}
								></div>
							{/each}
						</div>
					</div>
				{/if}
			{/if}
		</div>
	</div>
</div>

<style>
	.panel-backdrop {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(2px);
		z-index: 900;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding-top: min(15vh, 100px);
		animation: fadeIn 0.1s ease-out;
	}

	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	.panel {
		width: 440px;
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

	.panel-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 4px 12px 0;
		border-bottom: 1px solid var(--border);
	}

	.tabs {
		display: flex;
		gap: 0;
	}

	.tab {
		padding: 10px 16px;
		background: none;
		border: none;
		border-bottom: 2px solid transparent;
		color: var(--text-dim);
		font-size: 0.8rem;
		font-family: var(--font-sans);
		cursor: pointer;
		transition: all 0.15s;
	}

	.tab.active {
		color: var(--accent);
		border-bottom-color: var(--accent);
	}

	.tab:hover:not(.active) {
		color: var(--text-muted);
	}

	.close {
		background: none;
		border: none;
		color: var(--text-dim);
		cursor: pointer;
		padding: 4px 8px;
		border-radius: 4px;
		font-size: 0.9rem;
	}

	.close:hover {
		background: var(--bg-hover);
		color: var(--text);
	}

	.panel-body {
		flex: 1;
		overflow-y: auto;
		padding: 4px 0;
	}

	.item {
		display: flex;
		align-items: center;
	}

	.item-body {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 2px;
		padding: 10px 16px;
		background: none;
		border: none;
		text-align: left;
		cursor: pointer;
		color: var(--text);
		font-family: var(--font-sans);
		transition: background 0.1s;
		min-width: 0;
	}

	.item-body:hover {
		background: var(--bg-surface-2);
	}

	.history-item {
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		width: 100%;
	}

	.item-ref {
		font-size: 0.82rem;
		font-weight: 500;
		color: var(--accent);
	}

	.item-text {
		font-size: 0.75rem;
		color: var(--text-muted);
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.item-time {
		font-size: 0.7rem;
		color: var(--text-dim);
		flex-shrink: 0;
	}

	.remove-btn {
		background: none;
		border: none;
		color: var(--text-dim);
		cursor: pointer;
		padding: 4px 12px;
		font-size: 0.7rem;
		opacity: 0;
		transition: opacity 0.1s;
	}

	.item:hover .remove-btn {
		opacity: 1;
	}

	.remove-btn:hover {
		color: #dc5050;
	}

	.empty {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
		padding: 40px 16px;
		color: var(--text-dim);
		font-size: 0.82rem;
		text-align: center;
	}

	.empty-icon {
		font-size: 1.5rem;
		opacity: 0.5;
	}

	.hint {
		font-size: 0.72rem;
		color: var(--text-dim);
		opacity: 0.7;
	}

	/* Stats */
	.stats-grid {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 8px;
		padding: 16px;
	}

	.stat-card {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 2px;
		padding: 12px 8px;
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		border-radius: 8px;
	}

	.stat-value {
		font-size: 1.4rem;
		font-weight: 700;
		color: var(--accent);
	}

	.stat-label {
		font-size: 0.62rem;
		color: var(--text-dim);
		text-align: center;
		text-transform: uppercase;
		letter-spacing: 0.03em;
	}

	.streak-calendar {
		padding: 0 16px 16px;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.stats-section-title {
		font-size: 0.65rem;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--text-dim);
		font-weight: 600;
	}

	.calendar-grid {
		display: flex;
		gap: 3px;
		flex-wrap: wrap;
	}

	.calendar-dot {
		width: 12px;
		height: 12px;
		border-radius: 2px;
		background: var(--bg-surface-3);
		transition: background 0.2s;
	}

	.calendar-dot.active {
		background: var(--accent);
	}
</style>
