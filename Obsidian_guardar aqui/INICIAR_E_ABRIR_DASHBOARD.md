# 🚀 Iniciar e Abrir Dashboard - Passo a Passo

## 📋 Ferramentas Utilizadas

✅ **Streamlit** - Framework principal  
✅ **Plotly** - Gráficos  
✅ **Pandas** - Dados  
✅ **Streamlit-Option-Menu** - Menu  

## 🎯 Passo a Passo Rápido

### 1. Instalar Dependências (Primeira Vez)

```bash
pip install streamlit plotly pandas streamlit-option-menu requests
```

### 2. Iniciar o Dashboard

```bash
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

**Aguarde a mensagem:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8508
```

### 3. Abrir no Navegador

**Opção A: Via Assistente do Cursor (Recomendado)**
```
Peça ao assistente: "Abra http://localhost:8508 no navegador"
```

**Opção B: Manual**
- Pressione `Windows + R`
- Digite: `http://localhost:8508`
- Pressione Enter

**Opção C: Script Python**
```bash
python -c "import webbrowser; webbrowser.open('http://localhost:8508')"
```

**Opção D: PowerShell**
```powershell
start http://localhost:8508
```

## 🌐 Usar MCP Browser no Cursor

O Cursor tem suporte nativo para abrir URLs. Basta pedir:

```
"Abra http://localhost:8508 no navegador e me mostre a tela"
```

Ou:

```
"Navegue para http://localhost:8508, tire um screenshot e me mostre"
```

## 📱 URL do Dashboard

**http://localhost:8508**

## 💡 Dica Rápida

Execute estes comandos em sequência:

```bash
# 1. Instalar (se necessário)
pip install streamlit plotly pandas streamlit-option-menu

# 2. Iniciar
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508

# 3. Em outro terminal, abrir
start http://localhost:8508
```

Ou peça ao assistente do Cursor:
```
"Inicie o dashboard em http://localhost:8508 e abra no navegador"
```

---

**Pronto!** 🎉

