import fs from 'fs'
import path from 'path'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function TomDeVozPage() {
  const filePath = path.join(process.cwd(), '..', 'tom-de-voz.md')
  const content = fs.readFileSync(filePath, 'utf-8')

  return (
    <div>
      <div className="mb-8">
        <span className="text-xs text-[var(--accent)] font-medium uppercase tracking-widest">
          Referência
        </span>
        <h1 className="text-3xl font-bold mt-2">Tom de voz</h1>
      </div>

      <article className="prose prose-invert prose-sm max-w-none
        prose-headings:font-bold prose-headings:text-[var(--foreground)]
        prose-h1:text-2xl prose-h2:text-xl prose-h2:mt-10 prose-h2:mb-4
        prose-h3:text-base prose-h3:text-[var(--accent)]
        prose-p:text-[var(--foreground)] prose-p:leading-relaxed
        prose-li:text-[var(--foreground)]
        prose-strong:text-[var(--foreground)]
        prose-em:text-[var(--muted)]
        prose-blockquote:border-l-[var(--accent)] prose-blockquote:text-[var(--muted)] prose-blockquote:italic
        prose-code:text-[var(--accent)] prose-code:bg-[var(--card)] prose-code:px-1 prose-code:rounded
        prose-table:text-sm
        prose-th:text-[var(--foreground)] prose-th:bg-[var(--card)]
        prose-td:text-[var(--muted)]
        prose-hr:border-[var(--border)]
        prose-a:text-[var(--accent)]">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      </article>
    </div>
  )
}
