# Ep 83: onde parou (19/11/2026, noite)

## Pronto, em disco
- Vozes: `fel_p/bru_p` (Bruno bruto -32,9 LUFS → +12 dB antes do compressor) e `fel_d/bru_d` (nf -70/-74; apito do Bruno agora em 2/4/6 kHz, notch Q30).
- Whisper: `words_fel.json`, `words_bru.json`. Pausas `gaps.npy`, energia `E10_*.npy`.
- Finos: 90 verificados → 17 aceitos → 15 na página (tirei 825.6, dentro do grito, e 2611, o "é..." da piada do grilo).
- `ruidos.py` rodando/rodado depois do verifica (ruidos.json → mudos.py → FAIXA=m).
- Página: `aprovacao/aprovacao.html` (gerada por `aprovacao/gen.py`), porta 8796, salva em `aprovacao/decisoes.json`, localStorage `vtnsc-ep83`.
  Subir de novo: `cd aprovacao && nohup python3 ../../servidor_aprovacao.py aprovacao.html decisoes.json 8796 &` e `open http://127.0.0.1:8796/`.

## Tempos (Riverside, s)
- START 27.0 (opção 24.5); fim: "Tchau" do Bruno 3482.5; TCHAU_AT ~3482.0; "sobe o som" 3458.2; Ed Motta 3470–3480.
- Vinheta: INTRO_SPLIT 827.55 (fel; bru acaba 826.75), INTRO_LEAD 0.8.
- Cortes: Paula 2502.85–2550.0 (certo); dúvida 3053.7–3084.7 ou só 3082.8–3084.7 ("essa parte você corta").
- Segura na mão de Deus: pedido termina 804.8. Grilo: silêncio 2612.5–2616.4 (Felipe "esqueceu" 2616.5).
- Alertas: Yes sir fim ~953.0; Umbrella fim ~1258.9 (Felipe canta "ella" até 1261.4); war room ~1612.4; manager ~1233.0.
- Blocos: 827.55 feriado (papo solto) · 905.4 trabalho na gringa · 3301.9 contatos/tchau.

## 19/11 ~20h: corte 1 pronto, esperando ele ouvir inteiro
- Mapa e finos aprovados (aprovacao/decisoes.json); grito sincronizado na linha do tempo (aprovacao/grito.html → decisoes-grito.json → grito.py).
- Faixas: fel_d/bru_d → mudos (decide_mudos.py → mudos.json → mudos.py → *_m) → grito.py (F=m) → *_g. Render: `EP=83 V=1 FAIXA=g nice -n 19 bash master.sh`.
- Corte 1: 56:46, -16,0 LUFS, -2,0 dBTP, Cozy 27,1 dB abaixo da fala (BED_BELOW 29). Prévias aprovadas (decisoes-p1.json), saída v2 com Vamos Dançar a partir de 0:20.
- Página do corte inteiro: aprovacao/corte1.html, porta 8799, salva em decisoes-c1.json (minuto + o que mudar; "aprovo"). Minuto do corte → Riverside pelo mapping do mapa.json.
- Créditos em creditos-ep-83.md (Segura na mão de Deus e Vamos Dançar do YouTube, claim não se contesta).

## 19/11 ~21h: corte 2 (EQ + pausas)
- EQ "Compressed Vocal" do GarageBand do Felipe nas duas faixas (stems.sh); nf da limpeza -69/-73.
- Pausas medidas nas faixas finais (gaps_g.npy); acima de 0,9 s ficam com 0,5 s (GAP_MIN/GAP_LEFT no edit.py), protegendo grilo, vinheta e ±1 s dos alertas/efeitos.
- Corte 2: 55:45, -16,0 LUFS, -2,2 dBTP, Cozy 27,3 dB abaixo da fala. Mapa do corte 1 guardado em mapa_c1.json (edit_c1.py) pra converter os minutos que ele der do corte 1.

## Pra amanhã (20/11): ele ouve o corte 2 e aprova ou pede mudanças
- Ouvir: `~/Podcasts/Vai Tomar no Seu Cunhado/Temporada 6/83/Episódio 83 - corte 2 (normalizado).mp3` (Finder/QuickTime). Prévias em `prévias corte 2/` (segura 12:19, vinheta 12:42, alertas 14:56/19:34/20:02, grilo 41:33, saída 54:17).
- Mudanças chegam pelo chat, com minuto. Perguntar de qual corte é o minuto: corte 2 → `mapa.json`; corte 1 → `mapa_c1.json`.
- Aplicar no topo do `edit.py` e renderizar `EP=83 V=3 FAIXA=g nice -n 19 bash master.sh` (avisar antes, é pesado); conferir -16 LUFS, pico ≤ -1,5 dBTP e Cozy entre -27 e -28 dB; prévias novas só se mexer em vinheta, alerta, efeito ou saída.
- Servidores das páginas (se o Mac reiniciar, subir de novo de dentro de `aprovacao/` com `nohup python3 ../../servidor_aprovacao.py <pagina> <json> <porta> &`):
  8796 aprovacao.html/decisoes.json · 8797 grito.html/decisoes-grito.json · 8798 previas1.html/decisoes-p1.json · 8799 corte1.html/decisoes-c1.json. O servidor agora aceita Range (o player pula pro meio do mp3).
- Depois da aprovação: apagar cortes e prévias antigos só com o ok dele (Lixeira); título e descrição em página HTML → `descricao-ep-83.md`; fechar `creditos-ep-83.md`; `bruno-felipe.txt` → `transcricoes/83-slug/`; commit + push; `/publicar-episodio-vtnsc`.

## 20/11 manhã: corte 3 (grito de volta) + descrição aprovada
- Ele achou o grito cortado: os mudos zeravam o fim do "cunhadoooo" (AST: Wail/Speech). `mudos.py` ganhou PROTEGE 819–829 → mudos → grito.py → corte 3 (55:45, -16,0 LUFS, -2,2 dBTP). mapa do corte 2 em mapa_c2.json.
- Página aprovacao/descricao.html (porta 8800 → decisoes-descricao.json): título "Trampando pra gringa", descrição, músicas ok, tags salvos → descricao-ep-83.md na raiz. Falta ele salvar o card do grito (corte 3 ok?).
- 20/11 11:43: grito ok, corte 3 APROVADO. Falta: apagar cortes 1-2 e prévias antigas (só com ok dele) e /publicar-episodio-vtnsc.
- 20/11: pronto pra publicar, falta só a capa (a Paula faz; ele manda e aí roda /publicar-episodio-vtnsc). Apagar cortes 1-2 e prévias antigas: ele não respondeu, perguntar de novo.
