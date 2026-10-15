"""Corta as prévias de checagem do corte renderizado: vinheta, cada America alert, cada pedido ao Rômulo e a saída.
Uso: EP=81 V=1 python3 previas.py   → pasta "Temporada 6/<EP>/prévias corte <V>/" com mp3 numerados por ordem no episódio."""
import json, os, subprocess
EP, V = os.environ['EP'], os.environ['V']
base = os.path.expanduser(f'~/Desktop/Vai tomar no seu cunhado/Temporada 6/{EP}')
src = f'{base}/Episódio {EP} - corte {V} (normalizado).mp3'
dst = f'{base}/prévias corte {V}'; os.makedirs(dst, exist_ok=True)
m = json.load(open('mapa.json'))
mm = lambda t: f'{int(t//60):02d}m{int(t%60):02d}s'
clips = [(m['vinheta'] - 15, m['vinheta'] + 20, 'vinheta')]
clips += [(t - 8, t + 8, 'america alert') for t in m['alertas']]
clips += [(t - 8, t + 10, 'romulo ' + os.path.splitext(f)[0].removeprefix('sfx_')) for t, f in m['efeitos']]
clips += [(m['tchau'] - 60, m['fim'], 'saida')]
for i, (a, b, nome) in enumerate(sorted(clips), 1):
    a = max(0, a); f = f'{dst}/{i:02d} {nome} ({mm(a)}).mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.2f}', '-t', f'{b-a:.2f}', '-i', src,
                    '-af', 'afade=t=in:d=0.3', '-c:a', 'libmp3lame', '-b:a', '192k', f], check=True)
    print(f)
