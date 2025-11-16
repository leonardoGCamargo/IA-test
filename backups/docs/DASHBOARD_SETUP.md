# Setup do Agent Dashboard - Guia Rápido

## Resumo

Foi criada uma interface visual completa (Streamlit) para interagir com todos os agentes do sistema, incluindo:
- 💬 Conversa com agentes
- 🔍 Visualização de problemas diagnosticados
- 🛠️ Soluções e prompts de resolução
- 📊 Dashboard do sistema

## Arquivos Criados

### 1. Agentes
- `src/agents/diagnostic_agent.py` - Agente de diagnóstico
- `src/agents/resolution_agent.py` - Agente de resolução
- `src/agents/agent_dashboard_ui.py` - Interface Streamlit

### 2. Docker
- `docker/agent_dashboard.Dockerfile` - Dockerfile para a interface
- `config/docker-compose.yml` - Atualizado com serviço agent-dashboard

### 3. Scripts
- `scripts/run_dashboard.py` - Script para executar o dashboard

### 4. Documentação
- `docs/AGENT_DASHBOARD_README.md` - Documentação completa
- `docs/DASHBOARD_SETUP.md` - Este guia

## Instalação Rápida

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

## Uso Rápido

### 1. Executar Diagnóstico
1. Acesse a aba "🔍 Problemas"
2. Clique em "🔄 Executar Diagnóstico"
3. Visualize os problemas encontrados

### 2. Ver Soluções
1. Execute o diagnóstico primeiro
2. Acesse a aba "🛠️ Resoluções"
3. Siga os passos indicados
4. Execute os comandos fornecidos

### 3. Conversar com Agentes
1. Acesse a aba "💬 Conversa"
2. Digite sua mensagem
3. Comandos disponíveis:
   - "diagnóstico" - Executa diagnóstico completo
   - "status" - Mostra status do sistema
   - "agentes" - Lista agentes disponíveis

### 4. Ver Dashboard
1. Acesse a aba "📊 Dashboard"
2. Visualize métricas do sistema
3. Verifique status de agentes

## Funcionalidades Principais

### Diagnostic Agent
- ✅ Detecta problemas no sistema
- ✅ Verifica variáveis de ambiente
- ✅ Verifica chaves de API
- ✅ Verifica conexões de banco de dados
- ✅ Verifica dependências instaladas
- ✅ Verifica configurações
- ✅ Detecta problemas de permissão

### Resolution Agent
- ✅ Gera soluções para problemas
- ✅ Cria prompts de resolução
- ✅ Fornece comandos para executar
- ✅ Links para documentação
- ✅ Passos detalhados
- ✅ Tempo estimado e dificuldade

### Interface Visual
- ✅ Aba de conversa
- ✅ Aba de problemas
- ✅ Aba de resoluções
- ✅ Aba de dashboard
- ✅ Filtros e buscas
- ✅ Visualização de métricas
- ✅ Histórico de conversas

## Integração com Orchestrator

Todos os agentes estão integrados ao Orchestrator:
- ✅ Diagnostic Agent integrado
- ✅ Resolution Agent integrado
- ✅ Database Manager integrado
- ✅ Status do sistema disponível
- ✅ Tarefas gerenciadas

## Configuração

### Variáveis de Ambiente Necessárias

```bash
# Neo4j (obrigatório)
NEO4J_URI=neo4j://database:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# LLM e Embedding (recomendado)
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

## Troubleshooting

### Erro: "Module not found"
**Solução**: Instale as dependências:
```bash
pip install -r config/requirements.txt
```

### Erro: "Connection failed"
**Solução**: Verifique as variáveis de ambiente e conexões

### Interface não carrega
**Solução**: Verifique se a porta 8507 está disponível

### Diagnóstico não funciona
**Solução**: Verifique se o Diagnostic Agent está inicializado corretamente

## Próximos Passos

1. ✅ Executar o dashboard
2. ✅ Executar diagnóstico completo
3. ✅ Ver problemas encontrados
4. ✅ Seguir soluções sugeridas
5. ✅ Resolver problemas
6. ✅ Verificar status do sistema

## Documentação Completa

- [Agent Dashboard README](./AGENT_DASHBOARD_README.md)
- [Database Manager README](./DB_MANAGER_README.md)
- [Diagnostic Agent](./DIAGNOSTIC_AGENT_README.md) (se existir)
- [Resolution Agent](./RESOLUTION_AGENT_README.md) (se existir)

## Suporte

Para problemas ou dúvidas, consulte a documentação completa ou abra uma issue no repositório.

