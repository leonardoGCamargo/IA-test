# ✅ MCP do Linear - Configuração Corrigida

## 🔧 Correção Aplicada

O arquivo `.cursor/mcp.json` foi corrigido. A configuração do Linear agora usa:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-remote",
        "https://mcp.linear.app/sse"
      ]
    }
  }
}
```

## 🔄 Mudança Realizada

**Antes (quebrado):**
```json
"mcp-remote"
```

**Depois (corrigido):**
```json
"@modelcontextprotocol/server-remote"
```

## 📋 Próximos Passos

1. **Reinicie o Cursor** completamente para carregar a nova configuração
2. **Autorize a conexão** quando o Cursor solicitar
3. **Verifique** em Settings > MCP Servers se o Linear está ativo
4. **Teste** criando uma issue no chat do Cursor

## ✅ Validação

O arquivo JSON foi validado e está correto. Após reiniciar o Cursor, o MCP do Linear deve funcionar corretamente.

---

**Status:** Configuração corrigida e pronta para uso! 🎉

