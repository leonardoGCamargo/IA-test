# 🌐 Configurar MCP Browser no Cursor

## 📋 MCPs de Navegador Disponíveis

O Cursor tem suporte para MCPs de navegador que permitem abrir URLs diretamente. Existem duas opções principais:

### 1. **cursor-browser-extension** (Recomendado)
- MCP nativo do Cursor
- Permite navegar, clicar, preencher formulários
- Ideal para testes automatizados

### 2. **MCP Browser** (Alternativa)
- MCP genérico de navegador
- Funcionalidades similares

## 🚀 Configuração Rápida

### Opção 1: Usar Script Python (Mais Simples)

```bash
# Abre o dashboard automaticamente
python scripts/open_dashboard.py

# Ou apenas abre (se já estiver rodando)
python scripts/open_dashboard.py open
```

### Opção 2: Configurar MCP Browser no Cursor

1. **Abra as configurações do Cursor**
   - `Ctrl+,` ou `Cmd+,`
   - Procure por "MCP Servers"

2. **Adicione o Browser MCP:**

```json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-puppeteer"
      ]
    }
  }
}
```

3. **Ou use o cursor-browser-extension:**

O Cursor já vem com suporte para browser extension. Você pode pedir ao assistente:

```
"Abra http://localhost:8508 no navegador"
```

## 🎯 Como Usar

### Via Assistente do Cursor

Simplesmente peça:
```
"Abra o dashboard em http://localhost:8508"
```

Ou:
```
"Navegue para http://localhost:8508 e me mostre a tela"
```

### Via Script

```bash
# Inicia e abre automaticamente
python scripts/open_dashboard.py
```

### Via Comando Manual

```bash
# Windows
start http://localhost:8508

# Linux
xdg-open http://localhost:8508

# Mac
open http://localhost:8508
```

## 🔧 Ferramentas MCP Browser Disponíveis

### cursor-browser-extension

1. **browser_navigate** - Navegar para URL
2. **browser_snapshot** - Capturar snapshot da página
3. **browser_click** - Clicar em elementos
4. **browser_type** - Digitar texto
5. **browser_take_screenshot** - Tirar screenshot
6. **browser_evaluate** - Executar JavaScript

### Exemplo de Uso

Você pode pedir ao assistente:
```
"Navegue para http://localhost:8508, tire um screenshot e me mostre"
```

Ou:
```
"Abra http://localhost:8508, clique no botão de chat e tire um screenshot"
```

## 📱 Abrir Dashboard Automaticamente

### Script Automático

O script `scripts/open_dashboard.py` faz tudo automaticamente:

1. Verifica se o dashboard está rodando
2. Se não estiver, inicia o dashboard
3. Aguarda alguns segundos
4. Abre no navegador automaticamente

```bash
python scripts/open_dashboard.py
```

## 🐛 Troubleshooting

### Dashboard não abre

1. Verifique se está rodando:
```bash
# Windows
netstat -ano | findstr :8508

# Linux/Mac
lsof -i :8508
```

2. Inicie manualmente:
```bash
streamlit run src/apps/agent_dashboard.py --server.port=8508
```

3. Abra manualmente:
```
http://localhost:8508
```

### MCP Browser não funciona

1. Verifique se o MCP está configurado
2. Reinicie o Cursor
3. Use o script Python como alternativa

## 💡 Dicas

1. **Use o script:** `python scripts/open_dashboard.py` é a forma mais fácil
2. **Peça ao assistente:** "Abra http://localhost:8508"
3. **Atalho:** Crie um atalho no desktop apontando para `http://localhost:8508`

## 🎯 Próximos Passos

1. ✅ Execute: `python scripts/open_dashboard.py`
2. ✅ Ou peça ao assistente: "Abra http://localhost:8508"
3. ✅ Explore o dashboard
4. ✅ Teste as funcionalidades

---

**Última atualização:** 2025-01-27

