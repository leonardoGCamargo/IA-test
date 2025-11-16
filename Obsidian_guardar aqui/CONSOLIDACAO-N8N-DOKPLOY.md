# Consolidação N8N + Dokploy

## Problemas Identificados

### 1. PostgreSQL (`postgres_aula`)
- **Status**: Parado (Exited 0)
- **Causa**: Foi parado manualmente
- **Logs**: Iniciou normalmente, sem erros críticos
- **Ação**: Pode ser removido se não for necessário, ou iniciado se precisar

### 2. Traefik (`dokploy-traefik`)
- **Status**: Parado (Exited 0)
- **Causas**:
  1. **Rate Limit do Let's Encrypt**: Muitos certificados solicitados (50+ em 7 dias)
  2. **Problemas de conexão**: Erros ao conectar com Docker daemon
- **Ação**: Desabilitado por padrão na configuração consolidada (profile `traefik`)

## Solução: Configuração Consolidada

Foi criado um `docker-compose-consolidado.yml` que:
- ✅ Consolida N8N e Dokploy em uma única configuração
- ✅ Compartilha network para comunicação entre serviços
- ✅ Usa volumes nomeados para persistência
- ✅ Health checks em todos os serviços
- ✅ Traefik opcional (via profile)

## Estrutura Consolidada

### N8N (5 containers)
1. `n8n-postgres-consolidado` - PostgreSQL para N8N
2. `n8n-redis-consolidado` - Redis para filas
3. `n8n-consolidado` - N8N principal
4. `n8n-worker-consolidado` - Worker para processamento
5. `n8n-runner-consolidado` - Runner para execuções
6. `n8n-ollama-consolidado` - Ollama (opcional, profile `ollama`)

### Dokploy (3 containers)
1. `dokploy-postgres-consolidado` - PostgreSQL para Dokploy
2. `dokploy-redis-consolidado` - Redis para Dokploy
3. `dokploy-consolidado` - Dokploy principal

### Traefik (opcional)
- `traefik-consolidado` - Traefik (profile `traefik`)

## Como Usar

### 1. Migrar Containers Antigos

```bash
# Ver o que será migrado (simulação)
python scripts/migrar_para_consolidado.py

# Executar migração
python scripts/migrar_para_consolidado.py --executar
```

### 2. Iniciar Configuração Consolidada

```bash
# Stack completa (N8N + Dokploy)
docker compose -f config/docker-compose-consolidado.yml up -d

# Apenas N8N
docker compose -f config/docker-compose-consolidado.yml up -d n8n-postgres n8n-redis n8n n8n-worker n8n-runner

# Apenas Dokploy
docker compose -f config/docker-compose-consolidado.yml up -d dokploy-postgres dokploy-redis dokploy

# Com Ollama
docker compose -f config/docker-compose-consolidado.yml --profile ollama up -d

# Com Traefik (se necessário)
docker compose -f config/docker-compose-consolidado.yml --profile traefik up -d
```

### 3. Parar Serviços

```bash
# Parar tudo
docker compose -f config/docker-compose-consolidado.yml down

# Parar apenas N8N
docker compose -f config/docker-compose-consolidado.yml stop n8n n8n-worker n8n-runner

# Parar apenas Dokploy
docker compose -f config/docker-compose-consolidado.yml stop dokploy
```

## Portas

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| N8N | 5678 | Interface web do N8N |
| Dokploy | 3000 | Interface web do Dokploy |
| Traefik | 80, 443, 8080 | HTTP, HTTPS, Dashboard |
| Ollama | 11434 | API do Ollama |

## Volumes

Todos os volumes são nomeados e persistentes:

**N8N:**
- `n8n-postgres-data-consolidado`
- `n8n-redis-data-consolidado`
- `n8n-data-consolidado`
- `n8n-ollama-data-consolidado`

**Dokploy:**
- `dokploy-postgres-data-consolidado`
- `dokploy-redis-data-consolidado`
- `dokploy-data-consolidado`

## Network

Todos os serviços compartilham a network `consolidated-network` para comunicação interna.

## Benefícios

1. ✅ **Gerenciamento único**: Um único arquivo docker-compose
2. ✅ **Network compartilhada**: Comunicação facilitada entre serviços
3. ✅ **Volumes persistentes**: Dados preservados
4. ✅ **Health checks**: Monitoramento automático
5. ✅ **Profiles**: Ativa/desativa serviços conforme necessário
6. ✅ **Nomes consistentes**: Todos com sufixo `-consolidado`

## Migração de Dados

Os volumes antigos não são migrados automaticamente. Se precisar migrar dados:

1. **N8N**: Copie dados de `~/.n8n` ou do volume antigo
2. **Dokploy**: Copie dados do volume antigo do Dokploy
3. **PostgreSQL**: Use `pg_dump` e `pg_restore` se necessário

## Troubleshooting

### Traefik com Rate Limit

Se o Traefik falhar por rate limit do Let's Encrypt:
- Use o profile `traefik` apenas quando necessário
- Ou configure certificados manuais
- Ou use outro provedor de certificados

### PostgreSQL parado

Se `postgres_aula` estiver parado e você precisar:
```bash
docker start postgres_aula
```

Ou remova se não for necessário:
```bash
docker rm postgres_aula
```

## Próximos Passos

1. ✅ Configuração consolidada criada
2. ⏳ Migrar containers antigos
3. ⏳ Testar nova configuração
4. ⏳ Verificar se todos os serviços funcionam
5. ⏳ Documentar URLs e credenciais

