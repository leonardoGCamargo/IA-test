# 🗺️ MAPA DE AGENTES - Sistema Completo

> **Arquivo Principal do Sistema de Agentes**  
> Este é o ponto de entrada para toda a documentação do sistema.

## 📋 Índice

1. [[01-Guia-Obsidian|Guia de Uso do Obsidian]]
2. [[02-Guia-Cursor|Guia de Uso do Cursor]]
3. [[03-Manual-Sistema-Agentes|Manual do Sistema de Agentes]]
4. [[04-Como-Criar-Agentes|Como Criar Novos Agentes]]

## 🎯 Visão Geral do Sistema

Este sistema integra múltiplos agentes especializados coordenados pelo **Orchestrator**:

```
┌─────────────────────────────────────┐
│         ORCHESTRATOR                 │
│      (Coordenador Central)            │
│    orchestrator.py                    │
└──────────────┬────────────────────────┘
               │
    ┌──────────┼──────────┬──────────┬──────────┐
    │          │          │          │          │
    ▼          ▼          ▼          ▼          ▼
┌─────────┐ ┌───────┐ ┌──────────┐ ┌──────┐ ┌──────────┐
│ Master  │ │Helper │ │   MCP    │ │Neo4j │ │ Obsidian │
│ Agent   │ │System │ │ Manager  │ │GraphRAG│ │Integration│
└─────────┘ └───────┘ └──────────┘ └──────┘ └──────────┘
```

## 🤖 Agentes Principais

### 🎯 Orchestrator (Coordenador)
**Arquivo:** `orchestrator.py`  
**Descrição:** Coordenador central que gerencia todos os agentes  
**Documentação:** [[Agentes/Orchestrator|Ver Documentação Completa]]

**Responsabilidades:**
- Coordenar tarefas entre agentes
- Gerenciar sistema de tarefas
- Sincronizar componentes
- Monitorar status do sistema

**Como usar:**
```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()
task = orchestrator.create_task(AgentType.MCP_ARCHITECT, "Tarefa", {"action": "..."})
result = orchestrator.execute_task(task)
```

### 🧠 Kestra & LangChain Master
**Arquivo:** `kestra_langchain_master.py`  
**Descrição:** Agente mestre que combina LangChain Agents com Kestra Workflows  
**Documentação:** [[Agentes/Master-Agent|Ver Documentação Completa]]

**Funcionalidades:**
- Executar objetivos em linguagem natural
- Criar workflows Kestra dinamicamente
- Planejar tarefas usando LangChain
- Otimizar baseado em feedback

**Como usar:**
```python
from kestra_langchain_master import get_master_agent

master = get_master_agent()
result = master.execute_goal("Sincronizar todos os servidores MCP para Neo4j")
```

### 🛠️ Agent Helper System
**Arquivo:** `agent_helper_system.py`  
**Descrição:** Sistema de agentes helpers que monitoram e otimizam outros agentes  
**Documentação:** [[Agentes/Helper-System|Ver Documentação Completa]]

**Componentes:**
- **AgentMonitorHelper**: Monitora agentes e coleta métricas
- **AgentOptimizerHelper**: Otimiza agentes usando LangChain
- **AgentTunerHelper**: Ajusta prompts e configurações

**Como usar:**
```python
from agent_helper_system import get_helper_system

helper_system = get_helper_system()
report = helper_system.get_full_report()
```

### 🔌 MCP Manager
**Arquivo:** `mcp_manager.py`  
**Descrição:** Gerenciador de servidores MCP (Model Context Protocol)  
**Documentação:** [[Agentes/MCP-Manager|Ver Documentação Completa]]

**Funcionalidades:**
- Gerenciar servidores MCP
- Health checks e monitoramento
- CRUD de servidores
- Listar recursos e ferramentas

**Interface:** `mcp_manager_ui.py` - Streamlit UI na porta 8506

### 🐳 Docker Integration
**Arquivo:** `mcp_docker_integration.py`  
**Descrição:** Integração com Docker para detectar e gerenciar containers  
**Documentação:** [[Agentes/Docker-Integration|Ver Documentação Completa]]

**Funcionalidades:**
- Detectar containers MCP em execução
- Monitorar serviços Docker Compose
- Extrair informações de containers

### 📊 Neo4j GraphRAG
**Arquivo:** `mcp_neo4j_integration.py`  
**Descrição:** Gestão de grafo de conhecimento e GraphRAG com LangGraph  
**Documentação:** [[Agentes/Neo4j-GraphRAG|Ver Documentação Completa]]

**Funcionalidades:**
- Armazenar nós MCP, RAG e Obsidian
- Consultas GraphRAG usando LangGraph
- Visualização de grafo
- Busca semântica com embeddings

### 📝 Obsidian Integration
**Arquivo:** `mcp_obsidian_integration.py`  
**Descrição:** Gestão de notas no Obsidian  
**Documentação:** [[Agentes/Obsidian-Integration|Ver Documentação Completa]]

**Funcionalidades:**
- Criar notas sobre MCPs e RAGs
- Gerenciar links entre notas
- Buscar em notas

### ⚙️ Kestra Agent
**Arquivo:** `mcp_kestra_integration.py`  
**Descrição:** Orquestração de pipelines automatizados com Kestra  
**Documentação:** [[Agentes/Kestra-Agent|Ver Documentação Completa]]

**Funcionalidades:**
- Criar e gerenciar workflows Kestra
- Agendar tarefas automatizadas
- Orquestrar fluxos MCP → Neo4j → Obsidian

## 📚 Documentação Adicional

### Arquitetura
- [[ARCHITECTURE|Arquitetura do Sistema]]
- [[EXECUTION_PLAN|Plano de Execução]]
- [[ORCHESTRATOR_SUMMARY|Resumo do Orchestrator]]
- [[SURPRISE_PROJECT|Projeto Surpresa - Master Agent]]
- [[MASTER_AGENT_README|Manual do Master Agent]]

### Documentação Específica
- [[MCP_README|MCP Manager README]]
- [[DOCKER_INTEGRATION_README|Docker Integration README]]

## 🔗 Links Rápidos

### Ferramentas e Configuração
- `.env` - Configurações de ambiente
- `docker-compose.yml` - Configuração Docker
- `requirements.txt` - Dependências Python

### Scripts Principais
- `master_demo.py` - Demonstração completa do sistema
- `chains.py` - Cadeias LangChain
- `utils.py` - Utilitários

### UIs
- `mcp_manager_ui.py` - Interface Streamlit (porta 8506)
- `bot.py` - Support Bot (porta 8501)
- `loader.py` - Stack Overflow Loader (porta 8502)
- `pdf_bot.py` - PDF Reader (porta 8503)
- `api.py` - Standalone API (porta 8504)
- `front-end/` - Frontend Svelte (porta 8505)

## 🚀 Quick Start

### 1. Configuração Inicial
```bash
# Copiar arquivo de configuração
cp env.example .env

# Editar variáveis de ambiente
# NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, etc.
```

### 2. Iniciar Sistema
```bash
# Iniciar todos os serviços
docker compose up

# Ou em modo watch (auto-rebuild)
docker compose watch
```

### 3. Acessar Interfaces
- MCP Manager UI: http://localhost:8506
- Support Bot: http://localhost:8501
- Neo4j Browser: http://localhost:7474
- Kestra UI: http://localhost:8080

### 4. Testar Sistema
```bash
# Executar demonstração
python master_demo.py

# Ou usar Python interativo
python
>>> from orchestrator import get_orchestrator
>>> orchestrator = get_orchestrator()
>>> status = orchestrator.get_system_status()
```

## 📖 Próximos Passos

1. Leia o [[01-Guia-Obsidian|Guia de Uso do Obsidian]]
2. Consulte o [[02-Guia-Cursor|Guia de Uso do Cursor]]
3. Explore o [[03-Manual-Sistema-Agentes|Manual do Sistema]]
4. Aprenda a [[04-Como-Criar-Agentes|Criar Novos Agentes]]

## 🏷️ Tags

#mapa #agentes #orchestrator #documentação #sistema #mcp #neo4j #obsidian #kestra #langchain

---

**Última atualização:** {{date}}  
**Versão do Sistema:** 1.0.0

