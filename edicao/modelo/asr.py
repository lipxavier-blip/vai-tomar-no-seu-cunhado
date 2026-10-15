"""Whisper palavra a palavra por faixa, em pedaços de 10 min (o episódio inteiro de uma vez estoura a memória)."""
import json, sys, numpy as np, soundfile as sf, scipy.signal as ss
from faster_whisper import WhisperModel
SR = 44100; CH = 600; OV = 3
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
for tr in ('fel', 'bru'):
    info = sf.info(f'{tr}_d.wav'); dur = info.frames / SR; words = []; a = 0.0
    while a < dur:
        b = min(dur, a + CH + OV)
        x, _ = sf.read(f'{tr}_d.wav', start=int(a * SR), stop=int(b * SR), dtype='float32')
        x16 = ss.resample_poly(x, 160, 441).astype('float32')
        segs, _ = m.transcribe(x16, language='pt', word_timestamps=True, vad_filter=True,
                               condition_on_previous_text=False, initial_prompt='Éee, é, hã, tipo, né, eu eu, de de.')
        for sg in segs:
            for w in sg.words:
                t0 = a + w.start
                if (a == 0 or t0 >= a + OV / 2) and t0 < a + CH + OV / 2:
                    words.append([round(t0, 2), round(a + w.end, 2), w.word.strip(), round(w.probability, 2)])
        print(f'{tr} {b/60:.1f}/{dur/60:.1f} min, {len(words)} palavras', flush=True)
        a += CH
    json.dump(words, open(f'words_{tr}.json', 'w'), ensure_ascii=False)
print('ASR_DONE', flush=True)
