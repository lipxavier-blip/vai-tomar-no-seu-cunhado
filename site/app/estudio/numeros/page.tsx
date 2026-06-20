import Image from 'next/image'
import { getEpisodesWithStats, formatDate } from '@/lib/spreaker'

export const metadata = { title: 'Números — Estúdio' }

function fmt(n: number | undefined): string {
  if (n == null) return '—'
  return n.toLocaleString('pt-BR')
}

export default async function NumerosPage() {
  const episodes = await getEpisodesWithStats()

  const totalDownloads = episodes.reduce((sum, ep) => sum + (ep.downloads_count ?? 0), 0)
  const totalPlays = episodes.reduce((sum, ep) => sum + (ep.plays_count ?? 0), 0)
  const sorted = [...episodes].sort(
    (a, b) => (b.downloads_count ?? 0) - (a.downloads_count ?? 0)
  )

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Números</h1>
        <p className="text-[var(--muted)]">
          Downloads e plays por episódio, direto da API do Spreaker.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-2">Episódios</p>
          <p className="text-3xl font-bold">{episodes.length}</p>
        </div>
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-2">Downloads totais</p>
          <p className="text-3xl font-bold">{fmt(totalDownloads)}</p>
        </div>
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-2">Plays totais</p>
          <p className="text-3xl font-bold">{fmt(totalPlays)}</p>
        </div>
      </div>

      <div className="flex flex-col gap-2">
        {sorted.map((ep, i) => (
          <div
            key={ep.episode_id}
            className="flex items-center gap-4 bg-[var(--card)] border border-[var(--border)] rounded-xl p-4"
          >
            <span className="text-xs text-[var(--muted)] w-6 shrink-0 text-right tabular-nums">
              {i + 1}
            </span>
            <Image
              src={ep.image_url}
              alt={ep.title}
              width={40}
              height={40}
              className="rounded shrink-0"
            />
            <div className="flex-1 min-w-0">
              <p className="font-medium text-sm truncate">{ep.title}</p>
              <p className="text-xs text-[var(--muted)]">{formatDate(ep.published_at)}</p>
            </div>
            <div className="text-right shrink-0">
              <p className="text-sm font-semibold tabular-nums">{fmt(ep.downloads_count)}</p>
              <p className="text-xs text-[var(--muted)] tabular-nums">{fmt(ep.plays_count)} plays</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
