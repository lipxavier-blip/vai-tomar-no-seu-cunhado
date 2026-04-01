import Link from 'next/link'

const cards = [
  {
    href: '/estudio/tom-de-voz',
    title: 'Tom de voz',
    description: 'Vocabulário, ritmo, exemplos reais e guia para escrever no tom do podcast.',
    tag: 'Referência',
  },
]

export default function EstudioPage() {
  return (
    <div>
      <div className="mb-10">
        <h1 className="text-3xl font-bold mb-2">Estúdio</h1>
        <p className="text-[var(--muted)]">Tudo que a gente precisa para fazer o podcast acontecer.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {cards.map((card) => (
          <Link
            key={card.href}
            href={card.href}
            className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-6 hover:border-[var(--accent)] transition-colors group"
          >
            <span className="text-xs text-[var(--accent)] font-medium uppercase tracking-widest">
              {card.tag}
            </span>
            <h2 className="text-lg font-semibold mt-2 mb-1 group-hover:text-[var(--accent)] transition-colors">
              {card.title}
            </h2>
            <p className="text-sm text-[var(--muted)]">{card.description}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
