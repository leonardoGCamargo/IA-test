# 🔧 Configuração do Neo4j Cypher MCP no Cursor

Este guia explica como configurar o MCP (Model Context Protocol) do Neo4j Cypher no Cursor IDE.

## 📋 O que é o Neo4j Cypher MCP?

O MCP do Neo4j Cypher permite que o Cursor:
- ✅ Consulte o schema do banco Neo4j diretamente
- ✅ Execute queries Cypher através do chat
- ✅ Entenda a estrutura dos dados automaticamente
- ✅ Gere código baseado nos dados do grafo

## 🚀 Configuração Rápida

### Opção 1: Configuração Local (Recomendado)

O arquivo `.cursor/mcp.json` já foi criado na raiz do projeto com as configurações corretas.

**Parâmetros configurados:**
- **neo4j-cypher.url**: `neo4j://localhost:7687` (já configurado via env)
- **neo4j-cypher.username**: `neo4j` (já configurado via env)
- **neo4j-cypher.password**: `SenhaNeo4j123!` (já configurado via env)
- **neo4j-cypher.database**: `neo4j` (banco padrão, pode deixar vazio)

### Opção 2: Configuração Manual na Interface do Cursor

Se você está vendo a tela de configuração do Cursor, preencha assim:

1. **neo4j-cypher.url**: `neo4j://localhost:7687`
2. **neo4j-cypher.username**: `neo4j`
3. **neo4j-cypher.password**: `SenhaNeo4j123!` (a mesma senha do seu `.env`)
4. **neo4j-cypher.database**: Deixe vazio (usa o banco padrão `neo4j`)
5. **neo4j-cypher.read_timeout**: Deixe vazio (usa padrão)
6. **neo4j-cypher.response_token_limit**: Deixe vazio (usa padrão)
7. **neo4j-cypher.namespace**: Deixe vazio
8. **neo4j-cypher.transport**: Deixe vazio
9. **neo4j-cypher.server_host**: Deixe vazio
10. **neo4j-cypher.server_port**: Deixe vazio
11. **neo4j-cypher.server_path**: Deixe vazio
12. **neo4j-cypher.server_allow_origins**: Deixe vazio
13. **neo4j-cypher.server_allowed_hosts**: Deixe vazio
14. **neo4j-cypher.read_only**: Deixe desmarcado (para permitir escrita)

## 📝 Arquivo de Configuração

O arquivo `.cursor/mcp.json` contém:

```json
{
  "mcpServers": {
    "neo4j-cypher": {
      "command": "npx",
      "args": [
        "-y",
        "@neo4j/mcp-server-neo4j"
      ],
      "env": {
        "NEO4J_URI": "neo4j://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "SenhaNeo4j123!",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

## ✅ Como Verificar se Está Funcionando

1. **Reinicie o Cursor** (se necessário)
2. **Abra o chat do Cursor**
3. **Teste com uma pergunta:**
   ```
   "Quais são os agentes no Neo4j?"
   ```
   ou
   ```
   "Execute uma query Cypher para listar todos os nós do tipo Agent"
   ```

4. **O Cursor deve:**
   - Reconhecer que você tem um banco Neo4j
   - Conseguir consultar o schema
   - Executar queries Cypher automaticamente

## 🔧 Configuração Global (Opcional)

Se quiser que o MCP do Neo4j esteja disponível em TODOS os projetos:

1. Copie o arquivo `.cursor/mcp.json` para:
   - **Windows**: `C:\Users\SeuUsuario\.cursor\mcp.json`
   - **Mac/Linux**: `~/.cursor/mcp.json`

2. Reinicie o Cursor

## 🎯 Funcionalidades Disponíveis

Com o MCP do Neo4j configurado, você pode:

### 1. Consultar Schema
```
"Qual é o schema do banco Neo4j?"
"Quais são os tipos de nós no grafo?"
```

### 2. Executar Queries
```
"Liste todos os agentes do projeto"
"Quantos relacionamentos existem entre agentes e serviços?"
```

### 3. Gerar Código Baseado nos Dados
```
"Crie uma função Python que busca todos os agentes que usam LLM"
"Gere um script que lista todos os serviços Docker"
```

### 4. Entender Estrutura
```
"Como os agentes se relacionam com os serviços?"
"Qual é a arquitetura do projeto baseada no grafo?"
```

## ⚙️ Parâmetros Avançados (Opcional)

Se precisar configurar parâmetros avançados:

- **read_timeout**: Timeout para leitura (em segundos)
- **response_token_limit**: Limite de tokens na resposta
- **namespace**: Namespace para queries (geralmente vazio)
- **transport**: Tipo de transporte (geralmente vazio, usa padrão)
- **read_only**: Se marcado, apenas leitura (não permite CREATE/UPDATE/DELETE)

## 🔒 Segurança

⚠️ **IMPORTANTE**: 
- O arquivo `.cursor/mcp.json` contém a senha do Neo4j
- **NÃO commite** este arquivo no Git
- Adicione `.cursor/` ao `.gitignore` se ainda não estiver

## 🆘 Troubleshooting

### MCP não aparece no Cursor

1. Verifique se o arquivo `.cursor/mcp.json` existe
2. Reinicie o Cursor completamente
3. Verifique se o Neo4j está rodando: `docker ps | grep neo4j`

### Erro de conexão

1. Verifique se a URI está correta: `neo4j://localhost:7687`
2. Confirme que a senha está correta (mesma do `.env`)
3. Teste a conexão manualmente:
   ```bash
   python scripts/test_neo4j_connection.py
   ```

### MCP não executa queries

1. Verifique se o banco tem dados (execute o script de população)
2. Confirme que `read_only` está desmarcado se quiser escrever
3. Verifique os logs do Cursor para erros

## 📚 Recursos

- [Documentação oficial do Neo4j MCP](https://github.com/neo4j/mcp-server-neo4j)
- [Documentação do Model Context Protocol](https://modelcontextprotocol.io/)
- [Vídeo: Cursor + Neo4j MCP](https://www.youtube.com/watch?v=UilGH0j73rI)

---

**Última atualização:** 2025-01-27


