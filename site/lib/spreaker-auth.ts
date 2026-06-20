let cachedToken: { value: string; expiresAt: number } | null = null

async function refreshAccessToken(): Promise<string> {
  const res = await fetch('https://api.spreaker.com/oauth2/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      client_id: process.env.SPREAKER_CLIENT_ID!,
      client_secret: process.env.SPREAKER_CLIENT_SECRET!,
      refresh_token: process.env.SPREAKER_REFRESH_TOKEN!,
    }),
    cache: 'no-store',
  })
  if (!res.ok) throw new Error(`Spreaker refresh falhou: ${res.status}`)
  const data = await res.json()
  cachedToken = {
    value: data.access_token,
    expiresAt: Date.now() + (data.expires_in - 300) * 1000,
  }
  return data.access_token
}

export async function getSpreakerAccessToken(): Promise<string> {
  if (cachedToken && cachedToken.expiresAt > Date.now()) return cachedToken.value
  const envToken = process.env.SPREAKER_ACCESS_TOKEN
  if (envToken && !cachedToken) {
    cachedToken = { value: envToken, expiresAt: Date.now() + 6 * 60 * 60 * 1000 }
    return envToken
  }
  return refreshAccessToken()
}

export async function invalidateAccessToken(): Promise<string> {
  cachedToken = null
  return refreshAccessToken()
}
