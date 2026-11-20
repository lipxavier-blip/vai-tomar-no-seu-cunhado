"""ruidos.json → mudos.json (regra da skill): silencia tudo fora da fala menos risada, fala forte (AST Speech ≥ 0,3 e > -35 dB)
e trecho em que o Whisper acha 2+ palavras (alucinação típica do Whisper não conta)."""
import json, re, numpy as np, soundfile as sf, scipy.signal as ss
from faster_whisper import WhisperModel
SR = 44100
RISO = {'Laughter', 'Giggle', 'Chuckle, chortle', 'Belly laugh', 'Snicker'}
FALA = {'Speech', 'Male speech, man speaking', 'Conversation', 'Narration, monologue', 'Singing'}
ALUC = re.compile(r'legenda|amara|obrigad|inscreva|tchau|transcri', re.I)
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=3)
R = json.load(open('ruidos.json')); out = {}
for tr in ('fel', 'bru'):
    f = sf.SoundFile(f'{tr}_d.wav'); res = []
    for k, (a, b, lab, p, _, lvl) in enumerate(R[tr]):
        if lab in RISO: res.append([a, b, lab, 'fica (risada)']); continue
        if lab in FALA and p >= 0.3 and lvl > -35: res.append([a, b, lab, 'fica (fala forte)']); continue
        f.seek(max(0, int((a - 0.15) * SR))); x = f.read(int((b - a + 0.3) * SR), dtype='float32')
        x = x.mean(1) if x.ndim == 2 else x
        s, _ = m.transcribe(ss.resample_poly(x, 160, 441).astype('float32'), language='pt', vad_filter=False,
                            condition_on_previous_text=False, without_timestamps=True)
        txt = ' '.join(z.text.strip() for z in s)
        n = 0 if ALUC.search(txt) else len(re.findall(r'\w+', txt))
        res.append([a, b, lab, f'fica (palavras: {txt})' if n >= 2 else 'mudo'])
        if k % 100 == 0: print(tr, k, len(R[tr]), flush=True)
    out[tr] = res
    print(tr, sum(r[3] == 'mudo' for r in res), 'mudos de', len(res), flush=True)
json.dump(out, open('mudos.json', 'w'), ensure_ascii=False, indent=0)
print('MUDOS_DONE', flush=True)
