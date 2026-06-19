import { createClient } from '@/lib/supabase/server'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(req: NextRequest) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return new Response('Unauthorized', { status: 401 })

  const code = req.nextUrl.searchParams.get('code')
  const state = req.nextUrl.searchParams.get('state')
  const error = req.nextUrl.searchParams.get('error')

  if (error) return new Response(`Spreaker retornou erro: ${error}`, { status: 400 })
  if (!code || !state) return new Response('code/state ausentes', { status: 400 })

  const cookieStore = await cookies()
  const expectedState = cookieStore.get('spreaker_oauth_state')?.value
  if (state !== expectedState) return new Response('state inválido (possível CSRF)', { status: 400 })
  cookieStore.delete('spreaker_oauth_state')

  const tokenRes = await fetch('https://api.spreaker.com/oauth2/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      client_id: process.env.SPREAKER_CLIENT_ID!,
      client_secret: process.env.SPREAKER_CLIENT_SECRET!,
      redirect_uri: process.env.SPREAKER_REDIRECT_URI!,
      code,
    }),
  })

  const tokenData = await tokenRes.json()
  if (!tokenRes.ok) {
    return new Response(`Token exchange falhou: ${JSON.stringify(tokenData)}`, { status: 500 })
  }

  const html = `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Spreaker conectado</title>
<style>
  body { font-family: ui-monospace, monospace; background: #0a0a0a; color: #e5e5e5; padding: 2rem; max-width: 760px; margin: 0 auto; }
  h1 { color: #f5b400; }
  pre { background: #1a1a1a; padding: 1rem; border-radius: 8px; overflow-x: auto; word-break: break-all; white-space: pre-wrap; }
  .warn { background: #3a1f1f; border: 1px solid #6a3030; padding: 1rem; border-radius: 8px; margin-top: 1rem; }
</style></head>
<body>
  <h1>Spreaker conectado ✓</h1>
  <p>Copia o <code>refresh_token</code> abaixo e cola pro Claude. Esse token é de longa duração e será usado pra renovar o access_token automaticamente.</p>
  <pre>${JSON.stringify(tokenData, null, 2)}</pre>
  <div class="warn">Não compartilhe esse token publicamente. Depois de capturado, essa rota deveria ser desativada.</div>
</body></html>`

  return new Response(html, { headers: { 'Content-Type': 'text/html; charset=utf-8' } })
}
