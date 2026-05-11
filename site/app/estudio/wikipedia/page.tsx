import Link from 'next/link'
import { getWikiEntries } from '@/lib/wiki-server'
import RefreshButton from '@/components/RefreshButton'
import EstudioWikiIndex from '@/components/EstudioWikiIndex'

export default async function EstudioWikipediaPage() {
  const entries = await getWikiEntries()

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">Wikipedia</h1>
          <div className="flex items-center gap-2">
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
        <EstudioWikiIndex entries={entries} />
      )}
    </div>
  )
}
