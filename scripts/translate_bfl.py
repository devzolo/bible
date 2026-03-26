#!/usr/bin/env python3
"""
BFL Translator - Converts ACF Portuguese to simple modern Brazilian Portuguese.
Uses systematic text transformations for dynamic equivalence translation.
"""
import json, re, sys, os

def modernize_text(text):
    t = text

    # Sentence openers
    t = re.sub(r'^E aconteceu que,?\s*', '', t)
    t = re.sub(r'^Aconteceu,?\s*pois,?\s*que,?\s*', '', t)
    t = re.sub(r'^Falou mais o SENHOR', 'O Senhor falou', t)
    t = re.sub(r'^E falou o SENHOR', 'O Senhor falou', t)
    t = re.sub(r'^E falou o Senhor', 'O Senhor falou', t)
    t = re.sub(r'^Falou mais o Senhor', 'O Senhor falou', t)
    t = re.sub(r'^E disse o SENHOR', 'O Senhor disse', t)
    t = re.sub(r'^E disse o Senhor', 'O Senhor disse', t)
    t = re.sub(r'^Disse,?\s*pois,?\s*o Senhor', 'O Senhor disse', t)
    t = re.sub(r'^Disse mais o Senhor', 'O Senhor disse', t)
    t = re.sub(r'^Disse o Senhor', 'O Senhor disse', t)
    t = re.sub(r'^Disse ent[aã]o o Senhor', 'O Senhor disse', t)

    t = t.replace('SENHOR', 'Senhor')

    # Multi-word religious terms (before single-word replacements)
    t = re.sub(r'tenda da congrega[cç][aã]o', 'Tenda do Encontro', t, flags=re.IGNORECASE)
    t = re.sub(r'tabern[aá]culo do testemunho', 'Tenda do Testemunho', t, flags=re.IGNORECASE)
    t = re.sub(r'tenda do testemunho', 'Tenda do Testemunho', t, flags=re.IGNORECASE)
    t = re.sub(r'filhos de Israel', 'israelitas', t)
    t = re.sub(r'Filhos de Israel', 'Israelitas', t)
    t = re.sub(r'sacrif[ií]cios? pac[ií]ficos?', 'oferta de paz', t, flags=re.IGNORECASE)
    t = re.sub(r'ofertas? al[cç]adas?', 'oferta especial', t, flags=re.IGNORECASE)
    t = re.sub(r'ofertas? movidas?', 'oferta apresentada', t, flags=re.IGNORECASE)
    t = re.sub(r'oferta de alimentos', 'oferta de cereais', t, flags=re.IGNORECASE)

    # Single-word vocabulary
    word_map = {
        'congregacao': 'comunidade', 'congregacoes': 'comunidades',
        'arraial': 'acampamento', 'arraiais': 'acampamentos',
        'iniquidade': 'pecado', 'iniquidades': 'pecados',
        'holocausto': 'oferta queimada', 'holocaustos': 'ofertas queimadas',
        'longanimo': 'paciente',
        'misericordia': 'amor',
        'propiciatorio': 'tampa da arca',
    }
    # Use direct replacements with accented forms
    simple_replacements = {
        'congregacao': 'comunidade',
        'congregação': 'comunidade',
        'Congregação': 'Comunidade',
        'arraial': 'acampamento',
        'Arraial': 'Acampamento',
        'arraiais': 'acampamentos',
        'iniquidade': 'pecado',
        'iniquidades': 'pecados',
        'holocausto': 'oferta queimada',
        'Holocausto': 'Oferta queimada',
        'holocaustos': 'ofertas queimadas',
        'expiação': 'perdão',
        'Expiação': 'Perdão',
        'longânimo': 'paciente',
        'misericórdia': 'amor',
        'Misericórdia': 'Amor',
        'propiciatório': 'tampa da arca',
        'imundo': 'impuro',
        'imunda': 'impura',
        'imundos': 'impuros',
        'imundas': 'impuras',
        'imundícia': 'impureza',
        'porquanto': 'porque',
        'Porquanto': 'Porque',
        'outrossim': 'também',
        'libação': 'oferta de bebida',
        'libações': 'ofertas de bebida',
    }
    for old, new in simple_replacements.items():
        t = t.replace(old, new)

    # Pronoun modernization
    t = re.sub(r'\bconvosco\b', 'com vocês', t)
    t = re.sub(r'\bContigo\b', 'Com você', t)
    t = re.sub(r'\bcontigo\b', 'com você', t)
    t = re.sub(r'\bvossa\b', 'sua', t)
    t = re.sub(r'\bVossa\b', 'Sua', t)
    t = re.sub(r'\bvosso\b', 'seu', t)
    t = re.sub(r'\bVosso\b', 'Seu', t)
    t = re.sub(r'\bvossas\b', 'suas', t)
    t = re.sub(r'\bVossas\b', 'Suas', t)
    t = re.sub(r'\bvossos\b', 'seus', t)
    t = re.sub(r'\bVossos\b', 'Seus', t)

    # Archaic verb forms
    verb_map = {
        'oferecereis': 'oferecerão', 'fareis': 'farão', 'tereis': 'terão',
        'dareis': 'darão', 'tomareis': 'tomarão', 'comereis': 'comerão',
        'sereis': 'serão', 'passareis': 'passarão', 'lançareis': 'lançarão',
        'podeis': 'podem', 'tenhais': 'tenham', 'façais': 'façam',
        'sejais': 'sejam', 'estejais': 'estejam', 'temais': 'tenham medo',
        'saibais': 'saibam', 'houverdes': 'tiverem', 'entrardes': 'entrarem',
        'passardes': 'passarem', 'sairdes': 'saírem', 'fizerdes': 'fizerem',
        'vierdes': 'vierem', 'receberdes': 'receberem', 'cumprais': 'cumpram',
        'celebrareis': 'celebrarão', 'habitareis': 'habitarão',
        'herdareis': 'herdarão', 'edificareis': 'construirão',
        'contareis': 'contarão', 'guardareis': 'guardarão',
        'vivereis': 'viverão', 'morrereis': 'morrerão',
        'andareis': 'andarão', 'ouvireis': 'ouvirão',
        'amareis': 'amarão', 'servireis': 'servirão',
        'obedecereis': 'obedecerão', 'seguireis': 'seguirão',
        'temereis': 'temerão', 'adorareis': 'adorarão',
    }
    for old, new in verb_map.items():
        t = re.sub(r'\b' + old + r'\b', new, t)

    # Expressions
    t = re.sub(r'\bEis que\b', 'Vejam:', t)
    t = re.sub(r'\beis que\b', 'então', t)
    t = re.sub(r'\bpelo que\b', 'por isso', t)
    t = re.sub(r'\bPelo que\b', 'Por isso', t)
    t = re.sub(r'\bporventura\b', 'será que', t, flags=re.IGNORECASE)

    # Remove leading "E " connector
    t = re.sub(r'^E,?\s+(?=[A-Z])', '', t)

    # Simplify ", dizendo:" -> ":"
    t = re.sub(r',\s*dizendo:\s*$', ':', t)
    t = re.sub(r',\s*dizendo:', '.', t)

    # primogênito handling
    t = re.sub(r'\bprimogênitos?\b', 'primogênito', t)

    t = re.sub(r'  +', ' ', t)
    t = t.strip()
    if t and t[0].islower():
        t = t[0].upper() + t[1:]
    return t


def translate_book(book_id):
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'data')
    with open(os.path.join(data_dir, f'{book_id}.json'), 'r', encoding='utf-8') as f:
        source = json.load(f)

    chapters = []
    for ch in source['chapters']:
        verses = []
        for v in ch['verses']:
            verses.append({"v": v['v'], "t": modernize_text(v['t'])})
        chapters.append({"c": ch['c'], "verses": verses})

    bfl_dir = os.path.join(data_dir, 'bfl')
    os.makedirs(bfl_dir, exist_ok=True)
    out_path = os.path.join(bfl_dir, f'{book_id}_trans.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(chapters, f, ensure_ascii=False, separators=(',', ':'))

    total = sum(len(c['verses']) for c in chapters)
    print(f"OK: {book_id} - {len(chapters)} chapters, {total} verses -> {out_path}")

    for sc in source['chapters']:
        tc = next((c for c in chapters if c['c'] == sc['c']), None)
        if tc is None:
            print(f"  MISSING chapter {sc['c']}")
        elif len(tc['verses']) != len(sc['verses']):
            print(f"  Ch {sc['c']}: {len(sc['verses'])} vs {len(tc['verses'])} verses")
    return out_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python translate_bfl.py <book_id>")
        sys.exit(1)
    translate_book(sys.argv[1])
