<script lang="ts">
	import {
		currentBook, currentChapter, currentBookMeta, viewMode, fontSize, fontFamily, lineHeight,
		addBookmark, removeBookmark, bookmarks,
		highlights, setHighlight, removeHighlight, type HighlightColor,
		annotations, setAnnotation,
		focusedVerse,
		activeSearchHighlight,
		wordStudyQuery, wordStudyOpen,
		translation
	} from '$lib/store';
	import type { Chapter } from '$lib/types';
	import { TRANSLATIONS } from '$lib/types';

	let book = $derived($currentBook);
	let chapterNum = $derived($currentChapter);
	let mode = $derived($viewMode);
	let size = $derived($fontSize);
	let font = $derived($fontFamily);
	let lh = $derived($lineHeight);
	let meta = $derived($currentBookMeta);
	let searchHL = $derived($activeSearchHighlight);
	let focused = $derived($focusedVerse);

	let chapter = $derived.by((): Chapter | null => {
		if (!book) return null;
		return book.chapters[chapterNum - 1] ?? null;
	});

	let isHebrew = $derived(book?.lang === 'hebrew');
	let origDir = $derived(isHebrew ? 'rtl' : 'ltr');
	let origClass = $derived(isHebrew ? 'hebrew' : 'greek');

	let fontVar = $derived(
		font === 'sans' ? 'var(--font-sans)' :
		font === 'mono' ? "'Courier New', monospace" :
		'var(--font-serif)'
	);

	// Highlight colors
	const highlightColors: { id: HighlightColor; label: string; color: string }[] = [
		{ id: 'yellow', label: 'Amarelo', color: '#fbbf24' },
		{ id: 'green', label: 'Verde', color: '#34d399' },
		{ id: 'blue', label: 'Azul', color: '#60a5fa' },
		{ id: 'pink', label: 'Rosa', color: '#f472b6' },
		{ id: 'purple', label: 'Roxo', color: '#a78bfa' },
	];

	function getHighlightBg(v: number): string {
		if (!book) return '';
		const h = $highlights.find(h => h.bookId === book!.id && h.chapter === chapterNum && h.verse === v);
		if (!h) return '';
		const map: Record<HighlightColor, string> = {
			yellow: 'rgba(251, 191, 36, 0.15)',
			green: 'rgba(52, 211, 153, 0.12)',
			blue: 'rgba(96, 165, 250, 0.12)',
			pink: 'rgba(244, 114, 182, 0.12)',
			purple: 'rgba(167, 139, 250, 0.12)',
		};
		return map[h.color];
	}

	function getHighlightColor(v: number): HighlightColor | null {
		if (!book) return null;
		return $highlights.find(h => h.bookId === book!.id && h.chapter === chapterNum && h.verse === v)?.color ?? null;
	}

	function getAnnotationText(v: number): string {
		if (!book) return '';
		return $annotations.find(a => a.bookId === book!.id && a.chapter === chapterNum && a.verse === v)?.text ?? '';
	}

	function isVerseBookmarked(v: number): boolean {
		return $bookmarks.some(b => b.bookId === book?.id && b.chapter === chapterNum && b.verse === v);
	}

	function toggleBookmark(v: number, text: string) {
		if (!book || !meta) return;
		if (isVerseBookmarked(v)) {
			removeBookmark(book.id, chapterNum, v);
		} else {
			addBookmark({ bookId: book.id, bookName: meta.name, chapter: chapterNum, verse: v, text: text.slice(0, 120) });
		}
	}

	// Highlight text with search query
	function highlightText(text: string): Array<{ text: string; hl: boolean }> {
		if (!searchHL) return [{ text, hl: false }];
		const q = searchHL.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
		const normalized = text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
		const idx = normalized.indexOf(q);
		if (idx === -1) return [{ text, hl: false }];
		return [
			{ text: text.slice(0, idx), hl: false },
			{ text: text.slice(idx, idx + q.length), hl: true },
			{ text: text.slice(idx + q.length), hl: false }
		].filter(s => s.text);
	}

	// Word study — double click a word
	function handleWordClick(e: MouseEvent) {
		const selection = window.getSelection();
		if (!selection || selection.toString().trim().length < 2) return;
		const word = selection.toString().trim();
		if (word.split(/\s+/).length > 3) return; // max 3 words
		$wordStudyQuery = word;
		$wordStudyOpen = true;
	}

	async function copyVerse(v: number, text: string) {
		if (!meta) return;
		const ref = `${meta.name} ${chapterNum}:${v}`;
		const formatted = `"${text}" — ${ref}`;
		try {
			await navigator.clipboard.writeText(formatted);
			showToast(`Copiado: ${ref}`);
		} catch {
			showToast('Falha ao copiar');
		}
	}

	async function shareVerse(v: number, text: string) {
		if (!meta) return;
		const ref = `${meta.name} ${chapterNum}:${v}`;
		const formatted = `"${text}"\n— ${ref}`;
		if (navigator.share) {
			try { await navigator.share({ title: ref, text: formatted }); } catch { /* cancelled */ }
		} else {
			await copyVerse(v, text);
		}
	}

	let toastMsg = $state('');
	let toastVisible = $state(false);
	function showToast(msg: string) {
		toastMsg = msg;
		toastVisible = true;
		setTimeout(() => toastVisible = false, 2000);
	}

	// Active verse (hover for actions)
	let activeVerse = $state<number | null>(null);

	// Verse interaction panel
	let panelVerse = $state<number | null>(null);
	let panelTab = $state<'highlight' | 'note'>('highlight');
	let noteText = $state('');

	function openPanel(v: number) {
		if (panelVerse === v) {
			panelVerse = null;
			return;
		}
		panelVerse = v;
		panelTab = 'highlight';
		noteText = getAnnotationText(v);
	}

	function saveNote(v: number) {
		if (!book) return;
		setAnnotation(book.id, chapterNum, v, noteText);
		showToast(noteText.trim() ? 'Anotacao salva' : 'Anotacao removida');
	}

	function toggleFocus(v: number) {
		$focusedVerse = focused === v ? null : v;
	}

	function applyHighlight(v: number, color: HighlightColor) {
		if (!book) return;
		const current = getHighlightColor(v);
		if (current === color) {
			removeHighlight(book.id, chapterNum, v);
		} else {
			setHighlight(book.id, chapterNum, v, color);
		}
	}

	// Verse of the day (deterministic based on date)
	let verseOfDay = $derived.by(() => {
		if (!chapter) return null;
		const today = new Date();
		const dayOfYear = Math.floor((today.getTime() - new Date(today.getFullYear(), 0, 0).getTime()) / 86400000);
		return null; // used only in welcome screen
	});
</script>

{#if toastVisible}
	<div class="toast">{toastMsg}</div>
{/if}

{#if chapter}
	<div class="reader" style="--fs: {size}px; --lh: {lh}; --font-reading: {fontVar}" ondblclick={handleWordClick}>
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
							<div
								class="verse"
								id="v{verse.v}"
								class:dimmed={focused !== null && focused !== verse.v}
								style:background={getHighlightBg(verse.v)}
							>
								<button
									class="verse-num"
									class:bookmarked={isVerseBookmarked(verse.v)}
									onclick={() => openPanel(verse.v)}
									title="Marcar / anotar"
								>{verse.v}</button>
								<span class="verse-text {origClass}">{verse.o || '—'}</span>
								{#if panelVerse === verse.v}
									<div class="verse-panel">
										<div class="panel-tabs">
											<button class:active={panelTab === 'highlight'} onclick={() => panelTab = 'highlight'}>Cores</button>
											<button class:active={panelTab === 'note'} onclick={() => panelTab = 'note'}>Nota</button>
											<button class="panel-close" onclick={() => panelVerse = null}>✕</button>
										</div>
										{#if panelTab === 'highlight'}
											<div class="color-picker">
												{#each highlightColors as c}
													<button
														class="color-dot"
														class:active={getHighlightColor(verse.v) === c.id}
														style:background={c.color}
														onclick={() => applyHighlight(verse.v, c.id)}
														title={c.label}
													></button>
												{/each}
												{#if getHighlightColor(verse.v)}
													<button class="color-clear" onclick={() => book && removeHighlight(book.id, chapterNum, verse.v)}>✕</button>
												{/if}
											</div>
										{:else}
											<div class="note-editor">
												<textarea bind:value={noteText} placeholder="Escreva sua anotacao..." rows="3"></textarea>
												<button class="note-save" onclick={() => saveNote(verse.v)}>Salvar</button>
											</div>
										{/if}
									</div>
								{/if}
							</div>
						{/each}
					</div>
				</div>

				<div class="divider"></div>

				<div class="column translation-col">
					<div class="col-header">
						<span class="lang-label pt">Portugues — {TRANSLATIONS.find(t => t.id === $translation)?.shortName ?? 'ACF'}</span>
					</div>
					<div class="verses">
						{#each chapter.verses as verse}
							{@const hlBg = getHighlightBg(verse.v)}
							{@const hasNote = getAnnotationText(verse.v)}
							<div
								class="verse"
								id="vt{verse.v}"
								class:dimmed={focused !== null && focused !== verse.v}
								class:verse-active={activeVerse === verse.v}
								style:background={hlBg}
								onmouseenter={() => activeVerse = verse.v}
								onmouseleave={() => activeVerse = null}
							>
								<button
									class="verse-num"
									class:bookmarked={isVerseBookmarked(verse.v)}
									onclick={() => openPanel(verse.v)}
									title="Marcar / anotar"
								>{verse.v}</button>
								<span class="verse-text pt">
									{#each highlightText(verse.t || '—') as seg}
										{#if seg.hl}<mark class="search-hl">{seg.text}</mark>{:else}{seg.text}{/if}
									{/each}
								</span>
								{#if hasNote}
									<span class="note-indicator" title={hasNote}>📝</span>
								{/if}
								{#if activeVerse === verse.v}
									<span class="verse-actions">
										<button onclick={() => copyVerse(verse.v, verse.t)} title="Copiar">📋</button>
										<button onclick={() => shareVerse(verse.v, verse.t)} title="Compartilhar">↗</button>
										<button onclick={() => toggleBookmark(verse.v, verse.t)} title="Favorito">
											{isVerseBookmarked(verse.v) ? '★' : '☆'}
										</button>
									</span>
								{/if}

								{#if panelVerse === verse.v}
									<div class="verse-panel">
										<div class="panel-tabs">
											<button class:active={panelTab === 'highlight'} onclick={() => panelTab = 'highlight'}>Cores</button>
											<button class:active={panelTab === 'note'} onclick={() => panelTab = 'note'}>Nota</button>
											<button class="panel-close" onclick={() => panelVerse = null}>✕</button>
										</div>
										{#if panelTab === 'highlight'}
											<div class="color-picker">
												{#each highlightColors as c}
													<button
														class="color-dot"
														class:active={getHighlightColor(verse.v) === c.id}
														style:background={c.color}
														onclick={() => applyHighlight(verse.v, c.id)}
														title={c.label}
													></button>
												{/each}
												{#if getHighlightColor(verse.v)}
													<button class="color-clear" onclick={() => book && removeHighlight(book.id, chapterNum, verse.v)}>✕</button>
												{/if}
											</div>
										{:else}
											<div class="note-editor">
												<textarea
													bind:value={noteText}
													placeholder="Escreva sua anotacao..."
													rows="3"
												></textarea>
												<button class="note-save" onclick={() => saveNote(verse.v)}>Salvar</button>
											</div>
										{/if}
									</div>
								{/if}
							</div>
						{/each}
					</div>
				</div>
			</div>
		{:else if mode === 'interleaved'}
			<div class="interleaved">
				{#each chapter.verses as verse}
					{@const hlBg = getHighlightBg(verse.v)}
					{@const hasNote = getAnnotationText(verse.v)}
					<div
						class="verse-block"
						id="v{verse.v}"
						class:dimmed={focused !== null && focused !== verse.v}
						class:verse-active={activeVerse === verse.v}
						style:background={hlBg}
						onmouseenter={() => activeVerse = verse.v}
						onmouseleave={() => activeVerse = null}
					>
						<button
							class="verse-num-block"
							class:bookmarked={isVerseBookmarked(verse.v)}
							onclick={() => openPanel(verse.v)}
							title="Marcar / anotar"
						>{verse.v}</button>
						<div class="verse-pair">
							<div class="verse-orig {origClass}" dir={origDir}>{verse.o || '—'}</div>
							<div class="verse-trans pt">
								{#each highlightText(verse.t || '—') as seg}
									{#if seg.hl}<mark class="search-hl">{seg.text}</mark>{:else}{seg.text}{/if}
								{/each}
							</div>
							{#if hasNote}
								<div class="note-preview">{hasNote}</div>
							{/if}
						</div>
						{#if activeVerse === verse.v}
							<span class="verse-actions">
								<button onclick={() => copyVerse(verse.v, verse.t)} title="Copiar">📋</button>
								<button onclick={() => shareVerse(verse.v, verse.t)} title="Compartilhar">↗</button>
								<button onclick={() => toggleBookmark(verse.v, verse.t)} title="Favorito">
									{isVerseBookmarked(verse.v) ? '★' : '☆'}
								</button>
							</span>
						{/if}

						{#if panelVerse === verse.v}
							<div class="verse-panel">
								<div class="panel-tabs">
									<button class:active={panelTab === 'highlight'} onclick={() => panelTab = 'highlight'}>Cores</button>
									<button class:active={panelTab === 'note'} onclick={() => panelTab = 'note'}>Nota</button>
									<button class="panel-close" onclick={() => panelVerse = null}>✕</button>
								</div>
								{#if panelTab === 'highlight'}
									<div class="color-picker">
										{#each highlightColors as c}
											<button
												class="color-dot"
												class:active={getHighlightColor(verse.v) === c.id}
												style:background={c.color}
												onclick={() => applyHighlight(verse.v, c.id)}
												title={c.label}
											></button>
										{/each}
										{#if getHighlightColor(verse.v)}
											<button class="color-clear" onclick={() => book && removeHighlight(book.id, chapterNum, verse.v)}>✕</button>
										{/if}
									</div>
								{:else}
									<div class="note-editor">
										<textarea bind:value={noteText} placeholder="Escreva sua anotacao..." rows="3"></textarea>
										<button class="note-save" onclick={() => saveNote(verse.v)}>Salvar</button>
									</div>
								{/if}
							</div>
						{/if}
					</div>
				{/each}
			</div>
		{:else if mode === 'original-only'}
			<div class="single-view" dir={origDir}>
				{#each chapter.verses as verse}
					<div
						class="verse"
						id="v{verse.v}"
						class:dimmed={focused !== null && focused !== verse.v}
						style:background={getHighlightBg(verse.v)}
						onmouseenter={() => activeVerse = verse.v}
						onmouseleave={() => activeVerse = null}
					>
						<button
							class="verse-num"
							class:bookmarked={isVerseBookmarked(verse.v)}
							onclick={() => openPanel(verse.v)}
						>{verse.v}</button>
						<span class="verse-text {origClass}">{verse.o || '—'}</span>
						{#if activeVerse === verse.v}
							<span class="verse-actions">
								<button onclick={() => copyVerse(verse.v, verse.t)} title="Copiar">📋</button>
								<button onclick={() => toggleBookmark(verse.v, verse.t)} title="Favorito">
									{isVerseBookmarked(verse.v) ? '★' : '☆'}
								</button>
							</span>
						{/if}
						{#if panelVerse === verse.v}
							<div class="verse-panel">
								<div class="panel-tabs">
									<button class:active={panelTab === 'highlight'} onclick={() => panelTab = 'highlight'}>Cores</button>
									<button class:active={panelTab === 'note'} onclick={() => panelTab = 'note'}>Nota</button>
									<button class="panel-close" onclick={() => panelVerse = null}>✕</button>
								</div>
								{#if panelTab === 'highlight'}
									<div class="color-picker">
										{#each highlightColors as c}
											<button
												class="color-dot"
												class:active={getHighlightColor(verse.v) === c.id}
												style:background={c.color}
												onclick={() => applyHighlight(verse.v, c.id)}
												title={c.label}
											></button>
										{/each}
										{#if getHighlightColor(verse.v)}
											<button class="color-clear" onclick={() => book && removeHighlight(book.id, chapterNum, verse.v)}>✕</button>
										{/if}
									</div>
								{:else}
									<div class="note-editor">
										<textarea bind:value={noteText} placeholder="Escreva sua anotacao..." rows="3"></textarea>
										<button class="note-save" onclick={() => saveNote(verse.v)}>Salvar</button>
									</div>
								{/if}
							</div>
						{/if}
					</div>
				{/each}
			</div>
		{:else}
			<div class="single-view">
				{#each chapter.verses as verse}
					{@const hlBg = getHighlightBg(verse.v)}
					{@const hasNote = getAnnotationText(verse.v)}
					<div
						class="verse"
						id="v{verse.v}"
						class:dimmed={focused !== null && focused !== verse.v}
						class:verse-active={activeVerse === verse.v}
						style:background={hlBg}
						onmouseenter={() => activeVerse = verse.v}
						onmouseleave={() => activeVerse = null}
					>
						<button
							class="verse-num"
							class:bookmarked={isVerseBookmarked(verse.v)}
							onclick={() => openPanel(verse.v)}
						>{verse.v}</button>
						<span class="verse-text pt">
							{#each highlightText(verse.t || '—') as seg}
								{#if seg.hl}<mark class="search-hl">{seg.text}</mark>{:else}{seg.text}{/if}
							{/each}
						</span>
						{#if hasNote}
							<span class="note-indicator" title={hasNote}>📝</span>
						{/if}
						{#if activeVerse === verse.v}
							<span class="verse-actions">
								<button onclick={() => copyVerse(verse.v, verse.t)} title="Copiar">📋</button>
								<button onclick={() => shareVerse(verse.v, verse.t)} title="Compartilhar">↗</button>
								<button onclick={() => toggleBookmark(verse.v, verse.t)} title="Favorito">
									{isVerseBookmarked(verse.v) ? '★' : '☆'}
								</button>
							</span>
						{/if}

						{#if panelVerse === verse.v}
							<div class="verse-panel">
								<div class="panel-tabs">
									<button class:active={panelTab === 'highlight'} onclick={() => panelTab = 'highlight'}>Cores</button>
									<button class:active={panelTab === 'note'} onclick={() => panelTab = 'note'}>Nota</button>
									<button class="panel-close" onclick={() => panelVerse = null}>✕</button>
								</div>
								{#if panelTab === 'highlight'}
									<div class="color-picker">
										{#each highlightColors as c}
											<button
												class="color-dot"
												class:active={getHighlightColor(verse.v) === c.id}
												style:background={c.color}
												onclick={() => applyHighlight(verse.v, c.id)}
												title={c.label}
											></button>
										{/each}
										{#if getHighlightColor(verse.v)}
											<button class="color-clear" onclick={() => book && removeHighlight(book.id, chapterNum, verse.v)}>✕</button>
										{/if}
									</div>
								{:else}
									<div class="note-editor">
										<textarea bind:value={noteText} placeholder="Escreva sua anotacao..." rows="3"></textarea>
										<button class="note-save" onclick={() => saveNote(verse.v)}>Salvar</button>
									</div>
								{/if}
							</div>
						{/if}
					</div>
				{/each}
			</div>
		{/if}
	</div>
{:else if book}
	<div class="empty">
		<p>Selecione um capitulo para comecar a leitura.</p>
	</div>
{:else}
	<div class="empty">
		<div class="welcome">
			<h2>✦ Biblia — Original + Portugues</h2>
			<p>Selecione um livro na barra lateral para comecar.</p>
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
	/* Toast */
	.toast {
		position: fixed;
		bottom: 24px;
		left: 50%;
		transform: translateX(-50%);
		background: var(--bg-surface-3);
		color: var(--text);
		padding: 8px 20px;
		border-radius: 8px;
		font-size: 0.8rem;
		font-family: var(--font-sans);
		z-index: 999;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
		border: 1px solid var(--border-light);
		animation: toastIn 0.2s ease-out;
	}

	@keyframes toastIn {
		from { opacity: 0; transform: translateX(-50%) translateY(8px); }
		to { opacity: 1; transform: translateX(-50%) translateY(0); }
	}

	.reader {
		padding: 0 20px 60px;
		max-width: 1200px;
		margin: 0 auto;
		font-size: var(--fs);
	}

	/* Search highlight */
	:global(.search-hl) {
		background: rgba(251, 191, 36, 0.35);
		color: inherit;
		border-radius: 2px;
		padding: 0 2px;
	}

	/* Focus mode — dim non-focused verses */
	.dimmed {
		opacity: 0.2;
		transition: opacity 0.3s ease;
	}

	/* Note indicator */
	.note-indicator {
		font-size: 0.65rem;
		cursor: help;
		flex-shrink: 0;
		opacity: 0.7;
	}

	.note-preview {
		font-size: 0.72rem;
		color: var(--accent);
		background: rgba(201, 168, 76, 0.08);
		border-left: 2px solid var(--accent-dim);
		padding: 4px 8px;
		margin-top: 4px;
		border-radius: 0 4px 4px 0;
		font-style: italic;
	}

	/* Verse interaction panel */
	.verse-panel {
		width: 100%;
		margin-top: 6px;
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		border-radius: 8px;
		overflow: hidden;
		animation: panelIn 0.15s ease-out;
	}

	@keyframes panelIn {
		from { opacity: 0; transform: translateY(-4px); }
		to { opacity: 1; transform: translateY(0); }
	}

	.panel-tabs {
		display: flex;
		border-bottom: 1px solid var(--border);
	}

	.panel-tabs button {
		flex: 1;
		padding: 6px 12px;
		background: none;
		border: none;
		border-bottom: 2px solid transparent;
		color: var(--text-dim);
		font-size: 0.72rem;
		font-family: var(--font-sans);
		cursor: pointer;
		transition: all 0.15s;
	}

	.panel-tabs button.active {
		color: var(--accent);
		border-bottom-color: var(--accent);
	}

	.panel-tabs .panel-close {
		flex: 0;
		padding: 6px 10px;
		color: var(--text-dim);
	}

	.panel-tabs .panel-close:hover {
		color: var(--text);
	}

	/* Color picker */
	.color-picker {
		display: flex;
		gap: 8px;
		padding: 10px 12px;
		align-items: center;
	}

	.color-dot {
		width: 24px;
		height: 24px;
		border-radius: 50%;
		border: 2px solid transparent;
		cursor: pointer;
		transition: all 0.15s;
	}

	.color-dot:hover {
		transform: scale(1.2);
	}

	.color-dot.active {
		border-color: var(--text);
		box-shadow: 0 0 0 2px var(--bg-surface-2), 0 0 0 4px var(--text-dim);
	}

	.color-clear {
		background: var(--bg-surface-3);
		border: 1px solid var(--border);
		color: var(--text-dim);
		padding: 2px 8px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.7rem;
		margin-left: auto;
	}

	.color-clear:hover {
		color: #dc5050;
	}

	/* Note editor */
	.note-editor {
		padding: 8px;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.note-editor textarea {
		width: 100%;
		background: var(--bg-surface-3);
		border: 1px solid var(--border);
		border-radius: 6px;
		color: var(--text);
		font-family: var(--font-sans);
		font-size: 0.8rem;
		padding: 8px;
		resize: vertical;
		outline: none;
		line-height: 1.5;
	}

	.note-editor textarea:focus {
		border-color: var(--accent-dim);
	}

	.note-editor textarea::placeholder {
		color: var(--text-dim);
	}

	.note-save {
		align-self: flex-end;
		padding: 4px 16px;
		background: var(--accent);
		color: var(--bg);
		border: none;
		border-radius: 4px;
		font-size: 0.72rem;
		font-family: var(--font-sans);
		font-weight: 600;
		cursor: pointer;
	}

	.note-save:hover {
		opacity: 0.9;
	}

	/* Verse actions */
	.verse-actions {
		display: inline-flex;
		gap: 2px;
		margin-left: 8px;
		flex-shrink: 0;
	}

	.verse-actions button {
		background: var(--bg-surface-3);
		border: 1px solid var(--border-light);
		border-radius: 4px;
		padding: 3px 8px;
		cursor: pointer;
		font-size: 0.75rem;
		color: var(--text-muted);
		transition: all 0.1s;
	}

	.verse-actions button:hover {
		background: var(--bg-hover);
		color: var(--text);
		border-color: var(--text-dim);
	}

	.verse-active {
		border-radius: 4px;
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
		top: 0;
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
		padding: 6px 4px;
		line-height: var(--lh);
		border-bottom: 1px solid var(--border);
		position: relative;
		border-radius: 4px;
		transition: opacity 0.3s ease, background 0.2s ease;
	}

	.verse:last-child {
		border-bottom: none;
	}

	.verse-num, .verse-num-block {
		color: var(--verse-num);
		font-size: 0.7em;
		font-weight: 700;
		vertical-align: super;
		margin-right: 4px;
		font-family: var(--font-sans);
		background: none;
		border: none;
		cursor: pointer;
		padding: 1px 3px;
		border-radius: 3px;
		transition: all 0.15s;
	}

	.verse-num:hover, .verse-num-block:hover {
		background: rgba(201, 168, 76, 0.15);
	}

	.verse-num.bookmarked, .verse-num-block.bookmarked {
		background: rgba(201, 168, 76, 0.25);
		color: var(--accent);
	}

	.verse-num-block {
		vertical-align: unset;
		font-size: 0.8rem;
		min-width: 28px;
		text-align: right;
		padding-top: 4px;
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
		font-family: var(--font-reading);
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
		padding: 12px 4px;
		border-bottom: 1px solid var(--border);
		align-items: flex-start;
		position: relative;
		border-radius: 4px;
		transition: opacity 0.3s ease, background 0.2s ease;
		flex-wrap: wrap;
	}

	.verse-pair {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 6px;
		min-width: 0;
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
		font-family: var(--font-reading);
		color: var(--text);
		line-height: var(--lh);
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

	@media print {
		.toast, .verse-actions, .verse-panel, .note-indicator {
			display: none !important;
		}

		.reader {
			max-width: 100%;
			padding: 0;
			font-size: 11pt;
		}

		.verse {
			border-bottom: none;
			padding: 2px 0;
		}

		.col-header {
			position: static;
		}
	}
</style>
