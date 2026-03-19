import type { BibleIndex, BookData } from './types';

const cache = new Map<string, BookData>();

export async function loadIndex(): Promise<BibleIndex> {
	const res = await fetch('/data/index.json');
	return res.json();
}

export async function loadBook(bookId: string): Promise<BookData> {
	if (cache.has(bookId)) {
		return cache.get(bookId)!;
	}
	const res = await fetch(`/data/${bookId}.json`);
	const data = await res.json();
	cache.set(bookId, data);
	return data;
}
