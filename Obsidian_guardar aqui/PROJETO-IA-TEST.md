# 🚀 PROJETO IA-TEST - Mapeamento Completo

> **Arquivo Principal do Projeto**  
> Última atualização: 2025-01-27

## ⚠️ IMPORTANTE - Leia Primeiro

**[[00-ERROS-E-CONFIGURACOES-PENDENTES|🔴 Erros e Configurações Pendentes]]** - Documento central com todos os erros e como resolver

---

## 📋 Índice

1. [[00-ERROS-E-CONFIGURACOES-PENDENTES|🔴 Erros e Configurações Pendentes]] ⚠️ **LEIA PRIMEIRO**
2. [[VIDEOS_MCP_AGENTES|Vídeos sobre MCP e Agentes]]
3. [[OTIMIZACAO_AGENTES|Otimização e Consolidação de Agentes]]
4. [[ESTRUTURA-PROJETO|Estrutura do Projeto]]

---

## 🎯 Visão Geral

Sistema de agentes especializados coordenados pelo **Orchestrator** com planejamento inteligente integrado.

---

## 🤖 Agentes (11 - Otimizados)

### Agentes Principais

1. **[[Agentes/Orchestrator|Orchestrator]]** - `src.agents.orchestrator`
   - Coordenador central com planejamento inteligente
   - **CONSOLIDADO:** Inclui funcionalidades do Master Agent
   - Arquivo: `src/agents/orchestrator.py`

2. **[[Agentes/System-Health|System Health Agent]]** - `src.agents.system_health_agent`
   - Diagnóstico, monitoramento e resolução
   - **CONSOLIDADO:** Diagnostic + Helper + Resolution
   - Arquivo: `src/agents/system_health_agent.py`

3. **[[Agentes/DB-Manager|DB Manager]]** - `src.agents.db_manager`
   - Gerenciamento de bancos de dados (Supabase, Neon, MongoDB)
   - Arquivo: `src/agents/db_manager.py`

4. **[[Agentes/MCP-Manager|MCP Manager]]** - `src.agents.mcp_manager`
   - Gerenciamento de servidores MCP
   - Arquivo: `src/agents/mcp_manager.py`

5. **[[Agentes/Git-Integration|Git Integration]]** - `src.agents.git_integration`
   - Integração com Git/GitHub
   - Arquivo: `src/agents/git_integration.py`

6. **[[Agentes/Neo4j-GraphRAG|Neo4j GraphRAG]]** - `src.agents.mcp_neo4j_integration`
   - GraphRAG com Neo4j
   - Arquivo: `src/agents/mcp_neo4j_integration.py`

7. **[[Agentes/Obsidian-Integration|Obsidian Integration]]** - `src.agents.mcp_obsidian_integration`
   - Integração com Obsidian
   - Arquivo: `src/agents/mcp_obsidian_integration.py`

8. **[[Agentes/Kestra-Agent|Kestra Agent]]** - `src.agents.mcp_kestra_integration`
   - Orquestração de workflows Kestra
   - Arquivo: `src/agents/mcp_kestra_integration.py`

9. **[[Agentes/Docker-Integration|Docker Integration]]** - `src.agents.mcp_docker_integration`
   - Detecção e gerenciamento de serviços Docker
   - Arquivo: `src/agents/mcp_docker_integration.py`

### Interfaces

10. **[[Agentes/Agent-Dashboard-UI|Agent Dashboard UI]]** - `src.apps.agent_dashboard`
    - Dashboard Streamlit para interagir com agentes
    - Arquivo: `src/apps/agent_dashboard.py`

11. **[[Agentes/MCP-Manager-UI|MCP Manager UI]]** - `src.agents.mcp_manager_ui`
    - Interface Streamlit para MCP Manager
    - Arquivo: `src/agents/mcp_manager_ui.py`

---

## 📹 Vídeos e Recursos

### Vídeos Analisados

1. **Cursor + Neo4j MCP**
   - URL: https://www.youtube.com/watch?v=UilGH0j73rI
   - Pontos principais: Configuração MCP, Auto Run, integração profunda

2. **GitHub + IA - Gerenciando Repositórios**
   - URL: https://www.youtube.com/watch?v=t4lA9YD7grI
   - Pontos principais: GitHub MCP, gerenciamento via chat, automação

3. **TestSprite - Testes Automatizados**
   - URL: https://www.youtube.com/watch?v=BZUq2PtDI1Y
   - Pontos principais: Testes automatizados, cobertura, redução de débito técnico

Ver [[VIDEOS_MCP_AGENTES|detalhes completos dos vídeos]].

---

## 🔄 Otimizações Realizadas

### Consolidações

1. **System Health Agent** (Novo)
   - Consolidou: Diagnostic Agent + Helper System + Resolution Agent
   - Redução: 3 agentes → 1 agente

2. **Orchestrator** (Melhorado)
   - Consolidou: Funcionalidades do Master Agent
   - Adicionado: Planejamento inteligente integrado
   - Redução: 2 agentes → 1 agente (com mais funcionalidades)

**Total:** 14 agentes → 11 agentes (21% de redução)

Ver [[OTIMIZACAO_AGENTES|detalhes da otimização]].

---

## 📱 Aplicações

1. **API** - `src.apps.api`
2. **Bot** - `src.apps.bot`
3. **Chains** - `src.apps.chains`
4. **Loader** - `src.apps.loader`
5. **PDF Bot** - `src.apps.pdf_bot`
6. **Utils** - `src.apps.utils`
7. **Agent Dashboard** - `src.apps.agent_dashboard`

---

## 🚀 LangChain + LangGraph

### Guias e Tutoriais

- [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo LangChain + LangGraph]] ⭐ **NOVO**
- [[LANGCHAIN-FUNDAMENTOS|Fundamentos do LangChain]]
- [[LANGGRAPH-CONCEITOS|Conceitos do LangGraph]]
- [[LANGGRAPH-WORKFLOWS|Criando Workflows]]
- [[LANGCHAIN-NEO4J|Integração LangChain + Neo4j]]
- [[LANGGRAPH-PADROES|Padrões e Melhores Práticas]]
- [[LANGGRAPH-AGENTES|Criando Agentes]]
- [[LANGCHAIN-EXEMPLOS|Exemplos Práticos]]
- [[PREPARACAO-LANGCHAIN|Preparação e Configuração]]
- [[RESUMO-LANGCHAIN-PREPARACAO|Resumo Rápido]]

### Uso no Projeto

- [[Agentes/Orchestrator|Orchestrator]] - Usa LangChain para planejamento
- [[Agentes/Neo4j-GraphRAG|Neo4j GraphRAG]] - GraphRAG com LangChain
- `src/apps/chains.py` - Funções de chain
- `src/apps/utils.py` - Utilitários LangChain

---

## 📚 Documentação

### Documentos Principais

- [[00-ERROS-E-CONFIGURACOES-PENDENTES|🔴 Erros e Configurações Pendentes]] ⚠️ **LEIA PRIMEIRO**
- [[VIDEOS_MCP_AGENTES|Vídeos sobre MCP]]
- [[OTIMIZACAO_AGENTES|Otimização de Agentes]]
- [[ESTRUTURA-PROJETO|Estrutura do Projeto]]
- [[Agentes/Orchestrator|Orchestrator]]
- [[Agentes/System-Health|System Health Agent]]

### Documentos Técnicos (fora do Obsidian)

- `docs/CHAVES_E_CONFIGURACOES_FALTANTES.md` - Lista completa de chaves
- `docs/NEO4J_AURA_SETUP.md` - Setup Neo4j Aura
- `docs/ONDE_DADOS_SAO_SALVOS.md` - Onde dados são salvos
- `docs/IMPORTAR_DADOS_NEO4J_AURA.md` - Como importar dados

---

## 🏷️ Tags

#projeto #agentes #orchestrator #mcp #neo4j #obsidian #kestra #otimização #consolidação

---

**Versão:** 2.0 (Otimizada)  
**Última atualização:** 2025-01-27
