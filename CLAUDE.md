# Vai Tomar no Seu Cunhado — Instruções do Projeto

## O que é esse projeto

Podcast bem-humorado de Felipe Xavier e Bruno Rezende (cunhados). Conversas livres sobre a vida, família, cultura e tudo o mais. Tom casual, engraçado e genuíno — como uma conversa de varanda no fim de semana.

- **Página:** https://www.spreaker.com/podcast/vai-tomar-no-seu-cunhado--5951420
- **E-mail:** vaitomarnoseucunhado@gmail.com
- **Hosts:** Felipe Xavier e Bruno Rezende

## Tom de voz

- Informal, descontraído, bem-humorado
- Não se leva a sério, mas tem afeto genuíno por trás
- Pode usar gírias e humor ácido — sem exageros
- Referências cotidianas, família, cultura brasileira
- Evitar linguagem corporativa ou formal em qualquer comunicação

## Estrutura do projeto

```
vai-tomar-no-seu-cunhado/
├── CLAUDE.md          # este arquivo — instruções para o Claude
├── memory.md          # índice de memórias do projeto
├── .env.local         # credenciais YouTube OAuth (gitignored)
├── audiograma/
│   └── gerar_audiograma.py  # capa borrada como fundo + capa nítida + onda sonora
├── youtube/
│   ├── gerar_thumbnail.py   # thumbnail 1280x720, mesmo estilo do audiograma
│   ├── upload.py            # upload resumível via Data API v3
│   └── set_thumbnail.py
└── skills/
    ├── tone-checker.md  # skill para verificar tom de conteúdo
    └── learn.md         # skill para aprender sobre o podcast
```

## Publicar episódio

Pipeline completo (descrição → Spreaker → audiograma → YouTube → site) documentado na skill
global `publicar-episodio-vtnsc` (`~/.claude/skills/publicar-episodio-vtnsc/SKILL.md`).

## Regras gerais

- Sempre usar o tom de voz descrito acima em qualquer texto gerado
- Commits em português, diretos e sem formalidade
- Após alterações, commitar e fazer push
- Ao sugerir conteúdo para episódios, pensar em temas que os dois possam discutir com propriedade e humor
