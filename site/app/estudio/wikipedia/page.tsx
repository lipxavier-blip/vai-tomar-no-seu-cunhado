import Link from 'next/link'
import { CATEGORY_LABELS } from '@/lib/wiki'
import { getWikiEntries } from '@/lib/wiki-server'

export default async function EstudioWikipediaPage() {
  const entries = await getWikiEntries()

  return (
    <div>
      <div className="flex items-center justify-between mb-10">
        <div>
          <h1 className="text-3xl font-bold mb-2">Wikipedia</h1>
          <p className="text-[var(--muted)]">{entries.length} entrada{entries.length !== 1 ? 's' : ''}</p>
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
        <div className="flex flex-col gap-3">
          {entries.map((entry) => (
            <div
              key={entry.id}
              className="flex items-center justify-between bg-[var(--card)] border border-[var(--border)] rounded-xl px-5 py-4"
            >
              <div>
                <p className="font-medium">{entry.title}</p>
                <p className="text-xs text-[var(--muted)] mt-0.5">
                  {CATEGORY_LABELS[entry.category]}
                </p>
              </div>
              <Link
                href={`/estudio/wikipedia/${entry.slug}/editar`}
                className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
              >
                Editar
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
