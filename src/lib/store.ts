import { writable, get } from 'svelte/store';
import type { BibleIndex, BookData, BookMeta, TranslationId } from './types';

// --- Helpers for localStorage persistence ---
function persisted<T>(key: string, initial: T) {
	let stored: T = initial;
	if (typeof localStorage !== 'undefined') {
		try {
			const raw = localStorage.getItem(key);
			if (raw !== null) stored = JSON.parse(raw);
		} catch { /* ignore */ }
	}
	const store = writable<T>(stored);
	store.subscribe(value => {
		if (typeof localStorage !== 'undefined') {
			try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* ignore */ }
		}
	});
	return store;
}

// --- Core state ---
export const bibleIndex = writable<BibleIndex | null>(null);
export const currentBook = writable<BookData | null>(null);
export const currentChapter = writable<number>(1);
export const currentBookMeta = writable<BookMeta | null>(null);

// --- Persisted preferences ---
export const sidebarOpen = persisted<boolean>('bible:sidebar', true);
export const translation = persisted<TranslationId>('bible:translation', 'acf');
export const viewMode = persisted<'side-by-side' | 'interleaved' | 'original-only' | 'translation-only'>('bible:viewMode', 'side-by-side');
export const fontSize = persisted<number>('bible:fontSize', 16);
export const theme = persisted<'dark' | 'light' | 'sepia'>('bible:theme', 'dark');
export const fontFamily = persisted<'serif' | 'sans' | 'mono'>('bible:fontFamily', 'serif');
export const lineHeight = persisted<number>('bible:lineHeight', 1.8);

// --- Search ---
export const searchQuery = writable<string>('');
export const searchOpen = writable<boolean>(false);
// When navigating from search, store the query so VerseReader can highlight it
export const activeSearchHighlight = writable<string>('');

// --- Last position (to restore on reload) ---
export const lastPosition = persisted<{ bookId: string; chapter: number } | null>('bible:lastPosition', null);

// --- Bookmarks ---
export interface Bookmark {
	bookId: string;
	bookName: string;
	chapter: number;
	verse: number;
	text: string;
	createdAt: number;
}
export const bookmarks = persisted<Bookmark[]>('bible:bookmarks', []);

export function addBookmark(bm: Omit<Bookmark, 'createdAt'>) {
	const current = get(bookmarks);
	const exists = current.some(b => b.bookId === bm.bookId && b.chapter === bm.chapter && b.verse === bm.verse);
	if (!exists) {
		bookmarks.set([{ ...bm, createdAt: Date.now() }, ...current].slice(0, 200));
	}
}

export function removeBookmark(bookId: string, chapter: number, verse: number) {
	bookmarks.update(list => list.filter(b => !(b.bookId === bookId && b.chapter === chapter && b.verse === verse)));
}

export function isBookmarked(bookId: string, chapter: number, verse: number): boolean {
	return get(bookmarks).some(b => b.bookId === bookId && b.chapter === chapter && b.verse === verse);
}

// --- Highlights (colored markers per verse) ---
export type HighlightColor = 'yellow' | 'green' | 'blue' | 'pink' | 'purple';
export interface VerseHighlight {
	bookId: string;
	chapter: number;
	verse: number;
	color: HighlightColor;
}
export const highlights = persisted<VerseHighlight[]>('bible:highlights', []);

export function setHighlight(bookId: string, chapter: number, verse: number, color: HighlightColor) {
	highlights.update(list => {
		const filtered = list.filter(h => !(h.bookId === bookId && h.chapter === chapter && h.verse === verse));
		return [...filtered, { bookId, chapter, verse, color }];
	});
}

export function removeHighlight(bookId: string, chapter: number, verse: number) {
	highlights.update(list => list.filter(h => !(h.bookId === bookId && h.chapter === chapter && h.verse === verse)));
}

export function getHighlight(bookId: string, chapter: number, verse: number): HighlightColor | null {
	const list = get(highlights);
	const found = list.find(h => h.bookId === bookId && h.chapter === chapter && h.verse === verse);
	return found?.color ?? null;
}

// --- Annotations (personal notes per verse) ---
export interface Annotation {
	bookId: string;
	chapter: number;
	verse: number;
	text: string;
	updatedAt: number;
}
export const annotations = persisted<Annotation[]>('bible:annotations', []);

export function setAnnotation(bookId: string, chapter: number, verse: number, text: string) {
	annotations.update(list => {
		const filtered = list.filter(a => !(a.bookId === bookId && a.chapter === chapter && a.verse === verse));
		if (text.trim()) {
			return [...filtered, { bookId, chapter, verse, text, updatedAt: Date.now() }];
		}
		return filtered; // empty text = delete
	});
}

export function getAnnotation(bookId: string, chapter: number, verse: number): string {
	return get(annotations).find(a => a.bookId === bookId && a.chapter === chapter && a.verse === verse)?.text ?? '';
}

// --- Reading history ---
export interface HistoryEntry {
	bookId: string;
	bookName: string;
	chapter: number;
	visitedAt: number;
}
export const readingHistory = persisted<HistoryEntry[]>('bible:history', []);

export function addToHistory(entry: Omit<HistoryEntry, 'visitedAt'>) {
	const current = get(readingHistory);
	const filtered = current.filter(h => !(h.bookId === entry.bookId && h.chapter === entry.chapter));
	readingHistory.set([{ ...entry, visitedAt: Date.now() }, ...filtered].slice(0, 50));
}

// --- Reading stats ---
export interface ReadingStats {
	streak: number;
	lastReadDate: string; // YYYY-MM-DD
	chaptersRead: number;
	totalDays: number;
	readDates: string[]; // last 365 days
}
export const readingStats = persisted<ReadingStats>('bible:stats', {
	streak: 0,
	lastReadDate: '',
	chaptersRead: 0,
	totalDays: 0,
	readDates: []
});

export function trackReading() {
	const today = new Date().toISOString().slice(0, 10);
	const stats = get(readingStats);

	if (stats.lastReadDate === today) {
		// Already tracked today, just increment chapters
		readingStats.update(s => ({ ...s, chaptersRead: s.chaptersRead + 1 }));
		return;
	}

	const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
	const newStreak = stats.lastReadDate === yesterday ? stats.streak + 1 : 1;
	const dates = [...stats.readDates.filter(d => {
		const diff = Date.now() - new Date(d).getTime();
		return diff < 365 * 86400000;
	}), today];

	readingStats.set({
		streak: newStreak,
		lastReadDate: today,
		chaptersRead: stats.chaptersRead + 1,
		totalDays: stats.totalDays + 1,
		readDates: dates
	});
}

// --- Focus mode ---
export const focusedVerse = writable<number | null>(null);

// --- Word study ---
export const wordStudyQuery = writable<string>('');
export const wordStudyOpen = writable<boolean>(false);

// --- Fullscreen ---
export const fullscreen = writable<boolean>(false);
