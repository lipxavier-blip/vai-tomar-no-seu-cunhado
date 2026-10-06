# Edição do ep 80 (modelo para os próximos)

Rodar dentro de uma pasta de trabalho com estes arquivos (links ou cópias):

| arquivo | origem |
|---|---|
| `fel.wav`, `bru.wav` | faixas brutas do Riverside de cada um |
| `intro44.wav`, `alert44.wav` | intro e America alert convertidos (`ffmpeg -ar 44100 -ac 2 -c:a pcm_f32le`) |
| `m_*.wav` | trilhas de fundo e o Outro, convertidos do mesmo jeito |
| `gaps.npy` | pausas em que os dois ficam calados (início, duração), na linha do tempo do Riverside |

Ordem:

1. `bash stems.sh`: trata e nivela cada voz (`fel_p.wav`, `bru_p.wav`)
2. `bash denoise.sh`: tira ruído (`fel_d.wav`, `bru_d.wav`)
3. Editar o topo de `edit.py`: `START`/`END`, `CUTS`, `INTRO_SPLIT` (fim do grito pela energia da faixa),
   `ALERT_AT`, `OUTRO_AT` ("sobe o som aí") e `BEDS` (início de cada bloco + trilha)
4. `V=1 bash master.sh`: gera `Episódio NN - corte 1 (normalizado).mp3` (trocar a pasta `80` no `OUT`)

As regras de nível, vinheta e escolha de trilha estão na memória do projeto (seção "Edição").
