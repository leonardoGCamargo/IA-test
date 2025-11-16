# 🐳 Docker Integration

> **Tipo:** Integração Docker  
> **Arquivo:** `mcp_docker_integration.py`  
> **Status:** ✅ Funcional

## 📋 Descrição

Integração com Docker para detectar e gerenciar servidores MCP em execução em containers Docker.

## 🎯 Funcionalidades

- Detectar containers Docker em execução
- Identificar servidores MCP
- Extrair informações de containers
- Monitorar serviços Docker Compose

## 💻 Como Usar

```python
from mcp_docker_integration import DockerMCPDetector

detector = DockerMCPDetector()

# Listar containers em execução
containers = detector.list_running_containers()
for container in containers:
    print(f"{container.name}: {container.status}")

# Detectar servidores MCP
mcp_services = detector.detect_mcp_services()
print(f"Servidores MCP encontrados: {len(mcp_services)}")

# Informações detalhadas
info = detector.get_service_info("mcp-manager")
print(info)

# Serviços do docker-compose
services = detector.list_compose_services()
print(f"Serviços do compose: {services}")
```

### Via Orchestrator

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

task = orchestrator.create_task(
    AgentType.DOCKER_INTEGRATION,
    "Listar containers",
    {"action": "list_containers"}
)
result = orchestrator.execute_task(task)
```

## 🔗 Links Relacionados

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[Orchestrator|Orchestrator]]
- [[MCP-Manager|MCP Manager]]

## 🏷️ Tags

#docker #integração #containers #documentação

