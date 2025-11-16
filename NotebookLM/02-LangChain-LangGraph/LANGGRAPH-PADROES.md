# 🎨 LangGraph: Padrões e Melhores Práticas

> **Padrões Avançados e Melhores Práticas**  
> Parte do [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]

---

## 🎯 Padrões Comuns

### 1. RAG (Retrieval Augmented Generation)

**Padrão:**
```
[Pergunta] → [Retrieve] → [Generate] → [Resposta]
```

**Quando usar:**
- Busca em documentos
- Respostas baseadas em contexto
- Knowledge base Q&A

**Exemplo:**
```python
def retrieve(state):
    docs = vectorstore.similarity_search(state["question"])
    return {"context": docs}

def generate(state):
    context = format_docs(state["context"])
    answer = llm.invoke(f"Contexto: {context}\\nPergunta: {state['question']}")
    return {"answer": answer.content}
```

---

### 2. Agent Loop

**Padrão:**
```
[Input] → [Agent] → [Tool] → [Agent] → [Output]
              ↑                    ↓
              └────────────────────┘
```

**Quando usar:**
- Agentes autônomos
- Múltiplas ações necessárias
- Decisões iterativas

**Exemplo:**
```python
def agent_node(state):
    # Agente decide ação
    action = agent.decide(state["messages"])
    
    if action["type"] == "tool":
        return {"next": "tool"}
    return {"next": "end"}

def tool_node(state):
    # Executa tool
    result = execute_tool(state["action"])
    return {"messages": state["messages"] + [result]}
```

---

### 3. Multi-Agent

**Padrão:**
```
[Input] → [Agent1] → [Agent2] → [Agent3] → [Output]
```

**Quando usar:**
- Pipeline de processamento
- Especialização por etapa
- Processamento sequencial

---

### 4. Conditional Routing

**Padrão:**
```
[Decision] → [Branch1] → [End]
       ↓
    [Branch2] → [End]
```

**Quando usar:**
- Decisões baseadas em condições
- Fluxos diferentes por tipo
- Validação e tratamento de erros

---

## ✅ Melhores Práticas

### 1. Estado Tipado

**✅ Faça:**
```python
from typing import TypedDict, Annotated

class State(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    context: list
```

**❌ Evite:**
```python
# Estado não tipado
state = {"messages": [], "question": ""}
```

---

### 2. Nós Pequenos e Focados

**✅ Faça:**
```python
def retrieve_node(state):
    # Uma responsabilidade
    return {"context": search(state["question"])}
```

**❌ Evite:**
```python
def big_node(state):
    # Muitas responsabilidades
    context = search(state["question"])
    answer = generate(context)
    validate(answer)
    return {"answer": answer}
```

---

### 3. Tratamento de Erros

**✅ Faça:**
```python
def safe_node(state):
    try:
        result = process(state)
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}
```

---

### 4. Logging e Observabilidade

**✅ Faça:**
```python
import logging

logger = logging.getLogger(__name__)

def logged_node(state):
    logger.info(f"Processing: {state['question']}")
    result = process(state)
    logger.info(f"Result: {result}")
    return {"result": result}
```

---

### 5. Validação de Estado

**✅ Faça:**
```python
def validate_state(state):
    if not state.get("question"):
        raise ValueError("Question is required")
    return state
```

---

## 🔄 Padrões Avançados

### 1. Human-in-the-Loop

```python
def human_review_node(state):
    # Pausa para revisão humana
    return {"status": "pending_review"}

def continue_after_review(state):
    if state.get("approved"):
        return {"next": "continue"}
    return {"next": "revise"}
```

---

### 2. Parallel Processing

```python
def parallel_node(state):
    # Processa em paralelo
    results = parallel_map(process_item, state["items"])
    return {"results": results}
```

---

### 3. State Persistence

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Salva estado
config = {"configurable": {"thread_id": "1"}}
app.invoke(initial_state, config=config)
```

---

## 🔗 Próximos Passos

- [[LANGGRAPH-AGENTES|Criando Agentes →]]
- [[LANGCHAIN-EXEMPLOS|Exemplos Práticos →]]
- [[LANGCHAIN-NEO4J|Integração Neo4j →]]

---

## 🏷️ Tags

#langgraph #patterns #best-practices #workflows #agents

---

**Voltar:** [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]
"""

