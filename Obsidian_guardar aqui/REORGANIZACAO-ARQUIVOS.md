# 📁 Plano de Reorganização de Arquivos

> **Data:** 2025-01-27  
> **Status:** ⚠️ Ações recomendadas

---

## 🔍 Problemas Identificados

### 1. Arquivos Duplicados (Raiz vs src/apps/)

**Arquivos encontrados em ambos os locais:**
- `api.py` - Raiz e `src/apps/api.py`
- `bot.py` - Raiz e `src/apps/bot.py`
- `chains.py` - Raiz e `src/apps/chains.py`
- `loader.py` - Raiz e `src/apps/loader.py`
- `pdf_bot.py` - Raiz e `src/apps/pdf_bot.py`

**Recomendação:**
- ✅ **Manter em `src/apps/`** (estrutura correta)
- ❌ **Remover da raiz** (após verificar se são idênticos)

---

### 2. Estrutura Duplicada

**Problema:**
- Pasta `IA-test/IA-test/` dentro do projeto
- Pode ser duplicação desnecessária

**Ação:**
- Verificar conteúdo da pasta interna
- Se for duplicação, mover conteúdo para local correto e remover

---

### 3. Pasta Obsidian Duplicada

**Problema:**
- `Obsidian_guardar aqui/Obsidian_guardar aqui/`
- Pasta Obsidian dentro de Obsidian

**Ação:**
- Verificar conteúdo
- Mover arquivos para local correto se necessário
- Remover pasta duplicada

---

## ✅ Estrutura Correta

```
IA-test/
├── src/
│   ├── apps/          ← Arquivos Python aqui
│   │   ├── api.py
│   │   ├── bot.py
│   │   ├── chains.py
│   │   ├── loader.py
│   │   └── pdf_bot.py
│   └── agents/        ← Agentes aqui
├── Obsidian_guardar aqui/  ← Documentação aqui
├── scripts/          ← Scripts aqui
├── docs/             ← Documentação técnica
└── config/           ← Configurações
```

---

## 🎯 Plano de Ação

### Fase 1: Verificação
1. ✅ Comparar arquivos duplicados (raiz vs src/apps/)
2. ✅ Verificar conteúdo de `IA-test/IA-test/`
3. ✅ Verificar conteúdo de `Obsidian_guardar aqui/Obsidian_guardar aqui/`

### Fase 2: Decisão
- Se arquivos em `src/apps/` são mais recentes/completos → Remover da raiz
- Se arquivos na raiz são mais recentes → Mover para `src/apps/` e remover da raiz
- Se são idênticos → Manter em `src/apps/` e remover da raiz

### Fase 3: Limpeza
- Remover duplicatas da raiz
- Reorganizar estrutura `IA-test/IA-test/`
- Limpar pasta Obsidian duplicada

---

## ⚠️ Cuidados

1. **Backup antes de remover**
   - Fazer backup dos arquivos antes de remover
   - Verificar imports e referências

2. **Verificar dependências**
   - Verificar se algum código importa da raiz
   - Atualizar imports se necessário

3. **Testar após reorganização**
   - Executar testes
   - Verificar se tudo funciona

---

## 📊 Status Atual

| Item | Status | Ação Necessária |
|------|--------|-----------------|
| Arquivos duplicados | ⚠️ Encontrados | Verificar e remover |
| Estrutura IA-test/IA-test/ | ⚠️ Existe | Verificar conteúdo |
| Pasta Obsidian duplicada | ⚠️ Existe | Verificar e limpar |

---

## 🚀 Próximos Passos

1. Executar script de análise: `python scripts/reorganizar_arquivos.py`
2. Revisar resultados
3. Fazer backup
4. Executar limpeza (se aprovado)

---

**Última atualização:** 2025-01-27

