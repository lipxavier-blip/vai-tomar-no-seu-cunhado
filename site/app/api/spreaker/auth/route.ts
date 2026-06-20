import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'
import crypto from 'crypto'

export async function GET(req: NextRequest) {
  const bootstrap = req.nextUrl.searchParams.get('bootstrap')
  if (!bootstrap || bootstrap !== process.env.SPREAKER_BOOTSTRAP_SECRET) {
    return new Response('Not found', { status: 404 })
  }

  const state = crypto.randomBytes(16).toString('hex')
  const cookieStore = await cookies()
  cookieStore.set('spreaker_oauth_state', state, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 600,
    path: '/',
  })

  const authorizeUrl = new URL('https://www.spreaker.com/oauth2/authorize')
  authorizeUrl.searchParams.set('client_id', process.env.SPREAKER_CLIENT_ID!)
  authorizeUrl.searchParams.set('response_type', 'code')
  authorizeUrl.searchParams.set('scope', 'basic')
  authorizeUrl.searchParams.set('redirect_uri', process.env.SPREAKER_REDIRECT_URI!)
  authorizeUrl.searchParams.set('state', state)

  return NextResponse.redirect(authorizeUrl.toString())
}
