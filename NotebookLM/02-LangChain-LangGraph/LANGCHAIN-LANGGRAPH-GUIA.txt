# 🚀 Guia Completo: LangChain + LangGraph

> **Guia Estruturado para Uso Profissional**  
> Baseado em melhores práticas e pesquisas atualizadas  
> Última atualização: 2025-01-27

---

## 📋 Índice

1. [[LANGCHAIN-FUNDAMENTOS|Fundamentos do LangChain]]
2. [[LANGGRAPH-CONCEITOS|Conceitos do LangGraph]]
3. [[LANGGRAPH-WORKFLOWS|Criando Workflows com LangGraph]]
4. [[LANGCHAIN-NEO4J|Integração LangChain + Neo4j]]
5. [[LANGGRAPH-PADROES|Padrões e Melhores Práticas]]
6. [[LANGCHAIN-EXEMPLOS|Exemplos Práticos]]
7. [[LANGGRAPH-AGENTES|Criando Agentes com LangGraph]]

---

## 🎯 Visão Geral

### O que é LangChain?

**LangChain** é um framework para desenvolvimento de aplicações com LLMs (Large Language Models). Ele fornece:

- **Abstrações** para trabalhar com diferentes LLMs
- **Chains** para conectar componentes
- **Agents** para tarefas autônomas
- **Memory** para manter contexto
- **Vector Stores** para busca semântica

### O que é LangGraph?

**LangGraph** é uma extensão do LangChain que permite criar **workflows baseados em grafos**:

- **Estados** para gerenciar dados entre nós
- **Nós** para funções/operações
- **Arestas** para controlar fluxo
- **Ciclos** para loops e iterações
- **Condicionais** para decisões

---

## 🔗 Integração com o Projeto

### Como Usamos no Projeto

1. [[Agentes/Orchestrator|Orchestrator]] - Usa LangChain para planejamento inteligente
2. [[Agentes/Neo4j-GraphRAG|Neo4j GraphRAG]] - Usa LangChain + Neo4j para GraphRAG
3. [[PREPARACAO-LANGCHAIN|Preparação LangChain]] - Configurações e dependências

### Arquivos Relevantes

- `src/apps/chains.py` - Funções de chain
- `src/apps/utils.py` - Utilitários LangChain
- `src/agents/orchestrator.py` - Planejamento com LangChain
- `src/agents/mcp_neo4j_integration.py` - GraphRAG

---

## 📚 Recursos Externos

### Documentação Oficial

- [LangChain Docs](https://docs.langchain.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangChain Neo4j](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher)

### Tutoriais Recomendados

- [LangGraph Studio Tutorial](https://www.datacamp.com/pt/tutorial/langgraph-studio)
- [AWS LangChain Guide](https://docs.aws.amazon.com/pt_br/prescriptive-guidance/latest/agentic-ai-frameworks/langchain-langgraph.html)

### Ferramentas Úteis

- **LangSmith** - Observabilidade e debug
- **LangGraph Studio** - Interface visual para workflows
- **ObsidianLoader** - Carregar notas do Obsidian no LangChain

---

## 🏷️ Tags

#langchain #langgraph #workflows #agentes #neo4j #graphrag #tutorial #guia

---

**Próximo:** [[LANGCHAIN-FUNDAMENTOS|Fundamentos do LangChain →]]
