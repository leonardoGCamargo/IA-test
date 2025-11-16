# 🌐 Como Abrir o Dashboard no Cursor

## 🚀 Método Rápido

### 1. Iniciar o Dashboard

```bash
# Execute este comando
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

### 2. Abrir no Navegador

**Opção A: Via Script Python**
```bash
python -c "import webbrowser; webbrowser.open('http://localhost:8508')"
```

**Opção B: Via Comando Windows**
```bash
start http://localhost:8508
```

**Opção C: Pedir ao Assistente do Cursor**
```
"Abra http://localhost:8508 no navegador"
```

## 🔧 Usando MCP Browser no Cursor

O Cursor tem suporte para MCP Browser. Você pode:

1. **Pedir ao assistente:**
   ```
   "Navegue para http://localhost:8508 e me mostre a tela"
   ```

2. **Ou:**
   ```
   "Abra o dashboard em http://localhost:8508"
   ```

## 📱 Ferramentas MCP Browser Disponíveis

O Cursor já tem estas ferramentas disponíveis:

- ✅ `browser_navigate` - Navegar para URL
- ✅ `browser_snapshot` - Capturar snapshot da página
- ✅ `browser_take_screenshot` - Tirar screenshot
- ✅ `browser_click` - Clicar em elementos
- ✅ `browser_type` - Digitar texto
- ✅ `browser_evaluate` - Executar JavaScript

## 💡 Exemplo de Uso

Depois que o dashboard estiver rodando, peça ao assistente:

```
"Navegue para http://localhost:8508, tire um screenshot e me mostre como está"
```

Ou:

```
"Abra http://localhost:8508, clique no botão de chat e tire um screenshot"
```

## 🎯 Passos Completos

1. **Inicie o dashboard:**
   ```bash
   python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
   ```

2. **Aguarde alguns segundos** para o dashboard iniciar

3. **Peça ao assistente:**
   ```
   "Abra http://localhost:8508 no navegador"
   ```

4. **Ou abra manualmente:**
   - Pressione `Windows + R`
   - Digite: `http://localhost:8508`
   - Pressione Enter

## 🐛 Se Não Funcionar

1. **Verifique se o dashboard está rodando:**
   ```bash
   # Windows
   netstat -ano | findstr :8508
   ```

2. **Se não estiver, inicie:**
   ```bash
   python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
   ```

3. **Aguarde a mensagem:**
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8508
   ```

4. **Então abra no navegador**

## 📚 Mais Informações

- `docs/BROWSER_MCP_SETUP.md` - Configuração completa do MCP Browser
- `docs/DASHBOARD_AGENTES.md` - Documentação do dashboard
- `COMO_ACESSAR_DASHBOARD.md` - Guia rápido

---

**URL do Dashboard:** http://localhost:8508

