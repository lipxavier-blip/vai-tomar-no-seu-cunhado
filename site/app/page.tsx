import Link from 'next/link'
import Image from 'next/image'
import Nav from '@/components/Nav'
import { getEpisode, getEpisodes, formatDuration, formatDate, formatPlays } from '@/lib/spreaker'

export default async function Home() {
  const episodes = await getEpisodes()
  const latest = episodes[0] ? await getEpisode(episodes[0].episode_id) : null

  return (
    <div className="min-h-screen flex flex-col">
      <Nav />

      <main className="flex-1">
        {/* Hero */}
        <section className="px-6 py-20 max-w-4xl mx-auto">
          <p className="text-xs uppercase tracking-widest text-[var(--accent)] mb-4">
            Podcast
          </p>
          <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6">
            Vai tomar no
            <br />
            <span className="text-[var(--accent)]">seu cunhado</span>
          </h1>
          <p className="text-[var(--muted)] text-lg max-w-xl mb-8">
            Um podcast sobre nada. Dois cunhados jogando conversa fora — com
            amor, mas se recusam a assumir isso.
          </p>
          <div className="flex items-center gap-4">
            <Link
              href="/episodios"
              className="bg-[var(--accent)] text-white px-6 py-3 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity"
            >
              Ver episódios
            </Link>
            <Link
              href="/sobre"
              className="text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
            >
              Quem somos →
            </Link>
          </div>
        </section>

        {/* Último episódio */}
        {latest && (
          <section className="px-6 pb-20 max-w-4xl mx-auto">
            <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-6">
              Último episódio
            </p>
            <Link
              href={`/episodios/${latest.episode_id}`}
              className="flex gap-5 bg-[var(--card)] border border-[var(--border)] rounded-xl p-5 hover:border-[var(--accent)] transition-colors group"
            >
              <div className="shrink-0">
                <Image
                  src={latest.image_url}
                  alt={latest.title}
                  width={80}
                  height={80}
                  className="rounded-lg"
                />
              </div>
              <div className="min-w-0">
                <h2 className="font-semibold group-hover:text-[var(--accent)] transition-colors mb-1 truncate">
                  {latest.title}
                </h2>
                <p className="text-xs text-[var(--muted)]">
                  {formatDate(latest.published_at)} · {formatDuration(latest.duration)}
                  {formatPlays(latest.downloads_count) && ` · ${formatPlays(latest.downloads_count)}`}
                </p>
              </div>
            </Link>
          </section>
        )}
      </main>

      <footer className="border-t border-[var(--border)] px-6 py-6 text-center text-xs text-[var(--muted)]">
        <a
          href="https://www.instagram.com/vaitomarnoseucunhado/"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-[var(--foreground)] transition-colors"
        >
          @vaitomarnoseucunhado
        </a>
      </footer>
    </div>
  )
}
