# 🚀 Guia de Migração - Next.js + LangGraph

Este documento descreve a migração completa do sistema para usar Next.js 14+ e LangGraph.

## 📋 Visão Geral

O sistema foi migrado de:
- **Frontend:** Svelte → **Next.js 14+ (App Router, TypeScript)**
- **Orchestrator:** Python simples → **LangGraph (stateful, multi-actor)**
- **API:** FastAPI básico → **FastAPI completo com WebSockets**
- **Observabilidade:** Nenhuma → **LangSmith integrado**

## 🏗️ Nova Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│  - App Router (TypeScript)                              │
│  - React Query (data fetching)                          │
│  - WebSockets (real-time)                                │
│  - Tailwind CSS (styling)                                │
└────────────────────┬──────────────────────────────────────┘
                     │ HTTP/WebSocket
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI v2 (API Gateway)                    │
│  - Endpoints RESTful completos                           │
│  - WebSockets (Socket.IO)                               │
│  - Integração LangGraph                                  │
│  - Integração LangSmith                                  │
└────────────────────┬──────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         LangGraph Orchestrator (Python)                  │
│  - Stateful agent execution                              │
│  - Multi-actor coordination                              │
│  - Memory management (Neo4j)                             │
└────────────────────┬──────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ Neo4j  │  │ Kestra │  │  MCP   │
    │ Memory │  │Workflow│  │Servers │
    └────────┘  └────────┘  └────────┘
```

## 📁 Estrutura de Arquivos

### Frontend (Next.js)

```
frontend-nextjs/
├── src/
│   ├── app/                    # App Router
│   │   ├── layout.tsx          # Layout raiz
│   │   ├── page.tsx            # Homepage
│   │   └── dashboard/          # Páginas do dashboard
│   │       └── agents/         # Página de agentes
│   ├── components/             # Componentes React
│   │   └── agents/             # Componentes de agentes
│   ├── lib/                    # Utilitários
│   │   └── api.ts              # Cliente API
│   └── hooks/                  # React Hooks
│       └── useWebSocket.ts     # Hook WebSocket
├── package.json
├── tsconfig.json
└── next.config.js
```

### Backend (FastAPI)

```
src/
├── apps/
│   └── api_v2.py               # FastAPI v2 completo
└── agents/
    └── orchestrator_langgraph.py  # LangGraph Orchestrator
```

### Workflows (Kestra)

```
kestra_workflows/
├── agent_execution.yaml        # Execução de agentes
└── system_sync.yaml            # Sincronização do sistema
```

## 🔧 Configuração

### 1. Variáveis de Ambiente

Adicione ao `.env`:

```bash
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8504
NEXT_PUBLIC_WS_URL=ws://localhost:8504

# LangSmith (opcional mas recomendado)
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_PROJECT=ia-test
LANGCHAIN_TRACING_V2=true
```

### 2. Instalação

#### Frontend (Next.js)

```bash
cd frontend-nextjs
npm install
npm run dev
```

#### Backend (FastAPI)

```bash
pip install -r config/requirements.txt
uvicorn src.apps.api_v2:app --host 0.0.0.0 --port 8504 --reload
```

### 3. Docker Compose

```bash
# Iniciar todos os serviços
docker compose -f config/docker-compose.yml up

# Apenas serviços core (inclui Next.js)
docker compose -f config/docker-compose.yml --profile core up
```

## 🚀 Uso

### Executar um Agente

1. **Via Frontend (Next.js):**
   - Acesse `http://localhost:3000/dashboard/agents`
   - Selecione um agente
   - Clique em "Executar"
   - Digite o objetivo
   - Acompanhe em tempo real via WebSocket

2. **Via API:**

```bash
curl -X POST http://localhost:8504/api/v1/agents/neo4j_graphrag/execute \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Buscar informações sobre agentes MCP",
    "parameters": {}
  }'
```

3. **Via Kestra:**

```bash
# Executar workflow de agente
curl -X POST http://localhost:8080/api/v1/executions/trigger/agent-execution \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "agent_id": "neo4j_graphrag",
      "goal": "Buscar informações sobre agentes MCP"
    }
  }'
```

## 📊 Observabilidade

### LangSmith

Todos os traces do LangGraph são automaticamente enviados para LangSmith:

1. Configure `LANGCHAIN_API_KEY` no `.env`
2. Acesse https://smith.langchain.com
3. Veja todos os traces em tempo real

### WebSockets

O frontend recebe atualizações em tempo real via WebSocket:

- `agent_status`: Status de execução do agente
- `task_update`: Atualizações de tarefas
- `system_event`: Eventos do sistema

## 🔄 Migração do Frontend Antigo

O frontend antigo (Svelte) ainda está em `front-end/` e pode ser usado em paralelo.

Para desativar:

```yaml
# docker-compose.yml
front-end:
  profiles: ["legacy"]  # Mude de "core" para "legacy"
```

## 🐛 Troubleshooting

### Frontend não conecta ao backend

1. Verifique `NEXT_PUBLIC_API_URL` no `.env`
2. Verifique se o backend está rodando na porta 8504
3. Verifique CORS no `api_v2.py`

### WebSocket não funciona

1. Verifique `NEXT_PUBLIC_WS_URL` no `.env`
2. Verifique se Socket.IO está instalado no backend
3. Verifique logs do backend para erros de conexão

### LangGraph não executa

1. Verifique se `langgraph` está instalado: `pip install langgraph`
2. Verifique logs do orchestrator
3. Verifique se o LLM está configurado corretamente

## 📚 Próximos Passos

- [ ] Implementar autenticação (NextAuth/Clerk)
- [ ] Adicionar mais páginas do dashboard
- [ ] Implementar persistência de tarefas
- [ ] Melhorar integração com Kestra
- [ ] Adicionar testes E2E

## 🤝 Suporte

Para dúvidas ou problemas, consulte:
- `docs/ARCHITECTURE.md` - Arquitetura detalhada
- `docs/ENGINEERING_GUIDE.md` - Guia de engenharia
- Issues no repositório

