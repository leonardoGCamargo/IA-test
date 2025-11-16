# MCP (Model Context Protocol) - Documentação Completa

> **Documentação consolidada** - Última atualização: 2025-01-27

---

## BROWSER_MCP_SETUP.md

# 🌐 Configurar MCP Browser no Cursor

## 📋 MCPs de Navegador Disponíveis

O Cursor tem suporte para MCPs de navegador que permitem abrir URLs diretamente. Existem duas opções principais:

### 1. **cursor-browser-extension** (Recomendado)
- MCP nativo do Cursor
- Permite navegar, clicar, preencher formulários
- Ideal para testes automatizados

### 2. **MCP Browser** (Alternativa)
- MCP genérico de navegador
- Funcionalidades similares

## 🚀 Configuração Rápida

### Opção 1: Usar Script Python (Mais Simples)

```bash
# Abre o dashboard automaticamente
python scripts/open_dashboard.py

# Ou apenas abre (se já estiver rodando)
python scripts/open_dashboard.py open
```

### Opção 2: Configurar MCP Browser no Cursor

1. **Abra as configurações do Cursor**
   - `Ctrl+,` ou `Cmd+,`
   - Procure por "MCP Servers"

2. **Adicione o Browser MCP:**

```json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-puppeteer"
      ]
    }
  }
}
```

3. **Ou use o cursor-browser-extension:**

O Cursor já vem com suporte para browser extension. Você pode pedir ao assistente:

```
"Abra http://localhost:8508 no navegador"
```

## 🎯 Como Usar

### Via Assistente do Cursor

Simplesmente peça:
```
"Abra o dashboard em http://localhost:8508"
```

Ou:
```
"Navegue para http://localhost:8508 e me mostre a tela"
```

### Via Script

```bash
# Inicia e abre automaticamente
python scripts/open_dashboard.py
```

### Via Comando Manual

```bash
# Windows
start http://localhost:8508

# Linux
xdg-open http://localhost:8508

# Mac
open http://localhost:8508
```

## 🔧 Ferramentas MCP Browser Disponíveis

### cursor-browser-extension

1. **browser_navigate** - Navegar para URL
2. **browser_snapshot** - Capturar snapshot da página
3. **browser_click** - Clicar em elementos
4. **browser_type** - Digitar texto
5. **browser_take_screenshot** - Tirar screenshot
6. **browser_evaluate** - Executar JavaScript

### Exemplo de Uso

Você pode pedir ao assistente:
```
"Navegue para http://localhost:8508, tire um screenshot e me mostre"
```

Ou:
```
"Abra http://localhost:8508, clique no botão de chat e tire um screenshot"
```

## 📱 Abrir Dashboard Automaticamente

### Script Automático

O script `scripts/open_dashboard.py` faz tudo automaticamente:

1. Verifica se o dashboard está rodando
2. Se não estiver, inicia o dashboard
3. Aguarda alguns segundos
4. Abre no navegador automaticamente

```bash
python scripts/open_dashboard.py
```

## 🐛 Troubleshooting

### Dashboard não abre

1. Verifique se está rodando:
```bash
# Windows
netstat -ano | findstr :8508

# Linux/Mac
lsof -i :8508
```

2. Inicie manualmente:
```bash
streamlit run src/apps/agent_dashboard.py --server.port=8508
```

3. Abra manualmente:
```
http://localhost:8508
```

### MCP Browser não funciona

1. Verifique se o MCP está configurado
2. Reinicie o Cursor
3. Use o script Python como alternativa

## 💡 Dicas

1. **Use o script:** `python scripts/open_dashboard.py` é a forma mais fácil
2. **Peça ao assistente:** "Abra http://localhost:8508"
3. **Atalho:** Crie um atalho no desktop apontando para `http://localhost:8508`

## 🎯 Próximos Passos

1. ✅ Execute: `python scripts/open_dashboard.py`
2. ✅ Ou peça ao assistente: "Abra http://localhost:8508"
3. ✅ Explore o dashboard
4. ✅ Teste as funcionalidades

---

**Última atualização:** 2025-01-27



---

## MCP_ARCHITECTURE.md

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



---

## MCP_BROWSER_CURSOR.md

# 🌐 Usar MCP Browser no Cursor - Guia Completo

## 📋 O que é MCP Browser?

O Cursor tem suporte nativo para **MCP Browser Extension** que permite:
- ✅ Abrir URLs no navegador
- ✅ Navegar entre páginas
- ✅ Tirar screenshots
- ✅ Interagir com elementos (clicar, digitar)
- ✅ Capturar snapshots da página
- ✅ Executar JavaScript

## 🚀 Como Usar

### Método 1: Pedir ao Assistente (Mais Fácil)

Simplesmente peça ao assistente do Cursor:

```
"Abra http://localhost:8508 no navegador"
```

Ou:

```
"Navegue para http://localhost:8508 e me mostre como está a página"
```

Ou:

```
"Abra o dashboard em http://localhost:8508, tire um screenshot e me mostre"
```

### Método 2: Comandos Específicos

Você pode pedir comandos mais específicos:

```
"Navegue para http://localhost:8508, aguarde 5 segundos, tire um screenshot"
```

```
"Abra http://localhost:8508, clique no botão de chat, tire um screenshot"
```

```
"Navegue para http://localhost:8508, preencha o campo de busca com 'orchestrator', tire um screenshot"
```

## 🛠️ Ferramentas MCP Browser Disponíveis

O Cursor já tem estas ferramentas configuradas:

1. **browser_navigate** - Navegar para uma URL
2. **browser_snapshot** - Capturar snapshot da página (melhor que screenshot)
3. **browser_take_screenshot** - Tirar screenshot
4. **browser_click** - Clicar em elementos
5. **browser_type** - Digitar texto
6. **browser_select_option** - Selecionar opções em dropdowns
7. **browser_evaluate** - Executar JavaScript
8. **browser_wait_for** - Aguardar elementos ou tempo
9. **browser_console_messages** - Ver mensagens do console
10. **browser_network_requests** - Ver requisições de rede

## 📱 Exemplo Prático: Abrir Dashboard

### Passo 1: Iniciar o Dashboard

```bash
# Instalar dependências (se necessário)
pip install streamlit plotly pandas streamlit-option-menu

# Iniciar dashboard
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

### Passo 2: Pedir ao Assistente

Depois que o dashboard estiver rodando, peça:

```
"Abra http://localhost:8508 no navegador e me mostre a tela"
```

O assistente irá:
1. Navegar para a URL
2. Capturar um snapshot
3. Mostrar como está a página

### Passo 3: Interagir

Você pode pedir para interagir:

```
"Na página do dashboard, clique no botão de chat"
```

```
"Na página do dashboard, selecione o agente 'Orchestrator' no dropdown"
```

## 🎯 Casos de Uso

### 1. Verificar se Dashboard Está Funcionando

```
"Navegue para http://localhost:8508, aguarde 3 segundos, tire um screenshot e me mostre"
```

### 2. Testar Funcionalidade

```
"Abra http://localhost:8508, clique em 'Chat', digite 'Olá' no campo de mensagem, tire um screenshot"
```

### 3. Verificar Status

```
"Navegue para http://localhost:8508, vá para a seção 'Monitoramento', tire um screenshot"
```

### 4. Ver Logs do Console

```
"Abra http://localhost:8508, me mostre as mensagens do console do navegador"
```

## 🔧 Configuração (Opcional)

O MCP Browser já vem configurado no Cursor. Se precisar verificar:

1. Abra configurações do Cursor (`Ctrl+,`)
2. Procure por "MCP Servers"
3. Deve aparecer "cursor-browser-extension"

## 💡 Dicas

1. **Use "snapshot" em vez de "screenshot"** - É mais rápido e mostra melhor a estrutura
2. **Aguarde alguns segundos** após iniciar o dashboard antes de navegar
3. **Use descrições claras** ao pedir para clicar em elementos
4. **Peça screenshots** para ver como está a página

## 🐛 Troubleshooting

### "Connection refused"

O dashboard não está rodando. Inicie primeiro:
```bash
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

### MCP Browser não funciona

1. Reinicie o Cursor
2. Verifique se está pedindo corretamente ao assistente
3. Use o método manual (abrir navegador diretamente)

### Não consegue ver a página

Peça ao assistente:
```
"Navegue para http://localhost:8508, aguarde 5 segundos, tire um snapshot completo da página"
```

## 📚 Exemplos de Comandos

### Básico
```
"Abra http://localhost:8508"
```

### Com Screenshot
```
"Abra http://localhost:8508 e tire um screenshot"
```

### Interagir
```
"Na página http://localhost:8508, clique no botão 'Chat'"
```

### Verificar Console
```
"Abra http://localhost:8508 e me mostre os erros do console"
```

### Ver Requisições
```
"Abra http://localhost:8508 e me mostre as requisições de rede"
```

## 🎯 Resumo

1. ✅ **MCP Browser já está no Cursor** - Não precisa instalar nada
2. ✅ **Peça ao assistente** - "Abra http://localhost:8508"
3. ✅ **Use comandos específicos** - Para interagir com a página
4. ✅ **Tire screenshots** - Para ver como está

---

**Pronto!** Agora você pode abrir e testar o dashboard diretamente no Cursor! 🎉



---

## MCP_README.md

# Gerenciador de MCP (Model Context Protocol)

## Visão Geral

O Gerenciador de MCP é um sistema completo para gerenciar servidores MCP, integrando Docker, Obsidian, Neo4j e interfaces Streamlit para criar um ecossistema de gerenciamento de conhecimento e contexto.

## Recursos

- ✅ **Gerenciamento de Servidores MCP**: Adicione, remova e gerencie servidores MCP
- ✅ **Integração Docker**: Detecte e gerencie servidores MCP em execução no Docker
- ✅ **Integração Obsidian**: Crie e gerencie notas no Obsidian sobre MCPs e RAGs
- ✅ **Integração Neo4j GraphRAG**: Gerencie grafo de conhecimento e consulte com GraphRAG
- ✅ **Interface Web**: Interface Streamlit completa para gerenciar tudo
- ✅ **Visualização de Grafo**: Visualize o grafo de conhecimento com pyvis

## Início Rápido

### Via Docker Compose

```bash
# Iniciar o gerenciador MCP
docker compose up mcp-manager

# Acessar a interface web
# http://localhost:8506
```

### Via Streamlit Direto

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a interface
streamlit run mcp_manager_ui.py
```

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` com as seguintes variáveis:

```bash
# Neo4j
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# LLM e Embedding
LLM=llama2
EMBEDDING_MODEL=sentence_transformer
OLLAMA_BASE_URL=http://localhost:11434

# MCP (Opcional)
MCP_ENV_FILE=.env
MCP_CONFIG_FILE=mcp_servers.json
```

### Arquivo de Configuração MCP

O arquivo `mcp_servers.json` será criado automaticamente quando você adicionar servidores MCP. Você também pode criá-lo manualmente:

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

### Adicionar um Servidor MCP

1. Acesse a interface web em http://localhost:8506
2. Navegue para "Adicionar Servidor"
3. Preencha os campos:
   - Nome do servidor
   - Comando (ex: `npx`, `python`, `node`)
   - Argumentos (um por linha)
   - Descrição (opcional)
   - Variáveis de ambiente (opcional)
4. Clique em "Adicionar Servidor"

### Gerenciar Servidores MCP

1. Acesse a página "Servidores"
2. Visualize todos os servidores configurados
3. Habilite/desabilite servidores
4. Verifique a saúde dos servidores
5. Remova servidores se necessário

### Integração Docker

1. Acesse a página "Docker Integration"
2. Visualize containers Docker em execução
3. Detecte servidores MCP automaticamente
4. Obtenha informações detalhadas de serviços

### Integração Obsidian

1. Configure o caminho do vault do Obsidian na sidebar
2. Acesse a página "Obsidian Integration"
3. Crie notas sobre MCPs e RAGs
4. Crie links entre notas
5. Busque notas por conteúdo

### Integração Neo4j GraphRAG

1. Configure as variáveis de ambiente do Neo4j
2. Acesse a página "Neo4j GraphRAG"
3. Importe MCPs e notas do Obsidian para o Neo4j
4. Crie nós e relações no grafo
5. Consulte o grafo usando GraphRAG
6. Visualize o grafo de conhecimento

## Arquitetura

Ver `MCP_ARCHITECTURE.md` para detalhes completos da arquitetura.

## Módulos

- **`mcp_manager.py`**: Gerenciador central de servidores MCP
- **`mcp_docker_integration.py`**: Integração com Docker
- **`mcp_obsidian_integration.py`**: Integração com Obsidian
- **`mcp_neo4j_integration.py`**: Integração com Neo4j GraphRAG
- **`mcp_manager_ui.py`**: Interface Streamlit

## Dependências

- `langchain-neo4j`: Integração com Neo4j
- `langgraph`: GraphRAG com LangGraph
- `streamlit`: Interface web
- `pyvis`: Visualização de grafo
- `python-dotenv`: Gerenciamento de variáveis de ambiente

Ver `requirements.txt` para lista completa.

## Documentação

- **Arquitetura**: Ver `MCP_ARCHITECTURE.md`
- **API**: Ver documentação nos módulos Python
- **Exemplos**: Ver exemplos de uso nos módulos

## Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Ver arquivo LICENSE no repositório.

## Suporte

Para questões e suporte, abra uma issue no repositório.



---

