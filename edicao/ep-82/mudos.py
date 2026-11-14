"""Aplica mudos.json: silencia nas faixas os ruídos fora da fala (fade de 40 ms). Saída: fel_m.wav, bru_m.wav"""
import json, numpy as np, soundfile as sf
SR = 44100; R = json.load(open('mudos.json')); F = int(0.04 * SR)
for tr in ('fel', 'bru'):
    x, _ = sf.read(f'{tr}_d.wav', dtype='float32'); g = np.ones(len(x), np.float32)
    for a, b, lab, acao in R[tr]:
        if acao != 'mudo': continue
        i0, i1 = max(0, int((a - 0.03) * SR)), min(len(x), int((b + 0.03) * SR))
        g[i0:i1] = 0
    # rampas de 40 ms nas bordas de cada trecho mudo
    k = np.ones(F, np.float32) / F
    g = np.minimum(g, np.convolve(g, k, mode='same')) if False else g
    d = np.diff(np.concatenate([[1], g, [1]]))
    for i in np.where(d < 0)[0]: g[max(0, i - F):i] = np.minimum(g[max(0, i - F):i], np.linspace(1, 0, i - max(0, i - F)))
    for i in np.where(d > 0)[0]: g[i:i + F] = np.minimum(g[i:i + F], np.linspace(0, 1, len(g[i:i + F])))
    sf.write(f'{tr}_m.wav', x * g, SR, subtype='FLOAT')
    print(tr, 'mudo em', round((g < 0.5).sum() / SR, 1), 's')
