---
tags:
  - infraestrutura
  - docker
  - urls
---

## Visão geral

Mapa dos serviços principais do ambiente local, com portas e URLs.  
Para usuários e senhas, veja: [[SENHAS-SERVICOS-PRIVADO]].

---

## N8N

- **Descrição**: Automação de workflows
- **Container atual de acesso direto**: `n8n-acessivel`
- **URL**: `http://localhost:5678`
- **Porta**: `5678`
- **Banco de dados**: PostgreSQL (instância do stack N8N runner/Dokploy antigo)
- **Relacionado**:
  - [[SENHAS-SERVICOS-PRIVADO#N8N]]
  - [[INDEX-SERVICOS-DOCKER]]

---

## Kestra

- **Descrição**: Orquestrador de dados / workflows
- **Stack atual (independente do Dokploy)**:
  - App: container `ia-test-kestra`
  - DB: container `ia-test-kestra-postgres`
- **URL da UI**: `http://localhost:8080`
- **Portas**:
  - `8080` → UI / API
- **Banco de dados**:
  - Host interno: `kestra-postgres`
  - Banco: `kestra`
- **Relacionado**:
  - [[SENHAS-SERVICOS-PRIVADO#Kestra]]
  - [[INDEX-SERVICOS-DOCKER]]

---

## Dokploy e N8N consolidado

> Observação: este stack consolidado está preparado em `config/docker-compose-consolidado.yml` e scripts `scripts/migrar_automatico.py` e `scripts/iniciar_consolidado.ps1`.  
> No momento, você está usando o N8N de outro stack, mas esta seção documenta a configuração consolidada para uso futuro.

- **Dokploy (UI)**:
  - URL: `http://localhost:3000`
  - Porta: `3000`
- **N8N (consolidado via Dokploy Postgres)**:
  - URL: `http://localhost:5678`
  - Porta: `5678`
- **PostgreSQL compartilhado**:
  - Container: `dokploy-postgres-consolidado`
  - Databases: `dokploy`, `n8n`
- **Relacionado**:
  - [[SENHAS-SERVICOS-PRIVADO#Dokploy-e-PostgreSQL-compartilhado]]

---

## Stack IA-TEST core e streamlit

Conforme `config/docker-compose.yml` (perfil `core` e `streamlit`):

- **Neo4j**
  - URL Browser: `http://localhost:7474`
  - Bolt: `neo4j://localhost:7687`
  - Portas: `7474`, `7687`
- **API FastAPI**
  - URL: `http://localhost:8504`
  - Porta: `8504`
- **Frontend (Svelte)**
  - URL: `http://localhost:8505`
  - Porta: `8505`
- **Agent Dashboard**
  - URL: `http://localhost:8507`
  - Porta: `8507`
- **Bots Streamlit**
  - Bot principal: `http://localhost:8501`
  - Loader: `http://localhost:8502`
  - PDF Bot: `http://localhost:8503`
- **MCP Manager**
  - URL: `http://localhost:8506`
  - Porta: `8506`

Relacionado:

- Credenciais de Neo4j e outras integrações: [[SENHAS-SERVICOS-PRIVADO#Neo4j-e-outros-serviços-do-projeto]]

---

## Ollama

- **Descrição**: LLM local (opcional)
- **URL**: `http://localhost:11434`
- **Porta**: `11434`
- **Containers possíveis**:
  - `ia-test-ollama` (stack IA-TEST)
  - `n8n-ollama-consolidado` (stack consolidado N8N)








