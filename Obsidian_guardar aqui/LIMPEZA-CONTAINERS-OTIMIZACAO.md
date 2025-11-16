# Limpeza e Otimização de Containers Docker

## Situação Inicial

- **Total de containers**: 44
- **Containers órfãos**: 29+ (com nomes aleatórios do MCP)
- **Containers do projeto IA-test**: 0 (nenhum rodando)
- **Containers do N8N**: 6 (mantidos)

## Problemas Identificados

1. **Containers órfãos do MCP**: Muitos containers com nomes aleatórios (ex: `cool_chaplygin`, `gracious_newton`) que são do MCP Desktop e não são necessários para o projeto
2. **Containers parados**: Vários containers em estado "Exited" acumulados
3. **Docker Compose sem profiles**: Todos os serviços eram iniciados juntos, sem opção de escolher quais rodar

## Ações Executadas

### 1. Remoção de Containers Órfãos

Script criado: `scripts/remover_containers_orfos.py`

- Remove automaticamente containers com nomes aleatórios
- Mantém containers importantes: `ia-test`, `n8n`, `dokploy`, `postgres`, `redis`, `ollama`, `kestra`, `neo4j`, `traefik`
- Remove containers parados

### 2. Otimização do Docker Compose

Arquivo: `config/docker-compose.yml`

**Melhorias implementadas:**

#### Profiles Adicionados

- **`core`**: Serviços essenciais (database, api, front-end, agent-dashboard)
  - Agora todos os serviços core têm `profiles: ["core"]`
  - Permite iniciar apenas o essencial: `docker compose --profile core up -d`

- **`streamlit`**: Aplicações Streamlit (bot, loader, pdf-bot)
  - Já existia, mantido

- **`tools`**: Ferramentas adicionais (mcp-manager, kestra)
  - Já existia, mantido

- **`ollama`**: Ollama local (opcional)
  - Já existia, mantido

#### Benefícios

1. **Controle granular**: Escolha quais serviços iniciar
2. **Economia de recursos**: Inicie apenas o necessário
3. **Desenvolvimento**: Use apenas `core` para desenvolvimento
4. **Produção**: Adicione profiles conforme necessário

## Como Usar

### Stack Mínima (Core)

```bash
# Apenas serviços essenciais
docker compose -f config/docker-compose.yml --profile core up -d
```

Isso inicia:
- `ia-test-neo4j` (database)
- `ia-test-api` (API)
- `ia-test-frontend` (Frontend)
- `ia-test-agent-dashboard` (Dashboard)

### Stack Completa

```bash
# Todos os serviços
docker compose -f config/docker-compose.yml --profile core --profile streamlit --profile tools up -d
```

### Apenas Serviços Específicos

```bash
# Apenas database e API
docker compose -f config/docker-compose.yml --profile core up -d database api

# Apenas dashboard
docker compose -f config/docker-compose.yml --profile core up -d agent-dashboard
```

## Containers Mantidos

### N8N (Mantido conforme solicitado)

- `iaimplementation-n8nrunnerpostgresollama-ep0mt9-n8n-1`
- `iaimplementation-n8nrunnerpostgresollama-ep0mt9-n8n-runner-1`
- `iaimplementation-n8nrunnerpostgresollama-ep0mt9-n8n-worker-1`
- `iaimplementation-n8nrunnerpostgresollama-ep0mt9-postgres-1`
- `iaimplementation-n8nrunnerpostgresollama-ep0mt9-redis-1`
- `iaimplementation-n8nrunnerpostgresollama-ep0mt9-ollama-1`

### Outros Serviços

- `dokploy-*` (Dokploy deployment)
- `redis` (Redis standalone)
- `postgres_aula` (PostgreSQL para aulas)

## Scripts Disponíveis

1. **`scripts/remover_containers_orfos.py`**
   - Remove containers órfãos automaticamente
   - Não remove containers importantes

2. **`scripts/limpar_e_otimizar_containers.py`**
   - Análise completa de containers
   - Modo simulação e execução
   - Requer confirmação (`--executar`)

3. **`scripts/limpar_containers_mcp.py`**
   - Focado em containers MCP
   - Modo simulação e execução

## Resultado Final

- **Containers órfãos removidos**: 29+
- **Containers do projeto**: Configurados com profiles
- **Controle granular**: Escolha quais serviços iniciar
- **N8N mantido**: Todos os containers do N8N preservados

## Próximos Passos

1. ✅ Containers órfãos removidos
2. ✅ Docker Compose otimizado com profiles
3. ⏳ Testar stack core: `docker compose --profile core up -d`
4. ⏳ Verificar se todos os serviços funcionam corretamente
5. ⏳ Documentar portas e URLs dos serviços

## Comandos Úteis

```bash
# Ver containers rodando
docker ps

# Ver todos os containers
docker ps -a

# Parar stack core
docker compose -f config/docker-compose.yml --profile core down

# Ver logs
docker compose -f config/docker-compose.yml logs -f

# Reiniciar serviço específico
docker compose -f config/docker-compose.yml restart api
```

