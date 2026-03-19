<script lang="ts">
	import { currentBook, currentChapter, currentBookMeta } from '$lib/store';

	let book = $derived($currentBook);
	let chapter = $derived($currentChapter);
	let meta = $derived($currentBookMeta);
	let totalChapters = $derived(book?.chapters.length ?? 0);

	function goToChapter(c: number) {
		if (book && c >= 1 && c <= totalChapters) {
			window.location.hash = `#/${book.id}/${c}`;
		}
	}

	function prev() {
		goToChapter(chapter - 1);
	}

	function next() {
		goToChapter(chapter + 1);
	}
</script>

{#if book}
	<div class="chapter-nav">
		<button class="nav-btn" onclick={prev} disabled={chapter <= 1}>
			← Anterior
		</button>

		<div class="chapter-info">
			<span class="book-title">{book.name}</span>
			<select
				class="chapter-select"
				value={chapter}
				onchange={(e) => goToChapter(Number((e.target as HTMLSelectElement).value))}
			>
				{#each Array.from({ length: totalChapters }, (_, i) => i + 1) as c}
					<option value={c}>Capítulo {c}</option>
				{/each}
			</select>
		</div>

		<button class="nav-btn" onclick={next} disabled={chapter >= totalChapters}>
			Próximo →
		</button>
	</div>
{/if}

<style>
	.chapter-nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 12px 20px;
		background: var(--bg-surface);
		border-bottom: 1px solid var(--border);
		gap: 12px;
		position: sticky;
		top: 0;
		z-index: 10;
	}

	.nav-btn {
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		color: var(--text-muted);
		padding: 6px 14px;
		border-radius: 6px;
		cursor: pointer;
		font-size: 0.8rem;
		font-family: var(--font-sans);
		white-space: nowrap;
		transition: all 0.15s;
	}

	.nav-btn:hover:not(:disabled) {
		background: var(--bg-hover);
		color: var(--text);
		border-color: var(--border-light);
	}

	.nav-btn:disabled {
		opacity: 0.3;
		cursor: default;
	}

	.chapter-info {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 2px;
		min-width: 0;
	}

	.book-title {
		font-size: 0.85rem;
		font-weight: 600;
		color: var(--accent);
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.chapter-select {
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		color: var(--text);
		padding: 3px 8px;
		border-radius: 4px;
		font-size: 0.75rem;
		font-family: var(--font-sans);
		cursor: pointer;
	}

	@media (max-width: 600px) {
		.nav-btn {
			padding: 6px 10px;
			font-size: 0.75rem;
		}
	}
</style>
