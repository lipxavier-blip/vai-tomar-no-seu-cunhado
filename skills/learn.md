# Skill: Learn

Aprende sobre o podcast Vai Tomar no Seu Cunhado a partir de informações passadas pelo Felipe ou pelo Bruno.

## Quando usar

Use esta skill quando quiser registrar:
- Contexto de um episódio gravado ou planejado
- Decisões sobre o formato do podcast
- Preferências dos hosts sobre conteúdo, plataformas ou estilo
- Histórias ou referências internas (piadas recorrentes, apelidos, etc.)
- Feedback recebido de ouvintes

## Como funciona

Ao invocar esta skill com uma informação nova, o Claude vai:

1. **Identificar** o tipo da informação (episódio, decisão, feedback, ideia, referência)
2. **Salvar** um arquivo de memória em `memory/`
3. **Atualizar** o índice em `memory.md`

## Estrutura dos arquivos de memória

```markdown
---
name: nome descritivo
type: episodio | decisao | feedback | ideia | referencia
date: YYYY-MM-DD
---

Conteúdo da memória aqui.
```

## Exemplos de uso

**Episódio gravado:**
> "Gravamos um episódio sobre churrasco de família onde o Bruno queimou a picanha."

→ Salva em `memory/ep_churrasco_picanha.md`

**Decisão de formato:**
> "Decidimos que os episódios vão ter no máximo 40 minutos."

→ Salva em `memory/decisao_duracao_episodios.md`

**Referência interna:**
> "A piada do 'contrato' é uma referência ao fato de que viramos cunhados sem escolha."

→ Salva em `memory/referencia_contrato.md`
