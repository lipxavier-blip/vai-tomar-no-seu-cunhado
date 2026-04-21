import { notFound } from 'next/navigation'
import Link from 'next/link'
import Nav from '@/components/Nav'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CATEGORY_LABELS } from '@/lib/wiki'
import { getWikiEntry } from '@/lib/wiki-server'

interface Props {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params
  const entry = await getWikiEntry(slug)
  if (!entry) return {}
  return { title: `${entry.title} — Wikipedia VTSC` }
}

export default async function WikiEntryPage({ params }: Props) {
  const { slug } = await params
  const entry = await getWikiEntry(slug)
  if (!entry) notFound()

  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 px-6 py-12 max-w-2xl mx-auto w-full">
        <Link
          href="/wikipedia"
          className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors mb-8 inline-block"
        >
          ← Wikipedia
        </Link>

        <p className="text-xs uppercase tracking-widest text-[var(--accent)] mb-3">
          {CATEGORY_LABELS[entry.category]}
        </p>
        <h1 className="text-3xl font-bold mb-8">{entry.title}</h1>

        <article className="prose prose-invert prose-sm max-w-none text-[var(--muted)] prose-headings:text-[var(--foreground)] prose-a:text-[var(--accent)]">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {entry.content}
          </ReactMarkdown>
        </article>
      </main>
    </div>
  )
}
