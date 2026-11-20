"""Sons fora das palavras em cada faixa, classificados com AST/AudioSet (método do CoffeeX 67).
Respiração, mão no microfone, estalo etc. → mudo; risada e fala → fica. Saída: ruidos.json"""
import json, numpy as np, soundfile as sf, torch, scipy.signal as ss
from transformers import ASTFeatureExtractor, ASTForAudioClassification
M = 'MIT/ast-finetuned-audioset-10-10-0.4593'
fe = ASTFeatureExtractor.from_pretrained(M); md = ASTForAudioClassification.from_pretrained(M).eval(); lab = md.config.id2label
torch.set_num_threads(4)
RUIDO = {'Breathing','Gasp','Sniff','Snort','Cough','Throat clearing','Sneeze','Sigh','Rustle','Tap','Knock','Typing','Computer keyboard',
         'Clicking','Mouse','Chewing, mastication','Biting','Slurp','Burping, eructation','Hiccup','Dishes, pots, and pans','Cutlery, silverware',
         'Door','Squeak','Scrape','Wind noise (microphone)','Rub','Crumpling, crinkling','Zipper (clothing)','Thump, thud','Bang','Dog','Bark',
         'Cat','Meow','Vehicle','Car','Motorcycle','Siren','Television','Water','Pour','Liquid','Hum','Inside, small room','Mechanical fan',
         'Air conditioning','Pant','Wheeze','Snoring','Static','White noise','Noise','Environmental noise','Crackle','Pink noise','Mains hum',
         'Buzz','Microphone','Wood','Plastic','Writing','Scratch'}
FICA = {'Laughter','Giggle','Chuckle, chortle','Belly laugh','Snicker','Speech','Male speech, man speaking','Conversation',
        'Narration, monologue','Singing','Whistling'}
SR = 44100; res = {}
for tr in ('bru', 'fel'):
    x, _ = sf.read(f'{tr}_d.wav', dtype='float32')
    fr = int(0.02 * SR); n = len(x) // fr
    e = 20 * np.log10(np.sqrt((x[:n * fr].reshape(n, fr) ** 2).mean(1)) + 1e-9)
    ativo = e > max(np.percentile(e, 15) + 14, -55)
    occ = np.zeros(n, bool)
    for a, b, w, p in json.load(open(f'words_{tr}.json')):
        occ[max(0, int((a - 0.12) / 0.02)):min(n, int((b + 0.12) / 0.02) + 1)] = True
    cand = ativo & ~occ
    evs = []; i = 0
    while i < n:
        if cand[i]:
            j = i
            while j < n and (cand[j] or (j + 6 < n and cand[j:j + 6].any() and not occ[j])): j += 1
            if (j - i) * 0.02 >= 0.12: evs.append((i * 0.02, j * 0.02))
            i = j
        else: i += 1
    out = []
    for k, (a, b) in enumerate(evs):
        c = (a + b) / 2; L = max(1.0, b - a + 0.2); s0 = max(0, int((c - L / 2) * SR))
        seg = ss.resample_poly(x[s0:s0 + int(L * SR)], 160, 441).astype('float32')
        with torch.no_grad(): pr = torch.sigmoid(md(**fe(seg, sampling_rate=16000, return_tensors='pt')).logits)[0].numpy()
        top = [(lab[i], float(pr[i])) for i in pr.argsort()[::-1][:5]]
        r = sum(p for l, p in top if l in RUIDO); f = sum(p for l, p in top if l in FICA)
        acao = 'mudo' if r > f and r > 0.08 else 'fica'
        out.append([round(a, 2), round(b, 2), top[0][0], round(top[0][1], 2), acao, round(float(e[int(a / 0.02):int(b / 0.02) + 1].max()), 1)])
        if k % 200 == 0: print(tr, k, len(evs), flush=True)
    res[tr] = out
    print(tr, len(out), 'eventos;', sum(o[4] == 'mudo' for o in out), 'mudo', flush=True)
    json.dump(res, open('ruidos.json', 'w'), ensure_ascii=False)
print('RUIDOS_DONE', flush=True)
