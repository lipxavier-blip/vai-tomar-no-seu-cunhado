import Link from 'next/link'
import Image from 'next/image'
import Nav from '@/components/Nav'
import { getEpisodesWithStats, formatDuration, formatDate, formatPlays } from '@/lib/spreaker'

export const metadata = {
  title: 'Episódios — Vai Tomar no Seu Cunhado',
}

export default async function EpisodiosPage() {
  const episodes = await getEpisodesWithStats()

  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 px-6 py-12 max-w-4xl mx-auto w-full">
        <h1 className="text-3xl font-bold mb-2">Episódios</h1>
        <p className="text-[var(--muted)] mb-10">{episodes.length} episódios no total</p>

        <div className="flex flex-col gap-3">
          {episodes.map((ep) => (
            <Link
              key={ep.episode_id}
              href={`/episodios/${ep.episode_id}`}
              className="flex items-center gap-4 bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 hover:border-[var(--accent)] transition-colors group"
            >
              <div className="shrink-0">
                <Image
                  src={ep.image_url}
                  alt={ep.title}
                  width={56}
                  height={56}
                  className="rounded-lg"
                />
              </div>
              <div className="flex-1 min-w-0">
                <h2 className="font-medium group-hover:text-[var(--accent)] transition-colors truncate">
                  {ep.title}
                </h2>
                <p className="text-xs text-[var(--muted)] mt-0.5">
                  {formatDate(ep.published_at)} · {formatDuration(ep.duration)}
                  {formatPlays(ep.downloads_count) && ` · ${formatPlays(ep.downloads_count)}`}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </main>
    </div>
  )
}
