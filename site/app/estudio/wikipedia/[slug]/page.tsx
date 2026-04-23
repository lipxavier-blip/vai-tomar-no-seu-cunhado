import { notFound } from 'next/navigation'
import Link from 'next/link'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CATEGORY_LABELS } from '@/lib/wiki'
import { getWikiEntry } from '@/lib/wiki-server'

interface Props {
  params: Promise<{ slug: string }>
}

export default async function LerWikiPage({ params }: Props) {
  const { slug } = await params
  const entry = await getWikiEntry(slug)
  if (!entry) notFound()

  return (
    <div>
      <div className="flex items-start justify-between mb-8">
        <div>
          <Link
            href="/estudio/wikipedia"
            className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors inline-block mb-4"
          >
            ← Wikipedia
          </Link>
          <p className="text-xs uppercase tracking-widest text-[var(--accent)] mb-2">
            {CATEGORY_LABELS[entry.category]}
          </p>
          <h1 className="text-3xl font-bold">{entry.title}</h1>
        </div>
        <Link
          href={`/estudio/wikipedia/${entry.slug}/editar`}
          className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors mt-1 shrink-0"
        >
          Editar
        </Link>
      </div>

      <article className="prose prose-invert prose-sm max-w-none text-[var(--muted)] prose-headings:text-[var(--foreground)] prose-a:text-[var(--accent)] prose-strong:text-[var(--foreground)]">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {entry.content}
        </ReactMarkdown>
      </article>
    </div>
  )
}
