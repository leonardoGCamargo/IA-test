# 🌐 Como Abrir o Dashboard no Cursor - Guia Completo

## 🛠️ Ferramentas Utilizadas

### 1. **Streamlit** ⭐ Principal
- Framework Python para interfaces web
- Versão: 1.51.0
- **Já instalado!** ✅

### 2. **Plotly** 📊
- Gráficos interativos
- Versão: 6.4.0
- **Já instalado!** ✅

### 3. **Pandas** 📈
- Manipulação de dados
- Versão: 2.3.3
- **Já instalado!** ✅

### 4. **Streamlit-Option-Menu** 🎨
- Menu lateral moderno
- Versão: 0.4.0
- **Já instalado!** ✅

## 🚀 Como Abrir o Dashboard

### Método 1: Via MCP Browser no Cursor (Recomendado) ⭐

O Cursor já tem suporte para MCP Browser! Basta pedir ao assistente:

```
"Abra http://localhost:8508 no navegador e me mostre a tela"
```

Ou:

```
"Inicie o dashboard em http://localhost:8508, aguarde 10 segundos, navegue para lá e tire um screenshot"
```

### Método 2: Iniciar Manualmente

**Passo 1: Iniciar o Dashboard**

```bash
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

**Aguarde a mensagem:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8508
```

**Passo 2: Abrir no Navegador**

**Opção A: Pedir ao Assistente**
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

### Método 3: Script Automático

```powershell
.\scripts\start_dashboard.ps1
```

## 🌐 MCP Browser no Cursor

### O que é?

O Cursor tem suporte nativo para **MCP Browser Extension** que permite:
- ✅ Abrir URLs no navegador
- ✅ Navegar entre páginas
- ✅ Tirar screenshots
- ✅ Capturar snapshots (melhor que screenshot)
- ✅ Clicar em elementos
- ✅ Digitar texto
- ✅ Ver console e requisições

### Como Usar

**Simplesmente peça ao assistente:**

1. **Abrir URL:**
   ```
   "Abra http://localhost:8508 no navegador"
   ```

2. **Ver a página:**
   ```
   "Navegue para http://localhost:8508 e me mostre como está"
   ```

3. **Tirar screenshot:**
   ```
   "Abra http://localhost:8508, aguarde 5 segundos, tire um screenshot e me mostre"
   ```

4. **Interagir:**
   ```
   "Na página http://localhost:8508, clique no botão de chat"
   ```

### Ferramentas Disponíveis

- `browser_navigate` - Navegar para URL
- `browser_snapshot` - Capturar snapshot (recomendado)
- `browser_take_screenshot` - Tirar screenshot
- `browser_click` - Clicar em elementos
- `browser_type` - Digitar texto
- `browser_wait_for` - Aguardar elementos/tempo
- `browser_console_messages` - Ver console
- `browser_network_requests` - Ver requisições

## 📱 URL do Dashboard

**http://localhost:8508**

## 🎯 Passo a Passo Completo

### 1. Instalar Dependências (Já feito! ✅)

```bash
pip install streamlit plotly pandas streamlit-option-menu
```

### 2. Iniciar Dashboard

```bash
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

### 3. Aguardar Inicialização

Aguarde ver a mensagem:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8508
```

### 4. Abrir no Navegador

**Peça ao assistente do Cursor:**
```
"Abra http://localhost:8508 no navegador e me mostre a tela"
```

## 💡 Exemplos de Comandos para o Assistente

### Básico
```
"Abra http://localhost:8508"
```

### Com Screenshot
```
"Abra http://localhost:8508, aguarde 5 segundos, tire um screenshot e me mostre"
```

### Ver Snapshot
```
"Navegue para http://localhost:8508 e me mostre um snapshot da página"
```

### Interagir
```
"Na página http://localhost:8508, clique no botão 'Chat' e tire um screenshot"
```

### Verificar Status
```
"Abra http://localhost:8508, vá para a seção 'Monitoramento', tire um screenshot"
```

## 🔧 Troubleshooting

### Dashboard não inicia

1. Verifique se Streamlit está instalado:
```bash
python -c "import streamlit; print(streamlit.__version__)"
```

2. Verifique se está no diretório correto:
```bash
cd IA-test
```

3. Verifique se o arquivo existe:
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

- `docs/MCP_BROWSER_CURSOR.md` - Guia completo do MCP Browser
- `docs/DASHBOARD_AGENTES.md` - Documentação do dashboard
- `docs/FERRAMENTAS_FRONTEND.md` - Lista de ferramentas

## 🎯 Resumo Rápido

1. ✅ **Dependências instaladas** (Streamlit, Plotly, Pandas)
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

**Pronto!** Agora você pode abrir e testar o dashboard diretamente no Cursor usando o MCP Browser! 🎉

