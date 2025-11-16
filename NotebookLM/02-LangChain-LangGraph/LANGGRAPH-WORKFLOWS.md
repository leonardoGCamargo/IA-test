# 🔄 LangGraph: Criando Workflows

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

