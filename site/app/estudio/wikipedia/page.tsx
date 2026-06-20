import { getWikiEntries } from '@/lib/wiki-server'
import EstudioWikiIndex from '@/components/EstudioWikiIndex'

export default async function EstudioWikipediaPage() {
  const entries = await getWikiEntries()

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Wikipedia</h1>
        <p className="text-[var(--muted)]">{entries.length} entrada{entries.length !== 1 ? 's' : ''}</p>
      </div>

      <EstudioWikiIndex entries={entries} />
    </div>
  )
}
