"""Montagem do Vai Tomar (modelo a partir do ep 80). Roda via master.sh, que define EP.
Edite só o bloco de tempos abaixo; todos os tempos são na linha do tempo do Riverside (segundos)."""
import json, os
import numpy as np, soundfile as sf
SR = 44100
S = lambda t: int(round(t * SR))
EP = os.environ['EP']

# vozes somadas e já limitadas (ver master.sh); a música entra depois, sem passar pelo limitador
voice, _ = sf.read('voice_lim.wav', dtype='float32')
load = lambda f: sf.read(f, dtype='float32')[0]
intro = load('intro44.wav')

# ---- tempos na linha do tempo do Riverside (segundos) ----
START, END = 0.0, 0.0                 # START pula o teste de microfone
CUTS = []                             # (a, b): conteúdo que fica de fora (pedidos no ar, família/casa)
FINOS = []                            # (a, b, 'o quê'): "éee", "é isso", gagueira; emenda no silêncio entre palavras
INTRO_SPLIT = 0.0                     # fim do grito: a vinheta bate aqui, cheia e sem fade (achar pela energia)
INTRO_SOLO = 5.0                      # segundos de vinheta sozinha antes da fala voltar
ALERTS = []                           # (t, pausa): America alert por cima da fala; no 80 a pausa foi 1.4
SFX = []                              # (t, 'sfx_x.wav', pausa, dB acima da fala): pedidos ao Rômulo
TCHAU_AT = 0.0                        # último "tchau"/"sobe o som aí": a trilha do último bloco sobe daqui
FIRST_BED = 'm_chill.wav'             # cobre do fim da vinheta até o primeiro bloco de BEDS
# blocos de música de fundo: (início no Riverside, arquivo); o último bloco vai até o fim do episódio
BEDS = []
BED_BELOW_SPEECH_DB = 28.0
STING_DB_ABOVE_SPEECH = 10.0          # vinheta marcante (o 78 usava ~3 dB; 7 dB ainda ficou tímido)
END_FULL = 0.45                       # nível da trilha final depois do tchau (relativo à intro, como o Outro do 80)
END_TAIL = 20.0                       # segundos de música cheia depois do tchau
END_FADE = 5.0

gaps = np.load('gaps.npy')
CUTS = [(a, b) for a, b in CUTS] + [(a, b) for a, b, _ in FINOS]
for st, d in gaps:
    if d > 1.5 and START < st < END and not any(a <= st <= b for a, b in CUTS) \
            and not (INTRO_SPLIT - 5 < st < INTRO_SPLIT + 3):
        CUTS.append((st + 0.4, st + d - 0.4))
CUTS.sort()

segs = []; cur = START
for a, b in CUTS:
    if b <= cur: continue
    segs.append((cur, max(cur, a))); cur = b
segs.append((cur, END))
segs = [(a, b) for a, b in segs if b - a > 0.05]

F = S(0.015)
def piece(a, b):
    x = voice[S(a):S(b)].copy()
    r = np.linspace(0, 1, F, dtype=np.float32); x[:F] *= r; x[-F:] *= r[::-1]
    return x

out = []; pos = 0; mapping = []   # (src_a, src_b, out_a)
def emit(a, b):
    global pos
    mapping.append((a, b, pos)); out.append(piece(a, b)); pos += S(b) - S(a)
def gap(sec):
    global pos
    out.append(np.zeros(S(sec), np.float32)); pos += S(sec)

# eventos que abrem (ou não) pausa na fala: (t, tipo, pausa, extra)
events = [(INTRO_SPLIT, 'intro_solo', INTRO_SOLO, None)] + \
         [(t, 'alert', g, None) for t, g in ALERTS] + \
         [(t, 'sfx', g, (f, db)) for t, f, g, db in SFX]
events.sort()
marks = {'alert': [], 'sfx': []}
for a, b in segs:
    for t, kind, g, extra in events:
        if a <= t < b:
            emit(a, t)
            if kind == 'intro_solo': marks[kind] = pos
            else: marks[kind].append((pos, extra))
            if g: gap(g)
            a = t
    emit(a, b)
v = np.concatenate(out)

def O(t):
    for a, b, oa in mapping:
        if a <= t <= b: return oa + S(t) - S(a)
    raise ValueError(t)

speech_end = len(v)
v = np.concatenate([v, np.zeros(S(END_TAIL + END_FADE + 5), np.float32)])
mix = np.stack([v, v], axis=1)
L = len(mix)

def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
def loud(x):
    """potência média das janelas de 400 ms acima de -50 dBFS (aproxima o LUFS com gate)"""
    if x.ndim > 1: x = x.mean(axis=1)
    w = S(0.4); k = len(x) // w; fr = np.sqrt(np.mean(x[:k * w].reshape(k, w) ** 2, axis=1))
    fr = fr[fr > 10 ** (-50 / 20)]
    return float(np.sqrt(np.mean(fr ** 2)))
speech_rms = loud(voice[S(START):S(END)])
bed_rms = speech_rms * 10 ** (-BED_BELOW_SPEECH_DB / 20)
def bed_gain(track):
    return bed_rms / loud(track)
print(f"fala {20*np.log10(speech_rms):.1f} dB, fundo {20*np.log10(bed_rms):.1f} dB")

def env(points, length):
    t = np.array([p[0] for p in points]) * SR; g = np.array([p[1] for p in points])
    return np.interp(np.arange(length), t, g).astype(np.float32)

def add(track, at, envelope):
    e = min(L, at + len(envelope)); k = e - at
    mix[at:e] += track[:k] * envelope[:k, None]

def looped(track, length, xf=S(3)):
    """repete a faixa com crossfade até cobrir `length` amostras"""
    res = np.zeros((length + len(track), 2), np.float32); p = 0
    r = np.linspace(0, 1, xf, dtype=np.float32)[:, None]
    while p < length:
        t = track.copy()
        if p > 0: t[:xf] *= r
        t[-xf:] *= r[::-1]
        res[p:p + len(t)] += t; p += len(t) - xf
    return res[:length]

def mmss(n): return f"{n/SR//60:.0f}m{n/SR%60:04.1f}s"

XF = 4.0   # crossfade entre blocos de fundo
# ---- vinheta: entra cheia no fim do grito, solo, desce pra fundo e some em ~12s de conversa ----
solo = marks['intro_solo']; i0 = solo
t_full = 0.005                           # só o suficiente pra não estalar
t_solo_end = (solo + S(INTRO_SOLO) - i0) / SR
g_bed_intro = bed_gain(intro)
STING_GAIN = speech_rms * 10 ** (STING_DB_ABOVE_SPEECH / 20) / loud(intro[:S(10)])
intro_len = len(intro) / SR
intro_end = t_solo_end + 12.0
pts = [(0, 0.0), (t_full, STING_GAIN), (t_solo_end - 0.3, STING_GAIN),
       (t_solo_end + 1.5, STING_GAIN * 0.5), (t_solo_end + 5.0, STING_GAIN * 0.2),
       (t_solo_end + 9.0, g_bed_intro), (intro_end, 0.0), (intro_len, 0.0)]
add(intro, i0, env(pts, S(intro_len)))
intro_out_end = i0 + S(min(intro_end, intro_len))
print(f"vinheta {mmss(i0)}, fundo da intro até {mmss(intro_out_end)}")

# fundo nunca para: FIRST_BED cobre o buraco entre a intro e o primeiro bloco
bed_starts = [(O(t), f) for t, f in BEDS]
if not bed_starts or intro_out_end < bed_starts[0][0]:
    bed_starts.insert(0, (intro_out_end - S(6.0), FIRST_BED))

# ---- blocos; o último segue até o fim e sobe depois do tchau (sem trocar de música) ----
o_end = O(TCHAU_AT)
for k, (b0, f) in enumerate(bed_starts):
    tr = load(f); g = bed_gain(tr)
    if k + 1 < len(bed_starts):
        b1 = bed_starts[k + 1][0] + S(XF); length = b1 - b0
        e = env([(0, 0), (XF, g), (length / SR - XF, g), (length / SR, 0)], length)
    else:
        g_full = END_FULL * rms(intro[:S(8)]) / rms(tr[:S(8)])
        rise0 = (max(o_end, b0 + S(XF)) - b0) / SR      # sobe a partir do tchau, por cima do fim da fala
        rise1 = max(rise0, (speech_end - b0) / SR) + 1.5
        length = S(rise1 + END_TAIL + END_FADE); b1 = b0 + length
        e = env([(0, 0), (XF, g), (rise0, g), (rise1, g_full),
                 (rise1 + END_TAIL, g_full), (length / SR, 0)], length)
    add(looped(tr, length), b0, e)
    print(f"fundo {f:16s} {mmss(b0)} → {mmss(b1)}")

# ---- America alert: ~1,5 s cheio e fade até ~4 s, por cima da fala ----
if marks['alert']:
    alert = load('alert44.wav')
    for p, _ in marks['alert']:
        add(alert, p, env([(0, 1.0), (1.5, 1.0), (4.2, 0.0), (4.5, 0)], S(4.5)))
        print(f"alerta {mmss(p)}")

# ---- pedidos ao Rômulo: efeito no ponto, nível relativo à fala ----
for p, (f, db) in marks['sfx']:
    fx = load(f); g = speech_rms * 10 ** (db / 20) / loud(fx)
    n = len(fx); add(fx, p, env([(0, g), (n / SR - 0.05, g), (n / SR, 0)], n))
    print(f"efeito {f} {mmss(p)}")

last = int(np.max(np.nonzero(np.abs(mix).max(axis=1) > 1e-4))) + S(0.3)
mix = mix[:last]
sf.write(f'ep{EP}_premaster.wav', mix, SR, subtype='FLOAT')

# mapa pras prévias e pra converter minuto do corte → Riverside
json.dump({'mapping': [(a, b, oa / SR) for a, b, oa in mapping],
           'vinheta': i0 / SR, 'alertas': [p / SR for p, _ in marks['alert']],
           'efeitos': [[p / SR, f] for p, (f, _) in marks['sfx']],
           'tchau': o_end / SR, 'fim': len(mix) / SR,
           'finos': [[O(a) / SR, txt] for a, b, txt in FINOS if any(x <= a <= y for x, y, _ in mapping)]},
          open('mapa.json', 'w'), indent=1, ensure_ascii=False)
print(f"saída {mmss(o_end)}, duração {mmss(len(mix))}")
