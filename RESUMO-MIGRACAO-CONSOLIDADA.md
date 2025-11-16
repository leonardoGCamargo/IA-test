# Migração Consolidada - N8N + Dokploy

## Porta do N8N

**Porta:** `5678`
**URL:** `http://localhost:5678`

## Configuração Consolidada

### O que foi feito:

1. ✅ **N8N usa PostgreSQL do Dokploy** (compartilhado)
   - Não precisa de PostgreSQL separado para N8N
   - Economia de recursos
   - Gerenciamento unificado

2. ✅ **Scripts criados sem confirmação:**
   - `scripts/migrar_automatico.py` - Migração automática
   - `scripts/iniciar_consolidado.ps1` - Inicia tudo automaticamente

3. ✅ **Configuração otimizada:**
   - Todos os containers com sufixo `-consolidado`
   - Network compartilhada
   - Volumes persistentes

## Estrutura Consolidada

### N8N (5 containers)
- `n8n-consolidado` - Porta 5678
- `n8n-worker-consolidado`
- `n8n-runner-consolidado`
- `n8n-redis-consolidado`
- `n8n-ollama-consolidado` (opcional)

### Dokploy (3 containers)
- `dokploy-consolidado` - Porta 3000
- `dokploy-postgres-consolidado` - **Compartilhado com N8N**
- `dokploy-redis-consolidado`

## Como Usar

### 1. Migrar Containers Antigos (Automático)

```powershell
python scripts/migrar_automatico.py
```

### 2. Iniciar Configuração Consolidada

```powershell
# Opção 1: Script PowerShell (recomendado)
.\scripts\iniciar_consolidado.ps1

# Opção 2: Docker Compose direto
docker compose -f config/docker-compose-consolidado.yml up -d
```

### 3. Ver Status

```bash
docker compose -f config/docker-compose-consolidado.yml ps
```

## URLs dos Serviços

| Serviço | URL | Porta |
|---------|-----|-------|
| N8N | http://localhost:5678 | 5678 |
| Dokploy | http://localhost:3000 | 3000 |

## PostgreSQL Compartilhado

O PostgreSQL do Dokploy agora serve tanto o Dokploy quanto o N8N:

- **Banco Dokploy:** `dokploy`
- **Banco N8N:** `n8n` (criado automaticamente)

## Observações

- ✅ Scripts não travam (sem confirmação interativa)
- ✅ PostgreSQL compartilhado economiza recursos
- ✅ Todos os containers com nomes consistentes
- ✅ Network compartilhada para comunicação


