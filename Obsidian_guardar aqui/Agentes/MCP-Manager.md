# 🔌 MCP Manager

> **Tipo:** Gerenciador MCP  
> **Arquivo:** `mcp_manager.py`  
> **Interface:** `mcp_manager_ui.py`  
> **Status:** ✅ Funcional

## 📋 Descrição

Gerenciador centralizado de servidores MCP (Model Context Protocol). Permite gerenciar, monitorar e configurar servidores MCP.

## 🎯 Funcionalidades

- Gerenciar servidores MCP (CRUD)
- Health checks e monitoramento
- Listar recursos e ferramentas
- Conectar/desconectar servidores
- Interface web Streamlit (porta 8506)

## 💻 Como Usar

### Uso Básico

```python
from mcp_manager import get_mcp_manager, MCPServer

mcp_manager = get_mcp_manager()

# Adicionar servidor
server = MCPServer(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path"],
    description="Servidor de filesystem",
    enabled=True
)
mcp_manager.add_server(server)

# Listar servidores
servers = mcp_manager.list_servers()
for server in servers:
    print(f"{server.name}: {'✅' if server.enabled else '❌'}")

# Health check
import asyncio
health = asyncio.run(mcp_manager.check_server_health("filesystem"))
print(health)
```

### Via Orchestrator

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Listar servidores
task = orchestrator.create_task(
    AgentType.MCP_ARCHITECT,
    "Listar servidores MCP",
    {"action": "list_servers"}
)
result = orchestrator.execute_task(task)

# Health check
task = orchestrator.create_task(
    AgentType.MCP_ARCHITECT,
    "Verificar saúde do servidor",
    {"action": "check_health", "server_name": "filesystem"}
)
result = orchestrator.execute_task(task)
```

### Interface Web

Acesse: http://localhost:8506

Funcionalidades na UI:
- Visualizar todos os servidores
- Adicionar/remover servidores
- Habilitar/desabilitar servidores
- Verificar saúde
- Ver recursos e ferramentas

## 📊 Métodos Principais

- `add_server(server)` - Adicionar servidor
- `remove_server(name)` - Remover servidor
- `list_servers()` - Listar todos os servidores
- `list_enabled_servers()` - Listar apenas habilitados
- `enable_server(name)` / `disable_server(name)` - Habilitar/desabilitar
- `check_server_health(name)` - Health check
- `connect_server(name)` / `disconnect_server(name)` - Gerenciar conexão

## 🔗 Links Relacionados

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[Orchestrator|Orchestrator]]
- [[Docker-Integration|Docker Integration]]
- [[MCP_README|MCP README]]

## 🏷️ Tags

#mcp #mcp-manager #servidores #documentação

