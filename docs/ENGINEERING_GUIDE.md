# 🛠️ Engineering Guide - Sistema de Agentes MCP

> **Guia técnico para engenheiros** - Entenda, melhore e crie novos componentes

## 📋 Índice

1. [Arquitetura do Sistema](#arquitetura-do-sistema)
2. [Estrutura de Código](#estrutura-de-código)
3. [Agentes Principais](#agentes-principais)
4. [Como Melhorar](#como-melhorar)
5. [Como Criar Novos Componentes](#como-criar-novos-componentes)
6. [Padrões e Boas Práticas](#padrões-e-boas-práticas)
7. [Testes e Validação](#testes-e-validação)

## 🏗️ Arquitetura do Sistema

### Visão Geral

```
┌─────────────────────────────────────────┐
│         ORCHESTRATOR                    │
│      (Coordenador Central)               │
│    src/agents/orchestrator.py            │
└──────────────┬───────────────────────────┘
               │
    ┌──────────┼──────────┬──────────┬──────────┐
    │          │          │          │          │
    ▼          ▼          ▼          ▼          ▼
┌─────────┐ ┌───────┐ ┌──────────┐ ┌──────┐ ┌──────────┐
│ Master  │ │Helper │ │   MCP    │ │Neo4j │ │ Obsidian │
│ Agent   │ │System │ │ Manager  │ │GraphRAG│ │Integration│
└─────────┘ └───────┘ └──────────┘ └──────┘ └──────────┘
```

### Componentes Principais

#### 1. Orchestrator (`src/agents/orchestrator.py`)
**Responsabilidade:** Coordenação central de todos os agentes

**Padrão:** Singleton + Task Queue

**Principais Classes:**
- `Orchestrator`: Coordenador principal
- `Task`: Representa uma tarefa delegada
- `AgentType`: Enum dos tipos de agentes

**Como Funciona:**
```python
from src.agents.orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Criar tarefa
task = orchestrator.create_task(
    AgentType.MCP_ARCHITECT,
    "Descrição da tarefa",
    {"action": "list_servers"}
)

# Executar
result = orchestrator.execute_task(task)
```

**Melhorias Possíveis:**
- Adicionar retry logic
- Implementar task prioritization
- Adicionar task scheduling
- Implementar task history/persistence

#### 2. Master Agent (`src/agents/kestra_langchain_master.py`)
**Responsabilidade:** Planejamento inteligente usando LangChain + Kestra

**Padrão:** LangGraph State Machine

**Principais Classes:**
- `KestraLangChainMaster`: Agente mestre
- `MasterState`: Estado do agente (TypedDict)
- `LangGraph Workflow`: Fluxo de planejamento → execução → revisão

**Como Funciona:**
```python
from src.agents.kestra_langchain_master import get_master_agent

master = get_master_agent()

# Executar objetivo em linguagem natural
result = master.execute_goal(
    "Sincronizar todos os servidores MCP para Neo4j"
)
```

**Melhorias Possíveis:**
- Melhorar prompts para LangChain
- Adicionar mais ferramentas ao agente
- Implementar learning from feedback
- Adicionar cache de planos similares

#### 3. Helper System (`src/agents/agent_helper_system.py`)
**Responsabilidade:** Monitorar e otimizar outros agentes

**Padrão:** Observer + Strategy

**Componentes:**
- `AgentMonitorHelper`: Coleta métricas
- `AgentOptimizerHelper`: Otimiza usando LangChain
- `AgentTunerHelper`: Ajusta configurações

**Como Funciona:**
```python
from src.agents.agent_helper_system import get_helper_system

helper_system = get_helper_system()

# Relatório completo
report = helper_system.get_full_report()
```

**Melhorias Possíveis:**
- Adicionar mais métricas (tempo de resposta, uso de memória)
- Implementar alertas automáticos
- Adicionar dashboard de métricas
- Implementar auto-tuning baseado em histórico

## 📁 Estrutura de Código

### Organização Atual

```
projeto/
├── src/
│   ├── agents/          # Agentes principais
│   │   ├── orchestrator.py
│   │   ├── kestra_langchain_master.py
│   │   ├── agent_helper_system.py
│   │   ├── mcp_manager.py
│   │   ├── mcp_neo4j_integration.py
│   │   ├── mcp_obsidian_integration.py
│   │   ├── mcp_kestra_integration.py
│   │   └── mcp_docker_integration.py
│   └── apps/            # Aplicações existentes
│       ├── bot.py
│       ├── loader.py
│       ├── pdf_bot.py
│       ├── api.py
│       ├── chains.py
│       └── utils.py
├── scripts/             # Scripts utilitários
├── docs/                # Documentação técnica
├── Obsidian_guardar aqui/  # Documentação Obsidian
├── docker/              # Dockerfiles
├── examples/            # Exemplos de uso
└── config/              # Configurações
    ├── docker-compose.yml
    ├── env.example
    └── requirements.txt
```

### Padrões de Código

#### Singleton Pattern
Todos os agentes usam singleton para garantir uma única instância:

```python
_agent_instance: Optional[Agent] = None

def get_agent() -> Agent:
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = Agent()
    return _agent_instance
```

#### Factory Pattern
O Orchestrator usa factory pattern para criar tarefas:

```python
task = orchestrator.create_task(
    AgentType.MCP_ARCHITECT,
    "Descrição",
    {"action": "..."}
)
```

#### Strategy Pattern
O Helper System usa strategy para diferentes tipos de otimização:

```python
optimizer.optimize_agent("mcp_manager")  # Usa estratégia padrão
```

## 🔧 Como Melhorar o Sistema

### 1. Melhorar Orchestrator

**Ideias:**
- Adicionar retry logic para tarefas falhas
- Implementar task prioritization
- Adicionar task scheduling (agendar tarefas futuras)
- Implementar task history/persistence (salvar histórico)

**Exemplo de Melhoria:**
```python
# Adicionar retry logic
def execute_task_with_retry(self, task: Task, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return self.execute_task(task)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            logger.warning(f"Tentativa {attempt + 1} falhou: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 2. Melhorar Master Agent

**Ideias:**
- Melhorar prompts para LangChain
- Adicionar mais ferramentas ao agente
- Implementar learning from feedback
- Adicionar cache de planos similares

**Exemplo de Melhoria:**
```python
# Adicionar cache de planos
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_plan(goal: str) -> Dict:
    # Cache planos similares para evitar reprocessamento
    return master_agent.plan(goal)
```

### 3. Melhorar Helper System

**Ideias:**
- Adicionar mais métricas (tempo de resposta, uso de memória)
- Implementar alertas automáticos
- Adicionar dashboard de métricas
- Implementar auto-tuning baseado em histórico

**Exemplo de Melhoria:**
```python
# Adicionar métricas de performance
class PerformanceMetrics:
    response_time: float
    memory_usage: float
    cpu_usage: float
    error_rate: float

def collect_performance_metrics(self, agent_name: str) -> PerformanceMetrics:
    # Coleta métricas detalhadas de performance
    pass
```

## 🚀 Como Criar Novos Componentes

### Template para Novo Agente

Veja `Obsidian_guardar aqui/04-Como-Criar-Agentes.md` para guia completo.

**Estrutura Básica:**
```python
"""
Agente: Nome do Agente
Descrição: Breve descrição
"""

from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class NovoAgente:
    """Descrição do agente."""
    
    def __init__(self):
        """Inicializa o agente."""
        logger.info("NovoAgente inicializado")
    
    def execute_action(self, action: str, parameters: Dict[str, Any]) -> Any:
        """Executa uma ação."""
        if action == "example":
            return self._example_action(parameters)
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _example_action(self, parameters: Dict[str, Any]) -> Any:
        """Implementação da ação."""
        return {"result": "success"}


# Singleton
_agent_instance: Optional[NovoAgente] = None

def get_novo_agente() -> NovoAgente:
    """Retorna instância global."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = NovoAgente()
    return _agent_instance
```

### Integração com Orchestrator

1. Adicionar ao `AgentType` enum:
```python
class AgentType(Enum):
    # ... existentes ...
    NOVO_AGENTE = "novo_agente"
```

2. Importar no Orchestrator:
```python
from src.agents.novo_agente import get_novo_agente
```

3. Inicializar no `__init__`:
```python
try:
    self.novo_agente = get_novo_agente()
    self.novo_agente_available = True
except Exception as e:
    logger.warning(f"Novo Agente não disponível: {e}")
    self.novo_agente = None
    self.novo_agente_available = False
```

4. Implementar método de execução:
```python
def _execute_novo_agente_task(self, task: Task) -> Any:
    """Executa tarefas do Novo Agente."""
    if not self.novo_agente_available:
        raise RuntimeError("Novo Agente não está disponível")
    
    action = task.parameters.get("action")
    parameters = task.parameters.get("parameters", {})
    return self.novo_agente.execute_action(action, parameters)
```

## 📊 Padrões e Boas Práticas

### 1. Logging
Sempre use logging adequado:

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Operação iniciada")
logger.warning("Aviso: ...")
logger.error("Erro: ...", exc_info=True)
```

### 2. Error Handling
Use try/except adequadamente:

```python
try:
    result = operation()
except SpecificError as e:
    logger.error(f"Erro específico: {e}")
    raise
except Exception as e:
    logger.error(f"Erro inesperado: {e}", exc_info=True)
    raise
```

### 3. Type Hints
Use type hints sempre que possível:

```python
from typing import Dict, List, Optional, Any

def process_data(data: Dict[str, Any]) -> List[str]:
    """Processa dados."""
    return [item for item in data.values()]
```

### 4. Docstrings
Documente suas funções e classes:

```python
def exemplo(parametro: str) -> str:
    """
    Breve descrição.
    
    Args:
        parametro: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
        
    Raises:
        ValueError: Quando algo dá errado
    """
    pass
```

## 🧪 Testes e Validação

### Estrutura de Testes Recomendada

```
tests/
├── unit/
│   ├── test_orchestrator.py
│   ├── test_master_agent.py
│   └── test_helper_system.py
├── integration/
│   ├── test_mcp_integration.py
│   └── test_neo4j_integration.py
└── e2e/
    └── test_full_pipeline.py
```

### Exemplo de Teste

```python
import unittest
from src.agents.orchestrator import get_orchestrator, AgentType

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = get_orchestrator()
    
    def test_create_task(self):
        task = self.orchestrator.create_task(
            AgentType.MCP_ARCHITECT,
            "Teste",
            {"action": "list_servers"}
        )
        self.assertIsNotNone(task)
        self.assertEqual(task.agent_type, AgentType.MCP_ARCHITECT)
    
    def test_execute_task(self):
        task = self.orchestrator.create_task(
            AgentType.MCP_ARCHITECT,
            "Teste",
            {"action": "list_servers"}
        )
        result = self.orchestrator.execute_task(task)
        self.assertIsNotNone(result)
```

## 🔗 Referências

- [[../Obsidian_guardar aqui/00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[ARCHITECTURE|Arquitetura do Sistema]]
- [[EXECUTION_PLAN|Plano de Execução]]
- [[../Obsidian_guardar aqui/04-Como-Criar-Agentes|Como Criar Agentes]]

## 💡 Ideias para Melhorias Futuras

### Performance
- [ ] Implementar cache de resultados
- [ ] Adicionar paralelização de tarefas
- [ ] Otimizar queries Neo4j
- [ ] Implementar connection pooling

### Funcionalidades
- [ ] Adicionar suporte a múltiplos vaults Obsidian
- [ ] Implementar sincronização bidirecional
- [ ] Adicionar webhooks para eventos
- [ ] Implementar API REST para agentes

### Monitoramento
- [ ] Adicionar Prometheus metrics
- [ ] Implementar health checks
- [ ] Adicionar tracing distribuído
- [ ] Criar dashboard de monitoramento

### Segurança
- [ ] Implementar autenticação/autorização
- [ ] Adicionar criptografia de dados
- [ ] Implementar rate limiting
- [ ] Adicionar audit logs

## 🏷️ Tags

#engineering #arquitetura #desenvolvimento #técnico #documentação

---

**Última atualização:** {{date}}  
**Versão:** 1.0.0

