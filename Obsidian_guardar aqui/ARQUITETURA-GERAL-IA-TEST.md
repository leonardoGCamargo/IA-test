---
tags:
  - projeto
  - arquitetura
  - mermaid
---

# Arquitetura Geral – IA-TEST

Esta nota resume, em diagramas, como o seu sistema está montado hoje: aplicações, agentes, Kestra, N8N, bancos e LLMs.

Ligado a:
- Índice do projeto: [[INDEX-PROJETO-IA-TEST]]
- Serviços e portas: [[INFRA-SERVICOS-PORTAS]]
- Agentes e LLMs: [[AGENTES-E-LLMS]]

---

## 1. Visão macro do sistema

```mermaid
flowchart LR
    subgraph Usuario
      U[Usuário / Navegador]
    end

    subgraph App[Aplicações IA-TEST]
      FE[Frontend Svelte<br/>porta 8505]
      API[FastAPI / Chains<br/>porta 8504]
      DASH[Agent Dashboard<br/>porta 8507]
    end

    subgraph Infra[Infraestrutura]
      NEO4J[(Neo4j<br/>7687/7474)]
      OLLAMA[Ollama<br/>11434]
    end

    subgraph Orquestradores
      KESTRA[Kestra<br/>8080]
      N8N[N8N<br/>5678]
    end

    subgraph LLMs[LLMs Externos]
      GEMINI[Google Gemini<br/>GOOGLE_API_KEY]
    end

    U --> FE --> API
    DASH --> API

    API --> NEO4J
    API --> OLLAMA
    API --> GEMINI

    KESTRA <---> API
    KESTRA --> NEO4J

    N8N --> API
    N8N --> OLLAMA
    N8N --> GEMINI
```

**Como ler:**
- O usuário acessa o **Frontend** e o **Agent Dashboard**, que conversam com a API.
- A API centraliza acesso a **Neo4j**, LLMs (Gemini/Ollama) e lógica dos agentes.
- **Kestra** e **N8N** atuam como orquestradores de workflows, chamando a API e outros serviços.

---

## 2. Stacks Docker principais

```mermaid
flowchart TB
    subgraph StackCore["Stack core (perfil: core)"]
      DBNEO[database (Neo4j)]
      API[api]
      FE[front-end]
      DASH[agent-dashboard]
    end

    subgraph StackStreamlit["Stack streamlit (perfil: streamlit)"]
      BOT[bot]
      LOADER[loader]
      PDFBOT[pdf_bot]
    end

    subgraph StackTools["Stack tools (perfil: tools)"]
      MCP[mcp-manager]
      KESTRA[kestra<br/>ia-test-kestra]
    end

    subgraph StackN8N["Stack N8N runner (externo)"]
      N8NAPP[n8n-acessivel]
      N8NPG[(Postgres N8N)]
      N8NREDIS[(Redis N8N)]
    end

    DBNEO <--> API
    API <--> FE
    API <--> DASH

    BOT --> API
    LOADER --> API
    PDFBOT --> API

    MCP --> API
    KESTRA --> API

    N8NAPP --> API
    N8NAPP --> N8NPG
    N8NAPP --> N8NREDIS
```

**Ideia:** cada “Stack” corresponde a grupos de serviços que você sobe com perfis do `docker-compose.yml` ou com composes separados (no caso do N8N runner).

---

## 3. Fluxo de um job via Kestra (exemplo)

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuário (Kestra UI)
    participant K as Kestra (Flow)
    participant A as API IA-TEST
    participant N as Neo4j
    participant G as Gemini

    U->>K: Executa fluxo "ai-agent-calling-flows"
    K->>A: POST /orchestration/execute (dados do fluxo)
    A->>N: Consulta/atualiza grafo (contexto, tarefas, histórico)
    A->>G: Chamada LLM (prompt + contexto de Neo4j)
    G-->>A: Resposta do modelo
    A-->>K: Resultado estruturado (estado, logs, próxima tarefa)
    K-->>U: Exibe execução, logs e saída no painel
```

---

## 4. Fluxo de automação via N8N + agentes

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuário (N8N UI)
    participant N8 as N8N
    participant A as API IA-TEST
    participant O as Ollama
    participant G as Gemini

    U->>N8: Start workflow (trigger HTTP / agendado)
    N8->>A: Chamada HTTP (criar tarefa / recuperar contexto)
    A->>G: Pedido de raciocínio (Gemini) ou
    A->>O: Pedido para LLM local (Ollama)
    G-->>A: Resposta (plano/ação)
    O-->>A: Resposta (conteúdo)
    A-->>N8: Resultado da ação (JSON)
    N8-->>U: Atualiza execução no N8N
```

---

## 5. Próximos passos sugeridos para documentar

- Criar fluxos específicos por caso de uso:
  - `FLUXO-INGESTAO-DADOS.md` – como os dados entram no Neo4j e são disponibilizados.
  - `FLUXO-AGENTES-LLM.md` – detalhar como cada agente usa Gemini / Ollama.
- Para cada workflow importante no Kestra ou N8N, criar uma nota:
  - `KESRA-FLOW-<nome>.md` com:
    - link para o flow
    - print/resumo
    - um diagrama Mermaid simples com o passo a passo.





