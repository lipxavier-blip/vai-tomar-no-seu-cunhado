'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { createClient } from '@/lib/supabase/client'
import { CATEGORY_LABELS, WikiCategory, WikiEntry } from '@/lib/wiki'

interface Props {
  entry: WikiEntry
}

export default function EditarWikiForm({ entry }: Props) {
  const router = useRouter()
  const [title, setTitle] = useState(entry.title)
  const [category, setCategory] = useState<WikiCategory>(entry.category)
  const [content, setContent] = useState(entry.content)
  const [loading, setLoading] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')

    const supabase = createClient()
    const { error: err } = await supabase
      .from('wiki_entries')
      .update({ title, category, content })
      .eq('id', entry.id)

    setLoading(false)
    if (err) {
      setError(err.message)
      return
    }
    router.push('/estudio/wikipedia')
    router.refresh()
  }

  async function handleDelete() {
    if (!confirm(`Deletar "${entry.title}"? Isso não tem volta.`)) return
    setDeleting(true)

    const supabase = createClient()
    await supabase.from('wiki_entries').delete().eq('id', entry.id)

    router.push('/estudio/wikipedia')
    router.refresh()
  }

  return (
    <div>
      <div className="mb-8">
        <Link
          href="/estudio/wikipedia"
          className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
        >
          ← Wikipedia
        </Link>
        <h1 className="text-3xl font-bold mt-4">Editar entrada</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 max-w-2xl">
        <div>
          <label className="block text-sm font-medium mb-2">Título</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full bg-[var(--card)] border border-[var(--border)] rounded-lg px-4 py-3 text-[var(--foreground)] focus:outline-none focus:border-[var(--accent)] transition-colors"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Categoria</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value as WikiCategory)}
            className="w-full bg-[var(--card)] border border-[var(--border)] rounded-lg px-4 py-3 text-[var(--foreground)] focus:outline-none focus:border-[var(--accent)] transition-colors"
          >
            {(Object.entries(CATEGORY_LABELS) as [WikiCategory, string][]).map(([key, label]) => (
              <option key={key} value={key}>{label}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Conteúdo (Markdown)</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={16}
            className="w-full bg-[var(--card)] border border-[var(--border)] rounded-lg px-4 py-3 text-[var(--foreground)] focus:outline-none focus:border-[var(--accent)] transition-colors font-mono text-sm resize-y"
          />
        </div>

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <div className="flex items-center justify-between">
          <div className="flex gap-3">
            <button
              type="submit"
              disabled={loading}
              className="bg-[var(--accent)] text-white px-6 py-3 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {loading ? 'Salvando...' : 'Salvar'}
            </button>
            <Link
              href="/estudio/wikipedia"
              className="px-6 py-3 rounded-lg text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
            >
              Cancelar
            </Link>
          </div>
          <button
            type="button"
            onClick={handleDelete}
            disabled={deleting}
            className="text-xs text-[var(--muted)] hover:text-red-400 transition-colors disabled:opacity-50"
          >
            {deleting ? 'Deletando...' : 'Deletar entrada'}
          </button>
        </div>
      </form>
    </div>
  )
}
