<script lang="ts">
	import { sidebarOpen, viewMode, fontSize, searchOpen } from '$lib/store';

	let mode = $derived($viewMode);
	let size = $derived($fontSize);

	const modes = [
		{ id: 'side-by-side' as const, label: '⫏ Lado a lado' },
		{ id: 'interleaved' as const, label: '≡ Intercalado' },
		{ id: 'original-only' as const, label: '𐤀 Original' },
		{ id: 'translation-only' as const, label: 'A Tradução' }
	];
</script>

<div class="toolbar">
	<button class="menu-btn" onclick={() => ($sidebarOpen = !$sidebarOpen)}>
		☰
	</button>

	<div class="mode-buttons">
		{#each modes as m}
			<button
				class="mode-btn"
				class:active={mode === m.id}
				onclick={() => ($viewMode = m.id)}
				title={m.label}
			>
				{m.label}
			</button>
		{/each}
	</div>

	<button class="search-btn" onclick={() => ($searchOpen = true)} title="Buscar (Ctrl+K)">
		<span class="search-btn-icon">⌘</span>
		<span class="search-btn-text">Buscar...</span>
		<kbd class="search-kbd">Ctrl K</kbd>
	</button>

	<div class="font-controls">
		<button class="size-btn" onclick={() => ($fontSize = Math.max(12, size - 1))}>A−</button>
		<span class="size-label">{size}</span>
		<button class="size-btn" onclick={() => ($fontSize = Math.min(24, size + 1))}>A+</button>
	</div>
</div>

<style>
	.toolbar {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 8px 16px;
		background: var(--bg-surface);
		border-bottom: 1px solid var(--border);
	}

	.menu-btn {
		background: none;
		border: 1px solid var(--border);
		color: var(--text);
		font-size: 1.1rem;
		cursor: pointer;
		padding: 4px 10px;
		border-radius: 6px;
		line-height: 1;
	}

	.menu-btn:hover {
		background: var(--bg-hover);
	}

	.mode-buttons {
		display: flex;
		gap: 2px;
		background: var(--bg-surface-2);
		border-radius: 6px;
		padding: 2px;
		overflow-x: auto;
	}

	.mode-btn {
		background: none;
		border: none;
		color: var(--text-muted);
		padding: 5px 10px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.72rem;
		white-space: nowrap;
		font-family: var(--font-sans);
		transition: all 0.15s;
	}

	.mode-btn.active {
		background: var(--bg-surface-3);
		color: var(--accent);
		font-weight: 600;
	}

	.mode-btn:hover:not(.active) {
		color: var(--text);
	}

	.font-controls {
		display: flex;
		align-items: center;
		gap: 4px;
		margin-left: auto;
	}

	.size-btn {
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		color: var(--text-muted);
		padding: 3px 8px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.75rem;
		font-family: var(--font-sans);
	}

	.size-btn:hover {
		color: var(--text);
		border-color: var(--border-light);
	}

	.size-label {
		font-size: 0.7rem;
		color: var(--text-dim);
		min-width: 20px;
		text-align: center;
	}

	.search-btn {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 5px 12px;
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		border-radius: 6px;
		color: var(--text-dim);
		cursor: pointer;
		font-family: var(--font-sans);
		font-size: 0.78rem;
		transition: all 0.15s;
		margin-left: 8px;
	}

	.search-btn:hover {
		border-color: var(--border-light);
		color: var(--text-muted);
		background: var(--bg-surface-3);
	}

	.search-btn-icon {
		font-size: 0.7rem;
	}

	.search-btn-text {
		color: var(--text-dim);
	}

	.search-kbd {
		font-size: 0.55rem;
		background: var(--bg-surface-3);
		border: 1px solid var(--border);
		padding: 1px 4px;
		border-radius: 3px;
		font-family: var(--font-sans);
		color: var(--text-dim);
		margin-left: 4px;
	}

	@media (max-width: 600px) {
		.mode-btn {
			padding: 5px 7px;
			font-size: 0.65rem;
		}

		.font-controls {
			display: none;
		}

		.search-btn-text,
		.search-kbd {
			display: none;
		}

		.search-btn {
			padding: 5px 8px;
			margin-left: auto;
		}
	}
</style>
