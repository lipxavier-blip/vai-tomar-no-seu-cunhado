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

      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h2: ({ children }) => (
            <h2 className="text-[10px] font-bold uppercase tracking-widest text-[var(--muted)] mt-10 mb-4 pb-2 border-b border-[var(--border)]">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-sm font-semibold text-[var(--foreground)] mt-6 mb-1.5">
              {children}
            </h3>
          ),
          p: ({ children }) => (
            <p className="text-sm text-[var(--muted)] leading-relaxed mb-3">
              {children}
            </p>
          ),
          strong: ({ children }) => (
            <strong className="font-semibold text-[var(--foreground)]">{children}</strong>
          ),
          ul: ({ children }) => (
            <ul className="my-2 flex flex-col gap-1.5">
              {children}
            </ul>
          ),
          li: ({ children }) => (
            <li className="text-sm text-[var(--muted)] leading-relaxed flex gap-2">
              <span className="text-[var(--accent)] shrink-0 select-none mt-px">—</span>
              <span>{children}</span>
            </li>
          ),
        }}
      >
        {entry.content}
      </ReactMarkdown>
    </div>
  )
}
