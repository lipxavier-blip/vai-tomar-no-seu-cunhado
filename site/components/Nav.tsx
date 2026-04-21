import Link from 'next/link'

export default function Nav() {
  return (
    <header className="border-b border-[var(--border)] px-6 py-4 flex items-center justify-between">
      <Link href="/" className="font-bold text-sm hover:text-[var(--accent)] transition-colors">
        VTSC
      </Link>
      <nav className="flex items-center gap-6 text-sm text-[var(--muted)]">
        <Link href="/episodios" className="hover:text-[var(--foreground)] transition-colors">
          Episódios
        </Link>
        <Link href="/wikipedia" className="hover:text-[var(--foreground)] transition-colors">
          Wikipedia
        </Link>
        <Link href="/sobre" className="hover:text-[var(--foreground)] transition-colors">
          Sobre
        </Link>
      </nav>
    </header>
  )
}
