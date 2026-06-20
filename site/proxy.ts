import { NextResponse, type NextRequest } from 'next/server'

const AUTH_COOKIE = 'vtsc_auth'

export function proxy(request: NextRequest) {
  const isAuthed =
    request.cookies.get(AUTH_COOKIE)?.value === process.env.VTSC_AUTH_TOKEN

  if (!isAuthed && request.nextUrl.pathname.startsWith('/estudio')) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  if (isAuthed && request.nextUrl.pathname === '/login') {
    const url = request.nextUrl.clone()
    url.pathname = '/estudio'
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/estudio/:path*', '/login'],
}
