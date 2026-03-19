import { writable } from 'svelte/store';
import type { BibleIndex, BookData, BookMeta } from './types';

export const bibleIndex = writable<BibleIndex | null>(null);
export const currentBook = writable<BookData | null>(null);
export const currentChapter = writable<number>(1);
export const currentBookMeta = writable<BookMeta | null>(null);
export const sidebarOpen = writable<boolean>(true);
export const viewMode = writable<'side-by-side' | 'interleaved' | 'original-only' | 'translation-only'>('side-by-side');
export const fontSize = writable<number>(16);
export const searchQuery = writable<string>('');
