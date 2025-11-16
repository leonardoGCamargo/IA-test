# 📘 Manual do Sistema de Agentes

> **Manual completo de uso do sistema de agentes**

## 🎯 Visão Geral

O sistema de agentes é uma arquitetura modular que permite:
- Coordenação centralizada via Orchestrator
- Execução de tarefas complexas
- Integração entre múltiplos componentes
- Automação via Kestra
- Monitoramento e otimização automática

## 🏗️ Arquitetura

```
┌────────────────────────────────────────┐
│         ORCHESTRATOR                    │
│      (Coordenador Central)               │
│    - Gerencia tarefas                    │
│    - Coordena agentes                    │
│    - Monitora sistema                    │
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

## 🚀 Início Rápido

### 1. Configuração

```bash
# Copiar arquivo de configuração
cp env.example .env

# Editar variáveis (importante):
# NEO4J_URI=neo4j://database:7687
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=password
# OBSIDIAN_VAULT_PATH=/caminho/para/vault
```

### 2. Iniciar Sistema

```bash
# Iniciar todos os serviços
docker compose up

# Ou em modo watch
docker compose watch
```

### 3. Importar e Usar

```python
from orchestrator import get_orchestrator, AgentType

# Obter Orchestrator
orchestrator = get_orchestrator()

# Criar tarefa
task = orchestrator.create_task(
    AgentType.MCP_ARCHITECT,
    "Listar servidores MCP",
    {"action": "list_servers"}
)

# Executar tarefa
result = orchestrator.execute_task(task)
print(result)
```

## 🤖 Agentes Detalhados

### Orchestrator

**Documentação:** [[Agentes/Orchestrator|Ver Documentação Completa]]

**Funcionalidades principais:**
- `create_task()` - Criar nova tarefa
- `execute_task()` - Executar tarefa
- `sync_mcp_to_neo4j()` - Sincronizar MCP → Neo4j
- `sync_mcp_to_obsidian()` - Sincronizar MCP → Obsidian
- `get_system_status()` - Status do sistema

**Exemplo:**
```python
from orchestrator import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Sincronizar tudo
orchestrator.sync_mcp_to_neo4j()
orchestrator.sync_mcp_to_obsidian()

# Obter status
status = orchestrator.get_system_status()
```

### Master Agent

**Documentação:** [[Agentes/Master-Agent|Ver Documentação Completa]]

**Funcionalidades principais:**
- `execute_goal(goal)` - Executar objetivo em linguagem natural
- `create_intelligent_workflow(description)` - Criar workflow inteligente

**Exemplo:**
```python
from kestra_langchain_master import get_master_agent

master = get_master_agent()

# Executar objetivo complexo
result = master.execute_goal(
    "Sincronizar todos os servidores MCP para Neo4j e criar workflow de health check"
)

# Criar workflow inteligente
workflow = master.create_intelligent_workflow(
    "Workflow que importa notas Obsidian diariamente às 3h"
)
```

### Helper System

**Documentação:** [[Agentes/Helper-System|Ver Documentação Completa]]

**Funcionalidades principais:**
- Monitorar todos os agentes
- Otimizar agentes automaticamente
- Gerar relatórios completos

**Exemplo:**
```python
from agent_helper_system import get_helper_system

helper_system = get_helper_system()

# Obter relatório completo
report = helper_system.get_full_report()

# Ver métricas
print(report["metrics"])

# Ver otimizações aplicadas
print(report["optimizations"])
```

### MCP Manager

**Documentação:** [[Agentes/MCP-Manager|Ver Documentação Completa]]

**Interface Web:** http://localhost:8506

**Funcionalidades principais:**
- Adicionar/remover servidores MCP
- Health checks
- Listar recursos e ferramentas

**Exemplo:**
```python
from mcp_manager import get_mcp_manager, MCPServer

mcp_manager = get_mcp_manager()

# Adicionar servidor
server = MCPServer(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path"],
    description="Servidor de filesystem",
    enabled=True
)
mcp_manager.add_server(server)

# Listar servidores
servers = mcp_manager.list_servers()
```

### Neo4j GraphRAG

**Documentação:** [[Agentes/Neo4j-GraphRAG|Ver Documentação Completa]]

**Funcionalidades principais:**
- Criar nós MCP, RAG, Obsidian
- Consultas GraphRAG
- Visualização de grafo
- Importar vault Obsidian

**Exemplo:**
```python
from mcp_neo4j_integration import get_neo4j_manager

neo4j = get_neo4j_manager()

# Criar nó MCP
neo4j.create_mcp_node({
    "name": "filesystem",
    "id": "filesystem",
    "description": "Servidor filesystem"
})

# Consultar GraphRAG
answer = neo4j.query_graphrag("Quais MCPs estão relacionados a filesystem?")

# Importar vault Obsidian
from pathlib import Path
neo4j.import_obsidian_vault(Path("/caminho/vault"))
```

### Obsidian Integration

**Documentação:** [[Agentes/Obsidian-Integration|Ver Documentação Completa]]

**Funcionalidades principais:**
- Criar notas sobre MCPs e RAGs
- Gerenciar links entre notas
- Buscar em notas

**Exemplo:**
```python
from mcp_obsidian_integration import ObsidianManager

obsidian = ObsidianManager()

# Configurar vault
obsidian.set_vault_path("/caminho/para/vault")

# Criar nota sobre MCP
obsidian.create_mcp_note("filesystem", {
    "command": "npx",
    "description": "Servidor filesystem"
})

# Buscar notas
notes = obsidian.search_notes("MCP")
```

### Kestra Agent

**Documentação:** [[Agentes/Kestra-Agent|Ver Documentação Completa]]

**Interface Web:** http://localhost:8080

**Funcionalidades principais:**
- Criar workflows Kestra
- Agendar tarefas
- Executar pipelines automatizados

**Exemplo:**
```python
from mcp_kestra_integration import get_kestra_agent

kestra = get_kestra_agent()

# Criar workflow padrão
kestra.create_sync_mcp_workflow()
kestra.create_health_check_workflow()

# Listar workflows
workflows = kestra.list_workflows()
```

## 📊 Fluxos Comuns

### Fluxo 1: Sincronização Completa

```python
from orchestrator import get_orchestrator

orchestrator = get_orchestrator()

# 1. Sincronizar MCPs para Neo4j
orchestrator.sync_mcp_to_neo4j()

# 2. Sincronizar MCPs para Obsidian
orchestrator.sync_mcp_to_obsidian()

# 3. Importar notas Obsidian para Neo4j
from mcp_neo4j_integration import get_neo4j_manager
from mcp_obsidian_integration import ObsidianManager

obsidian = ObsidianManager()
neo4j = get_neo4j_manager()

if obsidian.vault_path:
    neo4j.import_obsidian_vault(obsidian.vault_path)
```

### Fluxo 2: Criar Pipeline Automatizado

```python
from kestra_langchain_master import get_master_agent

master = get_master_agent()

# Criar workflow inteligente
workflow = master.create_intelligent_workflow(
    "Workflow que sincroniza MCPs toda segunda-feira às 9h e gera relatório"
)
```

### Fluxo 3: Monitorar e Otimizar

```python
from agent_helper_system import get_helper_system

helper_system = get_helper_system()

# Obter relatório
report = helper_system.get_full_report()

# Ver agentes com problemas
for agent_name, data in report["metrics"]["agents"].items():
    if data["status"] in ["warning", "error"]:
        print(f"{agent_name} precisa de atenção: {data['issues']}")

# Otimizações já foram aplicadas automaticamente
print(report["optimizations"])
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```bash
# LLM
LLM=llama2                    # ou gpt-4, gpt-3.5, claudev2

# Embedding
EMBEDDING_MODEL=sentence_transformer  # ou openai, ollama

# Neo4j
NEO4J_URI=neo4j://database:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Obsidian
OBSIDIAN_VAULT_PATH=/caminho/para/vault

# Ollama
OLLAMA_BASE_URL=http://localhost:11434

# LangChain (opcional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=meu-projeto
```

### Docker Compose

O sistema usa Docker Compose para orquestração:

```bash
# Ver serviços
docker compose ps

# Ver logs
docker compose logs -f mcp-manager

# Reiniciar serviço
docker compose restart mcp-manager

# Rebuild
docker compose up --build
```

## 🐛 Troubleshooting

### Problema: Neo4j não conecta

**Solução:**
```bash
# Verificar se está rodando
docker compose ps database

# Ver logs
docker compose logs database

# Verificar variáveis de ambiente
echo $NEO4J_URI
```

### Problema: Obsidian não encontra vault

**Solução:**
```python
from mcp_obsidian_integration import ObsidianManager

obsidian = ObsidianManager()
# Configurar caminho explícito
obsidian.set_vault_path("/caminho/completo/para/vault")
```

### Problema: Master Agent não funciona

**Solução:**
```python
# Verificar se LLM está configurado
from chains import load_llm

llm = load_llm("llama2", config={"ollama_base_url": "http://localhost:11434"})
# Deve funcionar sem erro
```

## 📚 Referências

- [[00-MAPA-DE-AGENTES|Mapa de Agentes]]
- [[04-Como-Criar-Agentes|Como Criar Novos Agentes]]
- [[ARCHITECTURE|Arquitetura do Sistema]]
- [[EXECUTION_PLAN|Plano de Execução]]

## 🏷️ Tags

#manual #sistema #agentes #documentação #uso #tutorial

---

**Última atualização:** {{date}}

