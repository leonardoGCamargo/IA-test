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

