<script lang="ts">
	import { currentBook, currentChapter, viewMode, fontSize } from '$lib/store';
	import type { Chapter } from '$lib/types';

	let book = $derived($currentBook);
	let chapterNum = $derived($currentChapter);
	let mode = $derived($viewMode);
	let size = $derived($fontSize);

	let chapter = $derived.by((): Chapter | null => {
		if (!book) return null;
		return book.chapters[chapterNum - 1] ?? null;
	});

	let isHebrew = $derived(book?.lang === 'hebrew');
	let origDir = $derived(isHebrew ? 'rtl' : 'ltr');
	let origClass = $derived(isHebrew ? 'hebrew' : 'greek');
</script>

{#if chapter}
	<div class="reader" style="--fs: {size}px">
		{#if mode === 'side-by-side'}
			<div class="side-by-side">
				<div class="column original-col">
					<div class="col-header">
						<span class="lang-label {origClass}">
							{isHebrew ? 'עברית — Hebraico' : 'Ἑλληνικά — Grego'}
						</span>
					</div>
					<div class="verses" dir={origDir}>
						{#each chapter.verses as verse}
							<div class="verse" id="v{verse.v}">
								<span class="verse-num">{verse.v}</span>
								<span class="verse-text {origClass}">{verse.o || '—'}</span>
							</div>
						{/each}
					</div>
				</div>

				<div class="divider"></div>

				<div class="column translation-col">
					<div class="col-header">
						<span class="lang-label pt">Português — ACF</span>
					</div>
					<div class="verses">
						{#each chapter.verses as verse}
							<div class="verse" id="vt{verse.v}">
								<span class="verse-num">{verse.v}</span>
								<span class="verse-text pt">{verse.t || '—'}</span>
							</div>
						{/each}
					</div>
				</div>
			</div>
		{:else if mode === 'interleaved'}
			<div class="interleaved">
				{#each chapter.verses as verse}
					<div class="verse-block" id="v{verse.v}">
						<div class="verse-num-block">{verse.v}</div>
						<div class="verse-pair">
							<div class="verse-orig {origClass}" dir={origDir}>
								{verse.o || '—'}
							</div>
							<div class="verse-trans pt">
								{verse.t || '—'}
							</div>
						</div>
					</div>
				{/each}
			</div>
		{:else if mode === 'original-only'}
			<div class="single-view" dir={origDir}>
				{#each chapter.verses as verse}
					<div class="verse" id="v{verse.v}">
						<span class="verse-num">{verse.v}</span>
						<span class="verse-text {origClass}">{verse.o || '—'}</span>
					</div>
				{/each}
			</div>
		{:else}
			<div class="single-view">
				{#each chapter.verses as verse}
					<div class="verse" id="v{verse.v}">
						<span class="verse-num">{verse.v}</span>
						<span class="verse-text pt">{verse.t || '—'}</span>
					</div>
				{/each}
			</div>
		{/if}
	</div>
{:else if book}
	<div class="empty">
		<p>Selecione um capítulo para começar a leitura.</p>
	</div>
{:else}
	<div class="empty">
		<div class="welcome">
			<h2>✦ Bíblia — Original + Português</h2>
			<p>Selecione um livro na barra lateral para começar.</p>
			<div class="welcome-info">
				<div class="info-card">
					<span class="info-icon hebrew">עב</span>
					<span>39 livros em Hebraico</span>
				</div>
				<div class="info-card">
					<span class="info-icon greek">Ελ</span>
					<span>27 livros em Grego</span>
				</div>
				<div class="info-card">
					<span class="info-icon pt">PT</span>
					<span>66 livros traduzidos</span>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.reader {
		padding: 0 20px 60px;
		max-width: 1200px;
		margin: 0 auto;
		font-size: var(--fs);
	}

	/* Side by side */
	.side-by-side {
		display: grid;
		grid-template-columns: 1fr 1px 1fr;
		gap: 0;
		min-height: calc(100vh - 100px);
	}

	.column {
		padding: 0;
	}

	.col-header {
		padding: 12px 16px;
		border-bottom: 1px solid var(--border);
		position: sticky;
		top: 52px;
		background: var(--bg);
		z-index: 5;
	}

	.lang-label {
		font-size: 0.72rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		font-weight: 600;
	}

	.lang-label.hebrew { color: var(--hebrew); }
	.lang-label.greek { color: var(--greek); }
	.lang-label.pt { color: var(--text-muted); }

	.divider {
		background: var(--border);
		min-height: 100%;
	}

	.verses {
		padding: 12px 16px;
	}

	.verse {
		padding: 6px 0;
		line-height: 1.8;
		border-bottom: 1px solid var(--border);
	}

	.verse:last-child {
		border-bottom: none;
	}

	.verse-num {
		color: var(--verse-num);
		font-size: 0.7em;
		font-weight: 700;
		vertical-align: super;
		margin-right: 4px;
		font-family: var(--font-sans);
	}

	.verse-text.hebrew {
		font-family: var(--font-hebrew);
		color: var(--hebrew);
		font-size: 1.1em;
		line-height: 2;
	}

	.verse-text.greek {
		font-family: var(--font-serif);
		color: var(--greek);
		font-size: 1.05em;
	}

	.verse-text.pt {
		font-family: var(--font-serif);
		color: var(--text);
	}

	/* Interleaved */
	.interleaved {
		max-width: 800px;
		margin: 0 auto;
		padding: 20px 0;
	}

	.verse-block {
		display: flex;
		gap: 12px;
		padding: 12px 0;
		border-bottom: 1px solid var(--border);
	}

	.verse-num-block {
		color: var(--verse-num);
		font-size: 0.8rem;
		font-weight: 700;
		min-width: 28px;
		text-align: right;
		padding-top: 4px;
	}

	.verse-pair {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.verse-orig {
		line-height: 1.9;
	}

	.verse-orig.hebrew {
		font-family: var(--font-hebrew);
		color: var(--hebrew);
		font-size: 1.1em;
	}

	.verse-orig.greek {
		font-family: var(--font-serif);
		color: var(--greek);
		font-size: 1.05em;
	}

	.verse-trans.pt {
		font-family: var(--font-serif);
		color: var(--text);
		line-height: 1.7;
		padding-bottom: 2px;
	}

	/* Single view */
	.single-view {
		max-width: 700px;
		margin: 0 auto;
		padding: 20px 0;
	}

	/* Empty / Welcome */
	.empty {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: calc(100vh - 100px);
		color: var(--text-muted);
		text-align: center;
	}

	.welcome h2 {
		color: var(--accent);
		font-size: 1.5rem;
		margin-bottom: 8px;
	}

	.welcome p {
		color: var(--text-muted);
		margin-bottom: 32px;
	}

	.welcome-info {
		display: flex;
		gap: 24px;
		justify-content: center;
		flex-wrap: wrap;
	}

	.info-card {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 12px 16px;
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: 8px;
		font-size: 0.85rem;
	}

	.info-icon {
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 6px;
		font-size: 0.75rem;
		font-weight: 700;
	}

	.info-icon.hebrew {
		background: rgba(212, 197, 160, 0.15);
		color: var(--hebrew);
	}

	.info-icon.greek {
		background: rgba(168, 196, 212, 0.15);
		color: var(--greek);
	}

	.info-icon.pt {
		background: rgba(201, 168, 76, 0.15);
		color: var(--accent);
	}

	@media (max-width: 767px) {
		.side-by-side {
			grid-template-columns: 1fr;
		}

		.divider {
			height: 1px;
			min-height: unset;
		}

		.reader {
			padding: 0 12px 60px;
		}
	}
</style>
