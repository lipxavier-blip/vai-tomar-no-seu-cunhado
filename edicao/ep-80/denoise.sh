set -e
# Felipe: zumbido grave (60/120/240 Hz) → redução espectral moderada + expansor
ffmpeg -v error -y -i fel_p.wav -af "afftdn=nr=12:nf=-58:tn=1,agate=threshold=0.0056:ratio=2:range=0.25:attack=5:release=250:knee=4" -c:a pcm_f32le fel_d.wav
# Bruno: apito em ~1670 Hz (notch estreito) + redução espectral + expansor
ffmpeg -v error -y -i bru_p.wav -af "bandreject=f=1670:width_type=q:w=30,afftdn=nr=12:nf=-64:tn=1,agate=threshold=0.0040:ratio=2:range=0.25:attack=5:release=250:knee=4" -c:a pcm_f32le bru_d.wav
echo DENOISE_DONE
