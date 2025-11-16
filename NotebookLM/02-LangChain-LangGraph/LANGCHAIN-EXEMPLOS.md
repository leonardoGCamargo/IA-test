# 💡 LangChain + LangGraph: Exemplos Práticos

> **Exemplos Reais e Práticos**  
> Parte do [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]

---

## 🎯 Exemplos do Projeto

### 1. Orchestrator com Planejamento Inteligente

**Arquivo:** `src/agents/orchestrator.py`

```python
def execute_goal(self, goal: str):
    # Cria plano inteligente
    plan = self._create_intelligent_plan(goal)
    
    # Executa cada passo
    for step in plan["steps"]:
        result = self._execute_planned_step(
            step["action"],
            step["tool"],
            step["parameters"]
        )
    
    return results
```

---

### 2. Neo4j GraphRAG

**Arquivo:** `src/agents/mcp_neo4j_integration.py`

```python
def query_graphrag(self, question: str):
    # Busca semântica
    docs = vectorstore.similarity_search(question)
    
    # Busca no grafo
    graph_results = self.graph.query(cypher_query)
    
    # Combina e gera resposta
    context = docs + graph_results
    answer = llm.invoke(f"Contexto: {context}\\nPergunta: {question}")
    
    return answer
```

---

### 3. Chains Básicas

**Arquivo:** `src/apps/chains.py`

```python
def configure_qa_rag_chain(llm, embeddings, embeddings_store_url, username, password):
    # Vector store
    vectorstore = Neo4jVector.from_existing_index(...)
    
    # Retriever
    retriever = vectorstore.as_retriever()
    
    # Chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
```

---

## 📚 Exemplos Externos

### 1. RAG Simples

```python
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Carregar documentos
documents = load_documents()

# Dividir em chunks
text_splitter = RecursiveCharacterTextSplitter()
chunks = text_splitter.split_documents(documents)

# Criar vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

# Retriever
retriever = vectorstore.as_retriever()

# Chain
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)
```

---

### 2. Agente com Tools

```python
from langchain.agents import create_openai_tools_agent

tools = [search_tool, calculator_tool, database_tool]

agent = create_openai_tools_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

result = executor.invoke({
    "input": "Busque informações e calcule a média"
})
```

---

### 3. LangGraph Workflow

```python
from langgraph.graph import StateGraph, END

class State(TypedDict):
    question: str
    context: list
    answer: str

def retrieve(state):
    docs = vectorstore.similarity_search(state["question"])
    return {"context": docs}

def generate(state):
    answer = llm.invoke(f"Contexto: {state['context']}\\nPergunta: {state['question']}")
    return {"answer": answer.content}

graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

app = graph.compile()
result = app.invoke({"question": "Como funciona LangChain?"})
```

---

## 🔗 Recursos

- [[LANGCHAIN-FUNDAMENTOS|Fundamentos →]]
- [[LANGGRAPH-WORKFLOWS|Workflows →]]
- [[LANGCHAIN-NEO4J|Neo4j →]]

---

## 🏷️ Tags

#langchain #langgraph #exemplos #tutorial #code

---

**Voltar:** [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]
"""

