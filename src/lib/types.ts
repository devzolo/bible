export interface Verse {
	v: number;
	o: string; // original (hebrew/greek)
	t: string; // translation (portuguese)
}

export type TranslationId = 'acf' | 'bfl';

export interface TranslationInfo {
	id: TranslationId;
	name: string;
	shortName: string;
	description: string;
}

export const TRANSLATIONS: TranslationInfo[] = [
	{ id: 'acf', name: 'Almeida Corrigida Fiel', shortName: 'ACF', description: 'Tradução formal e clássica' },
	{ id: 'bfl', name: 'Bíblia Fácil de Ler', shortName: 'BFL', description: 'Linguagem simples e acessível' },
];

export interface Chapter {
	c: number;
	verses: Verse[];
}

export interface BookData {
	id: string;
	name: string;
	nameOrig: string;
	lang: 'hebrew' | 'greek';
	testament: 'AT' | 'NT';
	section: string;
	chapters: Chapter[];
}

export interface BookMeta {
	id: string;
	name: string;
	nameOrig: string;
	lang: 'hebrew' | 'greek';
	testament: 'AT' | 'NT';
	section: string;
	sectionName: string;
	chapters: number;
}

export interface Section {
	id: string;
	name: string;
	testament: 'AT' | 'NT';
}

export interface Testament {
	id: 'AT' | 'NT';
	name: string;
}

export interface BibleIndex {
	testaments: Testament[];
	books: BookMeta[];
	sections: Section[];
}
