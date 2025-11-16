# 🌐 Guia de Acesso ao Dashboard - Resumo Rápido

## 🛠️ Ferramentas Utilizadas

✅ **Streamlit** - Framework principal  
✅ **Plotly** - Gráficos interativos  
✅ **Pandas** - Manipulação de dados  
✅ **Streamlit-Option-Menu** - Menu lateral  

## 🚀 Como Abrir o Dashboard

### Método 1: Script PowerShell (Mais Fácil) ⭐

```powershell
.\scripts\start_dashboard.ps1
```

Este script:
- ✅ Verifica se Streamlit está instalado
- ✅ Inicia o dashboard
- ✅ Aguarda alguns segundos
- ✅ Abre automaticamente no navegador

### Método 2: Manual

```bash
# 1. Iniciar dashboard
python -m streamlit run src/apps/agent_dashboard.py --server.port=8508

# 2. Aguardar mensagem: "You can now view your Streamlit app"

# 3. Abrir no navegador
start http://localhost:8508
```

### Método 3: Via MCP Browser no Cursor

**Peça ao assistente:**
```
"Abra http://localhost:8508 no navegador"
```

Ou:
```
"Navegue para http://localhost:8508 e me mostre a tela"
```

## 📱 URL do Dashboard

**http://localhost:8508**

## 🎯 Funcionalidades

1. **📊 Visão Geral** - Status do sistema e métricas
2. **🤖 Agentes** - Lista completa de agentes
3. **💬 Chat** - Interface de chat com agentes
4. **📈 Monitoramento** - Métricas e logs
5. **⚙️ Configurações** - Ajustes do sistema

## 🔧 Se Não Funcionar

1. **Instale dependências:**
   ```bash
   pip install streamlit plotly pandas streamlit-option-menu
   ```

2. **Verifique se está no diretório correto:**
   ```bash
   cd IA-test
   ```

3. **Verifique se a porta está livre:**
   ```bash
   netstat -ano | findstr :8508
   ```

4. **Use outra porta se necessário:**
   ```bash
   streamlit run src/apps/agent_dashboard.py --server.port=8509
   ```

## 💡 Dica Rápida

**Execute este comando:**
```powershell
.\scripts\start_dashboard.ps1
```

Isso fará tudo automaticamente! 🎉

---

**Pronto!** O dashboard estará disponível em http://localhost:8508

