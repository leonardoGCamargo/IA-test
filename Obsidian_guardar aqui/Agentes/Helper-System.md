# 🛠️ Agent Helper System

> **Tipo:** Sistema de Helpers  
> **Arquivo:** `agent_helper_system.py`  
> **Status:** ✅ Funcional

## 📋 Descrição

Sistema completo de agentes helpers que monitoram, otimizam e ajustam outros agentes do sistema automaticamente usando LangChain.

## 🎯 Componentes

### AgentMonitorHelper
- Monitora agentes e coleta métricas
- Identifica problemas e avisos
- Gera relatórios de status

### AgentOptimizerHelper
- Analisa métricas usando LangChain
- Gera recomendações de otimização
- Aplica otimizações automaticamente

### AgentTunerHelper
- Ajusta prompts de agentes
- Otimiza configurações
- Melhora desempenho baseado em feedback

## 💻 Como Usar

### Monitorar Agentes

```python
from agent_helper_system import get_monitor_helper

monitor = get_monitor_helper()

# Monitorar um agente específico
metrics = monitor.monitor_agent("mcp_manager")
print(f"Status: {metrics.status.value}")
print(f"Performance: {metrics.performance_score}%")
print(f"Issues: {metrics.issues}")

# Monitorar todos os agentes
all_metrics = monitor.monitor_all_agents()
for name, m in all_metrics.items():
    print(f"{name}: {m.status.value}")

# Relatório completo
report = monitor.get_metrics_report()
print(report)
```

### Otimizar Agentes

```python
from agent_helper_system import get_optimizer_helper

optimizer = get_optimizer_helper()

# Otimizar um agente
result = optimizer.optimize_agent("mcp_manager")
print("Análise:", result["analysis"])
print("Recomendações:", result["recommendations"])
print("Otimizações:", result["optimizations"])
```

### Sistema Completo

```python
from agent_helper_system import get_helper_system

helper_system = get_helper_system()

# Relatório completo
report = helper_system.get_full_report()

print("Métricas:")
print(f"  Total: {report['metrics']['total_agents']}")
print(f"  Saudáveis: {report['metrics']['healthy_count']}")
print(f"  Com Avisos: {report['metrics']['warning_count']}")
print(f"  Com Erros: {report['metrics']['error_count']}")
print(f"  Performance Média: {report['metrics']['avg_performance']:.1f}%")

print("\nOtimizações:")
for agent_name, opt in report["optimizations"].items():
    print(f"  {agent_name}: {len(opt.get('recommendations', []))} recomendações")
```

### Via Orchestrator

```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Monitorar agente
task = orchestrator.create_task(
    AgentType.AGENT_HELPER,
    "Monitorar MCP Manager",
    {"action": "monitor_agent", "agent_name": "mcp_manager"}
)
result = orchestrator.execute_task(task)

# Otimizar agente
task = orchestrator.create_task(
    AgentType.AGENT_HELPER,
    "Otimizar MCP Manager",
    {"action": "optimize_agent", "agent_name": "mcp_manager"}
)
result = orchestrator.execute_task(task)

# Relatório completo
task = orchestrator.create_task(
    AgentType.AGENT_HELPER,
    "Relatório completo",
    {"action": "get_full_report"}
)
report = orchestrator.execute_task(task)
```

## 📊 Métricas Coletadas

- **Status**: healthy / warning / error / optimizing
- **Performance Score**: 0-100
- **Error Count**: Número de erros
- **Success Count**: Número de sucessos
- **Avg Response Time**: Tempo médio de resposta
- **Issues**: Lista de problemas identificados
- **Suggestions**: Sugestões de melhoria

## 🔗 Links Relacionados

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[Orchestrator|Orchestrator]]
- [[Master-Agent|Master Agent]]

## 🏷️ Tags

#helper-system #monitoramento #otimização #langchain #documentação

