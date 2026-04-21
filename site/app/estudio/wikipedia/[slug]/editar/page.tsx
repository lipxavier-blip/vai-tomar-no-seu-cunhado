import { notFound } from 'next/navigation'
import { getWikiEntry } from '@/lib/wiki-server'
import EditarWikiForm from './EditarWikiForm'

interface Props {
  params: Promise<{ slug: string }>
}

export default async function EditarWikiPage({ params }: Props) {
  const { slug } = await params
  const entry = await getWikiEntry(slug)
  if (!entry) notFound()

  return (
    <div>
      <EditarWikiForm entry={entry} />
    </div>
  )
}
