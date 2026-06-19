import { createClient } from '@/lib/supabase/server'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'
import crypto from 'crypto'

export async function GET() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return NextResponse.redirect(new URL('/login', process.env.SPREAKER_REDIRECT_URI!))

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
