# 🔍 Análise de MCPs: Redundâncias e Limpeza

> **Data:** 2025-01-27  
> **Objetivo:** Identificar e remover MCPs desnecessários

---

## 📊 Status Atual

### MCPs no Sistema

O sistema gerencia MCPs através de:
- `mcp_servers.json` - Configuração local
- `.cursor/mcp.json` - Configuração do Cursor
- `src/agents/mcp_manager.py` - Gerenciador

---

## 🎯 MCPs Essenciais (MANTER)

### 1. **Neo4j MCP** ✅
**Status:** Essencial  
**Uso:** GraphRAG, conhecimento estruturado  
**Mantém:** ✅ SIM

### 2. **Obsidian MCP** ✅
**Status:** Essencial  
**Uso:** Gestão de notas  
**Mantém:** ✅ SIM

### 3. **Git MCP** ✅
**Status:** Essencial  
**Uso:** Integração Git/GitHub  
**Mantém:** ✅ SIM

---

## ⚠️ MCPs Opcionais (AVALIAR)

### 4. **Filesystem MCP** ⚠️
**Status:** Opcional  
**Uso:** Acesso ao sistema de arquivos  
**Recomendação:** Desabilitar se não usar  
**Ação:** Desabilitar ou remover

### 5. **Puppeteer MCP** ⚠️
**Status:** Opcional  
**Uso:** Automação de navegador  
**Recomendação:** Remover se não usar  
**Ação:** Remover

### 6. **Brave Search MCP** ⚠️
**Status:** Opcional  
**Uso:** Busca na web  
**Recomendação:** Remover se não usar  
**Ação:** Remover

### 7. **GitHub MCP** ⚠️
**Status:** Opcional (duplicado)  
**Uso:** Gerenciamento GitHub  
**Recomendação:** Já temos Git Integration Agent  
**Ação:** Remover (redundante)

---

## 🔴 MCPs Redundantes (REMOVER)

### Redundâncias Identificadas

1. **GitHub MCP** vs **Git Integration Agent**
   - ✅ Git Integration Agent já faz isso
   - ❌ Remover GitHub MCP

2. **Filesystem MCP** vs **Código Python**
   - ✅ Python já acessa filesystem diretamente
   - ❌ Remover Filesystem MCP (se não usar)

3. **Múltiplos MCPs de busca**
   - Se tiver vários (Brave, Google, etc.)
   - ❌ Manter apenas um ou remover todos

---

## 📋 Plano de Limpeza

### Fase 1: Análise
- [x] Identificar MCPs configurados
- [x] Verificar uso no código
- [x] Identificar redundâncias

### Fase 2: Limpeza
- [ ] Remover MCPs não usados
- [ ] Desabilitar MCPs opcionais
- [ ] Remover redundâncias

### Fase 3: Otimização
- [ ] Manter apenas MCPs essenciais
- [ ] Documentar MCPs mantidos
- [ ] Atualizar configurações

---

## 🛠️ Como Limpar

### Opção 1: Script Automático
```bash
# 1. Analisar
python scripts/analisar_mcps.py

# 2. Limpar
python scripts/limpar_mcps.py
```

### Opção 2: Manual
1. Abrir `mcp_servers.json`
2. Remover MCPs não usados
3. Desabilitar MCPs opcionais (`"enabled": false`)

---

## 📊 Resultado Esperado

### Antes
- 10+ MCPs configurados
- Muitos desabilitados
- Redundâncias

### Depois
- 3-5 MCPs essenciais
- Todos habilitados
- Sem redundâncias

---

## 🔗 Links Relacionados

- [[PROJETO-IA-TEST|Projeto Principal]]
- [[Agentes/MCP-Manager|MCP Manager]]
- [[RESUMO-O-QUE-FALTA|O que Falta]]

---

## 🏷️ Tags

#mcp #limpeza #redundancias #otimizacao

---

**Última atualização:** 2025-01-27

