# 🚀 Como Acessar o Dashboard de Agentes

## 📋 Resumo Rápido

**Ferramentas utilizadas:**
- ✅ Streamlit (framework principal)
- ✅ Plotly (gráficos)
- ✅ Pandas (dados)
- ✅ Streamlit-Option-Menu (menu)

**Porta:** 8508  
**URL:** http://localhost:8508

## 🎯 Método Rápido (Recomendado)

### 1. Instalar Dependências

```bash
pip install streamlit plotly pandas streamlit-option-menu
```

### 2. Executar Dashboard

```bash
python scripts/run_dashboard.py
```

### 3. Acessar no Navegador

Abra: **http://localhost:8508**

## 📱 Funcionalidades Disponíveis

### 📊 Visão Geral
- Status do sistema
- Métricas principais
- Cards dos agentes

### 🤖 Agentes
- Lista completa
- Status de cada agente
- Informações detalhadas

### 💬 Chat
- Interface de chat
- Seleção de agente
- Histórico de conversas
- Respostas em tempo real

### 📈 Monitoramento
- Métricas de performance
- Estatísticas
- Logs do sistema

### ⚙️ Configurações
- Variáveis de ambiente
- Exportação de dados
- Limpeza de histórico

## 🐳 Via Docker (Alternativa)

```bash
docker compose -f config/docker-compose.yml up agent-dashboard
```

Acesse: http://localhost:8508

## 💡 Dicas

1. **Primeira vez:** Execute `python scripts/run_dashboard.py`
2. **Navegação:** Use o menu lateral
3. **Chat:** Selecione um agente e digite sua mensagem
4. **Monitoramento:** Veja métricas em tempo real

## 🔧 Troubleshooting

**Erro de módulo não encontrado:**
```bash
pip install streamlit plotly pandas streamlit-option-menu
```

**Porta em uso:**
```bash
streamlit run src/apps/agent_dashboard.py --server.port=8509
```

---

**Pronto!** Agora você pode interagir com todos os seus agentes através de uma interface web moderna! 🎉

