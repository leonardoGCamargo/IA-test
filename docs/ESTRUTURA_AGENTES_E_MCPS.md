# 📁 Estrutura de Agentes e MCPs - IA-Test Project

Este documento explica a organização dos agentes e MCPs no projeto.

## 🤖 Agentes do Sistema

### 📍 Localização
**Caminho:** `src/agents/`

Todos os agentes estão localizados em `src/agents/` e são módulos Python independentes.

### 📋 Lista de Agentes

#### 1. **Orchestrator** (Coordenador Central)
- **Arquivo:** `src/agents/orchestrator.py`
- **Função:** Coordena todos os outros agentes, planejamento inteligente
- **Usa LLM:** ✅ Sim
- **Importa:** Todos os outros agentes

#### 2. **System Health Agent** (Saúde do Sistema)
- **Arquivo:** `src/agents/system_health_agent.py`
- **Função:** Diagnóstico, monitoramento e resolução de problemas
- **Usa LLM:** ❌ Não
- **Consolidado:** Diagnostic + Helper + Resolution

#### 3. **DB Manager** (Gerenciador de Bancos)
- **Arquivo:** `src/agents/db_manager.py`
- **Função:** Gerenciamento de bancos de dados (Neo4j, Neon, MongoDB, Supabase)
- **Usa LLM:** ❌ Não

#### 4. **MCP Manager** (Gerenciador MCP)
- **Arquivo:** `src/agents/mcp_manager.py`
- **Função:** Gerenciamento de servidores MCP
- **Usa LLM:** ❌ Não

#### 5. **Git Integration** (Integração Git)
- **Arquivo:** `src/agents/git_integration.py`
- **Função:** Operações Git/GitHub
- **Usa LLM:** ❌ Não

#### 6. **Neo4j GraphRAG** (GraphRAG com Neo4j)
- **Arquivo:** `src/agents/mcp_neo4j_integration.py`
- **Função:** GraphRAG e busca semântica no Neo4j
- **Usa LLM:** ✅ Sim

#### 7. **Obsidian Integration** (Integração Obsidian)
- **Arquivo:** `src/agents/mcp_obsidian_integration.py`
- **Função:** Gerenciamento de notas Obsidian
- **Usa LLM:** ❌ Não

#### 8. **Docker Integration** (Integração Docker)
- **Arquivo:** `src/agents/mcp_docker_integration.py`
- **Função:** Detecção e gerenciamento de containers Docker
- **Usa LLM:** ❌ Não

#### 9. **Kestra Integration** (Integração Kestra)
- **Arquivo:** `src/agents/mcp_kestra_integration.py`
- **Função:** Orquestração de workflows Kestra
- **Usa LLM:** ❌ Não

### 🔧 Agentes Auxiliares (Deprecated mas mantidos para compatibilidade)

#### 10. **Diagnostic Agent**
- **Arquivo:** `src/agents/diagnostic_agent.py`
- **Status:** ⚠️ Deprecated - Funcionalidades migradas para System Health Agent
- **Mantido para:** Compatibilidade

#### 11. **Resolution Agent**
- **Arquivo:** `src/agents/resolution_agent.py`
- **Status:** ⚠️ Deprecated - Funcionalidades migradas para System Health Agent
- **Mantido para:** Compatibilidade

#### 12. **Agent Helper System**
- **Arquivo:** `src/agents/agent_helper_system.py`
- **Status:** ⚠️ Deprecated - Funcionalidades migradas para System Health Agent
- **Mantido para:** Compatibilidade

### 📦 Estrutura de Imports

Todos os agentes são importados através de `src/agents/__init__.py`:

```python
from src.agents import (
    get_orchestrator,
    get_mcp_manager,
    get_neo4j_manager,
    get_kestra_agent,
    get_git_agent,
    get_db_manager,
    get_system_health_agent
)
```

---

## 🔌 MCPs (Model Context Protocol)

### 📍 Localização
**Caminho:** Configurado em `mcp_servers.json` (raiz do projeto)

Os MCPs são servidores externos gerenciados via `npx` e configurados no arquivo `mcp_servers.json`.

### 📋 MCPs Configurados

#### 1. **Neo4j MCP**
- **ID:** `neo4j`
- **Pacote:** `@neo4j/mcp-server-neo4j`
- **Status:** ✅ Habilitado
- **Função:** GraphRAG e conhecimento estruturado
- **Configuração:** Via variáveis de ambiente (NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

#### 2. **Obsidian MCP**
- **ID:** `obsidian`
- **Pacote:** `@modelcontextprotocol/server-obsidian`
- **Status:** ✅ Habilitado
- **Função:** Gestão de notas Obsidian
- **Configuração:** Via variável OBSIDIAN_VAULT_PATH

#### 3. **Git MCP**
- **ID:** `git`
- **Pacote:** `@modelcontextprotocol/server-git`
- **Status:** ✅ Habilitado
- **Função:** Operações Git/GitHub
- **Configuração:** Usa repositório atual

#### 4. **Filesystem MCP**
- **ID:** `filesystem`
- **Pacote:** `@modelcontextprotocol/server-filesystem`
- **Status:** ❌ Desabilitado (opcional)
- **Função:** Acesso ao sistema de arquivos
- **Configuração:** Caminho do diretório

### 🔧 Configuração no Cursor

Os MCPs também podem ser configurados diretamente no Cursor via `.cursor/mcp.json`:

**Caminho:** `.cursor/mcp.json`

Atualmente configurado:
- **Neo4j Cypher MCP** - Para uso direto no Cursor

### 📝 Arquivo de Configuração

**`mcp_servers.json`** (raiz do projeto):
```json
{
  "neo4j": { ... },
  "obsidian": { ... },
  "git": { ... },
  "filesystem": { ... }
}
```

---

## 🗂️ Estrutura de Diretórios

```
IA-test/
├── src/
│   └── agents/              # 🤖 TODOS OS AGENTES AQUI
│       ├── __init__.py      # Exports principais
│       ├── orchestrator.py  # Coordenador central
│       ├── system_health_agent.py
│       ├── db_manager.py
│       ├── mcp_manager.py
│       ├── git_integration.py
│       ├── mcp_neo4j_integration.py
│       ├── mcp_obsidian_integration.py
│       ├── mcp_docker_integration.py
│       ├── mcp_kestra_integration.py
│       ├── diagnostic_agent.py      # Deprecated
│       ├── resolution_agent.py       # Deprecated
│       └── agent_helper_system.py   # Deprecated
│
├── mcp_servers.json         # 🔌 CONFIGURAÇÃO DOS MCPS
├── .cursor/
│   └── mcp.json            # 🔌 MCPs para uso no Cursor
│
└── docs/
    └── ESTRUTURA_AGENTES_E_MCPS.md  # Este arquivo
```

---

## 🔄 Diferença entre Agentes e MCPs

### Agentes (`src/agents/`)
- ✅ **Código Python próprio** do projeto
- ✅ **Importados diretamente** via `from src.agents import ...`
- ✅ **Controlados pelo projeto**
- ✅ **Podem usar LLM** (Orchestrator, Neo4j GraphRAG)
- ✅ **Integrados com o sistema**

### MCPs (`mcp_servers.json`)
- ✅ **Servidores externos** executados via `npx`
- ✅ **Gerenciados pelo MCP Manager**
- ✅ **Protocolo Model Context Protocol**
- ✅ **Comunicação via stdio/HTTP**
- ✅ **Podem ser usados no Cursor diretamente**

---

## 📚 Como Usar

### Importar um Agente

```python
from src.agents import get_orchestrator, get_mcp_manager

orchestrator = get_orchestrator()
mcp_manager = get_mcp_manager()
```

### Usar um MCP

```python
from src.agents.mcp_manager import get_mcp_manager

mcp_manager = get_mcp_manager()
# MCPs estão disponíveis via mcp_manager
```

### No Cursor Chat

Com MCPs configurados em `.cursor/mcp.json`, você pode perguntar diretamente:
- "Liste os nós no Neo4j"
- "Crie uma nota no Obsidian"
- "Quais são os commits recentes?"

---

## 🎯 Resumo Rápido

| Tipo | Localização | Exemplo |
|------|-------------|---------|
| **Agentes** | `src/agents/` | `src/agents/orchestrator.py` |
| **MCPs** | `mcp_servers.json` | `"neo4j": { ... }` |
| **MCPs Cursor** | `.cursor/mcp.json` | `"neo4j-cypher": { ... }` |

---

**Última atualização**: 2025-01-27

