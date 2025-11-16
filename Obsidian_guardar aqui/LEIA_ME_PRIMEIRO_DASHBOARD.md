# 🚀 Dashboard de Agentes - Leia-me Primeiro!

## 🛠️ Ferramentas Utilizadas

✅ **Streamlit** (1.51.0) - Framework principal  
✅ **Plotly** (6.4.0) - Gráficos interativos  
✅ **Pandas** (2.3.3) - Manipulação de dados  
✅ **Streamlit-Option-Menu** (0.4.0) - Menu lateral  

**Todas já estão instaladas!** ✅

## 🌐 Como Abrir no Cursor

### ⭐ Método Recomendado: Via MCP Browser

O Cursor tem suporte nativo para **MCP Browser Extension**! Basta pedir ao assistente:

```
"Abra http://localhost:8508 no navegador e me mostre a tela"
```

Ou:

```
"Inicie o dashboard em http://localhost:8508, aguarde 10 segundos, navegue para lá e tire um screenshot completo"
```

### 📝 Passo a Passo

**1. Iniciar o Dashboard:**

Abra um terminal no Cursor e execute:

```bash
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

**2. Aguardar a mensagem:**

```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8508
```

**3. Pedir ao Assistente do Cursor:**

```
"Abra http://localhost:8508 no navegador e me mostre como está"
```

## 📱 URL do Dashboard

**http://localhost:8508**

## 🎯 Funcionalidades

1. **📊 Visão Geral** - Status do sistema e métricas
2. **🤖 Agentes** - Lista completa de agentes
3. **💬 Chat** - Interface de chat com agentes
4. **📈 Monitoramento** - Métricas e logs
5. **⚙️ Configurações** - Ajustes do sistema

## 💡 Comandos para o Assistente

### Abrir Dashboard
```
"Abra http://localhost:8508 no navegador"
```

### Ver a Página
```
"Navegue para http://localhost:8508 e me mostre um snapshot"
```

### Tirar Screenshot
```
"Abra http://localhost:8508, aguarde 5 segundos, tire um screenshot"
```

### Interagir
```
"Na página http://localhost:8508, clique no botão 'Chat'"
```

## 🔧 Se Não Funcionar

1. **Verifique se Streamlit está instalado:**
   ```bash
   python -c "import streamlit; print('OK')"
   ```

2. **Instale se necessário:**
   ```bash
   pip install streamlit plotly pandas streamlit-option-menu
   ```

3. **Verifique se está no diretório correto:**
   ```bash
   cd IA-test
   ```

4. **Inicie o dashboard:**
   ```bash
   python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
   ```

5. **Peça ao assistente:**
   ```
   "Abra http://localhost:8508 no navegador"
   ```

## 📚 Mais Informações

- `INSTRUCOES_DASHBOARD.md` - Instruções completas
- `docs/MCP_BROWSER_CURSOR.md` - Guia do MCP Browser
- `docs/DASHBOARD_AGENTES.md` - Funcionalidades detalhadas

---

**Pronto!** Use o MCP Browser do Cursor para abrir e testar o dashboard! 🎉

