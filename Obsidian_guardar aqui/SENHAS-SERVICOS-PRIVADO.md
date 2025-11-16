---
tags:
  - infraestrutura
  - docker
  - senhas
  - privado
---

> ⚠️ **Nota privada**  
> Esta nota contém usuários e senhas de serviços locais.  
> Não compartilhar fora do ambiente pessoal.

Conectada a: [[INFRA-SERVICOS-PORTAS]] e [[INDEX-SERVICOS-DOCKER]].

---

## Kestra

- **UI (login na Web)**
  - URL: `http://localhost:8080`
  - Usuário (e‑mail): `admin@localhost.dev`
  - Senha: `K3str4P1`
- **Banco de dados PostgreSQL (container `ia-test-kestra-postgres`)**
  - Host interno: `kestra-postgres`
  - Porta: `5432`
  - Banco: `kestra`
  - Usuário: `kestra`
  - Senha: `k3str4`

Relacionados:

- [[INFRA-SERVICOS-PORTAS#Kestra]]

---

## N8N

> Atualmente, o N8N acessível está rodando no container `n8n-acessivel`, conectado ao Postgres do stack `iaimplementation-n8nrunnerpostgresollama-...`.

- **UI**
  - URL: `http://localhost:5678`
- **Banco de dados PostgreSQL do stack N8N runner**
  - Container: `iaimplementation-n8nrunnerpostgresollama-ep0mt9-postgres-1`
  - Host interno usado pelos serviços: `postgres`
  - Porta: `5432`
  - Banco: `n8n`
  - Usuário: `loren_bechtelar`
  - Senha: `or7hazppwqcpvzvfn6cp8gin`

> Quando você migrar definitivamente para o stack **consolidado Dokploy + N8N**, atualizar esta seção para usar o Postgres consolidado (`dokploy-postgres-consolidado` / usuário `n8n`).

Relacionados:

- [[INFRA-SERVICOS-PORTAS#N8N]]
- [[INFRA-SERVICOS-PORTAS#Dokploy-e-N8N-consolidado]]

---

## Dokploy e PostgreSQL compartilhado (stack consolidado)

> Este stack está definido em `config/docker-compose-consolidado.yml` para uso futuro / unificação.

- **Dokploy (UI)**
  - URL: `http://localhost:3000`
  - Usuário / senha: usar as credenciais configuradas no próprio Dokploy (definir e depois registrar aqui se alterar).
- **PostgreSQL compartilhado**
  - Container: `dokploy-postgres-consolidado`
  - Porta interna: `5432`
  - Usuário padrão: `dokploy`
  - Senha padrão: `dokploy`
  - Banco Dokploy: `dokploy`
  - Banco N8N: `n8n` (criado via `POSTGRES_MULTIPLE_DATABASES`)

Relacionados:

- [[INFRA-SERVICOS-PORTAS#Dokploy-e-N8N-consolidado]]

---

## Neo4j e outros serviços do projeto

- **Neo4j**
  - URL Browser: `http://localhost:7474`
  - Usuário: `neo4j`
  - Senha inicial: `password` (pode ter sido alterada na primeira configuração; se mudar, atualizar aqui)

- **LLMs / APIs (chaves em `.env`)**
  - `GOOGLE_API_KEY`: chave da API Gemini
  - `OPENAI_API_KEY`: chave da API OpenAI (se usada)
  - Outros: `LANGCHAIN_API_KEY`, `SUPABASE_KEY`, etc.

> As chaves de API ficam no arquivo `.env` e não são copiadas para o repositório.  
> Esta nota serve apenas como lembrete de onde elas estão e como se relacionam com os serviços.

Relacionados:

- [[INFRA-SERVICOS-PORTAS#Stack-IA-TEST-core-e-streamlit]]





