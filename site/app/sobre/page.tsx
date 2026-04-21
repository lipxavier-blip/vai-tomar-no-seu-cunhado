import Nav from '@/components/Nav'

export const metadata = {
  title: 'Sobre — Vai Tomar no Seu Cunhado',
}

export default function SobrePage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 px-6 py-12 max-w-2xl mx-auto w-full">
        <h1 className="text-3xl font-bold mb-2">Sobre</h1>
        <p className="text-[var(--muted)] mb-12">Quem são esses dois?</p>

        <div className="space-y-10">
          <section>
            <h2 className="text-lg font-semibold mb-3">O podcast</h2>
            <p className="text-[var(--muted)] leading-relaxed">
              Vai Tomar no Seu Cunhado é um podcast sobre nada. Dois cunhados que se encontraram
              por acaso na vida — Felipe casou com a irmã do Bruno — e descobriram que falar
              besteira juntos é uma das melhores coisas do mundo.
            </p>
            <p className="text-[var(--muted)] leading-relaxed mt-3">
              Sem pauta, sem estrutura, sem pretensão. Só duas pessoas jogando conversa fora
              sobre a vida, cultura, família e qualquer coisa que aparecer.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold mb-3">Felipe Xavier</h2>
            <p className="text-[var(--muted)] leading-relaxed">
              Content Designer, UX Writer e fundador da tradição de ter projetos demais ao mesmo
              tempo. Mora em Uberlândia, é fanático por cinema e podcasts, e considera que falar
              sobre streaming é uma profissão legítima.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold mb-3">Bruno Rezende</h2>
            <p className="text-[var(--muted)] leading-relaxed">
              Mineiro de Uberlândia que atualmente mora nos Estados Unidos enquanto a esposa
              Taís faz doutorado. Gamer convicto, pessimista confesso que prefere se chamar
              de realista, e responsável pelo melhor silêncio desconfortável do podcast.
            </p>
          </section>

          <section className="border-t border-[var(--border)] pt-8">
            <h2 className="text-lg font-semibold mb-4">Encontre a gente</h2>
            <div className="flex flex-col gap-2 text-sm text-[var(--muted)]">
              <a
                href="https://www.instagram.com/vaitomarnoseucunhado/"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-[var(--foreground)] transition-colors"
              >
                Instagram → @vaitomarnoseucunhado
              </a>
              <a
                href="https://www.spreaker.com/podcast/vai-tomar-no-seu-cunhado--5951420"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-[var(--foreground)] transition-colors"
              >
                Spreaker → vai-tomar-no-seu-cunhado
              </a>
              <a
                href="mailto:vaitomarnoseucunhado@gmail.com"
                className="hover:text-[var(--foreground)] transition-colors"
              >
                E-mail → vaitomarnoseucunhado@gmail.com
              </a>
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}
