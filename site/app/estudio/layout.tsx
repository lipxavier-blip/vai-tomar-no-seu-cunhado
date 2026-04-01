import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'
import LogoutButton from './LogoutButton'

export default async function EstudioLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) redirect('/login')

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
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-xs text-[var(--muted)]">{user.email}</span>
          <LogoutButton />
        </div>
      </header>
      <main className="flex-1 px-6 py-8 max-w-4xl mx-auto w-full">
        {children}
      </main>
    </div>
  )
}
