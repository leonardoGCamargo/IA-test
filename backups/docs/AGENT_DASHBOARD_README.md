# Agent Dashboard - Interface Visual para Agentes

## Visão Geral

O Agent Dashboard é uma interface Streamlit que permite interagir visualmente com todos os agentes do sistema, incluindo:
- 💬 Conversa com agentes
- 🔍 Visualização de problemas diagnosticados
- 🛠️ Soluções e prompts de resolução
- 📊 Dashboard do sistema

## Funcionalidades

### 1. Aba de Conversa 💬
- Interface de chat para interagir com os agentes
- Histórico de conversas
- Processamento de mensagens via Orchestrator
- Comandos de diagnóstico e status

### 2. Aba de Problemas 🔍
- Visualização de problemas diagnosticados
- Filtros por severidade e categoria
- Resumo de problemas (críticos, altos, médios, baixos)
- Detalhes de cada problema

### 3. Aba de Resoluções 🛠️
- Soluções geradas para cada problema
- Passos para resolução
- Comandos para executar
- Prompts para ajudar na resolução
- Links para documentação

### 4. Aba de Dashboard 📊
- Métricas do sistema
- Status de todos os agentes
- Informações sobre bancos de dados
- Estatísticas de tarefas

## Instalação

### Via Docker Compose

```bash
# Iniciar o dashboard
docker compose -f config/docker-compose.yml up agent-dashboard

# Acessar a interface
# http://localhost:8507
```

### Via Streamlit Direto

```bash
# Instalar dependências
pip install -r config/requirements.txt

# Executar a interface
streamlit run src/agents/agent_dashboard_ui.py --server.port=8507
```

## Configuração

### Variáveis de Ambiente

Certifique-se de que as variáveis de ambiente estão configuradas no arquivo `.env`:

```bash
# Neo4j
NEO4J_URI=neo4j://database:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# LLM e Embedding
LLM=llama2
EMBEDDING_MODEL=sentence_transformer
OLLAMA_BASE_URL=http://localhost:11434

# APIs (opcional)
OPENAI_API_KEY=...
GOOGLE_API_KEY=...
SUPABASE_URL=...
SUPABASE_KEY=...
NEON_DATABASE_URL=...
MONGODB_URI=...
```

## Uso

### Executar Diagnóstico

1. Acesse a aba "🔍 Problemas"
2. Clique no botão "🔄 Executar Diagnóstico"
3. Aguarde o diagnóstico completar
4. Visualize os problemas encontrados

### Ver Soluções

1. Execute o diagnóstico primeiro
2. Acesse a aba "🛠️ Resoluções"
3. Visualize as soluções geradas
4. Siga os passos indicados
5. Execute os comandos fornecidos

### Conversar com Agentes

1. Acesse a aba "💬 Conversa"
2. Digite sua mensagem
3. Aguarde a resposta do agente
4. Comandos disponíveis:
   - "diagnóstico" - Executa diagnóstico completo
   - "status" - Mostra status do sistema
   - "agentes" - Lista agentes disponíveis

### Ver Dashboard

1. Acesse a aba "📊 Dashboard"
2. Visualize métricas do sistema
3. Verifique status de agentes
4. Monitore tarefas

## Agentes Disponíveis

### Diagnostic Agent
- Detecta problemas no sistema
- Verifica variáveis de ambiente
- Verifica chaves de API
- Verifica conexões de banco de dados
- Verifica dependências instaladas

### Resolution Agent
- Gera soluções para problemas
- Cria prompts de resolução
- Fornece comandos para executar
- Links para documentação

### Database Manager
- Gerencia bancos de dados
- Suporta Supabase, Neon, MongoDB
- Executa queries
- Lista tabelas/coleções

### Orchestrator
- Coordena todos os agentes
- Gerencia tarefas
- Fornece status do sistema

## Estrutura de Problemas

### Severidades
- **CRITICAL**: Problemas críticos que impedem o funcionamento
- **HIGH**: Problemas importantes que afetam funcionalidades
- **MEDIUM**: Problemas médios que podem causar inconvenientes
- **LOW**: Problemas menores
- **INFO**: Informações úteis

### Categorias
- **ENVIRONMENT**: Problemas de ambiente
- **API_KEY**: Problemas de chaves de API
- **DATABASE**: Problemas de banco de dados
- **DEPENDENCY**: Problemas de dependências
- **CONFIGURATION**: Problemas de configuração
- **CONNECTION**: Problemas de conexão
- **PERMISSION**: Problemas de permissão
- **OTHER**: Outros problemas

## Soluções

Cada solução inclui:
- **Título**: Título da solução
- **Descrição**: Descrição do problema
- **Passos**: Passos para resolver
- **Comandos**: Comandos para executar
- **Prompts**: Prompts para ajudar na resolução
- **Links**: Links para documentação
- **Tempo estimado**: Tempo estimado para resolução
- **Dificuldade**: Dificuldade da resolução (easy, medium, hard)

## Troubleshooting

### Erro: "Module not found"
**Solução**: Instale as dependências:
```bash
pip install -r config/requirements.txt
```

### Erro: "Connection failed"
**Solução**: Verifique as variáveis de ambiente e conexões

### Erro: "Diagnostic agent not available"
**Solução**: Verifique se o Diagnostic Agent está inicializado corretamente

### Interface não carrega
**Solução**: Verifique se a porta 8507 está disponível

## Desenvolvimento

### Adicionar Novo Agente

1. Crie o agente em `src/agents/`
2. Adicione ao Orchestrator
3. Adicione à interface se necessário
4. Atualize a documentação

### Adicionar Nova Verificação

1. Adicione método em `DiagnosticAgent`
2. Chame o método em `run_full_diagnostic()`
3. Adicione resolução correspondente em `ResolutionAgent`

### Personalizar Interface

1. Edite `agent_dashboard_ui.py`
2. Adicione novas abas se necessário
3. Personalize CSS e layout
4. Teste a interface

## Referências

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Diagnostic Agent Documentation](./DIAGNOSTIC_AGENT_README.md)
- [Resolution Agent Documentation](./RESOLUTION_AGENT_README.md)
- [Orchestrator Documentation](./ORCHESTRATOR_SUMMARY.md)

## Contribuindo

Para contribuir com melhorias no Agent Dashboard, consulte a documentação de desenvolvimento do projeto.

