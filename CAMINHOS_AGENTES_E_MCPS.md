# 📍 Caminhos dos Agentes e MCPs - Referência Rápida

## 🤖 AGENTES

**Caminho Base:** `src/agents/`

### Agentes Principais (Ativos)

| Agente | Caminho Completo | Função |
|--------|------------------|--------|
| Orchestrator | `src/agents/orchestrator.py` | Coordenador central |
| System Health | `src/agents/system_health_agent.py` | Saúde do sistema |
| DB Manager | `src/agents/db_manager.py` | Gerenciador de bancos |
| MCP Manager | `src/agents/mcp_manager.py` | Gerenciador MCP |
| Git Integration | `src/agents/git_integration.py` | Integração Git |
| Neo4j GraphRAG | `src/agents/mcp_neo4j_integration.py` | GraphRAG Neo4j |
| Obsidian Integration | `src/agents/mcp_obsidian_integration.py` | Integração Obsidian |
| Docker Integration | `src/agents/mcp_docker_integration.py` | Integração Docker |
| Kestra Integration | `src/agents/mcp_kestra_integration.py` | Integração Kestra |

### Agentes Deprecated (Mantidos para Compatibilidade)

| Agente | Caminho Completo | Status |
|--------|------------------|--------|
| Diagnostic Agent | `src/agents/diagnostic_agent.py` | ⚠️ Deprecated |
| Resolution Agent | `src/agents/resolution_agent.py` | ⚠️ Deprecated |
| Agent Helper System | `src/agents/agent_helper_system.py` | ⚠️ Deprecated |

**Importação:**
```python
from src.agents import get_orchestrator, get_mcp_manager
```

---

## 🔌 MCPS

### Configuração do Projeto

**Caminho:** `mcp_servers.json` (raiz do projeto)

MCPs configurados:
- `neo4j` - `@neo4j/mcp-server-neo4j` ✅
- `obsidian` - `@modelcontextprotocol/server-obsidian` ✅
- `git` - `@modelcontextprotocol/server-git` ✅
- `filesystem` - `@modelcontextprotocol/server-filesystem` ❌

### Configuração do Cursor

**Caminho:** `.cursor/mcp.json`

MCPs configurados:
- `neo4j-cypher` - `@neo4j/mcp-server-neo4j` ✅

**Uso:**
- No Cursor: Pergunte diretamente no chat
- No código: Via `MCPManager` em `src/agents/mcp_manager.py`

---

## 📚 Documentação Completa

Para mais detalhes, veja:
- `docs/ESTRUTURA_AGENTES_E_MCPS.md` - Estrutura completa
- `docs/ORGANIZACAO_E_LIMPEZA.md` - Organização do projeto

---

**Última atualização**: 2025-01-27

