# Arquitetura MCP (Model Context Protocol)

## Visão Geral

O Gerenciador de MCP é um sistema completo para gerenciar servidores MCP (Model Context Protocol), integrando Docker, Obsidian, Neo4j e interfaces Streamlit para criar um ecossistema de gerenciamento de conhecimento e contexto.

## Componentes Principais

### 1. `mcp_manager.py` - Gerenciador Central

O módulo central que gerencia servidores MCP, suas configurações e conexões.

#### Classes Principais:

- **`MCPServer`**: Representa um servidor MCP configurado
  - `name`: Nome do servidor
  - `command`: Comando para executar o servidor
  - `args`: Argumentos do comando
  - `env`: Variáveis de ambiente (opcional)
  - `enabled`: Status de habilitação
  - `description`: Descrição do servidor

- **`MCPManager`**: Gerenciador principal de servidores MCP
  - Gerencia configurações em JSON
  - Controla conexões com servidores
  - Lista recursos e ferramentas
  - Verifica saúde dos servidores

#### Funcionalidades:

- ✅ Adicionar/remover servidores MCP
- ✅ Habilitar/desabilitar servidores
- ✅ Verificar saúde dos servidores
- ✅ Conectar/desconectar servidores
- ✅ Listar recursos e ferramentas
- ✅ Gerenciar configurações persistentes

### 2. `mcp_docker_integration.py` - Integração Docker

Detecta e gerencia servidores MCP em execução no Docker.

#### Classes Principais:

- **`DockerService`**: Representa um serviço Docker
  - `name`: Nome do serviço
  - `status`: Status do container
  - `ports`: Portas expostas
  - `image`: Imagem Docker
  - `container_id`: ID do container

- **`DockerMCPDetector`**: Detecta servidores MCP no Docker
  - Lista containers em execução
  - Detecta serviços MCP
  - Obtém informações detalhadas de serviços
  - Lista serviços do docker-compose.yml

#### Funcionalidades:

- ✅ Listar containers Docker em execução
- ✅ Detectar serviços MCP automaticamente
- ✅ Obter informações detalhadas de serviços
- ✅ Listar serviços do docker-compose.yml

### 3. `mcp_obsidian_integration.py` - Integração Obsidian

Cria e gerencia notas no Obsidian sobre MCPs e RAGs.

#### Classes Principais:

- **`ObsidianManager`**: Gerencia notas no Obsidian
  - Detecta vault do Obsidian automaticamente
  - Cria notas sobre MCPs e RAGs
  - Cria links entre notas
  - Busca notas por conteúdo

#### Funcionalidades:

- ✅ Detectar vault do Obsidian
- ✅ Criar notas sobre MCPs
- ✅ Criar notas sobre RAGs
- ✅ Criar notas de conexão
- ✅ Criar links bidirecionais entre notas
- ✅ Listar e buscar notas

### 4. `mcp_neo4j_integration.py` - Integração Neo4j GraphRAG

Gerencia grafo de conhecimento Neo4j e GraphRAG com LangGraph.

#### Classes Principais:

- **`Neo4jGraphRAGManager`**: Gerencia grafo de conhecimento Neo4j
  - Conecta ao Neo4j
  - Cria nós MCP, RAG e ObsidianNote
  - Cria relações entre nós
  - Implementa GraphRAG com LangGraph
  - Busca e visualiza o grafo

#### Funcionalidades:

- ✅ Criar nós MCP no grafo
- ✅ Criar nós RAG no grafo
- ✅ Criar nós ObsidianNote no grafo
- ✅ Criar relações entre nós
- ✅ Importar vault Obsidian para Neo4j
- ✅ Consultar GraphRAG
- ✅ Buscar no grafo
- ✅ Visualizar grafo
- ✅ Obter estatísticas do grafo

### 5. `mcp_manager_ui.py` - Interface Streamlit

Interface web completa para gerenciar servidores MCP.

#### Páginas:

1. **Servidores**: Lista e gerencia servidores MCP
2. **Adicionar Servidor**: Adiciona novos servidores MCP
3. **Recursos e Ferramentas**: Lista recursos e ferramentas disponíveis
4. **Docker Integration**: Gerencia servidores MCP no Docker
5. **Obsidian Integration**: Gerencia notas no Obsidian
6. **Neo4j GraphRAG**: Gerencia grafo de conhecimento e GraphRAG

#### Funcionalidades:

- ✅ Interface web completa
- ✅ Gerenciamento de servidores MCP
- ✅ Integração com Docker
- ✅ Integração com Obsidian
- ✅ Integração com Neo4j GraphRAG
- ✅ Visualização de grafo
- ✅ Busca e consulta GraphRAG

## Protocolo MCP

### Estrutura de Dados

#### Servidor MCP:
```json
{
  "name": "filesystem",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
  "env": {
    "VAR": "value"
  },
  "enabled": true,
  "description": "Servidor MCP para acesso ao sistema de arquivos"
}
```

#### Recurso MCP:
```json
{
  "uri": "mcp://server/resource/example",
  "name": "Exemplo de Recurso",
  "description": "Descrição do recurso",
  "mimeType": "text/plain"
}
```

#### Ferramenta MCP:
```json
{
  "name": "example_tool",
  "description": "Descrição da ferramenta",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param": {
        "type": "string",
        "description": "Parâmetro de exemplo"
      }
    }
  }
}
```

## Fluxo de Dados

```
┌─────────────────┐
│  MCP Manager    │
│  (Central)      │
└────────┬────────┘
         │
         ├─────────────────┬──────────────────┬──────────────────┐
         │                 │                  │                  │
         ▼                 ▼                  ▼                  ▼
┌─────────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Docker          │ │ Obsidian     │ │ Neo4j        │ │ Streamlit UI │
│ Integration     │ │ Integration  │ │ GraphRAG     │ │              │
└─────────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
         │                 │                  │                  │
         ▼                 ▼                  ▼                  ▼
    Containers        Vault Notes      Knowledge Graph    Web Interface
```

## Configuração

### Variáveis de Ambiente

```bash
# Neo4j
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# LLM e Embedding
LLM=llama2
EMBEDDING_MODEL=sentence_transformer
OLLAMA_BASE_URL=http://localhost:11434

# MCP
MCP_ENV_FILE=.env
MCP_CONFIG_FILE=mcp_servers.json
```

### Arquivo de Configuração MCP

O arquivo `mcp_servers.json` contém a configuração de todos os servidores MCP:

```json
{
  "filesystem": {
    "name": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
    "enabled": false,
    "description": "Servidor MCP para acesso ao sistema de arquivos"
  }
}
```

## Uso

### Iniciar o Gerenciador MCP

```bash
# Via Docker Compose
docker compose up mcp-manager

# Via Streamlit direto
streamlit run mcp_manager_ui.py
```

### Adicionar um Servidor MCP

```python
from mcp_manager import MCPManager, MCPServer

manager = MCPManager()
server = MCPServer(
    name="my_server",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-example"],
    enabled=True,
    description="Meu servidor MCP"
)
manager.add_server(server)
```

### Conectar a um Servidor

```python
manager.connect_server("my_server")
status = manager.get_server_status("my_server")
print(status)
```

### Usar GraphRAG

```python
from mcp_neo4j_integration import get_neo4j_manager

neo4j_manager = get_neo4j_manager()
answer = neo4j_manager.query_graphrag("Qual é a relação entre MCP e RAG?")
print(answer)
```

## Dependências

### Principais:

- `langchain-neo4j`: Integração com Neo4j
- `langgraph`: GraphRAG com LangGraph
- `streamlit`: Interface web
- `pyvis`: Visualização de grafo
- `python-dotenv`: Gerenciamento de variáveis de ambiente

### Ver `requirements.txt` para lista completa

## Extensibilidade

### Adicionar Novo Adaptador

1. Criar módulo `mcp_<service>_integration.py`
2. Implementar interface padrão
3. Integrar com `mcp_manager.py`
4. Adicionar à UI em `mcp_manager_ui.py`

### Adicionar Novo Protocolo

1. Definir estrutura de dados do protocolo
2. Implementar handlers em `mcp_manager.py`
3. Adicionar suporte na UI
4. Documentar na arquitetura

## Melhorias Futuras

- [ ] Implementar protocolo MCP completo (stdio, HTTP)
- [ ] Adicionar autenticação para servidores MCP
- [ ] Implementar cache de recursos e ferramentas
- [ ] Adicionar suporte a múltiplos vaults Obsidian
- [ ] Melhorar visualização de grafo
- [ ] Adicionar métricas e monitoramento
- [ ] Implementar testes automatizados
- [ ] Adicionar documentação de API

## Licença

Ver arquivo LICENSE no repositório.

