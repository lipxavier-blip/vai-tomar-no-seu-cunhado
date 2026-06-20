import { redirect } from 'next/navigation'
import Link from 'next/link'
import LogoutButton from './LogoutButton'
import { isAuthenticated } from '@/lib/auth'

export default async function EstudioLayout({
  children,
}: {
  children: React.ReactNode
}) {
  if (!(await isAuthenticated())) redirect('/login')

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-[var(--border)] px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/estudio" className="font-bold text-sm hover:text-[var(--accent)] transition-colors">
            VTSC <span className="text-[var(--accent)]">Estúdio</span>
          </Link>
          <nav className="flex items-center gap-4 text-sm text-[var(--muted)]">
            <Link href="/estudio/tom-de-voz" className="hover:text-[var(--foreground)] transition-colors">
              Tom de voz
            </Link>
            <Link href="/estudio/gerador" className="hover:text-[var(--foreground)] transition-colors">
              Gerador
            </Link>
            <Link href="/estudio/wikipedia" className="hover:text-[var(--foreground)] transition-colors">
              Wikipedia
            </Link>
            <Link href="/estudio/numeros" className="hover:text-[var(--foreground)] transition-colors">
              Números
            </Link>
          </nav>
        </div>
        <LogoutButton />
      </header>
      <main className="flex-1 px-6 py-8 max-w-4xl mx-auto w-full">
        {children}
      </main>
    </div>
  )
}
