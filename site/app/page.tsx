export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 text-center">
      <p className="text-sm uppercase tracking-widest text-[var(--muted)] mb-6">
        Em breve
      </p>
      <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6">
        Vai tomar no
        <br />
        <span className="text-[var(--accent)]">seu cunhado</span>
      </h1>
      <p className="text-[var(--muted)] text-lg max-w-md">
        Um podcast sobre nada. Dois cunhados jogando conversa fora, com amor,
        mas se recusam a assumir isso.
      </p>
    </main>
  )
}
