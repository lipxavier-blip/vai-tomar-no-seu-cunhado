import Link from 'next/link'
import { CATEGORY_LABELS, WikiCategory, WikiEntry } from '@/lib/wiki'
import { getWikiEntries } from '@/lib/wiki-server'
import RefreshButton from '@/components/RefreshButton'

const CATEGORY_ORDER: WikiCategory[] = ['episodios', 'personagens', 'piadas', 'temas', 'historia']

export default async function EstudioWikipediaPage() {
  const entries = await getWikiEntries()

  const grouped = CATEGORY_ORDER.reduce<Record<WikiCategory, WikiEntry[]>>(
    (acc, cat) => {
      acc[cat] = entries.filter((e) => e.category === cat)
      return acc
    },
    {} as Record<WikiCategory, WikiEntry[]>
  )

  const activeCategories = CATEGORY_ORDER.filter((cat) => grouped[cat].length > 0)

  return (
    <div>
      <div className="flex items-center justify-between mb-10">
        <div>
          <h1 className="text-3xl font-bold mb-2">Wikipedia</h1>
          <div className="flex items-center gap-2 mt-1">
            <p className="text-[var(--muted)]">{entries.length} entrada{entries.length !== 1 ? 's' : ''}</p>
            <RefreshButton />
          </div>
        </div>
        <Link
          href="/estudio/wikipedia/nova"
          className="bg-[var(--accent)] text-white px-4 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity"
        >
          Nova entrada
        </Link>
      </div>

      {entries.length === 0 ? (
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-12 text-center text-[var(--muted)]">
          Nenhuma entrada ainda.{' '}
          <Link href="/estudio/wikipedia/nova" className="text-[var(--accent)] hover:underline">
            Criar a primeira
          </Link>
        </div>
      ) : (
        <div className="flex flex-col gap-10">
          {activeCategories.map((cat) => (
            <section key={cat}>
              <h2 className="text-[10px] font-bold uppercase tracking-widest text-[var(--accent)] mb-3 pb-2 border-b border-[var(--border)]">
                {CATEGORY_LABELS[cat]}
              </h2>
              <div className="flex flex-col gap-2">
                {grouped[cat].map((entry) => (
                  <div
                    key={entry.id}
                    className="flex items-center justify-between bg-[var(--card)] border border-[var(--border)] rounded-xl px-5 py-4"
                  >
                    <Link href={`/estudio/wikipedia/${entry.slug}`} className="flex-1 min-w-0">
                      <p className="font-medium hover:text-[var(--accent)] transition-colors">{entry.title}</p>
                    </Link>
                    <Link
                      href={`/estudio/wikipedia/${entry.slug}/editar`}
                      className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors ml-4 shrink-0"
                    >
                      Editar
                    </Link>
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  )
}
