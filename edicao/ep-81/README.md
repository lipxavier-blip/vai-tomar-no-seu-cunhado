# Modelo de edição do Vai Tomar

Base da skill `/editar-episodio-vtnsc` (`~/.claude/skills/editar-episodio-vtnsc/SKILL.md`, que tem o passo a passo e as regras).
Copiar esta pasta para `edicao/ep-NN/` e rodar lá dentro.

| arquivo | origem |
|---|---|
| `fel.wav`, `bru.wav` | faixas brutas do Riverside de cada um |
| `intro44.wav`, `alert44.wav`, `m_*.wav`, `sfx_*.wav` | vinheta, America alert, trilhas e efeitos convertidos (`ffmpeg -ar 44100 -ac 2 -c:a pcm_f32le`) |
| `gaps.npy` | pausas em que os dois ficam calados (início, duração), na linha do tempo do Riverside |

1. `bash stems.sh` → `fel_p.wav`, `bru_p.wav`
2. `bash denoise.sh` → `fel_d.wav`, `bru_d.wav` (nf e notch medidos por episódio)
3. Preencher o topo de `edit.py` (cortes, finos, vinheta, alertas, efeitos, blocos, tchau)
4. `EP=NN V=1 nice -n 19 bash master.sh` → `Episódio NN - corte 1 (normalizado).mp3` + `mapa.json`
5. `EP=NN V=1 python3 previas.py` → `prévias corte 1/`

`ep-80/` é o episódio real que originou o modelo (lá a saída ainda usava o Outro do prettyjohn1).
