# 🤖 LangGraph: Criando Agentes

> **Guia para Criar Agentes com LangGraph**  
> Parte do [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]

---

## 🎯 O que são Agentes?

**Agentes** são sistemas autônomos que:
- Observam o ambiente
- Decidem ações
- Executam tools
- Aprendem com feedback

---

## 🏗️ Estrutura de um Agente

### Componentes

1. **LLM** - Cérebro do agente
2. **Tools** - Ferramentas disponíveis
3. **Memory** - Contexto e histórico
4. **State** - Estado do agente
5. **Prompt** - Instruções

---

## 📝 Exemplo Básico

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    tools_used: list
    answer: str

def agent_node(state: AgentState):
    # Agente decide ação
    response = llm.invoke(state["messages"])
    
    # Verifica se precisa usar tool
    if response.tool_calls:
        return {"next": "tool", "tool_calls": response.tool_calls}
    
    return {"next": "end", "answer": response.content}

def tool_node(state: AgentState):
    # Executa tools
    results = []
    for tool_call in state["tool_calls"]:
        result = execute_tool(tool_call)
        results.append(result)
    
    return {
        "tools_used": state["tools_used"] + results,
        "messages": state["messages"] + [{"role": "tool", "content": results}]
    }

# Construir grafo
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tool", tool_node)

graph.set_entry_point("agent")

def route(state: AgentState):
    return state.get("next", "end")

graph.add_conditional_edges(
    "agent",
    route,
    {"tool": "tool", "end": END}
)

graph.add_edge("tool", "agent")  # Volta para agente após tool

app = graph.compile()
```

---

## 🔧 Agente com Tools

### Definir Tools

```python
from langchain.tools import tool

@tool
def search_database(query: str) -> str:
    \"\"\"Busca no banco de dados.\"\"\"
    return database.search(query)

@tool
def call_api(endpoint: str) -> str:
    \"\"\"Chama API externa.\"\"\"
    return requests.get(endpoint).text

tools = [search_database, call_api]
```

### Agente com Tools

```python
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor

# Criar agente
agent = create_openai_tools_agent(llm, tools, prompt)

# Executor
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Executar
result = executor.invoke({"input": "Busque informações sobre LangChain"})
```

---

## 🔄 Agente com Loop

```python
def agent_loop(state: AgentState):
    max_iterations = 5
    iteration = state.get("iteration", 0)
    
    if iteration >= max_iterations:
        return {"next": "end"}
    
    # Agente decide
    action = agent.decide(state)
    
    if action["type"] == "final_answer":
        return {"next": "end", "answer": action["answer"]}
    
    # Executa tool
    result = execute_tool(action["tool"])
    
    return {
        "iteration": iteration + 1,
        "messages": state["messages"] + [result],
        "next": "agent"  # Volta para agente
    }
```

---

## 🎨 Agente Multi-Etapas

```python
def research_agent(state):
    # Pesquisa informações
    info = search(state["question"])
    return {"research": info}

def analyze_agent(state):
    # Analisa informações
    analysis = analyze(state["research"])
    return {"analysis": analysis}

def generate_agent(state):
    # Gera resposta final
    answer = generate(state["analysis"], state["question"])
    return {"answer": answer}

# Grafo
graph = StateGraph(AgentState)
graph.add_node("research", research_agent)
graph.add_node("analyze", analyze_agent)
graph.add_node("generate", generate_agent)

graph.set_entry_point("research")
graph.add_edge("research", "analyze")
graph.add_edge("analyze", "generate")
graph.add_edge("generate", END)
```

---

## 🔗 No Projeto

Veja como usamos:
- [[Agentes/Orchestrator|Orchestrator]] - Agente coordenador
- `src/agents/orchestrator.py` - Implementação

---

## 🏷️ Tags

#langgraph #agents #tools #loops #multi-agent

---

**Voltar:** [[LANGCHAIN-LANGGRAPH-GUIA|Guia Completo]]
"""

