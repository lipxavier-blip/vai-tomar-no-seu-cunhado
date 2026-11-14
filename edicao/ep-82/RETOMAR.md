# Ep 82: onde parou (13/11/2026, ~17h40)

## Pronto, em disco
- Vozes tratadas: `fel_p.wav`, `bru_p.wav` (compressor + nível -19 LUFS, a partir das faixas "(edição Rômulo)") e
  `fel_d.wav`, `bru_d.wav` (mono). Sem denoise: as faixas do Felipe já vieram com piso de -90 dB.
- Whisper palavra a palavra: `words_fel.json`, `words_bru.json` (não precisa rodar de novo).
- Pausas: `gaps.npy`. Energia: `E10_*.npy`. Cortes finos verificados: `aceitos.json` (23) e `rejeitados.json` (95).
- Wavs convertidos: `intro44.wav`, `alert44.wav`, `sfx_beep.wav`, `sfx_sino.wav` (Jingle Bells do NVDD),
  `m_soul.wav`, `m_propaganda.wav` (SyncLab).
- Página única de aprovação: `aprovacao/aprovacao.html` (mapa + 23 finos, Salvar por item, salva em `aprovacao/decisoes.json`).
  As escolhas que o Felipe marcar ficam também no localStorage do Chrome (chave `vtnsc-ep82`, origem 127.0.0.1:8792).

## Para retomar
1. Subir a página de novo (o servidor morre no reinício), **na mesma porta 8792** pra o localStorage voltar:
   `cd ~/Código/vai-tomar-no-seu-cunhado/edicao/ep-82/aprovacao && nohup python3 ../../servidor_aprovacao.py aprovacao.html decisoes.json 8792 &`
   e `open http://127.0.0.1:8792/` (fora do sandbox).
2. Esperar o Felipe salvar e baixar do Pixabay: grito (Efeitos/), efeito de backstage se for scratch/technical error
   (Efeitos/), trilha de Natal (Soundtrack/), e escolher a substituta da Chillhop (sumiu do disco).
3. Preencher o topo do `edit.py` e renderizar o corte 1 (`EP=82 V=1 FAIXA=d nice -n 19 bash master.sh`; sem `ruidos.py`
   por ora, as faixas já vieram limpas). **Avisar antes: ele não quer nada pesado durante gravação.**

## Tempos já levantados (linha do Riverside, segundos)
- Cortes pedidos: filho do Bruno 15.5–49.1 (opção: só 15.5–37.5); espuma do microfone 185.4–227.2.
- Vinheta: fim do grito em 540.5 (energia das duas faixas).
- Blocos: 540.5 papo solto · 771 comentários (Soul of Orleans) · 2163.9 dólar/trabalho (papo solto) · 2609.6 Natal (sobe no fim).
- Tchau: "Adeus" 51:26 (~3086).
- Propaganda: pedido 574.5, "R$ 19,90" termina ~578.6.
- Bipe: "que apesar de sulista não é Bolsonaro" 1957.7–1959.1 (Xanxerê em 1949.7–1950.3 e 1952.0–1952.5).
- Grito: fim do pedido ~2001 ("coloca uma pessoa gritando do nada aí, Rômulo, por favor").
- Christmas: Bruno 2632.28–2632.78. Why: Bruno 2447.76–2448.06. tbt: Felipe 2054.6. home office: Bruno 282.0.
- Sininho: fim do pedido 2636.4 (Felipe volta em 2637.0).
- Eita: 2701.0 "eita", silêncio 2704.9–2711.0, "não sei o que aconteceu" 2711.0.

## Rodada 2 (13/11, ~21h20)
- Decisões da página 1 em `aprovacao/decisoes.json` (filho 0:15–0:49, propaganda SyncLab, bipe só na frase, grito Loud Male Scream HD,
  eita = Record Scratch, alerta só no Christmas, trilhas: Cozy nos dois papos soltos, O Christmas Tree no Natal).
- Comentários: grito da vinheta fora de sincronia (Bruno 0,6 s atrasado no início, ~0,17 s no corpo; prévia adianta o Bruno 0,17 s
  de 534.2 a 540.5 só nas faixas, edit.py ainda não faz isso), piii no "cu" 2540.15–2540.45 (fino 13), cortar silêncio do fino 7
  (o corte automático de pausa >1,5 s já faz), scratch antes do fino 16.
- Página 2: `aprovacao/v2.html` na porta 8793, salva em `aprovacao/decisoes-v2.json`, prévias em `aprovacao/v2/`.
- Faltam os downloads do Pixabay: Loud Male Scream HD e Record Scratch (Efeitos/), O Christmas Tree (Soundtrack/).
- 13/11 ~21h25: rodada 2 aprovada inteira (vinheta com Bruno +0,17 s, bipe, piii). Downloads feitos: `Efeitos/Loud Male Scream HD -
  Virtual_Vibes (Pixabay 379385).mp3`, `Efeitos/Record Scratch - freesound_community (Pixabay 108233).mp3`,
  `Soundtrack/evolvingvibes-o-christmas-tree-632354/` (Content ID; certificado ali e em `licencas-musica/`). Próximo: preencher edit.py
  (com o deslocamento do Bruno no grito) e renderizar o corte 1.
- 13/11 ~21h40: corte 1 renderizado (`EP=82 V=1 FAIXA=s OUT=... bash master.sh`; FAIXA=s = fel_d + bru_s, o Bruno adiantado 0,17 s
  no grito). Em `~/Podcasts/Vai Tomar no Seu Cunhado/Temporada 6/82/`, 50:20, -16,0 LUFS / -1,1 dBTP. previas.py agora grava em
  ~/Podcasts. Página de aprovação do corte: `aprovacao/c1.html`, porta 8794, salva em `aprovacao/decisoes-c1.json`.
- 13/11 ~21h50: corte 1 aprovado menos 2 pontos. Corte 2 (50:17, -15,9 LUFS / -1,3 dBTP): BACKSTAGE (2701.4–2717.4, voz abafada com
  eco e sem trilha) e END=3086.6 (mics cortam no "Adeus"). Página `aprovacao/c2.html`, porta 8795, salva em `decisoes-c2.json`.
- 13/11 ~22h10: corte 3 (47:41, -16,0 LUFS): START=232.4, o episódio começa no "Bruno, você tá bem hoje?" a pedido dele. Resto igual ao corte 2 (deslocado -2:37).
- corte 4 (47:41): sininho movido pra 2636.85 (fim natural do "galera"; antes cortava a palavra a -21 dB) com fade-in de 0,35 s (5º item opcional do SFX no edit.py).
- corte 5 (47:41): alerta do Christmas em 2633.12 (fim do "s"; antes sobrava o "s"); sininho com fade-in de 1 s e -3 dB.
- APROVADO o corte 5 (13/11, ~22h30). Próximo: /publicar-episodio-vtnsc.
