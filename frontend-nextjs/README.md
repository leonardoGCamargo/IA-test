# IA-Test Frontend - Next.js 14+

Frontend moderno para o sistema multi-agente IA-Test, construído com Next.js 14+ (App Router), TypeScript, e React Query.

## 🚀 Quick Start

### Desenvolvimento Local

```bash
# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev

# Acessar
http://localhost:3000
```

### Build de Produção

```bash
# Build
npm run build

# Executar produção
npm start
```

## 📁 Estrutura

```
frontend-nextjs/
├── src/
│   ├── app/                    # App Router (Next.js 14+)
│   │   ├── layout.tsx          # Layout raiz
│   │   ├── page.tsx            # Homepage
│   │   ├── dashboard/          # Páginas do dashboard
│   │   │   └── agents/         # Página de agentes
│   │   └── providers.tsx       # Providers (React Query)
│   ├── components/             # Componentes React
│   │   └── agents/             # Componentes de agentes
│   ├── lib/                    # Utilitários
│   │   └── api.ts             # Cliente API
│   └── hooks/                  # React Hooks
│       └── useWebSocket.ts     # Hook WebSocket
├── public/                     # Arquivos estáticos
├── package.json
├── tsconfig.json
└── next.config.js
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8504
NEXT_PUBLIC_WS_URL=ws://localhost:8504
```

## 📚 Tecnologias

- **Next.js 14+** - Framework React com App Router
- **TypeScript** - Tipagem estática
- **React Query** - Gerenciamento de estado e cache
- **Socket.IO Client** - WebSockets para real-time
- **Tailwind CSS** - Estilização
- **Lucide React** - Ícones

## 🎨 Páginas

### Homepage (`/`)
Dashboard principal com visão geral do sistema.

### Dashboard de Agentes (`/dashboard/agents`)
- Lista todos os agentes disponíveis
- Executa agentes com objetivos
- Monitora execução em tempo real via WebSocket
- Visualiza status do sistema

## 🔌 Integração com Backend

O frontend se comunica com o backend FastAPI via:

1. **REST API** - Para operações CRUD e execução de agentes
2. **WebSockets** - Para atualizações em tempo real

Veja `src/lib/api.ts` para todos os endpoints disponíveis.

## 🚀 Deploy

### Vercel (Recomendado)

```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker

```bash
# Build
docker build -f docker/frontend-nextjs.Dockerfile -t ia-test-frontend .

# Run
docker run -p 3000:3000 ia-test-frontend
```

## 📝 Scripts

- `npm run dev` - Desenvolvimento
- `npm run build` - Build de produção
- `npm start` - Executar produção
- `npm run lint` - Linter
- `npm run type-check` - Verificar tipos TypeScript

## 🤝 Contribuindo

Veja `docs/MIGRATION_GUIDE.md` para detalhes sobre a arquitetura e migração.


