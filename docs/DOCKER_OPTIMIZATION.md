# Otimização Docker - Guia de Uso

## Data: 2025-01-27

## Resumo

Foi criada uma versão otimizada do docker-compose.yml que:
- ✅ Usa profiles para ativar/desativar serviços
- ✅ Consolida variáveis de ambiente compartilhadas
- ✅ Reduz duplicação de código
- ✅ Usa volumes nomeados
- ✅ Usa networks nomeados
- ✅ Melhora gerenciamento de recursos
- ✅ Facilita manutenção

## Limpeza Realizada

### Containers Removidos
1. **Containers do n8n** (removidos):
   - 8n8-n8n_webhook-1
   - 8n8-n8n_worker-1
   - 8n8-n8n_editor-1

2. **Containers parados do Dokploy** (removidos):
   - 10 containers parados removidos

3. **Containers parados diversos** (removidos):
   - cloudflared-cloudflared-1
   - cranky_proskuriakova
   - wizardly_spence (kestra parado - temos outro rodando)
   - frosty_euler (docker welcome)
   - open-webui

### Containers Mantidos
- **Dokploy** (se você usa): dokploy.1.551ofp4t1v9ku7xw68tjjiu50
- **Postgres Aula**: postgres_aula
- **Redis**: redis
- **Kestra**: (se rodando via docker-compose)

## Estrutura Otimizada

### Profiles Disponíveis

#### 1. Core (Serviços Essenciais)
Serviços que rodam por padrão:
- `database` - Neo4j
- `api` - FastAPI
- `front-end` - Svelte
- `agent-dashboard` - Dashboard de Agentes

#### 2. Streamlit (Aplicações Streamlit)
Serviços opcionais usando profile `streamlit`:
- `bot` - Bot Streamlit
- `loader` - Loader Streamlit
- `pdf_bot` - PDF Bot Streamlit

#### 3. Tools (Ferramentas Adicionais)
Serviços opcionais usando profile `tools`:
- `mcp-manager` - MCP Manager
- `kestra` - Kestra Workflow Engine

#### 4. Ollama (Ollama Local)
Serviço opcional usando profile `ollama`:
- `ollama` - Ollama local (se não usar externo)

#### 5. Pull Model (One-time Job)
Job opcional usando profile `pull-model`:
- `pull-model` - Pull model do Ollama

## Como Usar

### Stack Completa (Todos os Serviços)
```bash
docker compose -f config/docker-compose.yml up -d
```

### Stack Core (Apenas Serviços Essenciais)
```bash
docker compose -f config/docker-compose.yml --profile core up -d
```

### Stack Core + Streamlit
```bash
docker compose -f config/docker-compose.yml --profile core --profile streamlit up -d
```

### Stack Core + Tools
```bash
docker compose -f config/docker-compose.yml --profile core --profile tools up -d
```

### Apenas Serviços Específicos
```bash
# Apenas API e Frontend
docker compose -f config/docker-compose.yml up -d api front-end

# Apenas Agent Dashboard
docker compose -f config/docker-compose.yml up -d agent-dashboard

# Apenas Bot
docker compose -f config/docker-compose.yml --profile streamlit up -d bot
```

### Parar Serviços
```bash
# Parar todos
docker compose -f config/docker-compose.yml down

# Parar serviços específicos
docker compose -f config/docker-compose.yml stop api front-end

# Parar e remover volumes
docker compose -f config/docker-compose.yml down -v
```

## Melhorias Implementadas

### 1. Variáveis Compartilhadas
- Usa `x-common-variables` para variáveis de ambiente
- Reduz duplicação
- Facilita manutenção

### 2. Volumes Nomeados
- `neo4j_data` - Dados do Neo4j
- `embedding_model` - Modelos de embedding
- `ollama_data` - Dados do Ollama
- `kestra_workflows` - Workflows do Kestra
- `kestra_data` - Dados do Kestra

### 3. Networks Nomeados
- `ia-test-network` - Network principal
- Facilita comunicação entre containers
- Melhora isolamento

### 4. Container Names
- Todos os containers têm nomes descritivos
- Formato: `ia-test-{service-name}`
- Facilita identificação no Portainer

### 5. Health Checks
- Todos os serviços têm health checks
- Melhora confiabilidade
- Facilita monitoramento

### 6. Restart Policies
- `restart: unless-stopped` - Reinicia automaticamente
- Melhora disponibilidade
- Reduz necessidade de intervenção manual

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

## Comparação Antes/Depois

### Antes
- ❌ 10+ containers rodando
- ❌ Duplicação de código
- ❌ Variáveis de ambiente repetidas
- ❌ Sem profiles
- ❌ Containers com nomes aleatórios
- ❌ Sem health checks em alguns serviços
- ❌ Sem restart policies

### Depois
- ✅ 4-8 containers (dependendo do profile)
- ✅ Código consolidado
- ✅ Variáveis compartilhadas
- ✅ Profiles para ativar/desativar serviços
- ✅ Containers com nomes descritivos
- ✅ Health checks em todos os serviços
- ✅ Restart policies configuradas
- ✅ Volumes nomeados
- ✅ Networks nomeados

## Recomendações

### Para Desenvolvimento
```bash
# Stack mínima (core)
docker compose -f config/docker-compose.yml --profile core up -d

# Stack completa (core + streamlit)
docker compose -f config/docker-compose.yml --profile core --profile streamlit up -d
```

### Para Produção
```bash
# Stack core (essencial)
docker compose -f config/docker-compose.yml --profile core up -d

# Adicionar tools se necessário
docker compose -f config/docker-compose.yml --profile core --profile tools up -d
```

### Para Testes
```bash
# Apenas serviços necessários
docker compose -f config/docker-compose.yml up -d database api agent-dashboard
```

## Limpeza de Containers

### Script de Limpeza
```bash
# Windows PowerShell
.\scripts\cleanup_containers.ps1

# Linux/Mac
chmod +x scripts/cleanup_containers.sh
./scripts/cleanup_containers.sh
```

### Limpeza Manual
```bash
# Remover containers parados
docker container prune -f

# Remover containers do projeto
docker compose -f config/docker-compose.yml down

# Remover containers e volumes
docker compose -f config/docker-compose.yml down -v
```

## Containers com Nomes Aleatórios

Se você ver containers com nomes aleatórios (como `strange_roentgen`, `keen_volhard`, etc.):
- Estes são do MCP Desktop (não do projeto principal)
- Podem ser removidos se não usar MCP Desktop
- Use o script de limpeza para removê-los

## Próximos Passos

1. ✅ Testar a nova configuração
2. ✅ Verificar se todos os serviços funcionam
3. ✅ Ajustar profiles conforme necessário
4. ✅ Documentar mudanças
5. ✅ Atualizar scripts de deploy

## Troubleshooting

### Erro: "Service not found"
**Solução**: Verifique se o profile está correto:
```bash
docker compose -f config/docker-compose.yml --profile streamlit up -d bot
```

### Erro: "Port already in use"
**Solução**: Pare o container que está usando a porta:
```bash
docker ps | findstr 8501
docker stop <container-id>
```

### Erro: "Volume not found"
**Solução**: Crie os volumes:
```bash
docker volume create ia-test-neo4j-data
docker volume create ia-test-embedding-model
```

### Erro: "Network not found"
**Solução**: Crie a network:
```bash
docker network create ia-test-network
```

## Referências

- [Docker Compose Profiles](https://docs.docker.com/compose/profiles/)
- [Docker Compose Best Practices](https://docs.docker.com/compose/best-practices/)
- [Docker Networking](https://docs.docker.com/network/)

