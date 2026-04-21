import Link from 'next/link'
import Nav from '@/components/Nav'
import { getEpisode, formatDuration, formatDate } from '@/lib/spreaker'

interface Props {
  params: Promise<{ episodeId: string }>
}

export async function generateMetadata({ params }: Props) {
  const { episodeId } = await params
  const episode = await getEpisode(Number(episodeId))
  return { title: `${episode.title} — Vai Tomar no Seu Cunhado` }
}

export default async function EpisodePage({ params }: Props) {
  const { episodeId } = await params
  const episode = await getEpisode(Number(episodeId))

  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 px-6 py-12 max-w-2xl mx-auto w-full">
        <Link
          href="/episodios"
          className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors mb-8 inline-block"
        >
          ← Todos os episódios
        </Link>

        <h1 className="text-2xl font-bold mb-2">{episode.title}</h1>
        <p className="text-xs text-[var(--muted)] mb-8">
          {formatDate(episode.published_at)} · {formatDuration(episode.duration)}
        </p>

        {/* Player embed */}
        <div className="mb-8">
          <iframe
            src={`https://widget.spreaker.com/player?episode_id=${episode.episode_id}&theme=dark&playlist=false&cover_image_url=${encodeURIComponent(episode.image_url)}`}
            width="100%"
            height="200px"
            style={{ border: 'none', borderRadius: '12px' }}
          />
        </div>

        {/* Descrição */}
        {episode.description && (
          <div className="text-[var(--muted)] text-sm leading-relaxed whitespace-pre-line">
            {episode.description}
          </div>
        )}
      </main>
    </div>
  )
}
