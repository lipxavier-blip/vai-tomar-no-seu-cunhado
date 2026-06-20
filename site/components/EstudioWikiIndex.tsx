'use client'

import { useState, useMemo } from 'react'
import Link from 'next/link'
import { CATEGORY_LABELS, WikiCategory, WikiEntry } from '@/lib/wiki'

const CATEGORY_ORDER: WikiCategory[] = ['episodios', 'personagens', 'piadas', 'temas', 'historia']

export default function EstudioWikiIndex({ entries }: { entries: WikiEntry[] }) {
  const [activeTab, setActiveTab] = useState<WikiCategory>('episodios')
  const [query, setQuery] = useState('')

  const availableTabs = useMemo(
    () => CATEGORY_ORDER.filter((cat) => entries.some((e) => e.category === cat)),
    [entries]
  )

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return entries.filter(
      (e) => e.category === activeTab && (q === '' || e.title.toLowerCase().includes(q))
    )
  }, [entries, activeTab, query])

  return (
    <div>
      {/* Tabs */}
      <div className="flex overflow-x-auto border-b border-[var(--border)] mb-5 -mx-6 px-6">
        {availableTabs.map((cat) => (
          <button
            key={cat}
            onClick={() => { setActiveTab(cat); setQuery('') }}
            className={`shrink-0 px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
              activeTab === cat
                ? 'border-[var(--accent)] text-[var(--accent)]'
                : 'border-transparent text-[var(--muted)] hover:text-[var(--foreground)]'
            }`}
          >
            {CATEGORY_LABELS[cat]}
          </button>
        ))}
      </div>

      {/* Search */}
      <div className="relative mb-4">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--muted)]"
          width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"
        >
          <circle cx="11" cy="11" r="8" /><path d="M21 21l-4.35-4.35" />
        </svg>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="procura aí..."
          className="w-full bg-[var(--card)] border border-[var(--border)] rounded-lg pl-9 pr-4 py-2.5 text-sm placeholder:text-[var(--muted)] focus:outline-none focus:border-[var(--accent)] transition-colors"
        />
      </div>

      {/* Entries */}
      {filtered.length === 0 ? (
        <p className="text-[var(--muted)] text-sm py-8 text-center">Nenhum resultado.</p>
      ) : (
        <div className="flex flex-col gap-1.5">
          {filtered.map((entry) => (
            <Link
              key={entry.id}
              href={`/estudio/wikipedia/${entry.slug}`}
              className="block bg-[var(--card)] border border-[var(--border)] rounded-xl px-5 py-3.5 text-sm font-medium hover:border-[var(--accent)] hover:text-[var(--accent)] transition-colors"
            >
              {entry.title}
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
