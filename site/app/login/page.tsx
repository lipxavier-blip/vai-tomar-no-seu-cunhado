'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const supabase = createClient()
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      },
    })

    if (error) {
      setError('Algo deu errado. Tenta de novo.')
    } else {
      setSent(true)
    }
    setLoading(false)
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <p className="text-[var(--accent)] text-sm font-medium mb-2">Estúdio</p>
        <h1 className="text-3xl font-bold mb-8">Vai tomar no seu cunhado</h1>

        {sent ? (
          <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-6">
            <p className="font-medium mb-2">Confere seu e-mail</p>
            <p className="text-[var(--muted)] text-sm">
              Mandamos um link para <strong className="text-[var(--foreground)]">{email}</strong>.
              Clica lá para entrar.
            </p>
          </div>
        ) : (
          <form onSubmit={handleLogin} className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <label htmlFor="email" className="text-sm text-[var(--muted)]">
                E-mail
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu@email.com"
                required
                className="bg-[var(--card)] border border-[var(--border)] rounded-lg px-4 py-3 text-[var(--foreground)] placeholder-[var(--muted)] focus:outline-none focus:border-[var(--accent)] transition-colors"
              />
            </div>

            {error && (
              <p className="text-red-400 text-sm">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="bg-[var(--accent)] hover:opacity-90 disabled:opacity-50 text-white font-medium rounded-lg px-4 py-3 transition-opacity"
            >
              {loading ? 'Enviando...' : 'Entrar com magic link'}
            </button>
          </form>
        )}
      </div>
    </main>
  )
}
