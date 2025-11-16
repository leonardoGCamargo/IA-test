# 🚀 MCP Orchestrator - Plataforma Profissional de Orquestração de Agentes

> **Sistema modular profissional de agentes coordenados por Orchestrator**
> Integração completa: MCP + Docker + Obsidian + Neo4j + Kestra + LangChain + GitHub

## 🎯 Visão Geral

Sistema completo de agentes especializados coordenados por um **Orchestrator** central que gerencia tarefas, sincroniza componentes e monitora o sistema inteiro.

## 🏗️ Estrutura do Projeto

```
projeto/
├── src/
│   ├── agents/          # Agentes principais
│   │   ├── orchestrator.py           # Coordenador central
│   │   ├── kestra_langchain_master.py # Master Agent
│   │   ├── agent_helper_system.py    # Helper System
│   │   ├── mcp_manager.py            # MCP Manager
│   │   └── ...
│   └── apps/            # Aplicações existentes
│       ├── bot.py        # Support Bot
│       ├── loader.py     # Stack Overflow Loader
│       └── ...
├── scripts/             # Scripts utilitários
│   ├── master_demo.py
│   ├── sync_obsidian_docs.py
│   └── ...
├── docs/                # Documentação técnica
│   ├── ARCHITECTURE.md
│   ├── ENGINEERING_GUIDE.md
│   └── ...
├── Obsidian_guardar aqui/  # Documentação Obsidian
│   ├── 00-MAPA-DE-AGENTES.md
│   ├── Agentes/
│   └── ...
├── docker/              # Dockerfiles
├── examples/            # Exemplos
├── config/              # Configurações
│   ├── docker-compose.yml
│   ├── env.example
│   └── requirements.txt
└── front-end/           # Frontend (Svelte)
```

## 🚀 Quick Start

### 1. Configuração

```bash
cd config
cp env.example .env
# Edite o .env com suas configurações
```

### 2. Instalar Dependências

```bash
pip install -r config/requirements.txt
```

### 3. Iniciar Sistema

```bash
# Na raiz do projeto
docker compose -f config/docker-compose.yml up
```

### 4. Acessar Interfaces

- **MCP Manager UI:** http://localhost:8506
- **Support Bot:** http://localhost:8501
- **Neo4j Browser:** http://localhost:7474
- **Kestra UI:** http://localhost:8080

## 📚 Documentação

### Para Início Rápido
- **Mapa de Agentes:** `Obsidian_guardar aqui/00-MAPA-DE-AGENTES.md`
- **Guia do Obsidian:** `Obsidian_guardar aqui/01-Guia-Obsidian.md`
- **Guia do Cursor:** `Obsidian_guardar aqui/02-Guia-Cursor.md`

### Para Desenvolvedores
- **Arquitetura:** `docs/ARCHITECTURE.md`
- **Engineering Guide:** `docs/ENGINEERING_GUIDE.md`
- **Como Criar Agentes:** `Obsidian_guardar aqui/04-Como-Criar-Agentes.md`

### Para Engenheiros Sênior
- **Architecture Deep Dive:** `docs/ARCHITECTURE_DEEP_DIVE.md`
- **Execution Plan:** `docs/EXECUTION_PLAN.md`
- **Orchestrator Summary:** `docs/ORCHESTRATOR_SUMMARY.md`

## 🤖 Agentes Principais

### Orchestrator (Coordenador)
**Arquivo:** `src/agents/orchestrator.py`

Coordenador central que gerencia todos os agentes:

```python
from src.agents import get_orchestrator, AgentType

orchestrator = get_orchestrator()
task = orchestrator.create_task(AgentType.MCP_ARCHITECT, "Tarefa", {"action": "..."})
result = orchestrator.execute_task(task)
```

### Master Agent
**Arquivo:** `src/agents/kestra_langchain_master.py`

Agente mestre que combina LangChain + Kestra:

```python
from src.agents import get_master_agent

master = get_master_agent()
result = master.execute_goal("Sincronizar todos os servidores MCP para Neo4j")
```

### Helper System
**Arquivo:** `src/agents/agent_helper_system.py`

Sistema de helpers que monitora e otimiza:

```python
from src.agents import get_helper_system

helper_system = get_helper_system()
report = helper_system.get_full_report()
```

## 📖 Documentação Completa

Ver `docs/README.md` para documentação técnica completa.

## 🎯 Recursos Principais

- ✅ **Orchestrator** - Coordenação centralizada
- ✅ **Master Agent** - Planejamento inteligente com LangChain
- ✅ **Helper System** - Monitoramento e otimização automática
- ✅ **MCP Manager** - Gerenciamento de servidores MCP
- ✅ **Neo4j GraphRAG** - Grafo de conhecimento
- ✅ **Obsidian Integration** - Gestão de notas
- ✅ **Kestra Integration** - Orquestração de workflows
- ✅ **Docker Integration** - Detecção de containers

## 🔧 Configuração

### Variáveis de Ambiente

Copie `config/env.example` para `.env` e configure:

```bash
# Neo4j
NEO4J_URI=neo4j://database:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Obsidian (opcional)
OBSIDIAN_VAULT_PATH=/caminho/para/vault

# LLM
LLM=llama2
EMBEDDING_MODEL=sentence_transformer

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

## 📝 Scripts Úteis

### Sincronizar Documentação Obsidian

```bash
python scripts/sync_obsidian_docs.py
```

### Verificar Integração

```bash
python scripts/verificar_integracao_obsidian.py
```

### Demonstração Completa

```bash
python scripts/master_demo.py
```

## 🔗 Links Úteis

- **Documentação Obsidian:** `Obsidian_guardar aqui/`
- **Documentação Técnica:** `docs/`
- **Código Fonte:** `src/`
- **Scripts:** `scripts/`

## 📄 Licença

Ver `LICENSE` para detalhes.

## 🤝 Contribuindo

Ver `CONTRIBUTING.md` para guia de contribuição.

---

**Desenvolvido com ❤️ usando LangChain, Kestra, Neo4j e Obsidian**
