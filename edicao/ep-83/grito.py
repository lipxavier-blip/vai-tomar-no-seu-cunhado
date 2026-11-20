"""Aplica a sincronia do grito que o Felipe montou na linha do tempo (aprovacao/decisoes-grito.json).
Entrada fel_<F>.wav/bru_<F>.wav (F=m por padrão) → fel_g.wav/bru_g.wav. Só mexe na janela [R0, R1]; fora dela, a faixa fica igual.
R0 do Bruno cai num silêncio dele antes do "Eu sou o Bruno Rezende" (o pedaço deslocado começava em 814.5, no meio do "Beleza, claro",
que na página ficava fora da vista); R1 = 829.0, silêncio das duas faixas depois do grito."""
import json, os, numpy as np, soundfile as sf
SR = 44100; F = os.environ.get('F', 'm'); R1 = 829.0; RMP = int(0.005 * SR)
D = json.load(open('aprovacao/decisoes-grito.json'))['clips']
for tr in ('fel', 'bru'):
    x, _ = sf.read(f'{tr}_{F}.wav', dtype='float32'); y = x.copy()
    e = np.load(f'E10_{tr}.npy')
    i0, i1 = 81550, 81750; R0 = (i0 + int(np.argmin(e[i0:i1]))) / 100     # 815.5–817.5: ponto mais baixo
    if all(c['o'] == 0 for c in D[tr]): print(tr, 'sem deslocamento'); sf.write(f'{tr}_g.wav', y, SR, subtype='FLOAT'); continue
    y[int(R0 * SR):int(R1 * SR)] = 0
    for c in D[tr]:
        if c.get('mute'): continue
        a, b, o = max(c['a'], R0), min(c['b'], R1 - c['o']), c['o']        # fonte limitada pra o destino caber em [R0, R1]
        a = max(a, R0 - o) if o < 0 else a
        if b <= a: continue
        seg = x[int(a * SR):int(b * SR)].copy()
        if a > R0 + 0.001: seg[:RMP] *= np.linspace(0, 1, RMP, dtype=np.float32)
        if b < R1 - o - 0.001: seg[-RMP:] *= np.linspace(1, 0, RMP, dtype=np.float32)
        d0 = int((a + o) * SR); y[d0:d0 + len(seg)] += seg
        print(tr, f'{a:.3f}–{b:.3f} → {a+o:.3f} ({o:+.3f})')
    print(tr, f'janela {R0:.2f}–{R1:.2f}')
    sf.write(f'{tr}_g.wav', y, SR, subtype='FLOAT')
print('GRITO_DONE')
