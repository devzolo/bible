import type { BibleIndex, BookData, TranslationId } from './types';

const cache = new Map<string, BookData>();

export async function loadIndex(): Promise<BibleIndex> {
	const res = await fetch('/data/index.json');
	if (!res.ok) throw new Error(`Failed to load index: ${res.status}`);
	return res.json();
}

export async function loadBook(bookId: string, translationId: TranslationId = 'acf'): Promise<BookData> {
	const cacheKey = `${translationId}:${bookId}`;
	if (cache.has(cacheKey)) {
		return cache.get(cacheKey)!;
	}

	// Try translation-specific path first, fallback to root (ACF)
	if (translationId !== 'acf') {
		const res = await fetch(`/data/${translationId}/${bookId}.json`);
		if (res.ok) {
			const data = await res.json();
			cache.set(cacheKey, data);
			return data;
		}
		// Fallback to ACF if translation file doesn't exist yet
	}

	const res = await fetch(`/data/${bookId}.json`);
	if (!res.ok) throw new Error(`Failed to load book ${bookId}: ${res.status}`);
	const data = await res.json();
	cache.set(cacheKey, data);
	return data;
}

// Preload adjacent chapters' books silently
export function preloadAdjacentChapters(
	bookId: string,
	chapter: number,
	totalChapters: number,
	index: BibleIndex,
	translationId: TranslationId = 'acf'
) {
	// Current book is already cached, preload next/prev books if at boundaries
	if (chapter >= totalChapters) {
		const idx = index.books.findIndex(b => b.id === bookId);
		if (idx < index.books.length - 1) {
			loadBook(index.books[idx + 1].id, translationId).catch(() => {});
		}
	}
	if (chapter <= 1) {
		const idx = index.books.findIndex(b => b.id === bookId);
		if (idx > 0) {
			loadBook(index.books[idx - 1].id, translationId).catch(() => {});
		}
	}
}
