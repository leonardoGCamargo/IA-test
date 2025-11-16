# 🛠️ Ferramentas do Front-End - Dashboard de Agentes

## 📋 Lista de Ferramentas Utilizadas

### 1. **Streamlit** ⭐ Principal
- **Versão**: >= 1.28.0
- **Uso**: Framework principal para criar a interface web
- **Por quê**: 
  - Já está no projeto
  - Integração nativa com Python
  - Interface rápida de criar
  - Componentes prontos (chat, métricas, gráficos)

### 2. **Plotly** 📊
- **Versão**: >= 5.17.0
- **Uso**: Gráficos interativos e visualizações
- **Por quê**: 
  - Gráficos modernos e interativos
  - Fácil integração com Streamlit
  - Visualizações profissionais

### 3. **Pandas** 📈
- **Versão**: >= 2.0.0
- **Uso**: Manipulação de dados e métricas
- **Por quê**: 
  - Processamento eficiente de dados
  - Análise de métricas dos agentes
  - Integração com Streamlit

### 4. **Streamlit-Option-Menu** 🎨
- **Versão**: >= 0.3.6
- **Uso**: Menu lateral moderno
- **Por quê**: 
  - Navegação intuitiva
  - Interface profissional
  - Fácil de usar

### 5. **Requests** 🌐
- **Versão**: >= 2.31.0
- **Uso**: Comunicação com APIs (se necessário)
- **Por quê**: 
  - Chamadas HTTP para agentes
  - Integração com serviços externos

## 📦 Instalação

```bash
pip install streamlit plotly pandas streamlit-option-menu requests
```

Ou via requirements.txt:
```bash
pip install -r config/requirements.txt
```

## 🚀 Como Acessar o Dashboard

### Método 1: Executar Diretamente (Mais Rápido)

```bash
# 1. Navegue até o diretório do projeto
cd IA-test

# 2. Execute o script
python scripts/run_dashboard.py

# Ou diretamente com streamlit
streamlit run src/apps/agent_dashboard.py --server.port=8508
```

**Acesse no navegador:** http://localhost:8508

### Método 2: Via Docker

```bash
# Build e executar
docker compose -f config/docker-compose.yml up agent-dashboard

# Ou em background
docker compose -f config/docker-compose.yml up -d agent-dashboard
```

**Acesse no navegador:** http://localhost:8508

### Método 3: Via Docker Compose (Stack Completo)

```bash
# Executar todos os serviços incluindo dashboard
docker compose -f config/docker-compose.yml up

# Apenas o dashboard
docker compose -f config/docker-compose.yml up agent-dashboard
```

## 🎯 Funcionalidades do Dashboard

### 1. 📊 Visão Geral
- Status geral do sistema
- Número de agentes ativos
- Métricas principais
- Cards visuais dos agentes

### 2. 🤖 Lista de Agentes
- Lista completa de todos os agentes
- Status de cada agente (ativo/inativo)
- Informações detalhadas
- Botões para interagir

### 3. 💬 Chat com Agentes
- Interface de chat moderna
- Seleção de agente via dropdown
- Histórico de conversas
- Respostas em tempo real
- Timestamps nas mensagens

### 4. 📈 Monitoramento
- Métricas de performance
- Estatísticas do sistema
- Logs em tempo real
- Gráficos de uso

### 5. ⚙️ Configurações
- Visualização de variáveis de ambiente
- Exportação de histórico de chat (JSON)
- Limpeza de dados
- Configurações do sistema

## 🎨 Interface

- **Design**: Moderno e profissional
- **Cores**: Gradiente azul/roxo
- **Layout**: Sidebar + Conteúdo principal
- **Responsivo**: Funciona em diferentes tamanhos de tela
- **Tema**: Escuro/Claro (conforme preferência do navegador)

## 📱 Agentes Disponíveis no Dashboard

1. 🎯 **Orchestrator** - Coordenador central
2. 💾 **DB Manager** - Gerenciamento de bancos de dados
3. 🔍 **Diagnostic Agent** - Diagnóstico de problemas
4. 💡 **Resolution Agent** - Geração de soluções
5. 🔌 **MCP Manager** - Gerenciamento de servidores MCP
6. 📦 **Git Integration** - Integração com Git
7. 🕸️ **Neo4j GraphRAG** - GraphRAG com Neo4j
8. 📝 **Obsidian Integration** - Integração com Obsidian
9. ⚙️ **Kestra Agent** - Integração com Kestra
10. 👑 **Master Agent** - Agente mestre
11. 🆘 **Helper System** - Sistema de ajuda

## 💡 Exemplo de Uso

1. **Inicie o dashboard:**
   ```bash
   python scripts/run_dashboard.py
   ```

2. **Acesse no navegador:**
   ```
   http://localhost:8508
   ```

3. **Navegue pelas seções:**
   - Use o menu lateral para escolher a seção
   - Clique em "Chat" para interagir com agentes
   - Selecione um agente no dropdown
   - Digite sua mensagem e veja a resposta

4. **Monitore o sistema:**
   - Vá para "Monitoramento"
   - Veja métricas em tempo real
   - Acompanhe logs do sistema

## 🔧 Configuração

### Porta Padrão
- **8508** (para não conflitar com outros serviços Streamlit)

### Variáveis de Ambiente
O dashboard usa as mesmas variáveis do projeto:
- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `OLLAMA_BASE_URL`
- `LLM`
- etc.

## 📚 Arquivos Criados

- `src/apps/agent_dashboard.py` - Dashboard principal
- `docker/agent_dashboard.Dockerfile` - Dockerfile para container
- `scripts/run_dashboard.py` - Script para executar
- `docs/DASHBOARD_AGENTES.md` - Documentação completa
- `docs/FERRAMENTAS_FRONTEND.md` - Este arquivo

## 🐛 Troubleshooting

### Erro: "Module not found"
```bash
pip install streamlit plotly pandas streamlit-option-menu
```

### Erro: "Port already in use"
```bash
# Use outra porta
streamlit run src/apps/agent_dashboard.py --server.port=8509
```

### Dashboard não carrega
1. Verifique se está no diretório correto
2. Verifique se os arquivos existem
3. Veja os logs no terminal

## 🎯 Próximos Passos

1. ✅ Instale as dependências
2. ✅ Execute o dashboard
3. ✅ Acesse http://localhost:8508
4. ✅ Explore as funcionalidades
5. ✅ Interaja com os agentes

---

**Criado em:** 2025-01-27

