# 💾 Onde os Dados do Projeto São Salvos

## 📊 Resumo

**O projeto NÃO está sendo salvo em PostgreSQL, MySQL ou outros bancos relacionais por padrão.**

Os dados do projeto são salvos principalmente em:

1. **Arquivos JSON** (configurações)
2. **Arquivos Python** (código)
3. **Obsidian** (notas e documentação)
4. **Neo4j** (quando sincronizado - opcional)

---

## 📁 Onde Cada Tipo de Dado é Salvo

### 1. Configurações de MCP Servers

**Localização:** `mcp_servers.json` (raiz do projeto)

**Conteúdo:**
- Lista de servidores MCP configurados
- Comandos, argumentos, variáveis de ambiente
- Status (habilitado/desabilitado)

**Exemplo:**
```json
{
  "filesystem": {
    "name": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem"],
    "enabled": false,
    "description": "Servidor MCP para acesso ao sistema de arquivos"
  }
}
```

**Gerenciado por:** `src/agents/mcp_manager.py`

---

### 2. Configurações do Sistema

**Localização:** `.env` (raiz do projeto)

**Conteúdo:**
- Variáveis de ambiente
- Chaves de API
- URLs de conexão
- Senhas e credenciais

**Gerenciado por:** Sistema de configuração Python

---

### 3. Notas e Documentação

**Localização:** `Obsidian_guardar aqui/` (pasta do projeto)

**Conteúdo:**
- Notas sobre agentes
- Documentação do projeto
- Mapeamento de estrutura
- Links e referências

**Gerenciado por:** `src/agents/mcp_obsidian_integration.py`

---

### 4. Dados no Neo4j (Opcional - quando sincronizado)

**Localização:** Neo4j Aura DB (cloud)

**Conteúdo:**
- Nós MCP (quando sincronizado)
- Nós de notas Obsidian (quando sincronizado)
- Relacionamentos entre componentes
- Embeddings para busca semântica

**Gerenciado por:** `src/agents/mcp_neo4j_integration.py`

---

## ❌ O que NÃO está sendo usado

### Bancos Relacionais (PostgreSQL, MySQL, etc.)

**Status:** ❌ **NÃO está sendo usado para salvar dados do projeto**

O projeto TEM suporte para:
- **Supabase** (PostgreSQL) - via `db_manager.py`
- **Neon** (PostgreSQL) - via `db_manager.py`
- **MongoDB** - via `db_manager.py`

Mas esses são **opcionais** e só são usados se você:
1. Configurar as variáveis de ambiente
2. Usar explicitamente o DB Manager para salvar dados

**Atualmente:** Nenhum desses está configurado ou sendo usado.

---

## ✅ Como Passar o Projeto para Neo4j Aura

### ❌ NÃO precisa usar PostgreSQL como intermediário!

Você pode sincronizar **diretamente** do projeto para Neo4j Aura via código.

### Método Recomendado: Sincronização Direta

#### 1. Sincronizar MCPs

```python
from src.agents.orchestrator import get_orchestrator

orchestrator = get_orchestrator()
result = orchestrator.sync_mcp_to_neo4j()

print(f"Sincronizados: {result['synced_count']} MCPs")
```

Isso lê o arquivo `mcp_servers.json` e cria nós no Neo4j.

#### 2. Sincronizar Obsidian

```python
result = orchestrator.sync_mcp_to_obsidian()
print(f"Criadas: {result['created_count']} notas")
```

Isso lê as notas do Obsidian e cria nós no Neo4j.

#### 3. Script Automático

```bash
python scripts/sync_to_neo4j.py
```

Este script sincroniza tudo automaticamente.

---

## 🔄 Fluxo de Dados

```
┌─────────────────┐
│  mcp_servers.json │  ← Arquivo JSON local
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Orchestrator    │  ← Lê arquivo JSON
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Neo4j Aura DB  │  ← Cria nós no grafo
└─────────────────┘
```

**NÃO precisa de PostgreSQL!** A sincronização é direta.

---

## 📋 Se Você Quiser Usar PostgreSQL

Se você realmente quiser usar PostgreSQL (Supabase ou Neon) como intermediário:

### Opção 1: Exportar para CSV e Importar

1. **Exportar dados do projeto:**
   ```python
   # Criar script para exportar mcp_servers.json para CSV
   import json
   import csv
   
   with open('mcp_servers.json', 'r') as f:
       data = json.load(f)
   
   # Converter para CSV
   with open('mcp_servers.csv', 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(['name', 'command', 'args', 'enabled', 'description'])
       for name, server in data.items():
           writer.writerow([
               server['name'],
               server['command'],
               str(server['args']),
               server['enabled'],
               server.get('description', '')
           ])
   ```

2. **Importar CSV no Neo4j Aura:**
   - Use a interface web do Neo4j Aura
   - Selecione "CSV Files"
   - Faça upload do CSV
   - Configure o mapeamento

### Opção 2: Salvar no Supabase/Neon Primeiro

1. **Configurar Supabase ou Neon:**
   ```bash
   # No .env
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua-chave
   # ou
   NEON_DATABASE_URL=postgresql://...
   ```

2. **Salvar dados no PostgreSQL:**
   ```python
   from src.agents.db_manager import get_db_manager
   
   db = get_db_manager()
   # Salvar dados do projeto
   ```

3. **Importar do PostgreSQL para Neo4j:**
   - Use a interface web do Neo4j Aura
   - Selecione "PostgreSQL"
   - Configure conexão
   - Importe

---

## 🎯 Recomendação Final

### ✅ Use Sincronização Direta (Mais Simples)

**Não precisa de PostgreSQL!** Use o script de sincronização:

```bash
python scripts/sync_to_neo4j.py
```

Isso:
- ✅ Lê `mcp_servers.json` diretamente
- ✅ Lê notas do Obsidian diretamente
- ✅ Cria nós no Neo4j Aura automaticamente
- ✅ Não precisa de intermediários
- ✅ Mais rápido e simples

### ❌ Use PostgreSQL Apenas Se:

- Você já tem dados em PostgreSQL que quer importar
- Você quer usar PostgreSQL para outras coisas além do Neo4j
- Você precisa de um backup intermediário

---

## 📊 Estrutura de Dados no Neo4j

Quando sincronizado, os dados ficam assim no Neo4j:

```
(MCP:MCPServer {name: "filesystem", command: "npx", ...})
     │
     ├─[:HAS_TOOL]→ (Tool {name: "...", description: "..."})
     │
     └─[:RELATED_TO]→ (ObsidianNote {title: "...", content: "..."})
```

---

## 🔍 Verificar Onde os Dados Estão

### Verificar Arquivos Locais:

```bash
# Ver configurações MCP
cat mcp_servers.json

# Ver variáveis de ambiente
cat .env

# Ver notas Obsidian
ls Obsidian_guardar\ aqui/
```

### Verificar no Neo4j:

```cypher
// Ver todos os nós MCP
MATCH (n:MCP)
RETURN n

// Contar nós
MATCH (n)
RETURN labels(n) as tipo, count(n) as quantidade
```

---

## 💡 Resumo

| Tipo de Dado | Onde Está Salvo | Como Sincronizar para Neo4j |
|--------------|------------------|----------------------------|
| MCP Servers | `mcp_servers.json` | `orchestrator.sync_mcp_to_neo4j()` |
| Notas Obsidian | `Obsidian_guardar aqui/` | `orchestrator.sync_mcp_to_obsidian()` |
| Configurações | `.env` | Não precisa (são variáveis) |
| Código | `src/` | Não precisa (é código) |

**NÃO está em PostgreSQL/MySQL por padrão!**

---

**Última atualização:** 2025-01-27


