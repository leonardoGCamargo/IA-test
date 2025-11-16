# 🌐 Usar MCP Browser no Cursor - Guia Completo

## 📋 O que é MCP Browser?

O Cursor tem suporte nativo para **MCP Browser Extension** que permite:
- ✅ Abrir URLs no navegador
- ✅ Navegar entre páginas
- ✅ Tirar screenshots
- ✅ Interagir com elementos (clicar, digitar)
- ✅ Capturar snapshots da página
- ✅ Executar JavaScript

## 🚀 Como Usar

### Método 1: Pedir ao Assistente (Mais Fácil)

Simplesmente peça ao assistente do Cursor:

```
"Abra http://localhost:8508 no navegador"
```

Ou:

```
"Navegue para http://localhost:8508 e me mostre como está a página"
```

Ou:

```
"Abra o dashboard em http://localhost:8508, tire um screenshot e me mostre"
```

### Método 2: Comandos Específicos

Você pode pedir comandos mais específicos:

```
"Navegue para http://localhost:8508, aguarde 5 segundos, tire um screenshot"
```

```
"Abra http://localhost:8508, clique no botão de chat, tire um screenshot"
```

```
"Navegue para http://localhost:8508, preencha o campo de busca com 'orchestrator', tire um screenshot"
```

## 🛠️ Ferramentas MCP Browser Disponíveis

O Cursor já tem estas ferramentas configuradas:

1. **browser_navigate** - Navegar para uma URL
2. **browser_snapshot** - Capturar snapshot da página (melhor que screenshot)
3. **browser_take_screenshot** - Tirar screenshot
4. **browser_click** - Clicar em elementos
5. **browser_type** - Digitar texto
6. **browser_select_option** - Selecionar opções em dropdowns
7. **browser_evaluate** - Executar JavaScript
8. **browser_wait_for** - Aguardar elementos ou tempo
9. **browser_console_messages** - Ver mensagens do console
10. **browser_network_requests** - Ver requisições de rede

## 📱 Exemplo Prático: Abrir Dashboard

### Passo 1: Iniciar o Dashboard

```bash
# Instalar dependências (se necessário)
pip install streamlit plotly pandas streamlit-option-menu

# Iniciar dashboard
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

### Passo 2: Pedir ao Assistente

Depois que o dashboard estiver rodando, peça:

```
"Abra http://localhost:8508 no navegador e me mostre a tela"
```

O assistente irá:
1. Navegar para a URL
2. Capturar um snapshot
3. Mostrar como está a página

### Passo 3: Interagir

Você pode pedir para interagir:

```
"Na página do dashboard, clique no botão de chat"
```

```
"Na página do dashboard, selecione o agente 'Orchestrator' no dropdown"
```

## 🎯 Casos de Uso

### 1. Verificar se Dashboard Está Funcionando

```
"Navegue para http://localhost:8508, aguarde 3 segundos, tire um screenshot e me mostre"
```

### 2. Testar Funcionalidade

```
"Abra http://localhost:8508, clique em 'Chat', digite 'Olá' no campo de mensagem, tire um screenshot"
```

### 3. Verificar Status

```
"Navegue para http://localhost:8508, vá para a seção 'Monitoramento', tire um screenshot"
```

### 4. Ver Logs do Console

```
"Abra http://localhost:8508, me mostre as mensagens do console do navegador"
```

## 🔧 Configuração (Opcional)

O MCP Browser já vem configurado no Cursor. Se precisar verificar:

1. Abra configurações do Cursor (`Ctrl+,`)
2. Procure por "MCP Servers"
3. Deve aparecer "cursor-browser-extension"

## 💡 Dicas

1. **Use "snapshot" em vez de "screenshot"** - É mais rápido e mostra melhor a estrutura
2. **Aguarde alguns segundos** após iniciar o dashboard antes de navegar
3. **Use descrições claras** ao pedir para clicar em elementos
4. **Peça screenshots** para ver como está a página

## 🐛 Troubleshooting

### "Connection refused"

O dashboard não está rodando. Inicie primeiro:
```bash
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508
```

### MCP Browser não funciona

1. Reinicie o Cursor
2. Verifique se está pedindo corretamente ao assistente
3. Use o método manual (abrir navegador diretamente)

### Não consegue ver a página

Peça ao assistente:
```
"Navegue para http://localhost:8508, aguarde 5 segundos, tire um snapshot completo da página"
```

## 📚 Exemplos de Comandos

### Básico
```
"Abra http://localhost:8508"
```

### Com Screenshot
```
"Abra http://localhost:8508 e tire um screenshot"
```

### Interagir
```
"Na página http://localhost:8508, clique no botão 'Chat'"
```

### Verificar Console
```
"Abra http://localhost:8508 e me mostre os erros do console"
```

### Ver Requisições
```
"Abra http://localhost:8508 e me mostre as requisições de rede"
```

## 🎯 Resumo

1. ✅ **MCP Browser já está no Cursor** - Não precisa instalar nada
2. ✅ **Peça ao assistente** - "Abra http://localhost:8508"
3. ✅ **Use comandos específicos** - Para interagir com a página
4. ✅ **Tire screenshots** - Para ver como está

---

**Pronto!** Agora você pode abrir e testar o dashboard diretamente no Cursor! 🎉

