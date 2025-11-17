# 📋 Instruções para Criar Issues no Linear via MCP

## ✅ Secrets Removidos

Os secrets foram removidos dos scripts e commitados:
- ✅ `scripts/update_configs_simple.py` - Removido Google API Key e MongoDB URI
- ✅ `scripts/apply_configs.py` - Removido secrets
- ✅ `scripts/update_all_configs.py` - Removido secrets
- ✅ `scripts/adicionar_suporte_gemini.py` - Removido Google API Key
- ✅ `config/env.example` - Usando placeholders

## 🚀 Criar Issues no Linear

Como o MCP do Linear está ativo no Cursor, você pode criar as issues diretamente no chat do Cursor:

### No Chat do Cursor, digite:

```
Crie todas as 47 issues do arquivo LINEAR_ISSUES.md no Linear usando o MCP do Linear.

Para cada issue:
1. Use o título completo (ex: "L-001: Observabilidade Incompleta")
2. Mapeie prioridades: P0 → urgent, P1 → high, P2 → medium
3. Inclua toda a descrição, arquivos e acceptance criteria
4. Adicione as labels apropriadas
5. Configure a estimativa em dias quando disponível
```

## 📊 Issues a Criar

- **P0 (urgent):** 8 issues - L-001 a L-008
- **P1 (high):** 15 issues - L-009 a L-023
- **P2 (medium):** 24 issues - L-024 a L-047

**Total:** 47 issues

## 📁 Arquivos

- `LINEAR_ISSUES.md` - 23 issues detalhadas (L-001 a L-023)
- `LINEAR_ISSUES_COMPLETE.md` - Todas as 47 issues

---

**Após criar as issues, posso remover os scripts Python desnecessários!**

