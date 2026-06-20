import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'
import { AUTH_COOKIE } from '@/lib/auth'

export async function POST(req: NextRequest) {
  const { password } = await req.json().catch(() => ({ password: '' }))
  if (!password || password !== process.env.VTSC_PASSWORD) {
    return NextResponse.json({ error: 'senha inválida' }, { status: 401 })
  }
  const store = await cookies()
  store.set(AUTH_COOKIE, process.env.VTSC_AUTH_TOKEN!, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 90,
    path: '/',
  })
  return NextResponse.json({ ok: true })
}
