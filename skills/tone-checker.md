# Skill: Tone Checker

Verifica se um texto está alinhado com o tom de voz do podcast Vai Tomar no Seu Cunhado.

## Quando usar

Use esta skill quando quiser validar:
- Descrições de episódios
- Posts para redes sociais
- Títulos de episódios
- Qualquer texto que vá para o público do podcast

## Como funciona

Ao invocar esta skill com um texto, o Claude vai:

1. **Analisar** o texto segundo os critérios abaixo
2. **Apontar** o que está fora do tom (se houver)
3. **Reescrever** sugerindo uma versão mais alinhada

## Critérios de tom

### Deve ter
- Informalidade — como se fosse uma conversa, não um texto
- Humor leve a ácido, sem forçar
- Afeto disfarçado de deboche (a marca do podcast)
- Referências ao cotidiano, família, cultura pop brasileira
- Personalidade — nada genérico

### Não deve ter
- Linguagem corporativa ou de press release
- Elogios excessivos ou autopromocional demais
- Formalidade desnecessária
- Clickbait sem substância
- Emojis em excesso

## Exemplo de uso

**Input:**
> "Neste episódio incrível, Felipe e Bruno discutem de forma profunda e enriquecedora os desafios da vida moderna."

**Output:**
> Tom errado — formal demais e genérico. Sugestão:
> "Felipe e Bruno jogam conversa fora sobre a vida — sem profundidade nenhuma, e tudo bem assim."
