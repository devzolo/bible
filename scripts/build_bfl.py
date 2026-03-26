"""
Utility script to build BFL translation files.
Usage: python build_bfl.py <book_id> <translations_json_file>

The translations JSON file should contain an array of chapters:
[
  {
    "c": 1,
    "verses": [{"v": 1, "t": "translated text"}, ...]
  },
  ...
]

This script merges the translations with the original text (hebrew/greek)
from the ACF source file and writes the BFL output.
"""
import json
import sys
import os

def build_bfl(book_id, translations_file):
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'data')

    # Read source (ACF)
    source_path = os.path.join(data_dir, f'{book_id}.json')
    with open(source_path, 'r', encoding='utf-8') as f:
        source = json.load(f)

    # Read translations
    with open(translations_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    # Build translation map: {chapter_num: {verse_num: text}}
    trans_map = {}
    for ch in translations:
        c = ch['c']
        trans_map[c] = {v['v']: v['t'] for v in ch['verses']}

    # Merge: keep original 'o' field, replace 't' with BFL
    new_chapters = []
    for ch in source['chapters']:
        c_num = ch['c']
        new_verses = []
        for v in ch['verses']:
            t = v['t']  # default: keep ACF
            if c_num in trans_map and v['v'] in trans_map[c_num]:
                t = trans_map[c_num][v['v']]
            new_verses.append({"v": v['v'], "o": v['o'], "t": t})
        new_chapters.append({"c": c_num, "verses": new_verses})

    result = {
        "id": source['id'],
        "name": source['name'],
        "nameOrig": source['nameOrig'],
        "lang": source['lang'],
        "testament": source['testament'],
        "section": source['section'],
        "chapters": new_chapters
    }

    # Write BFL output
    bfl_dir = os.path.join(data_dir, 'bfl')
    os.makedirs(bfl_dir, exist_ok=True)
    out_path = os.path.join(bfl_dir, f'{book_id}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

    translated = len(trans_map)
    total = len(source['chapters'])
    print(f"OK: {book_id} - {translated}/{total} chapters translated, saved to bfl/{book_id}.json")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <book_id> <translations_json>")
        sys.exit(1)
    build_bfl(sys.argv[1], sys.argv[2])
