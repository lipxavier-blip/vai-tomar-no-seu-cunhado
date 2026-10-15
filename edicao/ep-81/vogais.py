"""Vogais sustentadas (candidatas a "éee") por acústica, por faixa (adaptado do CoffeeX 67 para 44,1 kHz).
Saída: vogais_<faixa>.json com [início, fim, f0, dist_timbre, energia]."""
import json, numpy as np, soundfile as sf
SR = 44100; H = 441; N = 1764   # passo 10 ms, janela 40 ms
win = np.hanning(N).astype(np.float32)
for tr in ('fel', 'bru'):
    x, _ = sf.read(f'{tr}_d.wav', dtype='float32')
    n = (len(x) - N) // H
    E = np.zeros(n, np.float32); P = np.zeros(n, np.float32); F = np.zeros(n, np.float32); S = np.zeros((n, 40), np.float32)
    B = 8000; lo, hi = SR // 350, SR // 70
    for b0 in range(0, n, B):
        k = min(B, n - b0)
        idx = np.arange(N)[None, :] + H * (b0 + np.arange(k))[:, None]
        fr = x[idx]; fr = fr - fr.mean(1, keepdims=True)
        E[b0:b0+k] = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
        pw = np.abs(np.fft.rfft(fr * win, n=2 * N, axis=1)) ** 2
        ac = np.fft.irfft(pw, axis=1)[:, :N]; ac /= ac[:, :1] + 1e-9
        lag = np.argmax(ac[:, lo:hi], 1) + lo
        P[b0:b0+k] = ac[np.arange(k), lag]; F[b0:b0+k] = SR / lag
        # envelope grosso: 40 bandas até ~4 kHz (bins de 12,5 Hz)
        S[b0:b0+k] = np.log(pw[:, :320].reshape(k, 40, 8).mean(2) + 1e-9)
        del idx, fr, pw, ac
    vog = (E > -32) & (P > 0.55)
    runs = []; i = 0
    while i < n:
        if vog[i]:
            j = i; f0 = [F[i]]
            while j + 1 < n and vog[j+1] and abs(F[j+1] - np.median(f0[-15:])) < 0.12 * np.median(f0[-15:]):
                j += 1; f0.append(F[j])
            if (j - i + 1) * 0.01 >= 0.33:
                seg = S[i:j+1]; k = 5
                dist = float(np.mean(np.abs(seg[k:] - seg[:-k]))) if len(seg) > k else 9
                runs.append([round(i * 0.01 + 0.02, 3), round(j * 0.01 + 0.02, 3), round(float(np.median(f0)), 1),
                             round(dist, 3), round(float(E[i:j+1].mean()), 1)])
            i = j + 1
        else: i += 1
    json.dump(runs, open(f'vogais_{tr}.json', 'w'))
    np.save(f'E10_{tr}.npy', E)
    print(tr, len(runs), 'vogais >= 0,33 s', flush=True)
    del x
