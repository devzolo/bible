<script lang="ts">
	import { sidebarOpen, viewMode, fontSize } from '$lib/store';

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

	@media (max-width: 600px) {
		.mode-btn {
			padding: 5px 7px;
			font-size: 0.65rem;
		}

		.font-controls {
			display: none;
		}
	}
</style>
