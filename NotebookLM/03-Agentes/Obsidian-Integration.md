# 📝 Obsidian Integration

> **Tipo:** Integração Obsidian  
> **Arquivo:** `mcp_obsidian_integration.py`  
> **Status:** ✅ Funcional

## 📋 Descrição

Gestão de notas no Obsidian. Permite criar notas sobre MCPs e RAGs, gerenciar links entre notas e buscar conteúdo.

## 🎯 Funcionalidades

- Criar notas sobre MCPs e RAGs
- Gerenciar links entre notas
- Buscar em notas
- Organizar por pastas
- Criar notas de conexão

## 💻 Como Usar

```python
from mcp_obsidian_integration import ObsidianManager

obsidian = ObsidianManager()

# Configurar vault
obsidian.set_vault_path("/caminho/para/vault")

# Criar nota sobre MCP
obsidian.create_mcp_note("filesystem", {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem"],
    "description": "Servidor filesystem",
    "enabled": True
})

# Criar nota sobre RAG
obsidian.create_rag_note("Meu RAG", {
    "description": "Sistema RAG customizado",
    "model": "llama2",
    "embedding_model": "sentence_transformer"
})

# Buscar notas
notes = obsidian.search_notes("MCP")
for note in notes:
    print(note.name)

# Listar notas
mcp_notes = obsidian.list_notes("MCP")
rag_notes = obsidian.list_notes("RAG")
```

### Via Orchestrator

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

task = orchestrator.create_task(
    AgentType.OBSIDIAN,
    "Criar nota MCP",
    {
        "action": "create_mcp_note",
        "mcp_name": "filesystem",
        "mcp_info": {
            "command": "npx",
            "description": "Servidor filesystem"
        }
    }
)
result = orchestrator.execute_task(task)
```

## 📊 Métodos Principais

- `create_note(title, content, folder)` - Criar nota genérica
- `create_mcp_note(mcp_name, mcp_info)` - Criar nota sobre MCP
- `create_rag_note(rag_name, rag_info)` - Criar nota sobre RAG
- `link_notes(note1_path, note2_path)` - Criar links entre notas
- `list_notes(folder)` - Listar notas
- `search_notes(query, folder)` - Buscar notas

## 🔗 Links Relacionados

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[01-Guia-Obsidian|Guia do Obsidian]]
- [[Orchestrator|Orchestrator]]
- [[Neo4j-GraphRAG|Neo4j GraphRAG]]

## 🏷️ Tags

#obsidian #notas #integração #documentação

