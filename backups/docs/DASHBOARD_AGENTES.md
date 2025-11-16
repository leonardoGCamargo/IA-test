# 🤖 Dashboard de Agentes - Guia de Uso

## 📋 Visão Geral

O Dashboard de Agentes é uma interface web moderna para interagir com todos os agentes do sistema IA-Test.

## 🛠️ Ferramentas Utilizadas

### 1. **Streamlit** ⭐ Principal
- Framework Python para criar interfaces web rapidamente
- Integração nativa com agentes Python
- Interface moderna e responsiva

### 2. **Plotly** 📊
- Gráficos interativos
- Visualização de métricas
- Gráficos de performance

### 3. **Pandas** 📈
- Manipulação de dados
- Processamento de métricas
- Estatísticas dos agentes

### 4. **Streamlit-Option-Menu** 🎨
- Menu lateral moderno
- Navegação intuitiva
- Interface profissional

## 🚀 Como Acessar

### Opção 1: Executar Diretamente (Recomendado)

```bash
# Instalar dependências (se ainda não instalou)
pip install streamlit plotly pandas streamlit-option-menu

# Executar dashboard
python scripts/run_dashboard.py

# Ou diretamente
streamlit run src/apps/agent_dashboard.py --server.port=8508
```

**Acesse:** http://localhost:8508

### Opção 2: Via Docker

```bash
# Build e executar
docker compose -f config/docker-compose.yml up agent-dashboard

# Ou apenas o dashboard
docker compose -f config/docker-compose.optimized.yml up agent-dashboard
```

**Acesse:** http://localhost:8508

## 📱 Funcionalidades

### 1. 📊 Visão Geral
- Status geral do sistema
- Número de agentes ativos
- Métricas principais
- Cards de agentes

### 2. 🤖 Lista de Agentes
- Lista completa de todos os agentes
- Status de cada agente
- Informações detalhadas
- Botões para interagir

### 3. 💬 Chat com Agentes
- Interface de chat moderna
- Seleção de agente
- Histórico de conversas
- Respostas em tempo real

### 4. 📈 Monitoramento
- Métricas de performance
- Estatísticas do sistema
- Logs em tempo real
- Gráficos de uso

### 5. ⚙️ Configurações
- Variáveis de ambiente
- Exportação de dados
- Limpeza de histórico
- Configurações do sistema

## 🎯 Agentes Disponíveis

1. **Orchestrator** 🎯 - Coordenador central
2. **DB Manager** 💾 - Gerenciamento de bancos de dados
3. **Diagnostic Agent** 🔍 - Diagnóstico de problemas
4. **Resolution Agent** 💡 - Geração de soluções
5. **MCP Manager** 🔌 - Gerenciamento de servidores MCP
6. **Git Integration** 📦 - Integração com Git
7. **Neo4j GraphRAG** 🕸️ - GraphRAG com Neo4j
8. **Obsidian Integration** 📝 - Integração com Obsidian
9. **Kestra Agent** ⚙️ - Integração com Kestra
10. **Master Agent** 👑 - Agente mestre
11. **Helper System** 🆘 - Sistema de ajuda

## 💡 Como Usar

### 1. Iniciar o Dashboard

```bash
python scripts/run_dashboard.py
```

### 2. Acessar no Navegador

Abra: http://localhost:8508

### 3. Navegar pelas Seções

Use o menu lateral para navegar:
- **Visão Geral**: Status geral do sistema
- **Agentes**: Lista completa de agentes
- **Chat**: Interagir com agentes
- **Monitoramento**: Métricas e logs
- **Configurações**: Ajustes do sistema

### 4. Interagir com Agentes

1. Vá para a seção **Chat**
2. Selecione um agente no dropdown
3. Digite sua mensagem
4. Veja a resposta em tempo real

### 5. Monitorar Sistema

1. Vá para **Monitoramento**
2. Veja métricas em tempo real
3. Acompanhe logs do sistema
4. Verifique status dos agentes

## 🎨 Interface

- **Tema**: Moderno e profissional
- **Layout**: Sidebar + Main content
- **Cores**: Azul e roxo (gradiente)
- **Responsivo**: Funciona em diferentes tamanhos

## 🔧 Configuração

### Variáveis de Ambiente

O dashboard usa as mesmas variáveis do projeto:
- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `OLLAMA_BASE_URL`
- `LLM`
- etc.

### Porta

Por padrão, o dashboard roda na porta **8508**.

Para mudar:
```bash
streamlit run src/apps/agent_dashboard.py --server.port=PORTA
```

## 🐛 Troubleshooting

### Dashboard não inicia

1. Verifique se as dependências estão instaladas:
```bash
pip install streamlit plotly pandas streamlit-option-menu
```

2. Verifique se está no diretório correto:
```bash
cd IA-test
```

3. Verifique os logs de erro no terminal

### Agentes não respondem

1. Verifique se o Orchestrator está configurado
2. Verifique as variáveis de ambiente
3. Veja os logs no terminal

### Erro de importação

1. Certifique-se de estar no diretório raiz do projeto
2. Verifique se `src/agents/orchestrator.py` existe
3. Execute: `python -c "from src.agents.orchestrator import get_orchestrator"`

## 📚 Recursos

- [Documentação Streamlit](https://docs.streamlit.io)
- [Documentação Plotly](https://plotly.com/python/)
- [Guia do Projeto](README.md)

## 🎯 Próximos Passos

1. ✅ Execute o dashboard
2. ✅ Explore as funcionalidades
3. ✅ Interaja com os agentes
4. ✅ Monitore o sistema
5. ✅ Personalize conforme necessário

---

**Última atualização:** 2025-01-27

