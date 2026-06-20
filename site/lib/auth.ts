import { cookies } from 'next/headers'

export const AUTH_COOKIE = 'vtsc_auth'

export async function isAuthenticated(): Promise<boolean> {
  const store = await cookies()
  const cookie = store.get(AUTH_COOKIE)?.value
  return !!cookie && cookie === process.env.VTSC_AUTH_TOKEN
}
