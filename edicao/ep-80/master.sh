set -e
V=${V:?defina V=numero do corte}
OUT=~/Desktop/"Vai tomar no seu cunhado/Temporada 6/80/Episódio 80 - corte ${V} (normalizado).mp3"
ffmpeg -v error -y -i fel_d.wav -i bru_d.wav -filter_complex "[0][1]amix=inputs=2:normalize=0,alimiter=limit=0.6:attack=3:release=80:level=false" -c:a pcm_f32le voice_lim.wav
python3 edit.py
ffmpeg -v error -y -i ep80_premaster.wav -af "alimiter=limit=0.75:attack=2:release=60:level=false" -c:a pcm_f32le ep80_lim.wav
I=$(ffmpeg -hide_banner -i ep80_lim.wav -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(-15.7-($I))")
ffmpeg -v error -y -i ep80_lim.wav -af "volume=${G}dB" -ar 44100 -c:a libmp3lame -b:a 192k -id3v2_version 3 -metadata title="Episódio 80" "$OUT"
ffmpeg -hide_banner -i "$OUT" -af "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary" -f null - 2>&1 | grep -E "Input Integrated|Input True Peak"
