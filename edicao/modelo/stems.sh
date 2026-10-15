set -e
ffmpeg -v error -y -i fel.wav -af "adeclip,highpass=f=80,acompressor=threshold=-22dB:ratio=3:attack=10:release=150:makeup=2" -c:a pcm_f32le fel_p1.wav
ffmpeg -v error -y -i bru.wav -af "highpass=f=80,volume=17dB,acompressor=threshold=-22dB:ratio=3:attack=10:release=150:makeup=2" -c:a pcm_f32le bru_p1.wav
for s in fel bru; do
  J=$(ffmpeg -hide_banner -i ${s}_p1.wav -af loudnorm=I=-19:TP=-3:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  mI=$(echo "$J"|python3 -c "import json,sys;print(json.load(sys.stdin)['input_i'])")
  g=$(python3 -c "print(-19-($mI))")
  echo "$s measured $mI gain $g"
  ffmpeg -v error -y -i ${s}_p1.wav -af "volume=${g}dB" -c:a pcm_f32le ${s}_p.wav
done
echo STEMS_DONE
