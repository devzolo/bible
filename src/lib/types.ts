export interface Verse {
	v: number;
	o: string; // original (hebrew/greek)
	t: string; // translation (portuguese)
}

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
