# -*- coding: utf-8 -*-
"""
Script para criar guia completo de LangChain-LangGraph
com base em pesquisas web e estruturação para Obsidian
"""

from pathlib import Path
import json

project_root = Path(__file__).parent.parent
obsidian_path = project_root / "Obsidian_guardar aqui"

def criar_guia_principal():
    """Cria o guia principal de LangChain-LangGraph."""
    
    conteudo = """# 🚀 Guia Completo: LangChain + LangGraph

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

1. **[[Agentes/Orchestrator|Orchestrator]]** - Usa LangChain para planejamento inteligente
2. **[[Agentes/Neo4j-GraphRAG|Neo4j GraphRAG]]** - Usa LangChain + Neo4j para GraphRAG
3. **[[PREPARACAO-LANGCHAIN|Preparação LangChain]]** - Configurações e dependências

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
"""

    arquivo = obsidian_path / "LANGCHAIN-LANGGRAPH-GUIA.md"
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Criado: {arquivo.name}")

def criar_fundamentos():
    """Cria documento sobre fundamentos do LangChain."""
    
    conteudo = """# 📚 LangChain: Fundamentos

> **Base do Framework LangChain**  
> Parte do [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]

---

## 🎯 Conceitos Principais

### 1. LLMs (Large Language Models)

**O que são:**
- Modelos de linguagem treinados em grandes volumes de texto
- Capazes de gerar, completar e entender texto
- Exemplos: GPT-4, Claude, Gemini, Llama

**Como usar no LangChain:**
```python
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

# Ollama (local)
llm = ChatOllama(model="llama2")

# Google Gemini
llm = ChatGoogleGenerativeAI(model="gemini-pro")
```

---

### 2. Prompts

**O que são:**
- Instruções para o LLM
- Templates reutilizáveis
- Podem incluir variáveis

**Exemplo:**
```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente especializado em {topico}."),
    ("human", "{pergunta}")
])

chain = prompt | llm
response = chain.invoke({
    "topico": "programação",
    "pergunta": "Como funciona Python?"
})
```

---

### 3. Chains

**O que são:**
- Sequências de operações conectadas
- Permitem encadear LLMs, prompts, tools
- Reutilizáveis e compostáveis

**Tipos:**
- **LLM Chain** - LLM + Prompt
- **Sequential Chain** - Múltiplas chains em sequência
- **Router Chain** - Escolhe qual chain usar

**Exemplo:**
```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"pergunta": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

---

### 4. Memory

**O que é:**
- Mantém contexto entre interações
- Histórico de conversas
- Estado persistente

**Tipos:**
- **ConversationBufferMemory** - Mantém todo histórico
- **ConversationSummaryMemory** - Resumo do histórico
- **ConversationBufferWindowMemory** - Últimas N mensagens

---

### 5. Vector Stores

**O que são:**
- Armazenamento de embeddings
- Busca semântica
- RAG (Retrieval Augmented Generation)

**Exemplo com Neo4j:**
```python
from langchain_neo4j import Neo4jVector

vectorstore = Neo4jVector.from_existing_index(
    embedding=embeddings,
    index_name="vector",
    url=neo4j_uri,
    username=neo4j_username,
    password=neo4j_password
)

# Busca semântica
results = vectorstore.similarity_search("sua pergunta")
```

---

### 6. Agents

**O que são:**
- Agentes autônomos que usam tools
- Podem fazer decisões
- Executam ações baseadas em observações

**Componentes:**
- **LLM** - Cérebro do agente
- **Tools** - Ferramentas disponíveis
- **Memory** - Contexto
- **Prompt** - Instruções

---

## 🔗 Próximos Passos

- [[LANGGRAPH-CONCEITOS|Conceitos do LangGraph →]]
- [[LANGCHAIN-EXEMPLOS|Exemplos Práticos →]]
- [[LANGCHAIN-NEO4J|Integração com Neo4j →]]

---

## 🏷️ Tags

#langchain #fundamentos #llm #chains #prompts #memory #vectorstores #agents

---

**Voltar:** [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]
"""

    arquivo = obsidian_path / "LANGCHAIN-FUNDAMENTOS.md"
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Criado: {arquivo.name}")

def criar_langgraph_conceitos():
    """Cria documento sobre conceitos do LangGraph."""
    
    conteudo = """# 🕸️ LangGraph: Conceitos e Arquitetura

> **Entendendo LangGraph**  
> Parte do [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]

---

## 🎯 O que é LangGraph?

**LangGraph** é uma biblioteca para construir **aplicações stateful e multi-actor** com LLMs usando grafos.

### Por que LangGraph?

- ✅ **Workflows Complexos** - Fluxos com loops, condicionais, paralelismo
- ✅ **Estado Persistente** - Mantém contexto entre chamadas
- ✅ **Controle de Fluxo** - Decisões baseadas em condições
- ✅ **Multi-Actor** - Múltiplos agentes trabalhando juntos
- ✅ **Ciclos** - Loops e iterações

---

## 🏗️ Componentes Principais

### 1. State (Estado)

**O que é:**
- Dados compartilhados entre nós
- Tipado e validado
- Persistente entre execuções

**Exemplo:**
```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    answer: str
    context: list
```

---

### 2. Nodes (Nós)

**O que são:**
- Funções que processam o estado
- Recebem estado, retornam atualizações
- Podem chamar LLMs, tools, etc.

**Exemplo:**
```python
def retrieve_node(state: GraphState):
    # Busca informações
    context = vectorstore.similarity_search(state["question"])
    return {"context": context}

def generate_node(state: GraphState):
    # Gera resposta
    answer = llm.invoke(state["question"])
    return {"answer": answer}
```

---

### 3. Edges (Arestas)

**O que são:**
- Conexões entre nós
- Controlam o fluxo
- Podem ser condicionais

**Tipos:**
- **Diretas** - Sempre seguem
- **Condicionais** - Baseadas em condições
- **Ciclos** - Voltam para nós anteriores

**Exemplo:**
```python
from langgraph.graph import StateGraph

graph = StateGraph(GraphState)

# Adiciona nós
graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)

# Adiciona arestas
graph.add_edge("retrieve", "generate")  # Direta
graph.add_conditional_edges(
    "generate",
    should_continue,  # Função que decide
    {"continue": "retrieve", "end": END}
)
```

---

### 4. Conditional Edges (Arestas Condicionais)

**O que são:**
- Decisões baseadas no estado
- Função que retorna próximo nó
- Permitem loops e branches

**Exemplo:**
```python
def should_continue(state: GraphState):
    if state["answer"]:
        return "end"
    return "continue"

graph.add_conditional_edges(
    "generate",
    should_continue,
    {
        "continue": "retrieve",
        "end": END
    }
)
```

---

## 🔄 Padrões Comuns

### 1. RAG (Retrieval Augmented Generation)

```
[Pergunta] → [Retrieve] → [Generate] → [Resposta]
```

### 2. Agent Loop

```
[Input] → [Agent] → [Tool] → [Agent] → [Output]
              ↑                    ↓
              └────────────────────┘
```

### 3. Multi-Agent

```
[Input] → [Agent1] → [Agent2] → [Agent3] → [Output]
```

---

## 🔗 Próximos Passos

- [[LANGGRAPH-WORKFLOWS|Criando Workflows →]]
- [[LANGGRAPH-PADROES|Padrões e Melhores Práticas →]]
- [[LANGGRAPH-AGENTES|Criando Agentes →]]

---

## 🏷️ Tags

#langgraph #workflows #state #nodes #edges #conditional #patterns

---

**Voltar:** [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]
"""

    arquivo = obsidian_path / "LANGGRAPH-CONCEITOS.md"
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Criado: {arquivo.name}")

def criar_workflows():
    """Cria documento sobre criação de workflows."""
    
    conteudo = """# 🔄 LangGraph: Criando Workflows

> **Guia Prático para Workflows**  
> Parte do [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]

---

## 🎯 Criando seu Primeiro Workflow

### Passo 1: Definir Estado

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class WorkflowState(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    context: list
    answer: str
    step: int
```

---

### Passo 2: Criar Nós

```python
def retrieve_node(state: WorkflowState):
    # Busca contexto
    context = vectorstore.similarity_search(state["question"])
    return {"context": context, "step": 1}

def generate_node(state: WorkflowState):
    # Gera resposta
    prompt = f"Contexto: {state['context']}\\nPergunta: {state['question']}"
    answer = llm.invoke(prompt)
    return {"answer": answer.content, "step": 2}

def validate_node(state: WorkflowState):
    # Valida resposta
    if len(state["answer"]) > 100:
        return {"step": 3, "valid": True}
    return {"step": 3, "valid": False}
```

---

### Passo 3: Construir Grafo

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(WorkflowState)

# Adiciona nós
graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)
graph.add_node("validate", validate_node)

# Define entrada
graph.set_entry_point("retrieve")

# Adiciona arestas
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", "validate")

# Aresta condicional
def should_end(state: WorkflowState):
    if state.get("valid"):
        return "end"
    return "retry"

graph.add_conditional_edges(
    "validate",
    should_end,
    {
        "end": END,
        "retry": "retrieve"
    }
)

# Compila
app = graph.compile()
```

---

### Passo 4: Executar

```python
# Executa workflow
result = app.invoke({
    "question": "Como funciona LangGraph?",
    "messages": [],
    "step": 0
})

print(result["answer"])
```

---

## 🔄 Padrões de Workflow

### 1. Linear (Sequencial)

```
[Start] → [Node1] → [Node2] → [Node3] → [End]
```

### 2. Conditional (Condicional)

```
[Start] → [Decision] → [Branch1] → [End]
              ↓
           [Branch2] → [End]
```

### 3. Loop (Ciclo)

```
[Start] → [Process] → [Check] → [End]
              ↑           ↓
              └───────────┘
```

### 4. Parallel (Paralelo)

```
[Start] → [Node1] ─┐
         → [Node2] ─┼→ [Merge] → [End]
         → [Node3] ─┘
```

---

## 🎨 Exemplo Completo: RAG com Validação

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class RAGState(TypedDict):
    question: str
    context: list
    answer: str
    validated: bool

def retrieve(state: RAGState):
    docs = vectorstore.similarity_search(state["question"], k=3)
    return {"context": [d.page_content for d in docs]}

def generate(state: RAGState):
    context = "\\n".join(state["context"])
    prompt = f"Contexto: {context}\\n\\nPergunta: {state['question']}"
    response = llm.invoke(prompt)
    return {"answer": response.content}

def validate(state: RAGState):
    # Validação simples
    is_valid = len(state["answer"]) > 50 and "?" not in state["answer"]
    return {"validated": is_valid}

# Construir grafo
graph = StateGraph(RAGState)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_node("validate", validate)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", "validate")

def route(state: RAGState):
    return "end" if state["validated"] else "retry"

graph.add_conditional_edges(
    "validate",
    route,
    {"end": END, "retry": "retrieve"}
)

app = graph.compile()
```

---

## 🔗 Próximos Passos

- [[LANGGRAPH-PADROES|Padrões Avançados →]]
- [[LANGGRAPH-AGENTES|Criando Agentes →]]
- [[LANGCHAIN-EXEMPLOS|Exemplos Práticos →]]

---

## 🏷️ Tags

#langgraph #workflows #tutorial #exemplos #patterns #rag

---

**Voltar:** [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]
"""

    arquivo = obsidian_path / "LANGGRAPH-WORKFLOWS.md"
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Criado: {arquivo.name}")

def criar_integracao_neo4j():
    """Cria documento sobre integração Neo4j."""
    
    conteudo = """# 🔗 LangChain + Neo4j: Integração Completa

> **GraphRAG e Integração Neo4j**  
> Parte do [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]

---

## 🎯 Por que Neo4j com LangChain?

- ✅ **GraphRAG** - RAG com grafo de conhecimento
- ✅ **Vector Search** - Busca semântica com embeddings
- ✅ **Relacionamentos** - Conexões entre entidades
- ✅ **Cypher Queries** - Consultas poderosas
- ✅ **Persistência** - Dados estruturados

---

## 📦 Instalação

```bash
pip install langchain-neo4j neo4j
```

---

## 🔧 Configuração

```python
import os
from langchain_neo4j import Neo4jGraph, Neo4jVector

# Configuração
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Criar grafo
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
)
```

---

## 🔍 Vector Store

### Criar Vector Index

```python
from src.apps.utils import create_vector_index

create_vector_index(graph)
```

### Usar Vector Store

```python
from langchain_neo4j import Neo4jVector

vectorstore = Neo4jVector.from_existing_index(
    embedding=embeddings,
    index_name="vector",
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
)

# Busca semântica
results = vectorstore.similarity_search("sua pergunta", k=5)
```

---

## 🕸️ GraphRAG

### O que é GraphRAG?

**GraphRAG** combina:
- **RAG tradicional** - Busca em documentos
- **Grafo de conhecimento** - Relacionamentos entre entidades
- **Cypher queries** - Consultas estruturadas

### Exemplo Básico

```python
from langchain_neo4j import Neo4jGraph

    # Query Cypher
    query = (
        "MATCH (n:Document)-[:CONTAINS]->(e:Entity) "
        "WHERE e.name CONTAINS $entity "
        "RETURN n, e "
        "LIMIT 10"
    )
    
    results = graph.query(query, {"entity": "LangChain"})
```

### GraphRAG Completo

```python
def graphrag_retrieve(state):
    question = state["question"]
    
    # 1. Busca semântica
    docs = vectorstore.similarity_search(question, k=3)
    
    # 2. Extrai entidades
    entities = extract_entities(question)
    
    # 3. Busca no grafo
    graph_query = (
        "MATCH (e:Entity)-[:RELATED_TO]->(d:Document) "
        f"WHERE e.name IN {entities} "
        "RETURN d "
        "LIMIT 5"
    )
    graph_docs = graph.query(graph_query)
    
    # 4. Combina resultados
    all_context = docs + graph_docs
    return {"context": all_context}
```

---

## 🔄 Workflow GraphRAG com LangGraph

```python
from langgraph.graph import StateGraph, END

class GraphRAGState(TypedDict):
    question: str
    entities: list
    vector_results: list
    graph_results: list
    context: list
    answer: str

def extract_entities_node(state: GraphRAGState):
    # Extrai entidades da pergunta
    entities = extract_entities(state["question"])
    return {"entities": entities}

def vector_search_node(state: GraphRAGState):
    # Busca semântica
    results = vectorstore.similarity_search(state["question"], k=3)
    return {"vector_results": results}

def graph_search_node(state: GraphRAGState):
    # Busca no grafo
    entities_str = str(state['entities'])
    query = (
        "MATCH (e:Entity)-[:RELATED_TO]->(d:Document) "
        f"WHERE e.name IN {entities_str} "
        "RETURN d"
    )
    results = graph.query(query)
    return {"graph_results": results}

def combine_context_node(state: GraphRAGState):
    # Combina resultados
    context = state["vector_results"] + state["graph_results"]
    return {"context": context}

def generate_answer_node(state: GraphRAGState):
    # Gera resposta
    context = "\\n".join([str(c) for c in state["context"]])
    prompt = f"Contexto: {context}\\n\\nPergunta: {state['question']}"
    answer = llm.invoke(prompt)
    return {"answer": answer.content}

# Construir grafo
graph = StateGraph(GraphRAGState)
graph.add_node("extract_entities", extract_entities_node)
graph.add_node("vector_search", vector_search_node)
graph.add_node("graph_search", graph_search_node)
graph.add_node("combine", combine_context_node)
graph.add_node("generate", generate_answer_node)

graph.set_entry_point("extract_entities")
graph.add_edge("extract_entities", "vector_search")
graph.add_edge("extract_entities", "graph_search")
graph.add_edge("vector_search", "combine")
graph.add_edge("graph_search", "combine")
graph.add_edge("combine", "generate")
graph.add_edge("generate", END)

app = graph.compile()
```

---

## 🔗 No Projeto

Veja como usamos:
- [[Agentes/Neo4j-GraphRAG|Neo4j GraphRAG Agent]]
- `src/agents/mcp_neo4j_integration.py`
- `src/apps/chains.py`

---

## 🏷️ Tags

#langchain #neo4j #graphrag #vectorstore #cypher #integration

---

**Voltar:** [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]
"""

    arquivo = obsidian_path / "LANGCHAIN-NEO4J.md"
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Criado: {arquivo.name}")

def atualizar_projeto_principal():
    """Atualiza PROJETO-IA-TEST.md com links para LangChain."""
    
    arquivo = obsidian_path / "PROJETO-IA-TEST.md"
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Adiciona seção de LangChain se não existir
    if "LANGCHAIN-LANGGRAPH-GUIA" not in conteudo:
        secao_langchain = """
## 🚀 LangChain + LangGraph

### Guias e Tutoriais

- [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo LangChain + LangGraph]] ⭐ **NOVO**
- [[LANGCHAIN-FUNDAMENTOS|Fundamentos do LangChain]]
- [[LANGGRAPH-CONCEITOS|Conceitos do LangGraph]]
- [[LANGGRAPH-WORKFLOWS|Criando Workflows]]
- [[LANGCHAIN-NEO4J|Integração LangChain + Neo4j]]
- [[PREPARACAO-LANGCHAIN|Preparação e Configuração]]

### Uso no Projeto

- [[Agentes/Orchestrator|Orchestrator]] - Usa LangChain para planejamento
- [[Agentes/Neo4j-GraphRAG|Neo4j GraphRAG]] - GraphRAG com LangChain
- `src/apps/chains.py` - Funções de chain
- `src/apps/utils.py` - Utilitários LangChain

---
"""
        
        # Insere após seção de Documentação
        if "## 📚 Documentação" in conteudo:
            conteudo = conteudo.replace(
                "## 📚 Documentação",
                secao_langchain + "\n## 📚 Documentação"
            )
        else:
            # Adiciona antes das tags
            conteudo = conteudo.replace(
                "## 🏷️ Tags",
                secao_langchain + "\n## 🏷️ Tags"
            )
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"✅ Atualizado: {arquivo.name}")

def main():
    """Função principal."""
    print("=" * 70)
    print("CRIANDO GUIA LANGCHAIN-LANGGRAPH")
    print("=" * 70)
    print()
    
    criar_guia_principal()
    criar_fundamentos()
    criar_langgraph_conceitos()
    criar_workflows()
    criar_integracao_neo4j()
    atualizar_projeto_principal()
    
    print()
    print("=" * 70)
    print("GUIA CRIADO COM SUCESSO!")
    print("=" * 70)
    print()
    print("Arquivos criados:")
    print("  - LANGCHAIN-LANGGRAPH-GUIA.md (principal)")
    print("  - LANGCHAIN-FUNDAMENTOS.md")
    print("  - LANGGRAPH-CONCEITOS.md")
    print("  - LANGGRAPH-WORKFLOWS.md")
    print("  - LANGCHAIN-NEO4J.md")
    print()
    print("PROJETO-IA-TEST.md atualizado com links")

if __name__ == "__main__":
    main()

