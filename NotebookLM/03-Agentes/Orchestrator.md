# 🎯 Orchestrator (Coordenador Central)

> **Tipo:** Coordenador  
> **Arquivo:** `orchestrator.py`  
> **Status:** ✅ Funcional

## 📋 Descrição

O Orchestrator é o coordenador central do sistema de agentes. Ele gerencia tarefas, coordena múltiplos agentes especializados e monitora o status do sistema inteiro.

## 🎯 Funcionalidades

- **Gerenciamento de Tarefas**: Criar e executar tarefas delegando para agentes
- **Coordenação**: Coordenar múltiplos agentes simultaneamente
- **Sincronização**: Sincronizar dados entre componentes (MCP → Neo4j → Obsidian)
- **Monitoramento**: Status do sistema em tempo real
- **Delegação**: Distribuir tarefas para agentes especializados

## 💻 Como Usar

### Uso Básico

```python
from orchestrator import get_orchestrator, AgentType

# Obter instância
orchestrator = get_orchestrator()

# Criar tarefa
task = orchestrator.create_task(
    AgentType.MCP_ARCHITECT,
    "Listar servidores MCP",
    {"action": "list_servers"}
)

# Executar tarefa
result = orchestrator.execute_task(task)
print(result)
```

### Sincronização Automática

```python
# Sincronizar MCPs para Neo4j
result = orchestrator.sync_mcp_to_neo4j()
print(f"Sincronizados: {result['synced']}, Falhas: {result['failed']}")

# Sincronizar MCPs para Obsidian
result = orchestrator.sync_mcp_to_obsidian()
print(f"Criadas: {result['created']}, Falhas: {result['failed']}")
```

### Status do Sistema

```python
status = orchestrator.get_system_status()
print(f"MCP Manager: {status['mcp_manager']['servers_count']} servidores")
print(f"Neo4j: {'✅' if status['neo4j']['available'] else '❌'}")
print(f"Kestra: {'✅' if status['kestra']['available'] else '❌'}")
```

## 🔧 Tipos de Agentes Suportados

- `AgentType.MCP_ARCHITECT` - MCP Manager
- `AgentType.DOCKER_INTEGRATION` - Docker Integration
- `AgentType.OBSIDIAN` - Obsidian Integration
- `AgentType.NEO4J_GRAPHRAG` - Neo4j GraphRAG
- `AgentType.KESTRA` - Kestra Agent
- `AgentType.KESTRA_LANGCHAIN_MASTER` - Master Agent
- `AgentType.AGENT_HELPER` - Helper System

## 📊 Métodos Principais

### `create_task(agent_type, description, parameters)`

Cria uma nova tarefa para um agente.

```python
task = orchestrator.create_task(
    AgentType.MCP_ARCHITECT,
    "Adicionar servidor MCP",
    {
        "action": "add_server",
        "server_info": {...}
    }
)
```

### `execute_task(task)`

Executa uma tarefa delegando para o agente apropriado.

```python
result = orchestrator.execute_task(task)
```

### `sync_mcp_to_neo4j(server_name=None)`

Sincroniza servidores MCP para o Neo4j.

```python
result = orchestrator.sync_mcp_to_neo4j()
# ou para um servidor específico
result = orchestrator.sync_mcp_to_neo4j("filesystem")
```

### `sync_mcp_to_obsidian(server_name=None)`

Sincroniza servidores MCP para o Obsidian.

```python
result = orchestrator.sync_mcp_to_obsidian()
```

### `get_system_status()`

Retorna status completo do sistema.

```python
status = orchestrator.get_system_status()
```

## 🔗 Links Relacionados

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[Master-Agent|Master Agent]]
- [[Helper-System|Helper System]]
- [[MCP-Manager|MCP Manager]]
- [[ARCHITECTURE|Arquitetura do Sistema]]

## 📝 Exemplo Completo

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# 1. Verificar status
status = orchestrator.get_system_status()
print("Status do Sistema:", status)

# 2. Sincronizar componentes
orchestrator.sync_mcp_to_neo4j()
orchestrator.sync_mcp_to_obsidian()

# 3. Criar tarefa complexa via Master Agent
task = orchestrator.create_task(
    AgentType.KESTRA_LANGCHAIN_MASTER,
    "Criar workflow inteligente",
    {
        "action": "create_intelligent_workflow",
        "description": "Sincronização semanal de todos os sistemas"
    }
)
result = orchestrator.execute_task(task)
print("Workflow criado:", result["id"])
```

## 🏷️ Tags

#orchestrator #coordenador #agente #sistema #documentação

---

**Ver também:** [[ORCHESTRATOR_SUMMARY|Resumo do Orchestrator]]

