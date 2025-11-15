# 🧠 Kestra & LangChain Master Agent

> **Tipo:** Agente Mestre  
> **Arquivo:** `kestra_langchain_master.py`  
> **Status:** ✅ Funcional

## 📋 Descrição

O Master Agent combina LangChain Agents com Kestra Workflows para criar um agente inteligente que:
- Planeja workflows usando LangChain
- Cria workflows Kestra dinamicamente
- Executa objetivos em linguagem natural
- Otimiza baseado em feedback iterativo

## 🎯 Funcionalidades

- **Execução de Objetivos**: Executar objetivos complexos em linguagem natural
- **Criação de Workflows**: Criar workflows Kestra inteligentes
- **Planejamento Automático**: Usar LangChain para planejar tarefas
- **Otimização Iterativa**: Refinar planos baseado em feedback

## 💻 Como Usar

### Executar Objetivo em Linguagem Natural

```python
from kestra_langchain_master import get_master_agent

master = get_master_agent()

# Objetivo complexo em linguagem natural
result = master.execute_goal(
    "Sincronizar todos os servidores MCP para o Neo4j e criar workflow de health check"
)

print(f"Plano: {result['plan']}")
print(f"Resultados: {result['results']}")
print(f"Iterações: {result['iterations']}")
```

### Criar Workflow Inteligente

```python
# Criar workflow a partir de descrição
workflow = master.create_intelligent_workflow(
    "Workflow que importa notas Obsidian para Neo4j diariamente às 3h da manhã"
)

print(f"Workflow criado: {workflow.id}")
print(f"Tarefas: {len(workflow.tasks)}")
print(f"Triggers: {len(workflow.triggers)}")
```

### Via Orchestrator

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

task = orchestrator.create_task(
    AgentType.KESTRA_LANGCHAIN_MASTER,
    "Criar workflow de sincronização",
    {
        "action": "create_intelligent_workflow",
        "description": "Sincronizar MCPs semanalmente às segundas-feiras"
    }
)

result = orchestrator.execute_task(task)
```

## 🔧 Funcionalidades Avançadas

### Fluxo de Execução

O Master Agent usa LangGraph para:
1. **Planejamento**: Analisa objetivo e cria plano
2. **Execução**: Executa cada passo do plano
3. **Revisão**: Avalia resultados
4. **Refinamento**: Itera até alcançar objetivo

### Ferramentas Disponíveis

O Master Agent tem acesso a:
- `create_sync_workflow` - Criar workflow de sincronização
- `create_health_check_workflow` - Criar workflow de health check
- `sync_mcp_to_neo4j` - Sincronizar MCPs para Neo4j
- `sync_mcp_to_obsidian` - Sincronizar MCPs para Obsidian
- `get_system_status` - Obter status do sistema
- `create_custom_workflow` - Criar workflow customizado

## 📊 Exemplo Completo

```python
from kestra_langchain_master import get_master_agent

master = get_master_agent()

# 1. Executar objetivo complexo
result = master.execute_goal(
    """
    Criar um sistema completo que:
    1. Sincroniza todos os MCPs para Neo4j
    2. Importa notas Obsidian
    3. Cria workflow que executa isso semanalmente
    4. Configura alertas se algo falhar
    """
)

# 2. Ver resultado
print("Plano criado:")
print(result["plan"])

print("\nPassos executados:")
for step in result["results"]:
    print(f"  - {step['action']}: {step['result']}")

print(f"\nIterações: {result['iterations']}")
print(f"Feedback: {result['feedback']}")
```

## 🔗 Links Relacionados

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[Orchestrator|Orchestrator]]
- [[Kestra-Agent|Kestra Agent]]
- [[Helper-System|Helper System]]
- [[MASTER_AGENT_README|Manual Completo]]

## 🏷️ Tags

#master-agent #langchain #kestra #agente-mestre #documentação

---

**Ver também:** [[SURPRISE_PROJECT|Projeto Surpresa - Master Agent]]

