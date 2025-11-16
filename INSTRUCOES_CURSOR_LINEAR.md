# 📋 Instruções para Criar Issues no Linear via Cursor
Como você já conectou sua conta do Cursor ao Linear, você pode criar as issues diretamente no chat do Cursor.
## 🚀 Método 1: Criar Issues Individualmente
Para cada issue, use este comando no chat do Cursor:
```
Crie uma issue no Linear com:
- Título: [TÍTULO]
- Prioridade: [PRIORIDADE]
- Descrição: [DESCRIÇÃO]
- Labels: [LABELS]
```

## 📝 Issues para Criar

### 🔴 P0 - Crítico (Urgent)

🔴 **001: Observabilidade Incompleta**

**Prioridade:** URGENT
**Labels:** backend, observability, critical
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
LangSmith está configurado mas não totalmente integrado. Falta:
- Métricas de performance (Prometheus)
- Logs estruturados (structlog)
- Alertas automáticos
- Dashboard de observabilidade

**Arquivos:**
- src/apps/api_v2.py
- src/agents/orchestrator_langgraph.py

**Acceptance Criteria:**
- [ ] LangSmith totalmente integrado
- [ ] Métricas expostas via Prometheus
- [ ] Logs estruturados em JSON
- [ ] Alertas configurados

---

🔴 **002: Task Queue Não Persistente**

**Prioridade:** URGENT
**Labels:** backend, infrastructure, critical
**Estimativa:** 3 dias (se aplicável)

**Descrição:**
Tarefas estão em memória e são perdidas em restart. Implementar:
- Redis/Celery para task queue
- Persistência em Neo4j ou PostgreSQL
- Retry automático
- Priorização de tarefas

**Arquivos:**
- src/agents/orchestrator_langgraph.py:502-514
- src/agents/orchestrator.py:145

**Acceptance Criteria:**
- [ ] Tasks persistem em Redis
- [ ] Retry automático implementado
- [ ] Priorização funcionando
- [ ] Histórico de tarefas

---

🔴 **003: Cache Semântico Não Implementado**

**Prioridade:** URGENT
**Labels:** backend, performance, critical
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Chamadas duplicadas ao LLM aumentam custo e latência. Implementar:
- Redis cache para LLM
- Cache de embeddings
- Cache de resultados de agentes

**Arquivos:**
- src/apps/chains.py
- src/agents/orchestrator_langgraph.py

**Acceptance Criteria:**
- [ ] Cache de LLM configurado
- [ ] Cache de embeddings
- [ ] Redução de 50%+ em chamadas duplicadas

---

🔴 **004: Rate Limiting Ausente**

**Prioridade:** URGENT
**Labels:** backend, security, critical
**Estimativa:** 1 dias (se aplicável)

**Descrição:**
API sem rate limiting, risco de sobrecarga e DDoS. Implementar:
- Rate limiting por IP
- Quotas por usuário
- Slowapi integration

**Arquivos:**
- src/apps/api_v2.py

**Acceptance Criteria:**
- [ ] Rate limiting em todos os endpoints
- [ ] Quotas configuráveis
- [ ] Mensagens de erro claras

---

🔴 **005: Autenticação Não Implementada**

**Prioridade:** URGENT
**Labels:** backend, frontend, security, critical
**Estimativa:** 4 dias (se aplicável)

**Descrição:**
Sistema sem autenticação, API pública. Implementar:
- NextAuth ou Clerk no frontend
- JWT no backend
- Middleware de autenticação
- Proteção de rotas

**Arquivos:**
- src/apps/api_v2.py
- frontend-nextjs/

**Acceptance Criteria:**
- [ ] Autenticação funcionando
- [ ] Rotas protegidas
- [ ] JWT tokens
- [ ] Refresh tokens

---

🔴 **006: Error Handling Inconsistente**

**Prioridade:** URGENT
**Labels:** backend, reliability, critical
**Estimativa:** 3 dias (se aplicável)

**Descrição:**
Erros genéricos, falta circuit breakers, sem retry logic. Implementar:
- Circuit breakers
- Retry logic
- Sentry integration
- Error tracking

**Arquivos:**
- src/agents/orchestrator_langgraph.py
- src/apps/api_v2.py

**Acceptance Criteria:**
- [ ] Circuit breakers implementados
- [ ] Retry logic em chamadas externas
- [ ] Sentry configurado
- [ ] Erros rastreados

---

🔴 **007: Integração Kestra Incompleta**

**Prioridade:** URGENT
**Labels:** backend, integration, critical
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Endpoints Kestra retornam "not yet implemented". Implementar:
- Cliente Kestra Python
- Integração com API
- Testes de workflows

**Arquivos:**
- src/apps/api_v2.py:339-345
- kestra_workflows/

**Acceptance Criteria:**
- [ ] Workflows executáveis via API
- [ ] Status de execução
- [ ] Resultados retornados

---

🔴 **008: WebSocket Implementation Incompleta**

**Prioridade:** URGENT
**Labels:** backend, frontend, real-time, critical
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Socket.IO configurado mas não totalmente testado. Melhorar:
- Reconexão automática robusta
- Queue de mensagens
- Testes de WebSocket

**Arquivos:**
- src/apps/api_v2.py:46-110
- frontend-nextjs/src/hooks/useWebSocket.ts

**Acceptance Criteria:**
- [ ] Reconexão automática
- [ ] Mensagens não se perdem
- [ ] Testes passando

---

### 🟡 P1 - Importante (High)

🟡 **009: Persistência de Memória Parcial**

**Prioridade:** HIGH
**Labels:** backend, memory, important
**Estimativa:** 3 dias (se aplicável)

**Descrição:**
Memória do LangGraph não persistida. Implementar salvamento estruturado no Neo4j.

**Arquivos:**
- src/agents/orchestrator_langgraph.py:335

---

🟡 **010: Testes Insuficientes**

**Prioridade:** HIGH
**Labels:** testing, quality, important
**Estimativa:** 5 dias (se aplicável)

**Descrição:**
Cobertura de testes ~5%. Adicionar testes unitários e de integração.

**Arquivos:**
- tests/

---

🟡 **011: Documentação Desatualizada**

**Prioridade:** HIGH
**Labels:** documentation, important
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Documentação não reflete Next.js. Atualizar docs principais.

**Arquivos:**
- docs/
- readme.md

---

🟡 **012: Docker Compose Pode Ser Otimizado**

**Prioridade:** HIGH
**Labels:** infrastructure, docker, important
**Estimativa:** 1 dias (se aplicável)

**Descrição:**
Adicionar health checks, resource limits, otimizar volumes.

**Arquivos:**
- config/docker-compose.yml

---

🟡 **013: Frontend Next.js Incompleto**

**Prioridade:** HIGH
**Labels:** frontend, ui, important
**Estimativa:** 5 dias (se aplicável)

**Descrição:**
Faltam páginas: workflows, memória, monitoramento.

**Arquivos:**
- frontend-nextjs/src/app/dashboard/

---

🟡 **014: Código Duplicado**

**Prioridade:** HIGH
**Labels:** refactoring, important
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Refatorar código duplicado entre orchestrators.

**Arquivos:**
- src/agents/orchestrator.py
- src/agents/orchestrator_langgraph.py

---

🟡 **015: Variáveis de Ambiente Não Validadas**

**Prioridade:** HIGH
**Labels:** backend, configuration, important
**Estimativa:** 1 dias (se aplicável)

**Descrição:**
Adicionar validação de variáveis de ambiente no startup.

---

🟡 **016: Falta de CI/CD**

**Prioridade:** HIGH
**Labels:** devops, ci-cd, important
**Estimativa:** 3 dias (se aplicável)

**Descrição:**
Implementar GitHub Actions para CI/CD.

---

🟡 **017: Logging Não Estruturado**

**Prioridade:** HIGH
**Labels:** backend, logging, important
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Implementar structlog para logs estruturados.

---

🟡 **018: Falta de Métricas de Negócio**

**Prioridade:** HIGH
**Labels:** analytics, important
**Estimativa:** 3 dias (se aplicável)

**Descrição:**
Adicionar métricas customizadas e analytics.

---

🟡 **019: Falta de Backup Automático**

**Prioridade:** HIGH
**Labels:** infrastructure, backup, important
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Implementar backup automático do Neo4j.

---

🟡 **020: Falta de Versionamento de API**

**Prioridade:** HIGH
**Labels:** api, important
**Estimativa:** 1 dias (se aplicável)

**Descrição:**
Implementar versionamento semântico da API.

---

🟡 **021: Falta de Validação de Inputs**

**Prioridade:** HIGH
**Labels:** backend, validation, important
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Melhorar validação de inputs com Pydantic.

---

🟡 **022: Falta de Paginação**

**Prioridade:** HIGH
**Labels:** backend, performance, important
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Implementar paginação em endpoints de lista.

---

🟡 **023: Falta de Filtros e Busca**

**Prioridade:** HIGH
**Labels:** frontend, ui, important
**Estimativa:** 2 dias (se aplicável)

**Descrição:**
Adicionar filtros e busca na UI.

---

### 🟢 P2 - Melhorias (Medium)

🟢 **024 a L-047: Melhorias Opcionais**

**Prioridade:** MEDIUM
**Labels:** enhancement
**Estimativa:** None dias (se aplicável)

**Descrição:**

---

