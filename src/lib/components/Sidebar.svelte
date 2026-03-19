<script lang="ts">
	import { bibleIndex, currentBookMeta, sidebarOpen } from '$lib/store';
	import type { BookMeta } from '$lib/types';

	let index = $derived($bibleIndex);
	let activeBook = $derived($currentBookMeta);
	let isOpen = $derived($sidebarOpen);
	let searchFilter = $state('');

	let filteredBooks = $derived.by(() => {
		if (!index) return [];
		if (!searchFilter) return index.books;
		const q = searchFilter.toLowerCase();
		return index.books.filter(
			(b) => b.name.toLowerCase().includes(q) || b.nameOrig.toLowerCase().includes(q)
		);
	});

	interface GroupedSection {
		id: string;
		name: string;
		testament: string;
		books: BookMeta[];
	}

	let groupedSections = $derived.by(() => {
		if (!index) return [];
		const sections: GroupedSection[] = [];
		let currentSection: GroupedSection | null = null;
		for (const book of filteredBooks) {
			if (!currentSection || currentSection.id !== book.section) {
				currentSection = {
					id: book.section,
					name: book.sectionName,
					testament: book.testament,
					books: []
				};
				sections.push(currentSection);
			}
			currentSection.books.push(book);
		}
		return sections;
	});

	function selectBook(book: BookMeta) {
		window.location.hash = `#/${book.id}/1`;
		if (window.innerWidth < 768) {
			$sidebarOpen = false;
		}
	}
</script>

<aside class="sidebar" class:open={isOpen}>
	<div class="sidebar-header">
		<h1 class="logo">
			<span class="logo-symbol">✦</span>
			<span>Bíblia</span>
		</h1>
		<button class="close-btn" onclick={() => ($sidebarOpen = false)}>✕</button>
	</div>

	<div class="search-box">
		<input type="text" placeholder="Buscar livro..." bind:value={searchFilter} />
	</div>

	<nav class="book-list">
		{#each groupedSections as section}
			{#if section.books.length > 0}
				<div class="section">
					<div class="section-header">
						<span class="testament-badge" class:nt={section.testament === 'NT'}>
							{section.testament}
						</span>
						<span class="section-name">{section.name}</span>
					</div>
					{#each section.books as book}
						<button
							class="book-item"
							class:active={activeBook?.id === book.id}
							onclick={() => selectBook(book)}
						>
							<span class="book-name">{book.name}</span>
							<span class="book-orig">{book.nameOrig}</span>
							<span class="book-chapters">{book.chapters}</span>
						</button>
					{/each}
				</div>
			{/if}
		{/each}
	</nav>
</aside>

<style>
	.sidebar {
		width: var(--sidebar-width);
		height: 100vh;
		background: var(--bg-surface);
		border-right: 1px solid var(--border);
		display: flex;
		flex-direction: column;
		position: fixed;
		left: 0;
		top: 0;
		z-index: 100;
		transform: translateX(-100%);
		transition: transform 0.25s ease;
	}

	.sidebar.open {
		transform: translateX(0);
	}

	.sidebar-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 16px 20px;
		border-bottom: 1px solid var(--border);
	}

	.logo {
		font-size: 1.2rem;
		font-weight: 600;
		color: var(--accent);
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.logo-symbol {
		font-size: 0.9rem;
	}

	.close-btn {
		background: none;
		border: none;
		color: var(--text-muted);
		font-size: 1.1rem;
		cursor: pointer;
		padding: 4px 8px;
		border-radius: 4px;
	}

	.close-btn:hover {
		background: var(--bg-hover);
		color: var(--text);
	}

	.search-box {
		padding: 12px 16px;
		border-bottom: 1px solid var(--border);
	}

	.search-box input {
		width: 100%;
		padding: 8px 12px;
		background: var(--bg-surface-2);
		border: 1px solid var(--border);
		border-radius: 6px;
		color: var(--text);
		font-size: 0.85rem;
		outline: none;
		font-family: var(--font-sans);
	}

	.search-box input:focus {
		border-color: var(--accent-dim);
	}

	.search-box input::placeholder {
		color: var(--text-dim);
	}

	.book-list {
		flex: 1;
		overflow-y: auto;
		padding: 8px 0;
	}

	.section {
		margin-bottom: 4px;
	}

	.section-header {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 16px 4px;
		font-size: 0.7rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--text-dim);
		font-weight: 600;
	}

	.testament-badge {
		font-size: 0.6rem;
		padding: 1px 5px;
		border-radius: 3px;
		background: var(--accent-dim);
		color: var(--text);
		font-weight: 700;
	}

	.testament-badge.nt {
		background: #2d5a3d;
	}

	.book-item {
		display: grid;
		grid-template-columns: 1fr auto;
		grid-template-rows: auto auto;
		gap: 0 8px;
		width: 100%;
		padding: 6px 16px 6px 24px;
		background: none;
		border: none;
		color: var(--text);
		cursor: pointer;
		text-align: left;
		font-family: var(--font-sans);
		transition: background 0.15s;
	}

	.book-item:hover {
		background: var(--bg-hover);
	}

	.book-item.active {
		background: var(--bg-surface-3);
		border-left: 2px solid var(--accent);
		padding-left: 22px;
	}

	.book-name {
		font-size: 0.85rem;
		font-weight: 500;
		grid-column: 1;
		grid-row: 1;
	}

	.book-orig {
		font-size: 0.7rem;
		color: var(--text-dim);
		grid-column: 1;
		grid-row: 2;
	}

	.book-chapters {
		font-size: 0.7rem;
		color: var(--text-dim);
		grid-column: 2;
		grid-row: 1 / 3;
		align-self: center;
	}

	@media (min-width: 768px) {
		.sidebar.open {
			transform: translateX(0);
		}

		.close-btn {
			display: none;
		}
	}

	@media (max-width: 767px) {
		.sidebar {
			width: 85vw;
			max-width: 340px;
		}
	}
</style>
