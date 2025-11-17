# ⚠️ Aviso - MCP do Linear

## 🔍 Situação Atual

O MCP do Linear foi configurado em `.cursor/mcp.json`, mas **não está ativo ainda** no Cursor.

## ✅ Soluções

### Opção 1: Ativar o MCP do Linear (Recomendado)

1. **Reinicie o Cursor** completamente
2. O Cursor deve solicitar autorização para o MCP do Linear
3. **Autorize a conexão** quando solicitado
4. **Verifique** em Settings > MCP Servers se o Linear está ativo
5. Depois, peça no chat: "Crie todas as 47 issues do arquivo LINEAR_ISSUES.md no Linear"

### Opção 2: Usar Script Python (Funciona Agora)

O script Python funciona imediatamente, mas precisa da API key:

1. **Obtenha sua API Key:**
   - Acesse: https://linear.app/settings/api
   - Clique em "Create API Key"
   - Copie a chave

2. **Execute:**
   ```bash
   python scripts/setup_linear.py
   python scripts/send_issues_to_linear.py LINEAR_ISSUES.md
   ```

## 📋 Próximo Passo

**Recomendação:** Tente reiniciar o Cursor primeiro para ativar o MCP. Se não funcionar, use o script Python.

---

**Status:** Aguardando ativação do MCP ou configuração da API key.


