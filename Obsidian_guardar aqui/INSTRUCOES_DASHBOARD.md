# 🚀 Instruções Completas - Dashboard de Agentes

## 🛠️ Ferramentas Utilizadas

| Ferramenta | Versão | Uso |
|------------|--------|-----|
| **Streamlit** | 1.51.0 | Framework principal para interface web |
| **Plotly** | 6.4.0 | Gráficos interativos |
| **Pandas** | 2.3.3 | Manipulação de dados |
| **Streamlit-Option-Menu** | 0.4.0 | Menu lateral moderno |

**✅ Todas já estão instaladas!**

## 🌐 Como Abrir no Cursor

### Método 1: Via MCP Browser (Recomendado) ⭐

O Cursor tem suporte nativo para **MCP Browser Extension**. Basta pedir ao assistente:

```
"Abra http://localhost:8508 no navegador e me mostre a tela"
```

Ou:

```
"Inicie o dashboard em http://localhost:8508, aguarde 10 segundos, navegue para lá e tire um screenshot completo"
```

### Método 2: Passo a Passo Manual

**1. Iniciar o Dashboard:**

Abra um terminal e execute:

```bash
cd IA-test
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

**2. Aguardar Inicialização:**

Aguarde ver a mensagem:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8508
Network URL: http://192.168.x.x:8508
```

**3. Abrir no Navegador:**

**Opção A: Pedir ao Assistente do Cursor**
```
"Abra http://localhost:8508 no navegador"
```

**Opção B: Comando Windows**
```bash
start http://localhost:8508
```

**Opção C: PowerShell**
```powershell
Start-Process "http://localhost:8508"
```

**Opção D: Python**
```bash
python -c "import webbrowser; webbrowser.open('http://localhost:8508')"
```

## 📱 URL do Dashboard

**http://localhost:8508**

## 🎯 Funcionalidades do Dashboard

### 1. 📊 Visão Geral
- Status geral do sistema
- Métricas principais (agentes, tarefas)
- Cards visuais dos agentes
- Status de saúde do sistema

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

## 💡 Comandos para o Assistente do Cursor

### Abrir Dashboard
```
"Abra http://localhost:8508 no navegador"
```

### Ver a Página
```
"Navegue para http://localhost:8508 e me mostre um snapshot da página"
```

### Tirar Screenshot
```
"Abra http://localhost:8508, aguarde 5 segundos, tire um screenshot e me mostre"
```

### Interagir
```
"Na página http://localhost:8508, clique no botão 'Chat'"
```

### Verificar Status
```
"Abra http://localhost:8508, vá para a seção 'Monitoramento', tire um screenshot"
```

## 🔧 Troubleshooting

### Dashboard não inicia

1. **Verifique se Streamlit está instalado:**
   ```bash
   python -c "import streamlit; print(streamlit.__version__)"
   ```

2. **Instale se necessário:**
   ```bash
   pip install streamlit plotly pandas streamlit-option-menu
   ```

3. **Verifique se está no diretório correto:**
   ```bash
   cd IA-test
   ```

4. **Verifique se o arquivo existe:**
   ```bash
   Test-Path src/apps/agent_dashboard.py
   ```

### Porta em uso

Use outra porta:
```bash
python -m streamlit run src/apps/agent_dashboard.py --server.port=8509
```

### MCP Browser não funciona

1. Reinicie o Cursor
2. Peça novamente ao assistente
3. Use método manual (abrir navegador diretamente)

## 📚 Documentação

- `COMO_ABRIR_DASHBOARD.md` - Guia completo
- `docs/MCP_BROWSER_CURSOR.md` - MCP Browser no Cursor
- `docs/DASHBOARD_AGENTES.md` - Funcionalidades detalhadas
- `docs/FERRAMENTAS_FRONTEND.md` - Lista de ferramentas

## 🎯 Resumo Rápido

1. ✅ **Ferramentas instaladas** (Streamlit, Plotly, Pandas)
2. ✅ **MCP Browser disponível** no Cursor
3. ⏳ **Inicie o dashboard:**
   ```bash
   python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
   ```
4. 🌐 **Peça ao assistente:**
   ```
   "Abra http://localhost:8508 no navegador e me mostre a tela"
   ```

---

**Pronto!** Agora você pode abrir e testar o dashboard diretamente no Cursor! 🎉

