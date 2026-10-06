import numpy as np, soundfile as sf
SR = 44100
S = lambda t: int(round(t * SR))

# vozes somadas e já limitadas (ver master.sh); a música entra depois, sem passar pelo limitador
voice, _ = sf.read('voice_lim.wav', dtype='float32')
load = lambda f: sf.read(f, dtype='float32')[0]
intro, alert, outro = load('intro44.wav'), load('alert44.wav'), load('m_outro.wav')

# ---- tempos na linha do tempo do Riverside (segundos) ----
START, END = 30.10, 3276.60
CUTS = [(952.75, 1016.45)]            # vento + família do Bruno
INTRO_SPLIT = 473.25                  # fim do grito do Bruno: a vinheta bate aqui, cheia e sem fade
INTRO_SOLO = 5.0                      # segundos de vinheta sozinha antes do Bruno voltar
ALERT_AT, ALERT_GAP = 1434.95, 1.4    # "accurate"
OUTRO_AT = 3273.40                    # "sobe o som aí"
# blocos de música de fundo: (início no Riverside, arquivo)
BEDS = [(1253.0, 'm_leitura.wav'),   # 20:53 leitura de comentários (trilha oficial de leitura de ouvinte)
        (1643.0, 'm_chill.wav'),      # 27:23 exame, comida, academia
        (2430.0, 'm_pizz.wav'),       # 40:30 história do antivax (Pizzicato é trilha de história)
        (3001.0, 'm_funky.wav')]      # 50:01 eleição até o fim
BED_BELOW_SPEECH_DB = 28.0
STING_DB_ABOVE_SPEECH = 10.0          # vinheta marcante (o 78 usava ~3 dB; 7 dB ainda ficou tímido)
OUTRO_FULL = 0.45

gaps = np.load('gaps.npy')
for st, d in gaps:
    if d > 1.5 and START < st < END and not any(a <= st <= b for a, b in CUTS) and not (468 < st < 476):
        CUTS.append((st + 0.4, st + d - 0.4))
CUTS.sort()

segs = []; cur = START
for a, b in CUTS:
    segs.append((cur, a)); cur = b
segs.append((cur, END))

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

marks = {}
for a, b in segs:
    for t, kind, g in [(INTRO_SPLIT, 'intro_solo', INTRO_SOLO), (ALERT_AT, 'alert', ALERT_GAP)]:
        if a <= t < b:
            emit(a, t); marks[kind] = pos; gap(g); a = t
    emit(a, b)
v = np.concatenate(out)

def O(t):
    for a, b, oa in mapping:
        if a <= t <= b: return oa + S(t) - S(a)
    raise ValueError(t)

speech_end = len(v)
v = np.concatenate([v, np.zeros(S(30), np.float32)])
mix = np.stack([v, v], axis=1)
L = len(mix)

def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
# nível da fala: mediana do RMS de 1s nos trechos com voz
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

XF = 4.0   # crossfade entre blocos de fundo
# ---- vinheta: sobe por baixo do grito, solo, desce pra fundo e segue até acabar ----
solo = marks['intro_solo']; i0 = solo   # entra impactando, característica da trilha
t_full = 0.005                           # só o suficiente pra não estalar
t_solo_end = (solo + S(INTRO_SOLO) - i0) / SR
g_bed_intro = bed_gain(intro)
STING_GAIN = speech_rms * 10 ** (STING_DB_ABOVE_SPEECH / 20) / loud(intro[:S(10)])
intro_len = len(intro) / SR
intro_end = t_solo_end + 12.0     # a intro some depois de ~12s de conversa; o Chillhop assume o fundo
# cheia até o Bruno falar, depois vai baixando aos poucos ao longo da conversa e some em ~12s
pts = [(0, 0.0), (t_full, STING_GAIN), (t_solo_end - 0.3, STING_GAIN),
       (t_solo_end + 1.5, STING_GAIN * 0.5), (t_solo_end + 5.0, STING_GAIN * 0.2),
       (t_solo_end + 9.0, g_bed_intro), (intro_end, 0.0), (intro_len, 0.0)]
add(intro, i0, env(pts, S(intro_len)))
intro_out_end = i0 + S(min(intro_end, intro_len))
print(f"vinheta {i0/SR/60:.0f}m{i0/SR%60:04.1f}s, fundo da intro até {intro_out_end/SR//60:.0f}m{intro_out_end/SR%60:04.1f}s")

# Se a intro acaba antes do primeiro bloco, o Pizzicato cobre o buraco (fundo nunca para)
bed_starts = [(O(t), f) for t, f in BEDS]
if intro_out_end < bed_starts[0][0]:
    bed_starts.insert(0, (intro_out_end - S(6.0), 'm_chill.wav'))  # headset + contagem até 20:53

o_out = O(OUTRO_AT)
for k, (b0, f) in enumerate(bed_starts):
    b1 = bed_starts[k + 1][0] + S(XF) if k + 1 < len(bed_starts) else o_out + S(2.5)
    tr = load(f); g = bed_gain(tr); length = b1 - b0
    seg = looped(tr, length)
    e = env([(0, 0), (XF, g), (length / SR - XF, g), (length / SR, 0)], length)
    add(seg, b0, e)
    print(f"fundo {f:16s} {b0/SR//60:.0f}m{b0/SR%60:04.1f}s → {b1/SR//60:.0f}m{b1/SR%60:04.1f}s")

# ---- alerta ("accurate") ----
p = marks['alert']; add(alert, p, env([(0, 1.0), (1.5, 1.0), (4.2, 0.0), (4.5, 0)], S(4.5)))

# ---- saída: Outro entra no "sobe o som aí" e sobe depois do tchau ----
g_out_bed = bed_gain(outro); g_out_full = OUTRO_FULL * rms(intro[:S(8)]) / rms(outro[:S(8)])
rise = (speech_end - o_out) / SR
add(outro, o_out, env([(0, g_out_bed), (rise, g_out_bed), (rise + 1.5, g_out_full),
                       (len(outro) / SR - 0.3, g_out_full), (len(outro) / SR, 0)], len(outro)))

last = int(np.max(np.nonzero(np.abs(mix).max(axis=1) > 1e-4))) + S(0.3)
mix = mix[:last]
sf.write('ep80_premaster.wav', mix, SR, subtype='FLOAT')
print(f"alerta {p/SR//60:.0f}m{p/SR%60:04.1f}s, saída {o_out/SR//60:.0f}m{o_out/SR%60:04.1f}s, duração {len(mix)/SR//60:.0f}m{len(mix)/SR%60:04.1f}s")
