# 🛠️ Como Criar Novos Agentes

> **Guia completo para criar e integrar novos agentes no sistema**

## 🎯 Visão Geral

Este guia mostra como criar novos agentes que se integram perfeitamente com o sistema existente, incluindo integração com o Orchestrator.

## 📋 Checklist de Criação

- [ ] Criar arquivo Python do agente
- [ ] Implementar classe principal
- [ ] Adicionar instância global (singleton)
- [ ] Integrar com Orchestrator
- [ ] Criar documentação
- [ ] Adicionar testes (opcional)
- [ ] Atualizar Mapa de Agentes

## 🏗️ Estrutura Básica de um Agente

### Template Base

```python
"""
Agente: Nome do Agente
Descrição: Breve descrição do que o agente faz
"""

from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuração do agente."""
    name: str
    enabled: bool = True
    # Adicione mais campos conforme necessário


class NomeAgente:
    """
    Agente: [Nome do Agente]
    
    Responsabilidades:
    - Responsabilidade 1
    - Responsabilidade 2
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Inicializa o agente.
        
        Args:
            config: Configuração do agente (opcional)
        """
        self.config = config or AgentConfig(name="nome_agente")
        self.initialized = False
        
        # Inicializações específicas aqui
        self._initialize()
        
        logger.info(f"{self.config.name} inicializado")
    
    def _initialize(self) -> None:
        """Inicializa componentes internos do agente."""
        # Adicione código de inicialização aqui
        self.initialized = True
    
    def execute_action(self, action: str, parameters: Dict[str, Any]) -> Any:
        """
        Executa uma ação do agente.
        
        Args:
            action: Nome da ação a executar
            parameters: Parâmetros da ação
            
        Returns:
            Resultado da execução
        """
        if not self.initialized:
            raise RuntimeError(f"{self.config.name} não está inicializado")
        
        # Implemente ações aqui
        if action == "example_action":
            return self._example_action(parameters)
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _example_action(self, parameters: Dict[str, Any]) -> Any:
        """Implementação de ação de exemplo."""
        # Implemente aqui
        return {"result": "success", "data": parameters}


# Instância global do agente
_agent_instance: Optional[NomeAgente] = None


def get_nome_agente() -> NomeAgente:
    """
    Retorna a instância global do agente.
    
    Returns:
        Instância do agente
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = NomeAgente()
    return _agent_instance
```

## 🔗 Integração com Orchestrator

### Passo 1: Adicionar ao Enum AgentType

Edite `orchestrator.py`:

```python
class AgentType(Enum):
    # ... existentes ...
    NOVO_AGENTE = "novo_agente"  # Adicione esta linha
```

### Passo 2: Importar o Agente

Edite `orchestrator.py`:

```python
from novo_agente import get_nome_agente  # Adicione este import
```

### Passo 3: Inicializar no Orchestrator

Edite `orchestrator.py` no método `__init__`:

```python
# Novo agente
try:
    self.novo_agente = get_nome_agente()
    self.novo_agente_available = True
except Exception as e:
    logger.warning(f"Novo Agente não disponível: {e}")
    self.novo_agente = None
    self.novo_agente_available = False
```

### Passo 4: Implementar Método de Execução

Edite `orchestrator.py`:

```python
def _execute_novo_agente_task(self, task: Task) -> Any:
    """Executa tarefas do Novo Agente."""
    if not self.novo_agente_available:
        raise RuntimeError("Novo Agente não está disponível")
    
    action = task.parameters.get("action")
    
    if action == "example_action":
        parameters = task.parameters.get("parameters", {})
        return self.novo_agente.execute_action("example_action", parameters)
    else:
        raise ValueError(f"Ação não suportada: {action}")
```

### Passo 5: Adicionar ao Router

Edite `orchestrator.py` no método `execute_task`:

```python
elif task.agent_type == AgentType.NOVO_AGENTE:
    result = self._execute_novo_agente_task(task)
```

### Passo 6: Adicionar ao Status

Edite `orchestrator.py` no método `get_system_status`:

```python
"novo_agente": {
    "available": self.novo_agente_available,
    # Adicione métricas específicas aqui
},
```

## 📝 Exemplo Completo: Agente de Monitoramento

```python
"""
Agente: SystemMonitorAgent
Descrição: Monitora métricas do sistema e gera alertas
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import psutil
import logging

logger = logging.getLogger(__name__)


@dataclass
class SystemMetrics:
    """Métricas do sistema."""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    timestamp: datetime


class SystemMonitorAgent:
    """
    Agente que monitora métricas do sistema.
    
    Responsabilidades:
    - Coletar métricas (CPU, memória, disco)
    - Gerar alertas quando necessário
    - Fornecer relatórios
    """
    
    def __init__(self):
        """Inicializa o agente de monitoramento."""
        self.metrics_history: List[SystemMetrics] = []
        self.alert_thresholds = {
            "cpu": 80.0,
            "memory": 80.0,
            "disk": 90.0
        }
        logger.info("SystemMonitorAgent inicializado")
    
    def collect_metrics(self) -> SystemMetrics:
        """
        Coleta métricas atuais do sistema.
        
        Returns:
            Métricas coletadas
        """
        metrics = SystemMetrics(
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage('/').percent,
            timestamp=datetime.now()
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def check_alerts(self, metrics: SystemMetrics) -> List[str]:
        """
        Verifica se há alertas baseado nas métricas.
        
        Args:
            metrics: Métricas a verificar
            
        Returns:
            Lista de alertas
        """
        alerts = []
        
        if metrics.cpu_percent > self.alert_thresholds["cpu"]:
            alerts.append(f"CPU alto: {metrics.cpu_percent:.1f}%")
        
        if metrics.memory_percent > self.alert_thresholds["memory"]:
            alerts.append(f"Memória alta: {metrics.memory_percent:.1f}%")
        
        if metrics.disk_percent > self.alert_thresholds["disk"]:
            alerts.append(f"Disco alto: {metrics.disk_percent:.1f}%")
        
        return alerts
    
    def get_report(self) -> Dict[str, Any]:
        """
        Gera relatório de métricas.
        
        Returns:
            Relatório completo
        """
        if not self.metrics_history:
            return {"error": "Nenhuma métrica coletada"}
        
        latest = self.metrics_history[-1]
        alerts = self.check_alerts(latest)
        
        return {
            "current_metrics": {
                "cpu": latest.cpu_percent,
                "memory": latest.memory_percent,
                "disk": latest.disk_percent,
                "timestamp": latest.timestamp.isoformat()
            },
            "alerts": alerts,
            "history_count": len(self.metrics_history)
        }


# Instância global
_monitor_agent_instance: Optional[SystemMonitorAgent] = None


def get_monitor_agent() -> SystemMonitorAgent:
    """Retorna instância global do agente de monitoramento."""
    global _monitor_agent_instance
    if _monitor_agent_instance is None:
        _monitor_agent_instance = SystemMonitorAgent()
    return _monitor_agent_instance
```

## 📚 Criando Documentação

### Template de Documentação

Crie `Agentes/Nome-Agente.md`:

```markdown
# Nome do Agente

> **Tipo:** Tipo do agente  
> **Arquivo:** `nome_agente.py`  
> **Status:** ✅ Funcional

## 📋 Descrição

Descrição detalhada do agente...

## 🎯 Funcionalidades

- Funcionalidade 1
- Funcionalidade 2

## 💻 Como Usar

### Uso Direto

\`\`\`python
from nome_agente import get_nome_agente

agente = get_nome_agente()
resultado = agente.execute_action("example_action", {"param": "value"})
\`\`\`

### Via Orchestrator

\`\`\`python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()
task = orchestrator.create_task(
    AgentType.NOVO_AGENTE,
    "Descrição da tarefa",
    {"action": "example_action", "parameters": {"param": "value"}}
)
result = orchestrator.execute_task(task)
\`\`\`

## 🔗 Links Relacionados

- [[Orchestrator]] - Coordenação central
- [[Outro-Agente]] - Agente relacionado

## 🏷️ Tags

#agente #novo #documentação
```

## 🧪 Testando o Agente

### Teste Básico

```python
# test_novo_agente.py
import unittest
from novo_agente import get_nome_agente

class TestNovoAgente(unittest.TestCase):
    def setUp(self):
        self.agente = get_nome_agente()
    
    def test_initialization(self):
        self.assertIsNotNone(self.agente)
        self.assertTrue(self.agente.initialized)
    
    def test_example_action(self):
        result = self.agente.execute_action(
            "example_action",
            {"param": "value"}
        )
        self.assertIn("result", result)

if __name__ == "__main__":
    unittest.main()
```

### Executar Testes

```bash
python -m pytest test_novo_agente.py -v
```

## 📊 Adicionar ao Mapa de Agentes

Edite `00-MAPA-DE-AGENTES.md`:

```markdown
### Novo Agente
**Arquivo:** `nome_agente.py`  
**Descrição:** Descrição do agente  
**Documentação:** [[Agentes/Nome-Agente|Ver Documentação Completa]]

**Funcionalidades:**
- Funcionalidade 1
- Funcionalidade 2

**Como usar:**
\`\`\`python
from nome_agente import get_nome_agente
agente = get_nome_agente()
resultado = agente.execute_action("example_action", {})
\`\`\`
```

## ✅ Checklist Final

- [ ] Código do agente implementado
- [ ] Integração com Orchestrator completa
- [ ] Documentação criada
- [ ] Testes escritos (opcional)
- [ ] Adicionado ao Mapa de Agentes
- [ ] Testado em ambiente local
- [ ] Verificado que funciona via Orchestrator

## 🔗 Links Úteis

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[03-Manual-Sistema-Agentes|Manual do Sistema]]
- [[Agentes/Orchestrator|Documentação do Orchestrator]]
- [[ARCHITECTURE|Arquitetura do Sistema]]

## 🏷️ Tags

#tutorial #agentes #desenvolvimento #criação #integração

---

**Dica:** Use agentes existentes como referência! Veja como eles estão estruturados.

