import type { BibleIndex, BookMeta, BookData } from './types';

export interface SearchResultNav {
	type: 'nav';
	bookId: string;
	bookName: string;
	chapter: number;
	verse?: number;
	label: string;
	detail: string;
}

export interface SearchResultBook {
	type: 'book';
	book: BookMeta;
	label: string;
	detail: string;
}

export interface SearchResultVerse {
	type: 'verse';
	bookId: string;
	bookName: string;
	chapter: number;
	verse: number;
	text: string;
	label: string;
	score: number;
}

export interface SearchResultAction {
	type: 'action';
	id: string;
	label: string;
	detail: string;
	icon: string;
}

export type SearchResult = SearchResultNav | SearchResultBook | SearchResultVerse | SearchResultAction;

// Strip accents/diacritics for fuzzy matching
function normalize(str: string): string {
	return str
		.normalize('NFD')
		.replace(/[\u0300-\u036f]/g, '')
		.toLowerCase()
		.trim();
}

// Check if all query words appear in the target (order-independent)
function fuzzyMatch(query: string, target: string): { match: boolean; score: number } {
	const nq = normalize(query);
	const nt = normalize(target);

	// Exact substring match — best score
	if (nt.includes(nq)) {
		const startBonus = nt.startsWith(nq) ? 20 : 0;
		return { match: true, score: 100 + startBonus - nq.length };
	}

	// Word-level match — all query words must appear
	const words = nq.split(/\s+/).filter(Boolean);
	if (words.length === 0) return { match: false, score: 0 };

	let totalScore = 0;
	for (const word of words) {
		const idx = nt.indexOf(word);
		if (idx === -1) return { match: false, score: 0 };
		totalScore += 50 - idx * 0.5;
	}

	return { match: true, score: totalScore / words.length };
}

// Book name aliases for navigation parsing
const bookAliases: Record<string, string> = {
	'gn': 'genesis', 'gen': 'genesis', 'genesis': 'genesis',
	'ex': 'exodo', 'exo': 'exodo', 'exodo': 'exodo',
	'lv': 'levitico', 'lev': 'levitico', 'levitico': 'levitico',
	'nm': 'numeros', 'num': 'numeros', 'numeros': 'numeros',
	'dt': 'deuteronomio', 'deut': 'deuteronomio', 'deuteronomio': 'deuteronomio',
	'js': 'josue', 'jos': 'josue', 'josue': 'josue',
	'jz': 'juizes', 'juizes': 'juizes',
	'rt': 'rute', 'rute': 'rute',
	'1sm': '1samuel', '1sam': '1samuel', '1samuel': '1samuel',
	'2sm': '2samuel', '2sam': '2samuel', '2samuel': '2samuel',
	'1rs': '1reis', '1reis': '1reis',
	'2rs': '2reis', '2reis': '2reis',
	'1cr': '1cronicas', '1cro': '1cronicas', '1cronicas': '1cronicas',
	'2cr': '2cronicas', '2cro': '2cronicas', '2cronicas': '2cronicas',
	'ed': 'esdras', 'esd': 'esdras', 'esdras': 'esdras',
	'ne': 'neemias', 'nee': 'neemias', 'neemias': 'neemias',
	'et': 'ester', 'est': 'ester', 'ester': 'ester',
	'jo': 'jo', 'job': 'jo',
	'sl': 'salmos', 'sal': 'salmos', 'salmos': 'salmos',
	'pv': 'proverbios', 'prov': 'proverbios', 'proverbios': 'proverbios',
	'ec': 'eclesiastes', 'ecl': 'eclesiastes', 'eclesiastes': 'eclesiastes',
	'ct': 'canticos', 'cant': 'canticos', 'canticos': 'canticos',
	'is': 'isaias', 'isa': 'isaias', 'isaias': 'isaias',
	'jr': 'jeremias', 'jer': 'jeremias', 'jeremias': 'jeremias',
	'lm': 'lamentacoes', 'lam': 'lamentacoes', 'lamentacoes': 'lamentacoes',
	'ez': 'ezequiel', 'eze': 'ezequiel', 'ezequiel': 'ezequiel',
	'dn': 'daniel', 'dan': 'daniel', 'daniel': 'daniel',
	'os': 'oseias', 'ose': 'oseias', 'oseias': 'oseias',
	'jl': 'joel', 'joel': 'joel',
	'am': 'amos', 'amos': 'amos',
	'ob': 'obadias', 'oba': 'obadias', 'obadias': 'obadias',
	'jn': 'jonas', 'jonas': 'jonas',
	'mq': 'miqueias', 'miq': 'miqueias', 'miqueias': 'miqueias',
	'na': 'naum', 'naum': 'naum',
	'hc': 'habacuque', 'hab': 'habacuque', 'habacuque': 'habacuque',
	'sf': 'sofonias', 'sof': 'sofonias', 'sofonias': 'sofonias',
	'ag': 'ageu', 'ageu': 'ageu',
	'zc': 'zacarias', 'zac': 'zacarias', 'zacarias': 'zacarias',
	'ml': 'malaquias', 'mal': 'malaquias', 'malaquias': 'malaquias',
	'mt': 'mateus', 'mat': 'mateus', 'mateus': 'mateus',
	'mc': 'marcos', 'mar': 'marcos', 'marcos': 'marcos',
	'lc': 'lucas', 'luc': 'lucas', 'lucas': 'lucas',
	'joao': 'joao', 'joa': 'joao',
	'at': 'atos', 'atos': 'atos',
	'rm': 'romanos', 'rom': 'romanos', 'romanos': 'romanos',
	'1co': '1corintios', '1cor': '1corintios', '1corintios': '1corintios',
	'2co': '2corintios', '2cor': '2corintios', '2corintios': '2corintios',
	'gl': 'galatas', 'gal': 'galatas', 'galatas': 'galatas',
	'ef': 'efesios', 'efe': 'efesios', 'efesios': 'efesios',
	'fp': 'filipenses', 'fil': 'filipenses', 'filipenses': 'filipenses',
	'cl': 'colossenses', 'col': 'colossenses', 'colossenses': 'colossenses',
	'1ts': '1tessalonicenses', '1tes': '1tessalonicenses', '1tessalonicenses': '1tessalonicenses',
	'2ts': '2tessalonicenses', '2tes': '2tessalonicenses', '2tessalonicenses': '2tessalonicenses',
	'1tm': '1timoteo', '1tim': '1timoteo', '1timoteo': '1timoteo',
	'2tm': '2timoteo', '2tim': '2timoteo', '2timoteo': '2timoteo',
	'tt': 'tito', 'tito': 'tito',
	'fm': 'filemom', 'filemom': 'filemom',
	'hb': 'hebreus', 'heb': 'hebreus', 'hebreus': 'hebreus',
	'tg': 'tiago', 'tia': 'tiago', 'tiago': 'tiago',
	'1pe': '1pedro', '1ped': '1pedro', '1pedro': '1pedro',
	'2pe': '2pedro', '2ped': '2pedro', '2pedro': '2pedro',
	'1jo': '1joao', '1joa': '1joao', '1joao': '1joao',
	'2jo': '2joao', '2joa': '2joao', '2joao': '2joao',
	'3jo': '3joao', '3joa': '3joao', '3joao': '3joao',
	'jd': 'judas', 'judas': 'judas',
	'ap': 'apocalipse', 'apo': 'apocalipse', 'apocalipse': 'apocalipse',
};

// Try to parse a direct navigation reference like "Gn 1:3" or "João 3:16"
function parseNavigation(query: string, index: BibleIndex): SearchResultNav | null {
	const q = normalize(query);

	// Pattern: <book> <chapter>:<verse> or <book> <chapter>
	const match = q.match(/^(\d?\s*[a-z]+)\s+(\d+)(?::(\d+))?$/);
	if (!match) return null;

	const bookRef = match[1].replace(/\s+/g, '');
	const chapter = parseInt(match[2]);
	const verse = match[3] ? parseInt(match[3]) : undefined;

	const bookId = bookAliases[bookRef];
	if (!bookId) return null;

	const book = index.books.find(b => b.id === bookId);
	if (!book) return null;

	if (chapter < 1 || chapter > book.chapters) return null;

	const verseStr = verse ? `:${verse}` : '';

	return {
		type: 'nav',
		bookId: book.id,
		bookName: book.name,
		chapter,
		verse,
		label: `${book.name} ${chapter}${verseStr}`,
		detail: `Ir para ${book.name} capítulo ${chapter}${verse ? `, versículo ${verse}` : ''}`
	};
}

const actions: SearchResultAction[] = [
	{ type: 'action', id: 'mode-side-by-side', label: 'Lado a lado', detail: 'Modo de visualização', icon: '⫏' },
	{ type: 'action', id: 'mode-interleaved', label: 'Intercalado', detail: 'Modo de visualização', icon: '≡' },
	{ type: 'action', id: 'mode-original-only', label: 'Somente original', detail: 'Modo de visualização', icon: '𐤀' },
	{ type: 'action', id: 'mode-translation-only', label: 'Somente tradução', detail: 'Modo de visualização', icon: 'A' },
	{ type: 'action', id: 'font-increase', label: 'Aumentar fonte', detail: 'Ajustar tamanho', icon: '+' },
	{ type: 'action', id: 'font-decrease', label: 'Diminuir fonte', detail: 'Ajustar tamanho', icon: '−' },
	{ type: 'action', id: 'sidebar-toggle', label: 'Alternar barra lateral', detail: 'Mostrar/ocultar sidebar', icon: '☰' },
];

function searchActions(query: string): SearchResultAction[] {
	if (!query) return actions;
	return actions.filter(a => {
		const { match } = fuzzyMatch(query, a.label);
		return match;
	});
}

function searchBooks(query: string, index: BibleIndex): SearchResultBook[] {
	if (!query) return [];
	const results: { result: SearchResultBook; score: number }[] = [];

	for (const book of index.books) {
		const nameMatch = fuzzyMatch(query, book.name);
		const origMatch = fuzzyMatch(query, book.nameOrig);
		const idMatch = fuzzyMatch(query, book.id);

		const bestScore = Math.max(nameMatch.score, origMatch.score, idMatch.score);
		const isMatch = nameMatch.match || origMatch.match || idMatch.match;

		if (isMatch) {
			results.push({
				result: {
					type: 'book',
					book,
					label: book.name,
					detail: `${book.nameOrig} — ${book.chapters} capítulos — ${book.testament}`
				},
				score: bestScore
			});
		}
	}

	return results
		.sort((a, b) => b.score - a.score)
		.map(r => r.result)
		.slice(0, 10);
}

// Cache for loaded book data used by verse search
const bookCache = new Map<string, BookData>();

export async function loadBookForSearch(bookId: string): Promise<BookData> {
	if (bookCache.has(bookId)) return bookCache.get(bookId)!;
	const res = await fetch(`/data/${bookId}.json`);
	const data = await res.json();
	bookCache.set(bookId, data);
	return data;
}

export async function searchVerses(
	query: string,
	index: BibleIndex,
	signal?: AbortSignal
): Promise<SearchResultVerse[]> {
	if (!query || query.length < 3) return [];

	const results: SearchResultVerse[] = [];
	const maxResults = 30;

	// Load all books progressively
	for (const bookMeta of index.books) {
		if (signal?.aborted) break;
		if (results.length >= maxResults) break;

		let bookData: BookData;
		try {
			bookData = await loadBookForSearch(bookMeta.id);
		} catch {
			continue;
		}

		for (const chapter of bookData.chapters) {
			if (results.length >= maxResults) break;

			for (const verse of chapter.verses) {
				const { match, score } = fuzzyMatch(query, verse.t);
				if (match) {
					results.push({
						type: 'verse',
						bookId: bookMeta.id,
						bookName: bookMeta.name,
						chapter: chapter.c,
						verse: verse.v,
						text: verse.t,
						label: `${bookMeta.name} ${chapter.c}:${verse.v}`,
						score
					});
				}
			}
		}
	}

	return results
		.sort((a, b) => b.score - a.score)
		.slice(0, maxResults);
}

export function search(
	query: string,
	index: BibleIndex
): { nav: SearchResultNav | null; books: SearchResultBook[]; actions: SearchResultAction[] } {
	const nav = parseNavigation(query, index);
	const books = searchBooks(query, index);
	const actionResults = searchActions(query);

	return { nav, books, actions: actionResults };
}

// Highlight matching parts of text
export function highlightMatch(text: string, query: string): { text: string; highlight: boolean }[] {
	if (!query) return [{ text, highlight: false }];

	const nq = normalize(query);
	const nt = normalize(text);
	const words = nq.split(/\s+/).filter(Boolean);
	const segments: { text: string; highlight: boolean }[] = [];

	// Find all match ranges
	const ranges: [number, number][] = [];
	for (const word of words) {
		let searchFrom = 0;
		while (searchFrom < nt.length) {
			const idx = nt.indexOf(word, searchFrom);
			if (idx === -1) break;
			ranges.push([idx, idx + word.length]);
			searchFrom = idx + 1;
		}
	}

	if (ranges.length === 0) return [{ text, highlight: false }];

	// Merge overlapping ranges
	ranges.sort((a, b) => a[0] - b[0]);
	const merged: [number, number][] = [ranges[0]];
	for (let i = 1; i < ranges.length; i++) {
		const last = merged[merged.length - 1];
		if (ranges[i][0] <= last[1]) {
			last[1] = Math.max(last[1], ranges[i][1]);
		} else {
			merged.push(ranges[i]);
		}
	}

	let pos = 0;
	for (const [start, end] of merged) {
		if (pos < start) {
			segments.push({ text: text.slice(pos, start), highlight: false });
		}
		segments.push({ text: text.slice(start, end), highlight: true });
		pos = end;
	}
	if (pos < text.length) {
		segments.push({ text: text.slice(pos), highlight: false });
	}

	return segments;
}
