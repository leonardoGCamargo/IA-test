# 🔗 LangChain + Neo4j: Integração Completa

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

