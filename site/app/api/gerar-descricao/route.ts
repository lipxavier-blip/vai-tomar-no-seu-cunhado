import { NextRequest } from 'next/server'
import Anthropic from '@anthropic-ai/sdk'
import fs from 'fs'
import path from 'path'

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

const tomDeVoz = fs.readFileSync(
  path.join(process.cwd(), 'content', 'tom-de-voz.md'),
  'utf-8'
)

export async function POST(req: NextRequest) {
  const { titulo, transcricao } = await req.json()

  if (!titulo || !transcricao) {
    return new Response('titulo e transcricao são obrigatórios', { status: 400 })
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    return new Response('ANTHROPIC_API_KEY não configurada no .env.local', { status: 500 })
  }

  const stream = await client.messages.stream({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 1024,
    system: [
      {
        type: 'text',
        text: `Você é um assistente especializado no podcast "Vai Tomar no Seu Cunhado". Seu trabalho é escrever descrições de episódios para publicar no Spreaker.

Aqui está o guia completo de tom de voz do podcast:

${tomDeVoz}

---

INSTRUÇÕES PARA A DESCRIÇÃO:
- Tom: como alguém contando pro amigo do que foi o episódio — casual, direto, com humor
- Estrutura: 2 a 4 parágrafos curtos + CTA + links fixos
- Mencione os assuntos principais e pelo menos uma história ou momento específico do ep
- Use o vocabulário do podcast quando natural (véi, mano, cara, a gente, etc.)
- NÃO use linguagem corporativa, clickbait ou formal
- Termine SEMPRE com exatamente estes dois parágrafos (sem alterar):

Sigam a gente no Instagram: https://www.instagram.com/vaitomarnoseucunhado/

Se você tem uma história ou um comentário mais longo, envie um e-mail para vaitomarnoseucunhado@gmail.com 📬`,
        cache_control: { type: 'ephemeral' },
      },
    ],
    messages: [
      {
        role: 'user',
        content: `Escreva a descrição do episódio "${titulo}" com base na transcrição abaixo.

TRANSCRIÇÃO:
${transcricao}`,
      },
    ],
  })

  const encoder = new TextEncoder()
  const readable = new ReadableStream({
    async start(controller) {
      for await (const chunk of stream) {
        if (
          chunk.type === 'content_block_delta' &&
          chunk.delta.type === 'text_delta'
        ) {
          controller.enqueue(encoder.encode(chunk.delta.text))
        }
      }
      controller.close()
    },
  })

  return new Response(readable, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  })
}
