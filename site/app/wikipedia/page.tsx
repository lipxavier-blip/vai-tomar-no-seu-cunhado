import Nav from '@/components/Nav'
import WikiIndex from '@/components/WikiIndex'
import { getWikiEntries } from '@/lib/wiki-server'

export const metadata = {
  title: 'Wikipedia — Vai Tomar no Seu Cunhado',
}

export default async function WikipediaPage() {
  const entries = await getWikiEntries()

  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 px-6 py-12 max-w-4xl mx-auto w-full">
        <h1 className="text-3xl font-bold mb-2">Wikipedia</h1>
        <p className="text-[var(--muted)] mb-8">
          A enciclopédia não oficial de tudo que já aconteceu nesse podcast.
        </p>

        {entries.length === 0 ? (
          <div className="text-center py-20 text-[var(--muted)]">
            Nenhuma entrada ainda. Em breve.
          </div>
        ) : (
          <WikiIndex entries={entries} />
        )}
      </main>
    </div>
  )
}
