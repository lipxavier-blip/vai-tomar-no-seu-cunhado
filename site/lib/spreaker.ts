import { getSpreakerAccessToken, invalidateAccessToken } from './spreaker-auth'

const SHOW_ID = 5951420

export interface SpreakerEpisode {
  episode_id: number
  title: string
  duration: number
  image_url: string
  image_original_url: string
  published_at: string
  slug: string
  site_url: string
  download_url: string
  playback_url: string
  plays_count?: number
  downloads_count?: number
}

export interface SpreakerEpisodeDetail extends SpreakerEpisode {
  description: string
  description_html: string
}

function formatDuration(ms: number): string {
  const totalSeconds = Math.floor(ms / 1000)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  if (hours > 0) return `${hours}h ${minutes}min`
  return `${minutes}min`
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

function formatPlays(count: number | undefined): string | null {
  if (count == null) return null
  const label = count === 1 ? 'download' : 'downloads'
  if (count >= 1000) return `${(count / 1000).toFixed(1).replace('.0', '')}k ${label}`
  return `${count} ${label}`
}

async function spreakerFetch(path: string): Promise<Response> {
  let token = await getSpreakerAccessToken()
  let res = await fetch(`https://api.spreaker.com${path}`, {
    headers: { Authorization: `Bearer ${token}` },
    next: { revalidate: 3600 },
  })
  if (res.status === 401) {
    token = await invalidateAccessToken()
    res = await fetch(`https://api.spreaker.com${path}`, {
      headers: { Authorization: `Bearer ${token}` },
      next: { revalidate: 3600 },
    })
  }
  return res
}

export async function getEpisodes(): Promise<SpreakerEpisode[]> {
  const res = await spreakerFetch(`/v2/shows/${SHOW_ID}/episodes?limit=100`)
  const data = await res.json()
  return data.response.items as SpreakerEpisode[]
}

export async function getEpisode(episodeId: number): Promise<SpreakerEpisodeDetail> {
  const res = await spreakerFetch(`/v2/episodes/${episodeId}`)
  const data = await res.json()
  return data.response.episode as SpreakerEpisodeDetail
}

async function getEpisodeStats(episodeId: number): Promise<Pick<SpreakerEpisode, 'plays_count' | 'downloads_count'>> {
  const res = await spreakerFetch(`/v2/episodes/${episodeId}`)
  if (!res.ok) return {}
  const data = await res.json()
  const ep = data.response.episode
  return { plays_count: ep.plays_count, downloads_count: ep.downloads_count }
}

export async function getEpisodesWithStats(): Promise<SpreakerEpisode[]> {
  const episodes = await getEpisodes()
  const stats = await Promise.all(episodes.map((ep) => getEpisodeStats(ep.episode_id)))
  return episodes.map((ep, i) => ({ ...ep, ...stats[i] }))
}

export { formatDuration, formatDate, formatPlays }
