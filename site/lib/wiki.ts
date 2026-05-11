export type WikiCategory = 'personagens' | 'episodios' | 'piadas' | 'temas' | 'historia'

export const CATEGORY_LABELS: Record<WikiCategory, string> = {
  personagens: 'Personagens',
  episodios: 'Episódios',
  piadas: 'Histórias, piadas e outros',
  temas: 'Temas recorrentes',
  historia: 'História do podcast',
}

export interface WikiEntry {
  id: string
  title: string
  slug: string
  content: string
  category: WikiCategory
  published_at: string
  updated_at: string
}
