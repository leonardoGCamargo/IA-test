# 🏥 System Health Agent

> **Tipo:** Agente Consolidado  
> **Arquivo:** `system_health_agent.py`  
> **Status:** ✅ Funcional  
> **Versão:** 2.0 (Consolidado)

## 📋 Descrição

Agente consolidado que combina funcionalidades de:
- ✅ **Diagnostic Agent** - Detecção de problemas
- ✅ **Helper System** - Monitoramento e otimização
- ✅ **Resolution Agent** - Geração de soluções

## 🎯 Funcionalidades

### 1. Diagnóstico
- Verifica variáveis de ambiente
- Verifica chaves de API
- Verifica conexões de banco de dados
- Verifica dependências instaladas
- Verifica configurações
- Detecta problemas de permissão

### 2. Monitoramento
- Monitora todos os agentes
- Coleta métricas de performance
- Identifica problemas e avisos
- Gera relatórios de status

### 3. Resolução
- Gera soluções para problemas
- Cria prompts de resolução
- Fornece comandos para executar
- Links para documentação

### 4. Otimização
- Analisa métricas usando LangChain
- Gera recomendações de otimização
- Aplica otimizações automaticamente

## 💻 Como Usar

### Verificação Completa

```python
from src.agents.system_health_agent import get_system_health_agent

health = get_system_health_agent()

# Verificação completa (diagnóstico + monitoramento + resoluções)
report = health.run_full_health_check()

print(f"Problemas encontrados: {report.summary['total_issues']}")
print(f"Agentes saudáveis: {report.summary['healthy_agents']}")
print(f"Resoluções geradas: {report.summary['total_resolutions']}")
```

### Apenas Diagnóstico

```python
issues = health.diagnose_issues()
for issue in issues:
    print(f"{issue.severity.value}: {issue.title}")
```

### Monitoramento

```python
metrics = health.monitor_agents()
for name, m in metrics.items():
    print(f"{name}: {m.status.value} - {m.performance_score}%")
```

### Resoluções

```python
issues = health.diagnose_issues()
resolutions = health.generate_resolutions(issues)

for resolution in resolutions:
    print(f"Problema: {resolution.title}")
    print(f"Solução: {resolution.description}")
    print(f"Comandos: {resolution.commands}")
```

### Otimização

```python
# Otimizar um agente específico
result = health.optimize_agent("mcp_manager")
print(result["recommendations"])
```

## 📊 Estrutura do Relatório

```python
report = health.run_full_health_check()

# Estrutura:
{
    "diagnostic_issues": [...],      # Lista de problemas
    "agent_metrics": {...},          # Métricas dos agentes
    "resolutions": [...],            # Soluções geradas
    "optimizations": [...],         # Otimizações aplicadas
    "summary": {
        "total_issues": 5,
        "critical_issues": 1,
        "healthy_agents": 8,
        "warning_agents": 2,
        "total_resolutions": 5
    }
}
```

## 🔄 Migração

### Código Antigo (Deprecated):
```python
from src.agents.diagnostic_agent import get_diagnostic_agent
from src.agents.helper_system import get_helper_system
from src.agents.resolution_agent import get_resolution_agent

diagnostic = get_diagnostic_agent()
helper = get_helper_system()
resolution = get_resolution_agent()
```

### Código Novo:
```python
from src.agents.system_health_agent import get_system_health_agent

health = get_system_health_agent()
# Tudo em um único agente!
```

## 📚 Referências

- [[VIDEOS_MCP_AGENTES|Vídeos sobre MCP]]
- [[OTIMIZACAO_AGENTES|Otimização de Agentes]]
- [[PROJETO-IA-TEST|Mapeamento do Projeto]]

---

**Última atualização:** 2025-01-27

