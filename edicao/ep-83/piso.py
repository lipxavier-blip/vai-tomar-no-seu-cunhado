import subprocess, numpy as np, sys
for s in ['fel','bru']:
    raw = subprocess.run(['ffmpeg','-v','error','-i',f'{s}_p.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    x = np.frombuffer(raw, np.float32); w=800; n=len(x)//w
    r = np.sqrt((x[:n*w].reshape(n,w)**2).mean(1)+1e-12); db=20*np.log10(r)
    print(s, 'p5 %.1f p10 %.1f p50 %.1f'%tuple(np.percentile(db,[5,10,50])))
