# ⚙️ Kestra Agent

> **Tipo:** Agente Kestra  
> **Arquivo:** `mcp_kestra_integration.py`  
> **Interface:** http://localhost:8080  
> **Status:** ✅ Funcional

## 📋 Descrição

Agente para orquestração de pipelines automatizados com Kestra. Permite criar, gerenciar e executar workflows Kestra para automação de tarefas.

## 🎯 Funcionalidades

- Criar e gerenciar workflows Kestra
- Agendar tarefas automatizadas
- Orquestrar fluxos MCP → Neo4j → Obsidian
- Gerar workflows padrão do sistema

## 💻 Como Usar

```python
from mcp_kestra_integration import get_kestra_agent

kestra = get_kestra_agent()

# Criar workflow de sincronização
workflow = kestra.create_sync_mcp_workflow()
print(f"Workflow criado: {workflow.id}")

# Criar workflow de health check
workflow = kestra.create_health_check_workflow()
print(f"Workflow criado: {workflow.id}")

# Criar workflow customizado
from pathlib import Path
workflow = kestra.create_import_obsidian_workflow("/caminho/vault")

# Listar workflows
workflows = kestra.list_workflows()
for w in workflows:
    print(f"{w.id}: {w.description}")

# Gerar workflows padrão
default_workflows = kestra.generate_default_workflows()
print(f"Criados {len(default_workflows)} workflows padrão")
```

### Via Orchestrator

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Criar workflow
task = orchestrator.create_task(
    AgentType.KESTRA,
    "Criar workflow de sincronização",
    {"action": "create_sync_workflow"}
)
result = orchestrator.execute_task(task)

# Gerar workflows padrão
task = orchestrator.create_task(
    AgentType.KESTRA,
    "Gerar workflows padrão",
    {"action": "generate_default_workflows"}
)
result = orchestrator.execute_task(task)
```

## 📊 Workflows Padrão

### 1. Sync MCP Full Pipeline
- Sincroniza MCPs entre componentes
- Executa a cada 6 horas

### 2. Import Obsidian Vault
- Importa notas Obsidian para Neo4j
- Executa diariamente às 2h

### 3. MCP Health Check
- Verifica saúde dos servidores MCP
- Executa a cada 30 minutos

## 🔗 Links Relacionados

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[Orchestrator|Orchestrator]]
- [[Master-Agent|Master Agent]]

## 🏷️ Tags

#kestra #workflows #automação #orquestração #documentação

---

**Interface Web:** http://localhost:8080

