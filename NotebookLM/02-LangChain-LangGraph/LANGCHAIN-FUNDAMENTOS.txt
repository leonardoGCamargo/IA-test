# 📚 LangChain: Fundamentos

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

