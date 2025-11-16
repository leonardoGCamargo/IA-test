# 📊 Neo4j GraphRAG

> **Tipo:** GraphRAG  
> **Arquivo:** `mcp_neo4j_integration.py`  
> **Status:** ✅ Funcional

## 📋 Descrição

Gestão de grafo de conhecimento Neo4j com GraphRAG usando LangGraph. Permite armazenar MCPs, RAGs e notas Obsidian em um grafo conectado.

## 🎯 Funcionalidades

- Armazenar nós MCP, RAG e Obsidian no Neo4j
- Consultas GraphRAG usando LangGraph
- Busca semântica com embeddings
- Visualização de grafo
- Importar vault Obsidian completo

## 💻 Como Usar

```python
from mcp_neo4j_integration import get_neo4j_manager

neo4j = get_neo4j_manager()

# Criar nó MCP
neo4j.create_mcp_node({
    "name": "filesystem",
    "id": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem"],
    "description": "Servidor filesystem",
    "enabled": True
})

# Consultar GraphRAG
answer = neo4j.query_graphrag("Quais MCPs estão relacionados a filesystem?")
print(answer)

# Importar vault Obsidian
from pathlib import Path
imported = neo4j.import_obsidian_vault(Path("/caminho/vault"))
print(f"Importadas {imported} notas")

# Estatísticas
stats = neo4j.get_graph_statistics()
print(f"MCPs: {stats['MCP_count']}")
print(f"RAGs: {stats['RAG_count']}")
print(f"Notas Obsidian: {stats['ObsidianNote_count']}")
```

### Via Orchestrator

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Criar nó
task = orchestrator.create_task(
    AgentType.NEO4J_GRAPHRAG,
    "Criar nó MCP",
    {
        "action": "create_mcp_node",
        "mcp_info": {
            "name": "filesystem",
            "id": "filesystem",
            "description": "Servidor filesystem"
        }
    }
)
result = orchestrator.execute_task(task)

# Consultar GraphRAG
task = orchestrator.create_task(
    AgentType.NEO4J_GRAPHRAG,
    "Consultar grafo",
    {
        "action": "query_graphrag",
        "question": "Quais MCPs existem?"
    }
)
result = orchestrator.execute_task(task)
```

## 📊 Métodos Principais

- `create_mcp_node(mcp_info)` - Criar nó MCP
- `create_rag_node(rag_info)` - Criar nó RAG
- `create_obsidian_note_node(note_path, content)` - Criar nó Obsidian
- `query_graphrag(question)` - Consultar GraphRAG
- `import_obsidian_vault(vault_path)` - Importar vault
- `get_graph_statistics()` - Estatísticas do grafo
- `get_graph_visualization_data()` - Dados para visualização

## 🔗 Links Relacionados

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[Orchestrator|Orchestrator]]
- [[Obsidian-Integration|Obsidian Integration]]

## 🏷️ Tags

#neo4j #graphrag #langgraph #grafo #documentação

