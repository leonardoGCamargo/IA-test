# 🕸️ LangGraph: Conceitos e Arquitetura

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

