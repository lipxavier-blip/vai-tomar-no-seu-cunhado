set -e
# ep 83 corte 2: pisos remedidos depois do EQ (Felipe -68,7, Bruno -73,4)
# ep 83: pisos medidos sem o silêncio digital (Felipe -70 dB, zumbido leve 120/140 Hz; Bruno -74 dB)
# Bruno: o apito mudou, agora é um tom em 2000/4000/6000 Hz (antes ~1670) → notch Q30 nos três
ffmpeg -v error -y -i fel_p.wav -af "afftdn=nr=12:nf=-69:tn=1,agate=threshold=0.0056:ratio=2:range=0.25:attack=5:release=250:knee=4" -c:a pcm_f32le fel_d.wav
ffmpeg -v error -y -i bru_p.wav -af "bandreject=f=2000:width_type=q:w=30,bandreject=f=4000:width_type=q:w=30,bandreject=f=6000:width_type=q:w=30,afftdn=nr=12:nf=-73:tn=1,agate=threshold=0.0040:ratio=2:range=0.25:attack=5:release=250:knee=4" -c:a pcm_f32le bru_d.wav
echo DENOISE_DONE
