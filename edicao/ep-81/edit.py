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
S_ = lambda t: int(round(t * 44100))

# ---- tempos na linha do tempo do Riverside (segundos) ----
START, END = 39.85, 3397.3              # começa no "Como é que você tá, Bruno?"; termina depois do tchau do Bruno
CUTS = [(601.65, 606.35), (2609.45, 2611.65)]             # "Ô Felipe, travou tudo aqui enquanto falava junto": volta no "Vou te falar, viu" (pedido do Felipe); silêncio de 2,8 s depois do "o Jair é foda, né?" (42:18 do corte 2): corta 2,2 s
FINOS = [
    (54.06, 55.23, "repetição: essa frase"),
    (180.85, 181.33, "é isso: é isso,"),
    (258.70, 259.16, "éee: éee"),
    (338.76, 340.74, "repetição: ela gosta,"),
    (382.83, 383.59, "repetição: ele pede"),
    (406.38, 407.56, "repetição: Eu fiz um,"),
    (654.07, 654.31, "repetição: o quê?"),
    (727.65, 729.51, "ajuste do Felipe (12:08): \"e tal, talvez até\""),
    (809.54, 813.15, "ajuste do Felipe (13:30): \"amizade, a gente não costuma\""),
    (1179.89, 1181.39, "repetição: ele vai..."),
    (1521.29, 1521.93, "éee: éee"),
    (1729.81, 1730.32, "éee: éee"),
    (1835.84, 1836.25, "repetição: que eu li,"),
    (1886.25, 1888.08, "ajuste do Felipe (31:27): \"Então, eu acho que o bolsonarismo\""),
    (2018.25, 2019.79, "ajuste do Felipe (33:38): \"a galera trata com menos importância\""),
    (2333.71, 2340.56, "ajuste do Felipe (38:57): \"sacou? Antes de chegar às eleições\""),
    (2580.44, 2580.85, "éee: éee"),
    (2670.64, 2672.51, "ajuste do Felipe (44:31): \"mesma coisa, eu acho que o bolsonarismo\""),
    (2945.70, 2946.31, "éee: éee"),
    (3006.31, 3006.80, "repetição: eu também,"),
    (3259.10, 3259.73, "éee: éee"),
    (3263.63, 3266.07, "ajuste do Felipe (54:24): \"é isso aí. Então, tipo assim\""),
    (3278.05, 3278.69, "éee: éee"),
]  # aprovados na página de cortes finos
INTRO_SPLIT = 601.6                     # fim do grito: a vinheta bate aqui, cheia e sem fade (achar pela energia)
INTRO_LEAD = 0.8                      # a vinheta entra este tanto antes do fim do grito, por cima do finzinho (81: 0.8)
INTRO_SOLO = 5.0                      # segundos de vinheta sozinha antes da fala voltar
ALERTS = [(3243.36, 2.4)]             # "fico meio down" (54:02), depois do fim do "down" (o "assim" começa em 3243.4)
SFX = []                              # (t, 'sfx_x.wav', pausa, dB acima da fala): pedidos ao Rômulo
BEEPS = [(26*60 + 44.93, 26*60 + 46.2)]  # "Nicolas Ferreira": o Bruno pede pro Rômulo mutar (27:12)
TCHAU_AT = 3391.2                        # último "tchau"/"sobe o som aí": a trilha do último bloco sobe daqui
FIRST_BED = 'm_chill.wav'             # cobre do fim da vinheta até o primeiro bloco de BEDS
# blocos de música de fundo: (início no Riverside, arquivo); o último bloco vai até o fim do episódio
BEDS = [(709.5, 'm_leitura.wav'),    # 11:50 comentário do Geli sobre o ep 79 (leitura de ouvinte)
        (866.0, 'm_sadpj.wav'),      # 14:26 política: pós primeiro turno, redes, o vídeo do analista
        (1801.0, 'm_sonican.wav'),   # 30:01 incêndios na UFPE
        (2060.3, 'm_rainy.wav'),     # 34:20 foro privilegiado, pão e circo, 8 de janeiro, voltar a votar
        (2580.3, 'm_calm.wav')]      # 43:00 "o que mudou na sua vida", bolsonarismo e igreja, fecho
BED_BELOW_SPEECH_DB = 28.0
BED_TRIM = {'m_sadpj.wav': -1.5}                        # ajuste fino por faixa em dB, depois de medir a camada de música (ex.: {'m_x.wav': -1.5})
STING_DB_ABOVE_SPEECH = 10.0          # vinheta marcante (o 78 usava ~3 dB; 7 dB ainda ficou tímido)
END_FULL = 0.45                       # nível da trilha final depois do tchau (relativo à intro, como o Outro do 80)
END_TAIL = 20.0                       # segundos de música cheia depois do tchau
END_FADE = 5.0
END_SONG = ('m_lara.wav', 3391.2)  # Love by Grace, pedida pelo Bruno ("a música da Carolina Dieckmann raspando a cabeça")
_END_SONG_DOC = None                       # ('m_x.wav', t no Riverside): música pedida no ar pro fim; entra baixa em t, a trilha
                                      # do último bloco sai em crossfade e ela sobe depois do tchau (no lugar da trilha)

for a, b in BEEPS:                    # zera a voz antes de cortar, com 10 ms de rampa
    r = np.linspace(1, 0, S_(0.01), dtype=np.float32)
    voice[S_(a) - len(r):S_(a)] *= r; voice[S_(a):S_(b)] = 0; voice[S_(b):S_(b) + len(r)] *= r[::-1]

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
def piece(a, b, fade_out=None):
    x = voice[S(a):S(b)].copy()
    r = np.linspace(0, 1, F, dtype=np.float32); x[:F] *= r
    fo = S(fade_out) if fade_out else F
    x[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)
    return x

# som ambiente pras pausas inseridas (silêncio digital denuncia o corte): a maior pausa real do episódio
_g = max(((st, d) for st, d in gaps if START < st < END), key=lambda z: z[1])
ROOM = voice[S(_g[0] + 0.2):S(_g[0] + _g[1] - 0.2)].copy()

out = []; pos = 0; mapping = []   # (src_a, src_b, out_a)
def emit(a, b, fade_out=None):
    global pos
    mapping.append((a, b, pos)); out.append(piece(a, b, fade_out)); pos += S(b) - S(a)
def gap(sec):
    global pos
    n = S(sec); x = np.resize(ROOM, n).astype(np.float32)
    r = min(S(0.05), n // 2); x[:r] *= np.linspace(0, 1, r, dtype=np.float32); x[-r:] *= np.linspace(1, 0, r, dtype=np.float32)
    out.append(x); pos += n

# eventos que abrem (ou não) pausa na fala: (t, tipo, pausa, extra)
events = [(INTRO_SPLIT, 'intro_solo', INTRO_SOLO, None)] + \
         [(t, 'alert', g, None) for t, g in ALERTS] + \
         [(t, 'sfx', g, (f, db)) for t, f, g, db in SFX]
events.sort()
marks = {'alert': [], 'sfx': []}
for a, b in segs:
    for t, kind, g, extra in events:
        if a <= t < b:
            emit(a, t, 0.06 if kind == 'alert' else None)   # alerta: a palavra morre em 60 ms por baixo dele
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
solo = marks['intro_solo']; i0 = solo - S(INTRO_LEAD)
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
    tr = load(f)
    if k + 1 < len(bed_starts):
        b1 = bed_starts[k + 1][0] + S(XF); length = b1 - b0
        g = bed_gain(looped(tr, length)) * 10 ** (BED_TRIM.get(f, 0) / 20)    # ganho medido no trecho que toca (faixa curta e irregular erra pela média)
        e = env([(0, 0), (XF, g), (length / SR - XF, g), (length / SR, 0)], length)
    elif END_SONG:
        b1 = O(END_SONG[1]) + S(XF); length = b1 - b0
        g = bed_gain(looped(tr, length))
        e = env([(0, 0), (XF, g), (length / SR - XF, g), (length / SR, 0)], length)
    else:
        g = bed_gain(tr); g_full = END_FULL * rms(intro[:S(8)]) / rms(tr[:S(8)])
        rise0 = (max(o_end, b0 + S(XF)) - b0) / SR      # sobe a partir do tchau, por cima do fim da fala
        rise1 = max(rise0, (speech_end - b0) / SR) + 1.5
        length = S(rise1 + END_TAIL + END_FADE); b1 = b0 + length
        e = env([(0, 0), (XF, g), (rise0, g), (rise1, g_full),
                 (rise1 + END_TAIL, g_full), (length / SR, 0)], length)
    add(looped(tr, length), b0, e)
    print(f"fundo {f:16s} {mmss(b0)} → {mmss(b1)}")

if END_SONG:
    song = load(END_SONG[0]); s0 = O(END_SONG[1]); g = bed_gain(song)
    g_full = END_FULL * rms(intro[:S(8)]) / rms(song[S(10):S(18)])
    rise0 = max(0.0, (o_end - s0) / SR); rise1 = max(rise0, (speech_end - s0) / SR) + 1.5
    length = min(len(song), S(rise1 + END_TAIL + END_FADE))
    add(song, s0, env([(0, 0), (XF, g), (rise0, g), (rise1, g_full), (length / SR - END_FADE, g_full), (length / SR, 0)], length))
    print(f"fim com {END_SONG[0]} {mmss(s0)}, sobe em {mmss(s0 + S(rise1))}")

# ---- America alert: ~1,5 s cheio e fade até ~4 s, por cima da fala ----
if marks['alert']:
    alert = load('alert44.wav')
    alert = alert[int(np.argmax(np.abs(alert).max(axis=1) > 10 ** (-40 / 20))):]   # pula o silêncio do começo do arquivo
    # cheio até o 1º pico da frase (~2 s), depois cai; a fala volta no fim da pausa (ALERTS, 2.4 s), já com ele baixando
    for p, _ in marks['alert']:
        p -= S(0.03)                      # cobre os 60 ms em que a palavra morre
        add(alert, p, env([(0, 1.0), (2.0, 1.0), (2.4, 0.45), (3.0, 0.15), (3.8, 0.0), (4.0, 0)], S(4.0)))
        print(f"alerta {mmss(p)}")

# ---- pedidos ao Rômulo: efeito no ponto, nível relativo à fala ----
for p, (f, db) in marks['sfx']:
    fx = load(f); g = speech_rms * 10 ** (db / 20) / loud(fx)
    n = len(fx); add(fx, p, env([(0, g), (n / SR - 0.05, g), (n / SR, 0)], n))
    print(f"efeito {f} {mmss(p)}")

# ---- censura: bipe no tamanho exato do nome, no nível da fala ----
if BEEPS:
    beep = load('sfx_beep.wav'); g = speech_rms / loud(beep)
    for a, b in BEEPS:
        n = S(b - a); p = O(a); r = S(0.01)
        add(beep[S(0.3):S(0.3) + n], p, env([(0, 0), (0.01, g), ((n - r) / SR, g), (n / SR, 0)], n))
        print(f"bipe {mmss(p)} ({b - a:.2f}s)")

last = int(np.max(np.nonzero(np.abs(mix).max(axis=1) > 1e-4))) + S(0.3)
mix = mix[:last]
sf.write(f'ep{EP}_premaster.wav', mix, SR, subtype='FLOAT')
if os.environ.get('SO_MUSICA'):     # conferência: só a camada de música, mais a voz montada pra medir contra
    sf.write(f'ep{EP}_musica.wav', mix - np.stack([v, v], axis=1)[:len(mix)], SR, subtype='FLOAT')
    sf.write(f'ep{EP}_voz.wav', v[:len(mix)], SR, subtype='FLOAT')

# mapa pras prévias e pra converter minuto do corte → Riverside
json.dump({'mapping': [(a, b, oa / SR) for a, b, oa in mapping],
           'vinheta': i0 / SR, 'alertas': [p / SR for p, _ in marks['alert']],
           'efeitos': [[p / SR, f] for p, (f, _) in marks['sfx']],
           'bipes': [O(a) / SR for a, b in BEEPS], 'tchau': o_end / SR, 'fim': len(mix) / SR,
           'finos': [[O(a) / SR, txt] for a, b, txt in FINOS if any(x <= a <= y for x, y, _ in mapping)]},
          open('mapa.json', 'w'), indent=1, ensure_ascii=False)
print(f"saída {mmss(o_end)}, duração {mmss(len(mix))}")
