# Roadmap — Bíblia App

## Fase 1 — Fundação & Polish (essencial)

- [ ] **Favicon & App Icons** — SVG favicon + PNG icons (192x192, 512x512) com símbolo ✝ ou 📖
- [ ] **Meta tags & SEO** — title, description, og:image, og:title, theme-color no `app.html`
- [ ] **PWA Manifest** — `manifest.webmanifest` com nome, ícones, cores, display standalone
- [ ] **Service Worker** — cache offline dos assets + dados dos livros já visitados
- [ ] **localStorage** — persistir: último livro/capítulo, viewMode, fontSize, sidebarOpen
- [ ] **Restaurar posição** — ao abrir o app, voltar exatamente onde parou
- [ ] **Loading states** — skeleton/spinner ao carregar livro ou capítulo
- [ ] **Error handling** — fallback visual quando um livro falha ao carregar, com botão de retry
- [ ] **Ctrl+K Search Palette** — implementar o design aprovado (fuzzy search, navegação por teclado)

## Fase 2 — UX & Navegação

- [ ] **Swipe para navegar** — gesto touch para capítulo anterior/próximo no mobile
- [ ] **Atalhos de teclado globais** — `←`/`→` para capítulos, `Esc` para fechar sidebar
- [ ] **Scroll to verse** — ao navegar para "Jo 3:16", scroll suave até o versículo 16
- [ ] **Highlight de versículo ativo** — destaque visual ao clicar ou navegar para um versículo
- [ ] **Breadcrumb** — mostrar "Gênesis > Capítulo 1" no topo do conteúdo
- [ ] **Modo de leitura contínua** — scroll infinito entre capítulos (sem precisar clicar "Próximo")
- [ ] **Modo tela cheia** — esconder toolbar e sidebar para leitura imersiva (F11 ou botão)
- [ ] **Animação de transição** — fade/slide suave ao trocar de capítulo

## Fase 3 — Recursos de Estudo

- [ ] **Bookmarks / Favoritos** — salvar versículos marcados no localStorage
- [ ] **Últimos lidos** — histórico das últimas 10 passagens visitadas
- [ ] **Copiar versículo** — botão para copiar texto formatado ("João 3:16 — Porque Deus amou...")
- [ ] **Compartilhar** — Web Share API para enviar versículo via WhatsApp/Telegram
- [ ] **Notas pessoais** — textarea por capítulo, salvo localmente
- [ ] **Busca no texto original** — buscar também no hebraico/grego, não só no português
- [ ] **Cross-references** — links entre versículos que se referenciam
- [ ] **Planos de leitura** — tracker diário (ex: "Bíblia em 1 ano")

## Fase 4 — Visual & Temas

- [ ] **Tema claro** — toggle dark/light com transição suave
- [ ] **Tema sépia** — modo de leitura quente para leitura longa
- [ ] **Seletor de fonte** — escolher entre serif/sans-serif/monospace
- [ ] **Espaçamento de linha** — controle fino de line-height
- [ ] **Print styles** — CSS @media print para impressão limpa de capítulos
- [ ] **Responsividade refinada** — otimizar layout para tablets em landscape
- [ ] **Animações micro** — hover states, press feedback, transitions em todos os botões

## Fase 5 — Performance & Infraestrutura

- [ ] **Preload de capítulos adjacentes** — fetch silencioso do capítulo anterior e próximo
- [ ] **IndexedDB** — cache robusto de todos os livros já carregados (sobrevive clear de cache)
- [ ] **Bundle analysis** — otimizar tamanho do JS (atualmente ~90KB gzipped)
- [ ] **Image optimization** — comprimir ícones/favicons, usar WebP onde possível
- [ ] **CI/CD** — GitHub Actions: build → test → deploy Cloudflare Pages automaticamente
- [ ] **Testes** — vitest para search.ts, api.ts, e lógica de stores
- [ ] **Error tracking** — integrar Sentry ou similar para capturar erros em produção
- [ ] **Analytics** — Plausible/Umami (privacy-friendly) para entender uso

## Fase 6 — Conteúdo & Expansão

- [ ] **Múltiplas traduções** — ARA, NVI, KJV além da ACF
- [ ] **Comparação de traduções** — ver 2-3 traduções lado a lado por versículo
- [ ] **Concordância** — índice de palavras-chave com todas as ocorrências
- [ ] **Mapas bíblicos** — visualização geográfica de locais mencionados
- [ ] **Dicionário bíblico** — tooltip com definição de termos e nomes próprios
- [ ] **i18n da interface** — suportar inglês e espanhol na UI

---

## Prioridade de impacto

| Item | Esforço | Impacto | Prioridade |
|------|---------|---------|------------|
| Favicon + Meta tags | 🟢 Baixo | 🔴 Alto | **P0** |
| localStorage (posição + prefs) | 🟢 Baixo | 🔴 Alto | **P0** |
| Ctrl+K Search Palette | 🟡 Médio | 🔴 Alto | **P0** |
| PWA Manifest | 🟢 Baixo | 🟡 Médio | **P1** |
| Loading states + Error handling | 🟡 Médio | 🔴 Alto | **P1** |
| Service Worker (offline) | 🟡 Médio | 🟡 Médio | **P1** |
| Swipe + Atalhos de teclado | 🟢 Baixo | 🟡 Médio | **P1** |
| Bookmarks + Copiar versículo | 🟡 Médio | 🟡 Médio | **P2** |
| Tema claro/sépia | 🟡 Médio | 🟡 Médio | **P2** |
| Testes (vitest) | 🟡 Médio | 🟡 Médio | **P2** |
| CI/CD | 🟡 Médio | 🟢 Baixo | **P3** |
| Múltiplas traduções | 🔴 Alto | 🔴 Alto | **P3** |
