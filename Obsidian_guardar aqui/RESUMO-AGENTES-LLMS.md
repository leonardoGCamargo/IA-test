# 📊 Resumo: Agentes e LLMs

> **Data:** 2025-01-27  
> **Resumo rápido**

---

## 🤖 AGENTES ATIVOS (14)

### Com LLM (3 agentes)
1. ✅ **Orchestrator** - Planejamento inteligente
2. ✅ **Neo4j GraphRAG** - Consultas GraphRAG
3. ⚠️ **Agent Helper System** - Otimização (deprecated)

### Sem LLM (11 agentes)
4. System Health Agent
5. DB Manager
6. MCP Manager
7. Git Integration
8. Obsidian Integration
9. Kestra Agent
10. Docker Integration
11. Streamlit Dashboard
12. MCP Manager UI
13-14. Diagnostic/Resolution (deprecated)

---

## 🔧 LLM ATUAL

### Configuração
- **LLM:** `llama2` (Ollama)
- **Embedding:** `sentence_transformer`
- **GOOGLE_API_KEY:** Configurada, mas só para embeddings

### Status
- ✅ **Ollama** - Funcionando (padrão)
- ❌ **Gemini** - NÃO suportado como LLM (só embeddings)
- ⚠️ **OpenAI** - Suportado, mas não configurado
- ⚠️ **AWS** - Suportado, mas não configurado

---

## 🎯 PARA USAR GEMINI

1. Executar: `python scripts/adicionar_suporte_gemini.py`
2. Configurar `.env`:
   ```bash
   LLM=gemini-pro
   GOOGLE_API_KEY=AIzaSyD7lSqUzy-xvlP3sQHf0IaqAnemtgOqoeM
   ```
3. Agentes automaticamente usarão Gemini

---

**Última atualização:** 2025-01-27

