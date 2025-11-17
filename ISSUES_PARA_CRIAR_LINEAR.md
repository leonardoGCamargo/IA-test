# 📋 Issues para Criar no Linear - Use no Chat do Cursor

Como o MCP do Linear está ativo, você pode criar as issues diretamente no chat do Cursor usando este comando:

```
Crie todas as 47 issues abaixo no Linear usando o MCP do Linear. Para cada issue:
1. Use o título completo (ex: "L-001: Observabilidade Incompleta")
2. Mapeie prioridades: P0 → urgent, P1 → high, P2 → medium  
3. Inclua toda a descrição, arquivos e acceptance criteria
4. Adicione as labels apropriadas
5. Configure a estimativa em dias quando disponível
```

---

## 🔴 P0 - Crítico (8 issues) - Prioridade: urgent

### L-001: Observabilidade Incompleta
**Labels:** backend, observability, critical  
**Estimate:** 2-3 days

**Description:**
LangSmith está configurado mas não totalmente integrado. Falta:
- Métricas de performance (Prometheus)
- Logs estruturados (structlog)
- Alertas automáticos
- Dashboard de observabilidade

**Files:**
- `src/apps/api_v2.py`
- `src/agents/orchestrator_langgraph.py`

**Acceptance Criteria:**
- [ ] LangSmith totalmente integrado
- [ ] Métricas expostas via Prometheus
- [ ] Logs estruturados em JSON
- [ ] Alertas configurados

---

### L-002: Task Queue Não Persistente
**Labels:** backend, infrastructure, critical  
**Estimate:** 3-4 days

**Description:**
Tarefas estão em memória e são perdidas em restart. Implementar:
- Redis/Celery para task queue
- Persistência em Neo4j ou PostgreSQL
- Retry automático
- Priorização de tarefas

**Files:**
- `src/agents/orchestrator_langgraph.py:502-514`
- `src/agents/orchestrator.py:145`

**Acceptance Criteria:**
- [ ] Tasks persistem em Redis
- [ ] Retry automático implementado
- [ ] Priorização funcionando
- [ ] Histórico de tarefas

---

### L-003: Cache Semântico Não Implementado
**Labels:** backend, performance, critical  
**Estimate:** 2 days

**Description:**
Chamadas duplicadas ao LLM aumentam custo e latência. Implementar:
- Redis cache para LLM
- Cache de embeddings
- Cache de resultados de agentes

**Files:**
- `src/apps/chains.py`
- `src/agents/orchestrator_langgraph.py`

**Acceptance Criteria:**
- [ ] Cache de LLM configurado
- [ ] Cache de embeddings
- [ ] Redução de 50%+ em chamadas duplicadas

---

### L-004: Rate Limiting Ausente
**Labels:** backend, security, critical  
**Estimate:** 1 day

**Description:**
API sem rate limiting, risco de sobrecarga e DDoS. Implementar:
- Rate limiting por IP
- Quotas por usuário
- Slowapi integration

**Files:**
- `src/apps/api_v2.py`

**Acceptance Criteria:**
- [ ] Rate limiting em todos os endpoints
- [ ] Quotas configuráveis
- [ ] Mensagens de erro claras

---

### L-005: Autenticação Não Implementada
**Labels:** backend, frontend, security, critical  
**Estimate:** 4-5 days

**Description:**
Sistema sem autenticação, API pública. Implementar:
- NextAuth ou Clerk no frontend
- JWT no backend
- Middleware de autenticação
- Proteção de rotas

**Files:**
- `src/apps/api_v2.py`
- `frontend-nextjs/`

**Acceptance Criteria:**
- [ ] Autenticação funcionando
- [ ] Rotas protegidas
- [ ] JWT tokens
- [ ] Refresh tokens

---

### L-006: Error Handling Inconsistente
**Labels:** backend, reliability, critical  
**Estimate:** 3 days

**Description:**
Erros genéricos, falta circuit breakers, sem retry logic. Implementar:
- Circuit breakers
- Retry logic
- Sentry integration
- Error tracking

**Files:**
- `src/agents/orchestrator_langgraph.py`
- `src/apps/api_v2.py`

**Acceptance Criteria:**
- [ ] Circuit breakers implementados
- [ ] Retry logic em chamadas externas
- [ ] Sentry configurado
- [ ] Erros rastreados

---

### L-007: Integração Kestra Incompleta
**Labels:** backend, integration, critical  
**Estimate:** 2-3 days

**Description:**
Endpoints Kestra retornam "not yet implemented". Implementar:
- Cliente Kestra Python
- Integração com API
- Testes de workflows

**Files:**
- `src/apps/api_v2.py:339-345`
- `kestra_workflows/`

**Acceptance Criteria:**
- [ ] Workflows executáveis via API
- [ ] Status de execução
- [ ] Resultados retornados

---

### L-008: WebSocket Implementation Incompleta
**Labels:** backend, frontend, real-time, critical  
**Estimate:** 2 days

**Description:**
Socket.IO configurado mas não totalmente testado. Melhorar:
- Reconexão automática robusta
- Queue de mensagens
- Testes de WebSocket

**Files:**
- `src/apps/api_v2.py:46-110`
- `frontend-nextjs/src/hooks/useWebSocket.ts`

**Acceptance Criteria:**
- [ ] Reconexão automática
- [ ] Mensagens não se perdem
- [ ] Testes passando

---

## 🟡 P1 - Importante (15 issues) - Prioridade: high

### L-009: Persistência de Memória Parcial
**Labels:** backend, memory, important  
**Estimate:** 3 days

**Description:**
Memória do LangGraph não persistida. Implementar salvamento estruturado no Neo4j.

**Files:**
- `src/agents/orchestrator_langgraph.py:335`

---

### L-010: Testes Insuficientes
**Labels:** testing, quality, important  
**Estimate:** 5-7 days

**Description:**
Cobertura de testes ~5%. Adicionar testes unitários e de integração.

**Files:**
- `tests/`

---

### L-011: Documentação Desatualizada
**Labels:** documentation, important  
**Estimate:** 2-3 days

**Description:**
Documentação não reflete Next.js. Atualizar docs principais.

**Files:**
- `docs/`
- `readme.md`

---

### L-012: Docker Compose Pode Ser Otimizado
**Labels:** infrastructure, docker, important  
**Estimate:** 1 day

**Description:**
Adicionar health checks, resource limits, otimizar volumes.

**Files:**
- `config/docker-compose.yml`

---

### L-013: Frontend Next.js Incompleto
**Labels:** frontend, ui, important  
**Estimate:** 5-7 days

**Description:**
Faltam páginas: workflows, memória, monitoramento.

**Files:**
- `frontend-nextjs/src/app/dashboard/`

---

### L-014: Código Duplicado
**Labels:** refactoring, important  
**Estimate:** 2-3 days

**Description:**
Refatorar código duplicado entre orchestrators.

**Files:**
- `src/agents/orchestrator.py`
- `src/agents/orchestrator_langgraph.py`

---

### L-015: Variáveis de Ambiente Não Validadas
**Labels:** backend, configuration, important  
**Estimate:** 1 day

**Description:**
Adicionar validação de variáveis de ambiente no startup.

---

### L-016: Falta de CI/CD
**Labels:** devops, ci-cd, important  
**Estimate:** 3-4 days

**Description:**
Implementar GitHub Actions para CI/CD.

---

### L-017: Logging Não Estruturado
**Labels:** backend, logging, important  
**Estimate:** 2 days

**Description:**
Implementar structlog para logs estruturados.

---

### L-018: Falta de Métricas de Negócio
**Labels:** analytics, important  
**Estimate:** 3 days

**Description:**
Adicionar métricas customizadas e analytics.

---

### L-019: Falta de Backup Automático
**Labels:** infrastructure, backup, important  
**Estimate:** 2 days

**Description:**
Implementar backup automático do Neo4j.

---

### L-020: Falta de Versionamento de API
**Labels:** api, important  
**Estimate:** 1 day

**Description:**
Implementar versionamento semântico da API.

---

### L-021: Falta de Validação de Inputs
**Labels:** backend, validation, important  
**Estimate:** 2 days

**Description:**
Melhorar validação de inputs com Pydantic.

---

### L-022: Falta de Paginação
**Labels:** backend, performance, important  
**Estimate:** 2 days

**Description:**
Implementar paginação em endpoints de lista.

---

### L-023: Falta de Filtros e Busca
**Labels:** frontend, ui, important  
**Estimate:** 2 days

**Description:**
Adicionar filtros e busca na UI.

---

## 🟢 P2 - Melhorias (24 issues) - Prioridade: medium

As issues L-024 a L-047 estão no arquivo `LINEAR_ISSUES_COMPLETE.md`. Use o comando:

```
Crie as issues L-024 a L-047 do arquivo LINEAR_ISSUES_COMPLETE.md no Linear com prioridade medium
```

---

**Total:** 47 issues


