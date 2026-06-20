import fs from 'fs'
import path from 'path'
import type { WikiEntry } from '@/lib/wiki'

let cache: WikiEntry[] | null = null

function loadAll(): WikiEntry[] {
  if (cache) return cache
  const filePath = path.join(process.cwd(), 'content', 'wiki.json')
  const raw = fs.readFileSync(filePath, 'utf-8')
  cache = JSON.parse(raw) as WikiEntry[]
  return cache
}

export async function getWikiEntries(): Promise<WikiEntry[]> {
  const entries = loadAll()
  return [...entries].sort((a, b) => a.title.localeCompare(b.title, 'pt-BR'))
}

export async function getWikiEntry(slug: string): Promise<WikiEntry | null> {
  const entries = loadAll()
  return entries.find((e) => e.slug === slug) ?? null
}
