import { createClient } from '@/lib/supabase/server'
import type { WikiEntry } from '@/lib/wiki'

export async function getWikiEntries(): Promise<WikiEntry[]> {
  const supabase = await createClient()
  const { data, error } = await supabase
    .from('wiki_entries')
    .select('*')
    .order('title', { ascending: true })
  if (error) throw error
  return data as WikiEntry[]
}

export async function getWikiEntry(slug: string): Promise<WikiEntry | null> {
  const supabase = await createClient()
  const { data, error } = await supabase
    .from('wiki_entries')
    .select('*')
    .eq('slug', slug)
    .single()
  if (error) return null
  return data as WikiEntry
}
