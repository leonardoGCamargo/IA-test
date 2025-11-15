# Arquitetura do Sistema MCP + Docker + Obsidian + Neo4j + Kestra + UI

## Visão Geral

Este documento descreve a arquitetura modular do sistema de gerenciamento MCP (Model Context Protocol) integrado com Docker, Obsidian, Neo4j, Kestra e interfaces de usuário.

## Componentes Principais

### 1. MCP Manager (`mcp_manager.py`)
**Responsabilidade:** Gerenciamento centralizado de servidores MCP
- Gerenciamento de configuração de servidores
- Health checks e monitoramento
- CRUD de servidores MCP
- Listagem de recursos e ferramentas

**Interface:**
- Classe `MCPManager`
- Métodos: `add_server()`, `remove_server()`, `list_servers()`, `check_server_health()`

### 2. Docker Integration (`mcp_docker_integration.py`)
**Responsabilidade:** Integração com ecossistema Docker
- Detecção de containers MCP em execução
- Monitoramento de serviços Docker Compose
- Extração de informações de containers

**Interface:**
- Classe `DockerMCPDetector`
- Métodos: `list_running_containers()`, `detect_mcp_services()`, `get_service_info()`

### 3. Neo4j GraphRAG (`mcp_neo4j_integration.py`)
**Responsabilidade:** Gestão de grafo de conhecimento e GraphRAG
- Armazenamento de nós MCP, RAG e Obsidian
- Consultas GraphRAG usando LangGraph
- Visualização de grafo
- Busca semântica com embeddings

**Interface:**
- Classe `Neo4jGraphRAGManager`
- Métodos: `create_mcp_node()`, `query_graphrag()`, `import_obsidian_vault()`

### 4. Obsidian Integration (`mcp_obsidian_integration.py`)
**Responsabilidade:** Gestão de notas no Obsidian
- Criação de notas sobre MCPs e RAGs
- Gestão de links entre notas
- Busca em notas

**Interface:**
- Classe `ObsidianManager`
- Métodos: `create_mcp_note()`, `create_rag_note()`, `link_notes()`

### 5. Streamlit UI (`mcp_manager_ui.py`)
**Responsabilidade:** Interface de usuário web
- Dashboard para gerenciamento de servidores MCP
- Visualização de dados Neo4j
- Criação de notas Obsidian
- Monitoramento de containers Docker

### 6. Kestra Agent (A IMPLEMENTAR)
**Responsabilidade:** Orquestração de pipelines automatizados
- Agendamento de tarefas
- Workflows de integração MCP → Neo4j → Obsidian
- Automação de importações e sincronizações

## Fluxo de Dados

```
┌─────────────┐
│   MCP UI    │
│ (Streamlit) │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  MCP Manager    │ ◄──┐
│  (Coordenação)  │    │
└────────┬────────┘    │
         │             │
    ┌────┴────┬────────┼────────┐
    │         │        │        │
    ▼         ▼        ▼        ▼
┌────────┐ ┌─────┐ ┌──────┐ ┌─────────┐
│ Docker │ │Neo4j│ │Obsid.│ │ Kestra  │
│Integration│GraphRAG│Integration│ Agent   │
└────────┘ └─────┘ └──────┘ └─────────┘
```

## Fluxos Principais

### 1. Criação de Servidor MCP
```
User → UI → MCP Manager → Save Config
                      └→ Neo4j (Criar nó)
                      └→ Obsidian (Criar nota)
```

### 2. Importação de Vault Obsidian
```
Obsidian Vault → Neo4j Manager → Neo4j Graph
                              └→ Cria nós ObsidianNote
                              └→ Cria relações e tags
```

### 3. Consulta GraphRAG
```
Query → Neo4j GraphRAG Manager → Retrieve Context
                              └→ Generate Answer (LLM)
```

### 4. Pipeline Automatizado (Kestra)
```
Schedule → Kestra → Import Obsidian → Neo4j
                  └→ Sync MCP Status
                  └→ Generate Reports
```

## Dependências

### Infraestrutura
- Docker & Docker Compose
- Neo4j Database
- Obsidian Vault (opcional)

### Python
- `langchain-neo4j` - Integração Neo4j
- `langgraph` - GraphRAG
- `streamlit` - UI
- `pyvis` - Visualização de grafos
- `python-dotenv` - Gerenciamento de env vars

### Outros
- Kestra (a ser integrado)

## Configuração

### Variáveis de Ambiente
- `NEO4J_URI` - URI de conexão Neo4j
- `NEO4J_USERNAME` - Usuário Neo4j
- `NEO4J_PASSWORD` - Senha Neo4j
- `OBSIDIAN_VAULT_PATH` - Caminho do vault Obsidian
- `LLM` - Modelo LLM a usar
- `EMBEDDING_MODEL` - Modelo de embedding

## Próximos Passos

1. ✅ Implementar Kestra Agent
2. ✅ Criar módulo de orquestração centralizado
3. ✅ Documentar APIs e interfaces
4. ✅ Implementar testes de integração
5. ✅ Criar pipelines de CI/CD

