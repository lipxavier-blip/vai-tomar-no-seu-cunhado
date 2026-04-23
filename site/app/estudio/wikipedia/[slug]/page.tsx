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
    <div className="max-w-2xl">
      <div className="flex items-start justify-between mb-10">
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
          className="text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors mt-1 shrink-0 ml-6"
        >
          Editar
        </Link>
      </div>

      <div className="wiki-body">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {entry.content}
        </ReactMarkdown>
      </div>

      <style>{`
        .wiki-body h2 {
          font-size: 10px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.15em;
          color: var(--accent);
          margin-top: 2.5rem;
          margin-bottom: 1rem;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid var(--border);
        }
        .wiki-body h3 {
          font-size: 0.9375rem;
          font-weight: 700;
          color: var(--foreground);
          margin-top: 1.75rem;
          margin-bottom: 0.375rem;
        }
        .wiki-body p {
          font-size: 0.875rem;
          color: var(--muted);
          line-height: 1.75;
          margin-bottom: 0.75rem;
        }
        .wiki-body strong {
          font-weight: 600;
          color: var(--foreground);
        }
        .wiki-body ul {
          margin: 0.5rem 0 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.375rem;
          list-style: none;
          padding: 0;
        }
        .wiki-body li {
          font-size: 0.875rem;
          color: var(--muted);
          line-height: 1.6;
          display: flex;
          gap: 0.5rem;
        }
        .wiki-body li::before {
          content: '—';
          color: var(--accent);
          flex-shrink: 0;
        }
        .wiki-body li p {
          margin: 0;
        }
      `}</style>
    </div>
  )
}
