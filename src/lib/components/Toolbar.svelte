<script lang="ts">
	import { onMount } from 'svelte';
	import { sidebarOpen, viewMode, fontSize, searchOpen, theme, fullscreen, fontFamily, lineHeight, translation } from '$lib/store';
	import { TRANSLATIONS } from '$lib/types';

	let { ontogglebookmarks }: { ontogglebookmarks?: () => void } = $props();

	let mode = $derived($viewMode);
	let size = $derived($fontSize);
	let currentTheme = $derived($theme);
	let isFullscreen = $derived($fullscreen);
	let toolbarEl: HTMLElement | undefined = $state();

	const modes = [
		{ id: 'side-by-side' as const, label: 'Lado a lado', icon: '⫏' },
		{ id: 'interleaved' as const, label: 'Intercalado', icon: '≡' },
		{ id: 'original-only' as const, label: 'Original', icon: '𐤀' },
		{ id: 'translation-only' as const, label: 'Traducao', icon: 'A' }
	];

	const themes = [
		{ id: 'dark' as const, label: 'Escuro', icon: '🌙' },
		{ id: 'light' as const, label: 'Claro', icon: '☀' },
		{ id: 'sepia' as const, label: 'Sepia', icon: '📜' }
	];

	const fonts = [
		{ id: 'serif' as const, label: 'Serif' },
		{ id: 'sans' as const, label: 'Sans' },
		{ id: 'mono' as const, label: 'Mono' }
	];

	let showSettings = $state(false);

	onMount(() => {
		function handleClickOutside(e: MouseEvent) {
			if (showSettings && toolbarEl && !toolbarEl.contains(e.target as Node)) {
				showSettings = false;
			}
		}
		document.addEventListener('click', handleClickOutside);
		return () => document.removeEventListener('click', handleClickOutside);
	});
</script>

<div class="toolbar" bind:this={toolbarEl}>
	<button class="menu-btn" onclick={() => ($sidebarOpen = !$sidebarOpen)} title="Sidebar (S)">
		☰
	</button>

	<div class="translation-selector">
		{#each TRANSLATIONS as t}
			<button
				class="trans-btn"
				class:active={$translation === t.id}
				onclick={() => ($translation = t.id)}
				title={t.name + ' — ' + t.description}
			>
				{t.shortName}
			</button>
		{/each}
	</div>

	<div class="mode-buttons">
		{#each modes as m}
			<button
				class="mode-btn"
				class:active={mode === m.id}
				onclick={() => ($viewMode = m.id)}
				title={m.label}
			>
				<span class="mode-icon">{m.icon}</span>
				<span class="mode-label">{m.label}</span>
			</button>
		{/each}
	</div>

	<button class="search-btn" onclick={() => ($searchOpen = true)} title="Buscar (Ctrl+K)">
		<span class="search-btn-icon">⌘</span>
		<span class="search-btn-text">Buscar...</span>
		<kbd class="search-kbd">Ctrl K</kbd>
	</button>

	<div class="toolbar-actions">
		<button class="icon-btn" onclick={() => ontogglebookmarks?.()} title="Favoritos (B)">
			<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
		</button>

		<button class="icon-btn" onclick={() => ($fullscreen = !isFullscreen)} title="Tela cheia (F)">
			{#if isFullscreen}
				<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"/></svg>
			{:else}
				<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
			{/if}
		</button>

		<button class="icon-btn" onclick={() => showSettings = !showSettings} title="Configuracoes">
			<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
		</button>

		<div class="font-controls">
			<button class="size-btn" onclick={() => ($fontSize = Math.max(12, size - 1))}>A−</button>
			<span class="size-label">{size}</span>
			<button class="size-btn" onclick={() => ($fontSize = Math.min(24, size + 1))}>A+</button>
		</div>
	</div>
</div>

{#if showSettings}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="settings-dropdown" onkeydown={(e) => e.key === 'Escape' && (showSettings = false)}>
		<div class="settings-group">
			<span class="settings-label">Tema</span>
			<div class="settings-row">
				{#each themes as t}
					<button
						class="setting-chip"
						class:active={currentTheme === t.id}
						onclick={() => ($theme = t.id)}
					>
						{t.icon} {t.label}
					</button>
				{/each}
			</div>
		</div>

		<div class="settings-group">
			<span class="settings-label">Fonte</span>
			<div class="settings-row">
				{#each fonts as f}
					<button
						class="setting-chip"
						class:active={$fontFamily === f.id}
						onclick={() => ($fontFamily = f.id)}
					>
						{f.label}
					</button>
				{/each}
			</div>
		</div>

		<div class="settings-group">
			<span class="settings-label">Espacamento</span>
			<div class="settings-row">
				<input
					type="range"
					min="1.4"
					max="2.4"
					step="0.1"
					value={$lineHeight}
					oninput={(e) => ($lineHeight = parseFloat((e.target as HTMLInputElement).value))}
				/>
				<span class="settings-value">{$lineHeight.toFixed(1)}</span>
			</div>
		</div>

		<div class="settings-shortcuts">
			<span class="settings-label">Atalhos</span>
			<div class="shortcut-list">
				<span><kbd>←</kbd><kbd>→</kbd> Capitulos</span>
				<span><kbd>Ctrl</kbd><kbd>K</kbd> Buscar</span>
				<span><kbd>F</kbd> Tela cheia</span>
				<span><kbd>B</kbd> Favoritos</span>
				<span><kbd>S</kbd> Sidebar</span>
				<span><kbd>Swipe</kbd> Capitulos</span>
			</div>
		</div>
	</div>
{/if}

<style>
	.toolbar {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 16px;
		background: var(--bg-surface);
		border-bottom: 1px solid var(--border);
		flex-wrap: nowrap;
		min-height: 44px;
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
		flex-shrink: 0;
	}

	.menu-btn:hover {
		background: var(--bg-hover);
	}

	.translation-selector {
		display: flex;
		gap: 2px;
		background: var(--bg-surface-2);
		border-radius: 6px;
		padding: 2px;
		flex-shrink: 0;
	}

	.trans-btn {
		background: none;
		border: none;
		color: var(--text-muted);
		padding: 5px 10px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.72rem;
		font-weight: 600;
		font-family: var(--font-sans);
		transition: all 0.15s;
		white-space: nowrap;
	}

	.trans-btn.active {
		background: var(--accent);
		color: var(--bg);
	}

	.trans-btn:hover:not(.active) {
		color: var(--text);
		background: var(--bg-surface-3);
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
		display: flex;
		align-items: center;
		gap: 4px;
	}

	.mode-btn.active {
		background: var(--bg-surface-3);
		color: var(--accent);
		font-weight: 600;
	}

	.mode-btn:hover:not(.active) {
		color: var(--text);
	}

	.mode-label {
		display: inline;
	}

	.toolbar-actions {
		display: flex;
		align-items: center;
		gap: 4px;
		margin-left: auto;
	}

	.icon-btn {
		background: none;
		border: 1px solid transparent;
		color: var(--text-muted);
		padding: 6px;
		border-radius: 4px;
		cursor: pointer;
		transition: all 0.15s;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.icon-btn:hover {
		color: var(--text);
		border-color: var(--border-light);
		background: var(--bg-surface-2);
	}

	.font-controls {
		display: flex;
		align-items: center;
		gap: 4px;
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
		flex-shrink: 0;
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

	/* Settings dropdown */
	.settings-dropdown {
		position: absolute;
		top: 44px;
		right: 16px;
		width: 280px;
		background: var(--bg-surface);
		border: 1px solid var(--border-light);
		border-radius: 10px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
		z-index: 200;
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}

	.settings-group {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.settings-label {
		font-size: 0.65rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--text-dim);
		font-weight: 600;
	}

	.settings-row {
		display: flex;
		gap: 4px;
		align-items: center;
	}

	.settings-row input[type="range"] {
		flex: 1;
		accent-color: var(--accent);
		height: 4px;
	}

	.settings-value {
		font-size: 0.7rem;
		color: var(--text-muted);
		min-width: 28px;
		text-align: right;
	}

	.setting-chip {
		flex: 1;
		padding: 5px 8px;
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		border-radius: 5px;
		color: var(--text-muted);
		font-size: 0.72rem;
		font-family: var(--font-sans);
		cursor: pointer;
		transition: all 0.15s;
		text-align: center;
	}

	.setting-chip.active {
		background: var(--bg-surface-3);
		border-color: var(--accent-dim);
		color: var(--accent);
	}

	.setting-chip:hover:not(.active) {
		border-color: var(--border-light);
		color: var(--text);
	}

	.settings-shortcuts {
		display: flex;
		flex-direction: column;
		gap: 6px;
		border-top: 1px solid var(--border);
		padding-top: 12px;
	}

	.shortcut-list {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 4px;
		font-size: 0.68rem;
		color: var(--text-dim);
	}

	.shortcut-list kbd {
		font-size: 0.6rem;
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		padding: 1px 4px;
		border-radius: 2px;
		font-family: var(--font-sans);
		margin-right: 2px;
	}

	@media (max-width: 600px) {
		.mode-label {
			display: none;
		}

		.mode-btn {
			padding: 5px 8px;
		}

		.font-controls,
		.search-btn-text,
		.search-kbd {
			display: none;
		}

		.search-btn {
			padding: 5px 8px;
		}

		.icon-btn:not(:first-child):not(:last-child) {
			display: none;
		}

		.settings-dropdown {
			right: 8px;
			width: calc(100vw - 16px);
		}
	}
</style>
