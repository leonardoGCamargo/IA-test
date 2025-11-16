# 🧠 Kestra & LangChain Master + Agent Helper System

## 🎯 Visão Geral

Este projeto implementa um sistema avançado de agentes que combinam:

1. **Kestra & LangChain Master** - Agente mestre que usa LangChain para planejar e Kestra para executar workflows
2. **Agent Helper System** - Sistema de agentes especializados que ajudam nossos agentes principais
3. **Integração completa com Orchestrator** - Coordenação centralizada de todos os componentes

## 🚀 Componentes

### 1. Kestra & LangChain Master (`kestra_langchain_master.py`)

**O que faz:**
- Recebe objetivos em linguagem natural
- Usa LangChain Agents para planejar workflows
- Cria workflows Kestra dinamicamente
- Executa e monitora workflows
- Otimiza baseado em feedback

**Principais funcionalidades:**
- `execute_goal(goal)` - Executa objetivo em linguagem natural
- `create_intelligent_workflow(description)` - Cria workflow inteligente

**Exemplo:**
```python
from kestra_langchain_master import get_master_agent

master = get_master_agent()

# Executar objetivo complexo
result = master.execute_goal(
    "Sincronizar todos os servidores MCP para o Neo4j e criar workflow de health check"
)

# Criar workflow inteligente
workflow = master.create_intelligent_workflow(
    "Workflow que importa notas Obsidian para Neo4j diariamente às 3h"
)
```

### 2. Agent Helper System (`agent_helper_system.py`)

**Componentes:**

#### AgentMonitorHelper
- Monitora agentes e coleta métricas
- Identifica problemas e avisos
- Gera relatórios de status

#### AgentOptimizerHelper
- Analisa métricas usando LangChain
- Gera recomendações de otimização
- Aplica otimizações automaticamente

#### AgentTunerHelper
- Ajusta prompts de agentes
- Otimiza configurações
- Melhora desempenho baseado em feedback

**Exemplo:**
```python
from agent_helper_system import get_helper_system, get_monitor_helper

# Monitorar todos os agentes
monitor = get_monitor_helper()
metrics = monitor.monitor_all_agents()

# Obter relatório completo
helper_system = get_helper_system()
report = helper_system.get_full_report()
```

### 3. Integração com Orchestrator

Todos os novos agentes estão integrados no Orchestrator:

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Criar tarefa para Master Agent
task = orchestrator.create_task(
    AgentType.KESTRA_LANGCHAIN_MASTER,
    "Criar workflow inteligente",
    {
        "action": "create_intelligent_workflow",
        "description": "Workflow de sincronização semanal"
    }
)
result = orchestrator.execute_task(task)

# Criar tarefa para Helper System
task = orchestrator.create_task(
    AgentType.AGENT_HELPER,
    "Otimizar agente MCP",
    {
        "action": "optimize_agent",
        "agent_name": "mcp_manager"
    }
)
result = orchestrator.execute_task(task)
```

## 📊 Fluxo de Funcionamento

### Fluxo 1: Execução de Objetivo
```
User → Master Agent → LangChain Planner → Executor → Kestra Workflow → Results → Reviewer
```

### Fluxo 2: Monitoramento e Otimização
```
Monitor → Collect Metrics → Optimizer → Analyze → Recommend → Tune → Apply
```

### Fluxo 3: Integração Completa
```
Orchestrator → Master Agent → Helper System → Optimize → Kestra → Results
```

## 🎨 Demonstração

Execute o script de demonstração:

```bash
python master_demo.py
```

Isso demonstra:
1. ✅ Orchestrator coordenando múltiplos agentes
2. ✅ Master Agent criando workflows inteligentes
3. ✅ Helper System monitorando e otimizando
4. ✅ Integração completa entre componentes

## 🔧 Configuração

### Variáveis de Ambiente
```bash
LLM=llama2                    # Modelo LLM
EMBEDDING_MODEL=sentence_transformer  # Modelo de embedding
OLLAMA_BASE_URL=http://localhost:11434  # URL do Ollama
```

### Dependências
- `langchain` - Para agentes LangChain
- `langgraph` - Para grafos de agentes
- `neo4j` - Para grafo de conhecimento
- `streamlit` - Para UI (opcional)

## 📈 Métricas Coletadas

O Helper System coleta:
- **Status do agente** (healthy/warning/error)
- **Score de performance** (0-100)
- **Contagem de erros/sucessos**
- **Tempo médio de resposta**
- **Problemas identificados**
- **Sugestões de melhoria**

## 🎯 Casos de Uso

### 1. Criar Workflow Automatizado
```python
master = get_master_agent()
workflow = master.create_intelligent_workflow(
    "Sincronizar MCPs e gerar relatório semanalmente"
)
```

### 2. Monitorar e Otimizar Agentes
```python
helper_system = get_helper_system()
report = helper_system.get_full_report()

# Agentes com problemas são otimizados automaticamente
for agent_name, opt in report["optimizations"].items():
    print(f"{agent_name}: {opt['recommendations']}")
```

### 3. Executar Pipeline Complexo
```python
master = get_master_agent()
result = master.execute_goal(
    "Sincronizar todos os sistemas, verificar saúde e gerar relatório"
)
```

## 🔄 Workflows Padrão

O Master Agent pode criar workflows para:
- Sincronização MCP → Neo4j → Obsidian
- Health checks periódicos
- Importação de dados
- Geração de relatórios
- Otimização automática

## 📚 Documentação

- **Orchestrator**: Veja `ORCHESTRATOR_SUMMARY.md`
- **Kestra Integration**: Veja `mcp_kestra_integration.py`
- **Architecture**: Veja `ARCHITECTURE.md`

## 🎊 Status

✅ **Kestra & LangChain Master** - Funcionando
✅ **Agent Helper System** - Funcionando  
✅ **Integração com Orchestrator** - Completa
✅ **Monitoramento e Otimização** - Automático

## 🚀 Próximos Passos

1. Adicionar mais ferramentas ao Master Agent
2. Implementar aprendizado contínuo
3. Adicionar dashboards de métricas
4. Expandir casos de uso de workflows

---

**Desenvolvido com ❤️ usando LangChain, Kestra e Orchestrator**

