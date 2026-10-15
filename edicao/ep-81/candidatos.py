"""Candidatos a corte fino por faixa: "éee" (vogal sustentada sem palavra real), gagueira/recomeço (n-grama repetido)
e "é isso" de muleta. Saída: candidatos.json. Corte sempre ajustado ao vale de energia da própria faixa."""
import json, re, unicodedata, numpy as np
def norm(s): return re.sub(r'[^\w]', '', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn'))
FILL = re.compile(r'^(e+h*|a+h*|ha+|hu*m+|uh+|ham|an+|hã+|eh+)$')
FUNC = set('eu de que o a os as essa esse isso ele ela tipo e é no na com pra para se voce um uma do da em mas nao ta ai entao porque quando como'.split())
ENF = set('muito nao sim nunca insuportavel foda merda demais tchau uhum isso'.split())
W = {t: [[a, b, w, norm(w), p] for a, b, w, p in json.load(open(f'words_{t}.json'))] for t in ('fel', 'bru')}
E = {t: np.load(f'E10_{t}.npy') for t in ('fel', 'bru')}
def outros(t, a, b):
    o = 'bru' if t == 'fel' else 'fel'
    return sum(max(0, min(b, y) - max(a, x)) for x, y, *_ in W[o] if y > a and x < b)
def vale(t, s, r=0.15):
    """posição de menor energia em ±r s (onde a emenda não come sílaba)"""
    e = E[t]; i0, i1 = max(0, int((s - r) * 100)), int((s + r) * 100)
    return (i0 + int(np.argmin(e[i0:i1]))) * 0.01 + 0.02
def ctx(t, i, j):
    ws = W[t]; return ' '.join(w[2] for w in ws[max(0, i - 7):i]) + ' ⟦' + ' '.join(w[2] for w in ws[i:j]) + '⟧ ' + ' '.join(w[2] for w in ws[j:j + 7])
C = []
for t in ('fel', 'bru'):
    ws = W[t]
    # 1. éee: vogal sustentada sem palavra real por cima
    for v0, v1, f0, dist, en in json.load(open(f'vogais_{t}.json')):
        ov = [(k, max(0, min(v1, w[1]) - max(v0, w[0]))) for k, w in enumerate(ws) if w[1] > v0 and w[0] < v1]
        reais = [(k, o) for k, o in ov if not FILL.match(ws[k][3])]
        if reais:
            k, o = max(reais, key=lambda z: z[1])
            if o / (v1 - v0) >= 0.35: continue
        prev = max([k for k, w in enumerate(ws) if w[1] <= v0 + 0.05], default=0)
        palavra_e = ws[prev][3] in ('e', 'e') and v0 - ws[prev][1] < 0.1
        c0, c1, tipo = (v0 + 0.15, v1 + 0.02, 'éee encurtado') if palavra_e else (v0 - 0.03, v1 + 0.02, 'éee')
        if c1 - c0 < 0.2: continue
        C.append(dict(faixa=t, tipo=tipo, c0=round(vale(t, c0, 0.05), 2), c1=round(vale(t, c1, 0.05), 2), ctx=ctx(t, prev + 1, prev + 1)))
    # 2. repetição em sequência: corta a primeira ocorrência
    for n in (4, 3, 2, 1):
        for i in range(len(ws) - 2 * n + 1):
            a = [w[3] for w in ws[i:i + n]]; b = [w[3] for w in ws[i + n:i + 2 * n]]
            if a != b or not all(a): continue
            if ws[i + n][0] - ws[i + n - 1][1] > 1.2: continue
            if n == 1 and a[0] not in FUNC: continue
            if any(x in ENF for x in a) and n <= 2: continue
            c0, c1 = vale(t, ws[i][0]), vale(t, ws[i + n][0])
            if any(abs(c['c0'] - c0) < 0.3 and c['faixa'] == t for c in C): continue
            C.append(dict(faixa=t, tipo='repetição', c0=round(c0, 2), c1=round(c1, 2), ctx=ctx(t, i, i + n)))
    # 3. "é isso" de muleta
    for i in range(len(ws) - 1):
        if ws[i][3] == 'e' and ws[i + 1][3] == 'isso':
            C.append(dict(faixa=t, tipo='é isso', c0=round(vale(t, ws[i][0]), 2), c1=round(vale(t, ws[i + 1][1]), 2), ctx=ctx(t, i, i + 2)))
for c in C: c['sobre'] = round(outros(c['faixa'], c['c0'], c['c1']), 2)
C.sort(key=lambda c: c['c0'])
json.dump(C, open('candidatos.json', 'w'), ensure_ascii=False, indent=0)
from collections import Counter
print(Counter((c['faixa'], c['tipo']) for c in C), 'com fala do outro por cima:', sum(c['sobre'] > 0.1 for c in C))
for c in C[:12] + [c for c in C if c['tipo'] in ('repetição', 'é isso')][:25]:
    print(f"{c['faixa']} {int(c['c0']//60)}:{c['c0']%60:05.2f} {c['c1']-c['c0']:.2f}s {c['tipo']:13s} {c['ctx'][:110]}")
