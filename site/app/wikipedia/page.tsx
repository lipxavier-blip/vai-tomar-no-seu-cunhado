import Link from 'next/link'
import Nav from '@/components/Nav'
import { CATEGORY_LABELS, WikiCategory } from '@/lib/wiki'
import { getWikiEntries } from '@/lib/wiki-server'

export const metadata = {
  title: 'Wikipedia — Vai Tomar no Seu Cunhado',
}

export default async function WikipediaPage() {
  const entries = await getWikiEntries()

  const byCategory = entries.reduce<Record<WikiCategory, typeof entries>>((acc, entry) => {
    if (!acc[entry.category]) acc[entry.category] = []
    acc[entry.category].push(entry)
    return acc
  }, {} as Record<WikiCategory, typeof entries>)

  const hasEntries = entries.length > 0

  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 px-6 py-12 max-w-4xl mx-auto w-full">
        <h1 className="text-3xl font-bold mb-2">Wikipedia</h1>
        <p className="text-[var(--muted)] mb-12">
          A enciclopédia não oficial de tudo que já aconteceu nesse podcast.
        </p>

        {!hasEntries ? (
          <div className="text-center py-20 text-[var(--muted)]">
            Nenhuma entrada ainda. Em breve.
          </div>
        ) : (
          <div className="space-y-12">
            {(Object.keys(CATEGORY_LABELS) as WikiCategory[]).map((category) => {
              const items = byCategory[category]
              if (!items || items.length === 0) return null
              return (
                <section key={category}>
                  <h2 className="text-xs uppercase tracking-widest text-[var(--accent)] mb-4">
                    {CATEGORY_LABELS[category]}
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {items.map((entry) => (
                      <Link
                        key={entry.id}
                        href={`/wikipedia/${entry.slug}`}
                        className="bg-[var(--card)] border border-[var(--border)] rounded-xl px-5 py-4 hover:border-[var(--accent)] transition-colors group"
                      >
                        <h3 className="font-medium group-hover:text-[var(--accent)] transition-colors">
                          {entry.title}
                        </h3>
                      </Link>
                    ))}
                  </div>
                </section>
              )
            })}
          </div>
        )}
      </main>
    </div>
  )
}
