'use client'

import { useState } from 'react'

export default function GeradorPage() {
  const [titulo, setTitulo] = useState('')
  const [transcricao, setTranscricao] = useState('')
  const [descricao, setDescricao] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  async function handleGerar(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    setDescricao('')
    setCopied(false)

    try {
      const res = await fetch('/api/gerar-descricao', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ titulo, transcricao }),
      })

      if (!res.ok) {
        const msg = await res.text()
        setError(msg)
        setLoading(false)
        return
      }

      const reader = res.body!.getReader()
      const decoder = new TextDecoder()
      let result = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        const chunk = decoder.decode(value, { stream: true })
        result += chunk
        setDescricao(result)
      }
    } catch {
      setError('Erro ao conectar com a API. Tente novamente.')
    }

    setLoading(false)
  }

  async function handleCopiar() {
    await navigator.clipboard.writeText(descricao)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div>
      <div className="mb-10">
        <h1 className="text-3xl font-bold mb-2">Gerador de descrições</h1>
        <p className="text-[var(--muted)]">
          Cole a transcrição e receba a descrição pronta para o Spreaker.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Formulário */}
        <form onSubmit={handleGerar} className="space-y-5">
          <div>
            <label className="block text-sm font-medium mb-2">Título do episódio</label>
            <input
              type="text"
              value={titulo}
              onChange={(e) => setTitulo(e.target.value)}
              required
              placeholder="Ex: 76 - O nome do episódio"
              className="w-full bg-[var(--card)] border border-[var(--border)] rounded-lg px-4 py-3 text-[var(--foreground)] focus:outline-none focus:border-[var(--accent)] transition-colors"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Transcrição</label>
            <textarea
              value={transcricao}
              onChange={(e) => setTranscricao(e.target.value)}
              required
              rows={18}
              placeholder="Cole aqui a transcrição gerada pelo Whisper..."
              className="w-full bg-[var(--card)] border border-[var(--border)] rounded-lg px-4 py-3 text-[var(--foreground)] focus:outline-none focus:border-[var(--accent)] transition-colors font-mono text-sm resize-y"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[var(--accent)] text-white px-6 py-3 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {loading ? 'Gerando...' : 'Gerar descrição'}
          </button>

          {error && (
            <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-lg">{error}</p>
          )}
        </form>

        {/* Resultado */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="block text-sm font-medium">Descrição gerada</label>
            {descricao && (
              <button
                onClick={handleCopiar}
                className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
              >
                {copied ? 'Copiado ✓' : 'Copiar'}
              </button>
            )}
          </div>
          <textarea
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
            rows={24}
            placeholder={loading ? 'Gerando...' : 'A descrição aparece aqui — você pode editar antes de copiar.'}
            className="w-full bg-[var(--card)] border border-[var(--border)] rounded-lg px-4 py-3 text-[var(--foreground)] focus:outline-none focus:border-[var(--accent)] transition-colors text-sm resize-y"
          />
        </div>
      </div>
    </div>
  )
}
