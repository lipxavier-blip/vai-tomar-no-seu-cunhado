"""Aceita a emenda só se o que some é o vício: éee → só hesitação; repetição → só a 1ª ocorrência; é isso → só "é isso".
Ignora a 1ª e a última palavra das janelas (a borda de 2,5 s varia). Saída: aceitos.json / rejeitados.json"""
import json, re, unicodedata, difflib
def toks(s): return re.sub(r'[^\w\s]', ' ', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')).split()
FIL = re.compile(r'^(e+[hmn]*|a+[hmn]*|ah+|ha+|hu*m+|uh+|ai+|ham|hum)$')
V = json.load(open('verif.json')); ok, rej = [], []
for c in V:
    a, d, iso = toks(c['antes'])[1:-1], toks(c['depois'])[1:-1], toks(c['iso'])
    alvo = toks(c['ctx'].split('⟦')[1].split('⟧')[0])
    perdeu, ganhou = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=d, autojunk=False).get_opcodes():
        if op in ('delete', 'replace'): perdeu += a[i1:i2]
        if op in ('insert', 'replace'): ganhou += d[j1:j2]
    resto = [p for p in perdeu if not FIL.match(p)]
    if c['tipo'].startswith('éee'):
        bom = all(FIL.match(t) for t in iso) and not resto and not [g for g in ganhou if not FIL.match(g)]
    else:
        sobra = list(resto)
        for w in alvo:
            if w in sobra: sobra.remove(w)
        bom = not sobra and len(resto) >= max(1, len(alvo) - 1) and not [g for g in ganhou if not FIL.match(g)]
        if c['tipo'] == 'repetição': bom = bom and all(w in d for w in alvo)   # a 2ª ocorrência ficou
    c['perdeu'], c['ganhou'] = perdeu, ganhou
    (ok if bom else rej).append(c)
json.dump(ok, open('aceitos.json', 'w'), ensure_ascii=False, indent=0); json.dump(rej, open('rejeitados.json', 'w'), ensure_ascii=False, indent=0)
from collections import Counter
print('aceitos', Counter(c['tipo'] for c in ok), '| rejeitados', Counter(c['tipo'] for c in rej))
for c in ok: print('OK ', c['faixa'], f"{int(c['c0']//60)}:{c['c0']%60:05.2f}", c['tipo'], '| perdeu', c['perdeu'], '|', c['depois'][:70])
