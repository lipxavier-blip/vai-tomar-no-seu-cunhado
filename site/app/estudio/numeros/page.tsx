import Image from 'next/image'
import {
  getEpisodesWithStats,
  getShowStats,
  formatDate,
  type ShowStatPoint,
} from '@/lib/spreaker'

export const metadata = { title: 'Números — Estúdio' }
export const revalidate = 3600

function fmt(n: number | undefined | null): string {
  if (n == null) return '—'
  return n.toLocaleString('pt-BR')
}

function toIsoDate(d: Date): string {
  return d.toISOString().slice(0, 10)
}

function sumDownloads(points: ShowStatPoint[]): number {
  return points.reduce((s, p) => s + (p.downloads_count ?? 0), 0)
}

const SPREAKER_HISTORY_START = '2025-06-01'

export default async function NumerosPage() {
  const today = new Date()
  const last30Start = new Date(today)
  last30Start.setDate(today.getDate() - 29)
  const last7Start = new Date(today)
  last7Start.setDate(today.getDate() - 6)

  const [episodes, daily30, monthly] = await Promise.all([
    getEpisodesWithStats(),
    getShowStats(toIsoDate(last30Start), toIsoDate(today), 'day'),
    getShowStats(SPREAKER_HISTORY_START, toIsoDate(today), 'month'),
  ])

  const totalDownloads = episodes.reduce((sum, ep) => sum + (ep.downloads_count ?? 0), 0)
  const downloads7 = sumDownloads(daily30.slice(-7))
  const downloads30 = sumDownloads(daily30)
  const sorted = [...episodes].sort(
    (a, b) => (b.downloads_count ?? 0) - (a.downloads_count ?? 0)
  )

  const maxMonth = Math.max(1, ...monthly.map((m) => m.downloads_count))
  const maxDay = Math.max(1, ...daily30.map((d) => d.downloads_count))

  const monthLabel = (iso: string) =>
    new Date(iso + 'T12:00:00').toLocaleDateString('pt-BR', { month: 'short' }).replace('.', '')

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Números</h1>
        <p className="text-[var(--muted)]">Downloads do podcast, direto da API do Spreaker.</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-10">
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-2">Total</p>
          <p className="text-2xl font-bold tabular-nums">{fmt(totalDownloads)}</p>
        </div>
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-2">Últimos 30d</p>
          <p className="text-2xl font-bold tabular-nums">{fmt(downloads30)}</p>
        </div>
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-2">Últimos 7d</p>
          <p className="text-2xl font-bold tabular-nums">{fmt(downloads7)}</p>
        </div>
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-2">Média por ep</p>
          <p className="text-2xl font-bold tabular-nums">
            {fmt(Math.round(totalDownloads / Math.max(episodes.length, 1)))}
          </p>
        </div>
      </div>

      {monthly.length > 0 && (
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5 mb-6">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-4">
            Downloads por mês ({monthly.length} {monthly.length === 1 ? 'mês' : 'meses'})
          </p>
          <div className="flex items-end gap-1.5 h-40">
            {monthly.map((m) => {
              const h = (m.downloads_count / maxMonth) * 100
              return (
                <div key={m.date} className="flex-1 flex flex-col items-center gap-1 min-w-0">
                  <div className="text-[10px] text-[var(--muted)] tabular-nums">
                    {m.downloads_count > 0 ? m.downloads_count : ''}
                  </div>
                  <div
                    className="w-full bg-[var(--accent)] rounded-t opacity-90 hover:opacity-100 transition-opacity"
                    style={{ height: `${Math.max(h, 2)}%` }}
                    title={`${m.date}: ${m.downloads_count} downloads`}
                  />
                  <div className="text-[10px] text-[var(--muted)] truncate w-full text-center">
                    {monthLabel(m.date)}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {daily30.length > 0 && (
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5 mb-10">
          <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-4">
            Downloads por dia (últimos 30)
          </p>
          <div className="flex items-end gap-0.5 h-32">
            {daily30.map((d) => {
              const h = (d.downloads_count / maxDay) * 100
              return (
                <div
                  key={d.date}
                  className="flex-1 bg-[var(--accent)] rounded-t opacity-80 hover:opacity-100 transition-opacity min-w-0"
                  style={{ height: `${Math.max(h, 2)}%` }}
                  title={`${d.date}: ${d.downloads_count} downloads`}
                />
              )
            })}
          </div>
          <div className="flex justify-between text-[10px] text-[var(--muted)] mt-2">
            <span>{daily30[0]?.date}</span>
            <span>{daily30[daily30.length - 1]?.date}</span>
          </div>
        </div>
      )}

      <p className="text-xs uppercase tracking-widest text-[var(--muted)] mb-3">
        Ranking por episódio
      </p>
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
              {ep.plays_count != null && ep.plays_count > 0 && (
                <p className="text-xs text-[var(--muted)] tabular-nums">{fmt(ep.plays_count)} plays</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
