# 🤖 Agentes do Sistema e Configuração de LLMs

> **Data:** 2025-01-27  
> **Status:** Sistema otimizado com 14 agentes

---

## 📋 AGENTES ATIVOS (14)

### 1. **Orchestrator** ✅
**Arquivo:** `src/agents/orchestrator.py`  
**LLM:** ✅ **SIM** - Usa LLM para planejamento inteligente  
**Configuração:**
- Lê `LLM` do `.env` (padrão: `llama2`)
- Suporta: Ollama, OpenAI, AWS Bedrock
- **NÃO usa Gemini** (não implementado no `load_llm()`)

**Uso do LLM:**
- Planejamento inteligente de tarefas
- Criação de planos em linguagem natural
- Execução de objetivos complexos

---

### 2. **System Health Agent** ✅
**Arquivo:** `src/agents/system_health_agent.py`  
**LLM:** ❌ **NÃO** - Não usa LLM diretamente  
**Funcionalidades:**
- Diagnóstico de problemas
- Monitoramento de agentes
- Geração de resoluções (sem LLM)

---

### 3. **DB Manager** ✅
**Arquivo:** `src/agents/db_manager.py`  
**LLM:** ❌ **NÃO** - Apenas gerenciamento de bancos  
**Funcionalidades:**
- Conexão com bancos (Neo4j, Neon, MongoDB, Supabase)
- Execução de queries
- Gerenciamento de configurações

---

### 4. **MCP Manager** ✅
**Arquivo:** `src/agents/mcp_manager.py`  
**LLM:** ❌ **NÃO** - Apenas gerenciamento de servidores MCP  
**Funcionalidades:**
- Gerenciamento de servidores MCP
- Health checks
- Listagem de recursos

---

### 5. **Git Integration** ✅
**Arquivo:** `src/agents/git_integration.py`  
**LLM:** ❌ **NÃO** - Apenas operações Git  
**Funcionalidades:**
- Operações Git/GitHub
- Commits, branches, PRs

---

### 6. **Neo4j GraphRAG** ✅
**Arquivo:** `src/agents/mcp_neo4j_integration.py`  
**LLM:** ✅ **SIM** - Usa LLM para GraphRAG  
**Configuração:**
- Lê `LLM` do `.env` (padrão: `llama2`)
- Suporta: Ollama, OpenAI, AWS Bedrock
- **NÃO usa Gemini** (não implementado)

**Uso do LLM:**
- Consultas GraphRAG
- Geração de respostas baseadas no grafo
- Busca semântica

---

### 7. **Obsidian Integration** ✅
**Arquivo:** `src/agents/mcp_obsidian_integration.py`  
**LLM:** ❌ **NÃO** - Apenas gestão de notas  
**Funcionalidades:**
- Criação de notas
- Gestão de links
- Busca em notas

---

### 8. **Kestra Agent** ✅
**Arquivo:** `src/agents/mcp_kestra_integration.py`  
**LLM:** ❌ **NÃO** - Apenas criação de workflows  
**Funcionalidades:**
- Criação de workflows Kestra
- Agendamento de tarefas
- Gerenciamento de workflows

---

### 9. **Docker Integration** ✅
**Arquivo:** `src/agents/mcp_docker_integration.py`  
**LLM:** ❌ **NÃO** - Apenas detecção de containers  
**Funcionalidades:**
- Detecção de containers Docker
- Monitoramento de serviços
- Informações de containers

---

### 10. **Streamlit Dashboard** ✅
**Arquivo:** `src/apps/agent_dashboard.py`  
**LLM:** ⚠️ **INDIRETO** - Via System Health Agent  
**Funcionalidades:**
- Interface visual
- Visualizações
- Chat com agentes

---

### 11. **MCP Manager UI** ✅
**Arquivo:** `src/agents/mcp_manager_ui.py`  
**LLM:** ❌ **NÃO** - Apenas interface  
**Funcionalidades:**
- Interface para MCP Manager
- Gerenciamento visual

---

### 12-14. **Agentes Deprecated** (Mantidos para compatibilidade)
- `diagnostic_agent.py` - Consolidado no System Health
- `resolution_agent.py` - Consolidado no System Health
- `agent_helper_system.py` - Consolidado no System Health

**LLM:** ⚠️ **PARCIAL** - `agent_helper_system.py` usa LLM para otimização

---

## 🔧 CONFIGURAÇÃO DE LLM

### LLMs Suportados

O sistema usa `load_llm()` de `src/apps/chains.py` que suporta:

1. **Ollama** (Padrão) ✅
   - Modelo: `llama2` (configurado no `.env`)
   - Variável: `LLM=llama2`
   - URL: `OLLAMA_BASE_URL=http://localhost:11434`

2. **OpenAI** ⚠️
   - Modelos: `gpt-4`, `gpt-4o`, `gpt-4-turbo`, `gpt-3.5`
   - Variável: `OPENAI_API_KEY` (não configurada)

3. **AWS Bedrock** ⚠️
   - Modelos: Claude, Titan, etc.
   - Variável: `AWS_ACCESS_KEY_ID` (comentada)

4. **Google Gemini** ❌
   - **NÃO IMPLEMENTADO** no `load_llm()`
   - `GOOGLE_API_KEY` está configurada, mas só é usada para **embeddings**
   - Embedding: `google-genai-embedding-001` ✅

---

## 📊 RESUMO POR AGENTE

| Agente | Usa LLM? | Qual LLM? | Status |
|--------|----------|-----------|--------|
| **Orchestrator** | ✅ Sim | Ollama (llama2) | Ativo |
| **Neo4j GraphRAG** | ✅ Sim | Ollama (llama2) | Ativo |
| **Agent Helper System** | ✅ Sim | Ollama (llama2) | Deprecated |
| **System Health** | ❌ Não | - | Ativo |
| **DB Manager** | ❌ Não | - | Ativo |
| **MCP Manager** | ❌ Não | - | Ativo |
| **Git Integration** | ❌ Não | - | Ativo |
| **Obsidian** | ❌ Não | - | Ativo |
| **Kestra** | ❌ Não | - | Ativo |
| **Docker** | ❌ Não | - | Ativo |
| **Dashboard** | ⚠️ Indireto | Via outros | Ativo |
| **MCP Manager UI** | ❌ Não | - | Ativo |

---

## ⚠️ GEMINI (Google)

### Status Atual
- ✅ **GOOGLE_API_KEY** configurada: `AIzaSyD7lSqUzy-xvlP3sQHf0IaqAnemtgOqoeM`
- ✅ **Embeddings** suportados: `google-genai-embedding-001`
- ❌ **LLM (Chat)** NÃO suportado no `load_llm()`

### O que Funciona
- ✅ Embeddings do Google (se `EMBEDDING_MODEL=google-genai-embedding-001`)

### O que NÃO Funciona
- ❌ Usar Gemini como LLM principal
- ❌ Agentes não usam Gemini para processamento

---

## 🔧 COMO ADICIONAR SUPORTE A GEMINI

Para usar Gemini como LLM, precisa adicionar no `load_llm()`:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

def load_llm(llm_name: str, logger=BaseLogger(), config={}):
    # ... código existente ...
    
    elif llm_name in ["gemini", "gemini-pro", "gemini-1.5-pro"]:
        logger.info(f"LLM: Using Google Gemini: {llm_name}")
        return ChatGoogleGenerativeAI(
            model=llm_name,
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
```

Depois, configurar no `.env`:
```bash
LLM=gemini-pro
GOOGLE_API_KEY=AIzaSyD7lSqUzy-xvlP3sQHf0IaqAnemtgOqoeM
```

---

## 📋 CONFIGURAÇÃO ATUAL

### `.env` (Atual)
```bash
LLM=llama2                    # Ollama (padrão)
EMBEDDING_MODEL=sentence_transformer  # SentenceTransformer
GOOGLE_API_KEY=AIzaSyD7lSqUzy-xvlP3sQHf0IaqAnemtgOqoeM  # Só para embeddings
OLLAMA_BASE_URL=http://localhost:11434
```

### Agentes que Usam LLM
1. **Orchestrator** → `llama2` (Ollama)
2. **Neo4j GraphRAG** → `llama2` (Ollama)
3. **Agent Helper System** → `llama2` (Ollama)

---

## 🎯 CONCLUSÃO

### LLM Atual
- **Padrão:** Ollama (`llama2`)
- **Configurado:** `LLM=llama2` no `.env`
- **Status:** ✅ Funcionando

### Gemini
- **Embeddings:** ✅ Suportado (mas não está sendo usado)
- **LLM:** ❌ **NÃO suportado** (precisa adicionar código)

### Para Usar Gemini
1. Adicionar suporte no `load_llm()`
2. Configurar `LLM=gemini-pro` no `.env`
3. Agentes automaticamente usarão Gemini

---

## 🔗 Links Relacionados

- [[PROJETO-IA-TEST|Projeto Principal]]
- [[SISTEMA-OTIMIZADO-FINAL|Sistema Otimizado]]
- [[Agentes/Orchestrator|Orchestrator]]

---

## 🏷️ Tags

#agentes #llm #gemini #ollama #configuracao

---

**Última atualização:** 2025-01-27

