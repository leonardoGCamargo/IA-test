# 🛠️ Ferramentas do Front-End - Dashboard de Agentes

## 📋 Ferramentas Escolhidas

### 1. **Streamlit** ⭐ Principal
- **Por quê**: Já está no projeto, fácil integração com Python, interface rápida
- **Uso**: Framework principal para o dashboard
- **Versão**: >= 1.28.0

### 2. **Plotly** 📊
- **Por quê**: Gráficos interativos e modernos
- **Uso**: Visualização de métricas, status dos agentes, gráficos de performance
- **Versão**: >= 5.17.0

### 3. **Pandas** 📈
- **Por quê**: Manipulação de dados dos agentes
- **Uso**: Processar métricas, histórico de tarefas, estatísticas
- **Versão**: >= 2.0.0

### 4. **Requests** 🌐
- **Por quê**: Comunicação com APIs dos agentes (se necessário)
- **Uso**: Chamadas HTTP para endpoints dos agentes
- **Versão**: >= 2.31.0

### 5. **Streamlit-Authenticator** 🔐 (Opcional)
- **Por quê**: Autenticação simples se necessário
- **Uso**: Proteger acesso ao dashboard
- **Versão**: >= 0.2.3

### 6. **Streamlit-Option-Menu** 🎨
- **Por quê**: Menu lateral moderno
- **Uso**: Navegação entre seções do dashboard
- **Versão**: >= 0.3.6

## 🎯 Funcionalidades do Dashboard

### 1. **Visão Geral**
- Status geral do sistema
- Número de agentes ativos
- Métricas principais
- Gráficos de performance

### 2. **Lista de Agentes**
- Cards com status de cada agente
- Informações detalhadas
- Botões de ação (iniciar/parar)
- Logs em tempo real

### 3. **Interface de Chat**
- Chat para interagir com agentes
- Histórico de conversas
- Seleção de agente
- Respostas em tempo real

### 4. **Monitoramento**
- Métricas de performance
- Gráficos de uso
- Histórico de tarefas
- Alertas e notificações

### 5. **Configurações**
- Configuração de agentes
- Variáveis de ambiente
- Logs do sistema
- Exportação de dados

## 📦 Instalação

```bash
pip install streamlit plotly pandas requests streamlit-option-menu
```

## 🚀 Execução

```bash
streamlit run src/apps/agent_dashboard.py
```

Acesse: http://localhost:8501

## 🎨 Design

- **Tema**: Dark/Light mode
- **Layout**: Sidebar + Main content
- **Cores**: Modernas e profissionais
- **Responsivo**: Funciona em diferentes tamanhos de tela

