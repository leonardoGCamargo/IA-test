# Docker - Guia Rápido

## Limpeza Realizada

### Containers Removidos
- ✅ Containers do n8n (3 containers)
- ✅ Containers parados do Dokploy (10 containers)
- ✅ Containers parados diversos (5 containers)

### Containers Mantidos
- ✅ Containers do projeto (via docker-compose.yml)
- ✅ Containers externos (Dokploy, Postgres, Redis - se você usa)

## Como Usar

### Stack Completa (Todos os Serviços)
```bash
docker compose -f config/docker-compose.yml up -d
```

### Stack Core (Apenas Serviços Essenciais)
```bash
docker compose -f config/docker-compose.yml up -d database api front-end agent-dashboard
```

### Stack Core + Streamlit
```bash
docker compose -f config/docker-compose.yml --profile streamlit up -d
```

### Stack Core + Tools
```bash
docker compose -f config/docker-compose.yml --profile tools up -d
```

## Profiles Disponíveis

- `core` - Serviços essenciais (database, api, front-end, agent-dashboard)
- `streamlit` - Aplicações Streamlit (bot, loader, pdf_bot)
- `tools` - Ferramentas adicionais (mcp-manager, kestra)
- `ollama` - Ollama local (opcional)
- `pull-model` - Pull model (one-time job)

## Portas dos Serviços

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| Neo4j | 7687, 7474 | Database e Browser |
| API | 8504 | FastAPI |
| Frontend | 8505 | Svelte |
| Agent Dashboard | 8507 | Dashboard de Agentes |
| Bot | 8501 | Bot Streamlit |
| Loader | 8502 | Loader Streamlit |
| PDF Bot | 8503 | PDF Bot Streamlit |
| MCP Manager | 8506 | MCP Manager |
| Kestra | 8080 | Kestra Workflow Engine |
| Ollama | 11434 | Ollama (se usar local) |

## Documentação Completa

- [Docker Optimization Guide](./docs/DOCKER_OPTIMIZATION.md)
- [Docker Cleanup Summary](./docs/DOCKER_CLEANUP_SUMMARY.md)

