"""Filtra candidatos.json e transcreve cada emenda (isolado / antes / depois) com o Whisper small (medium levou ~1,5 min por emenda). Saída: verif.json"""
import json, numpy as np, soundfile as sf, scipy.signal as ss
from faster_whisper import WhisperModel
SR = 44100; START, END = float(__import__("os").environ["START"]), float(__import__("os").environ["END"])  # EP: START=... END=... python3 verifica.py
C = json.load(open('candidatos.json'))
ok = []
for c in C:
    if c['c1'] - c['c0'] < 0.15 or c['c0'] < START or c['c1'] > END or c['sobre'] > 0.1: continue
    if any(o['faixa'] == c['faixa'] and o['c0'] < c['c1'] and c['c0'] < o['c1'] for o in ok): continue
    ok.append(c)
print(len(ok), 'candidatos depois do filtro', flush=True)
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=6)
X = {t: sf.SoundFile(f'{t}_d.wav') for t in ('fel', 'bru')}
def rd(t, a, b):
    f = X[t]; f.seek(int(a * SR)); return f.read(int((b - a) * SR), dtype='float32')
def tr(x):
    x = ss.resample_poly(x, 160, 441).astype('float32')
    s, _ = m.transcribe(x, language='pt', beam_size=5, condition_on_previous_text=False, vad_filter=False, without_timestamps=True)
    return ' '.join(z.text.strip() for z in s)
for k, c in enumerate(ok):
    t, c0, c1 = c['faixa'], c['c0'], c['c1']
    c['iso'] = tr(rd(t, c0 - 0.05, c1 + 0.05))
    c['antes'] = tr(rd(t, c0 - 2.5, c1 + 2.5))
    c['depois'] = tr(np.concatenate([rd(t, c0 - 2.5, c0), rd(t, c1, c1 + 2.5)]))
    if k % 10 == 0: print(f'{k}/{len(ok)}', flush=True)
json.dump(ok, open('verif.json', 'w'), ensure_ascii=False, indent=0)
print('VERIF_DONE', flush=True)
