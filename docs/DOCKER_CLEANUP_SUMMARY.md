# Resumo da Limpeza e Otimização Docker

## Data: 2025-01-27

## Resumo Executivo

Foi realizada uma limpeza completa dos containers Docker e criada uma versão otimizada do docker-compose.yml que:
- ✅ Remove containers do n8n (não mais necessários)
- ✅ Remove containers parados e inúteis
- ✅ Otimiza configuração com profiles
- ✅ Consolida variáveis de ambiente
- ✅ Reduz duplicação de código
- ✅ Melhora gerenciamento de recursos

## Containers Removidos

### 1. Containers do n8n (Removidos)
- ✅ `8n8-n8n_webhook-1` - Removido
- ✅ `8n8-n8n_worker-1` - Removido
- ✅ `8n8-n8n_editor-1` - Removido

### 2. Containers Parados do Dokploy (Removidos)
- ✅ 10 containers parados removidos
- ✅ Containers antigos do Dokploy limpos

### 3. Containers Parados Diversos (Removidos)
- ✅ `cloudflared-cloudflared-1` - Removido
- ✅ `cranky_proskuriakova` - Removido
- ✅ `wizardly_spence` (kestra parado) - Removido
- ✅ `frosty_euler` (docker welcome) - Removido
- ✅ `open-webui` - Removido

## Containers Mantidos

### 1. Containers do Projeto (Via docker-compose.yml)
- `ia-test-neo4j` - Neo4j Database
- `ia-test-api` - FastAPI
- `ia-test-frontend` - Svelte Frontend
- `ia-test-agent-dashboard` - Agent Dashboard
- `ia-test-bot` - Bot Streamlit (profile: streamlit)
- `ia-test-loader` - Loader Streamlit (profile: streamlit)
- `ia-test-pdf-bot` - PDF Bot Streamlit (profile: streamlit)
- `ia-test-mcp-manager` - MCP Manager (profile: tools)
- `ia-test-kestra` - Kestra (profile: tools)

### 2. Containers Externos (Mantidos)
- `dokploy.1.551ofp4t1v9ku7xw68tjjiu50` - Dokploy (se você usa)
- `postgres_aula` - Postgres Aula
- `redis` - Redis
- `dokploy-traefik` - Traefik (se você usa Dokploy)

### 3. Containers com Nomes Aleatórios (MCP Desktop)
- `strange_roentgen` - mcp/mongodb (MCP Desktop)
- `keen_volhard` - mcp/desktop-commander (MCP Desktop)
- Outros containers do MCP Desktop

**Nota**: Estes containers são do MCP Desktop, não do projeto principal. Podem ser removidos se não usar MCP Desktop.

## Melhorias Implementadas

### 1. Docker Compose Otimizado

#### Variáveis Compartilhadas
- ✅ Usa `x-common-variables` para variáveis de ambiente
- ✅ Reduz duplicação
- ✅ Facilita manutenção

#### Profiles
- ✅ `core` - Serviços essenciais (database, api, front-end, agent-dashboard)
- ✅ `streamlit` - Aplicações Streamlit (bot, loader, pdf_bot)
- ✅ `tools` - Ferramentas adicionais (mcp-manager, kestra)
- ✅ `ollama` - Ollama local (opcional)
- ✅ `pull-model` - Pull model (one-time job)

#### Volumes Nomeados
- ✅ `neo4j_data` - Dados do Neo4j
- ✅ `ollama_data` - Dados do Ollama
- ✅ `kestra_workflows` - Workflows do Kestra
- ✅ `kestra_data` - Dados do Kestra
- ✅ `embedding_model` - Bind mount para modelos de embedding

#### Networks Nomeados
- ✅ `ia-test-network` - Network principal
- ✅ Facilita comunicação entre containers
- ✅ Melhora isolamento

#### Container Names
- ✅ Todos os containers têm nomes descritivos
- ✅ Formato: `ia-test-{service-name}`
- ✅ Facilita identificação no Portainer

#### Health Checks
- ✅ Todos os serviços têm health checks
- ✅ Melhora confiabilidade
- ✅ Facilita monitoramento

#### Restart Policies
- ✅ `restart: unless-stopped` - Reinicia automaticamente
- ✅ Melhora disponibilidade
- ✅ Reduz necessidade de intervenção manual

## Como Usar

### Stack Completa (Todos os Serviços)
```bash
docker compose -f config/docker-compose.yml up -d
```

### Stack Core (Apenas Serviços Essenciais)
```bash
docker compose -f config/docker-compose.yml up -d
```

### Stack Core + Streamlit
```bash
docker compose -f config/docker-compose.yml --profile streamlit up -d
```

### Stack Core + Tools
```bash
docker compose -f config/docker-compose.yml --profile tools up -d
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
- ❌ Containers do n8n desnecessários
- ❌ Containers parados acumulados
- ❌ Duplicação de código
- ❌ Variáveis de ambiente repetidas
- ❌ Sem profiles
- ❌ Containers com nomes aleatórios
- ❌ Sem health checks em alguns serviços
- ❌ Sem restart policies

### Depois
- ✅ 4-8 containers (dependendo do profile)
- ✅ Containers do n8n removidos
- ✅ Containers parados limpos
- ✅ Código consolidado
- ✅ Variáveis compartilhadas
- ✅ Profiles para ativar/desativar serviços
- ✅ Containers com nomes descritivos
- ✅ Health checks em todos os serviços
- ✅ Restart policies configuradas
- ✅ Volumes nomeados
- ✅ Networks nomeados

## Próximos Passos

1. ✅ Testar a nova configuração
2. ✅ Verificar se todos os serviços funcionam
3. ✅ Ajustar profiles conforme necessário
4. ✅ Documentar mudanças
5. ✅ Atualizar scripts de deploy

## Containers com Nomes Aleatórios

Se você ver containers com nomes aleatórios (como `strange_roentgen`, `keen_volhard`, etc.):
- Estes são do MCP Desktop (não do projeto principal)
- Podem ser removidos se não usar MCP Desktop
- Use o script `scripts/stop_random_containers.ps1` para removê-los

## Scripts de Limpeza

### Windows PowerShell
```powershell
# Limpar containers inúteis
.\scripts\cleanup_containers.ps1

# Remover containers com nomes aleatórios
.\scripts\stop_random_containers.ps1
```

### Linux/Mac
```bash
# Limpar containers inúteis
chmod +x scripts/cleanup_containers.sh
./scripts/cleanup_containers.sh
```

## Referências

- [Docker Compose Profiles](https://docs.docker.com/compose/profiles/)
- [Docker Compose Best Practices](https://docs.docker.com/compose/best-practices/)
- [Docker Networking](https://docs.docker.com/network/)
- [Docker Optimization Guide](./DOCKER_OPTIMIZATION.md)

