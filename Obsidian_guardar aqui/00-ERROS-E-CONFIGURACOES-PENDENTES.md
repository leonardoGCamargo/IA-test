# 🔴 Erros e Configurações Pendentes - Documento Central

> **Documento Principal de Troubleshooting**  
> Última atualização: 2025-01-27  
> Status: 🟡 Em andamento

Este documento centraliza **todos os erros e configurações faltantes** do projeto, com links para explicações detalhadas de cada um.

---

## 📋 Índice Rápido

1. [🔴 Crítico - Bloqueia Funcionamento](#crítico)
2. [🟡 Importante - Funcionalidades Específicas](#importante)
3. [🟢 Opcional - Melhorias](#opcional)
4. [📊 Status Geral](#status-geral)
5. [🛠️ Scripts de Verificação](#scripts)
6. [📚 Links para Documentação](#documentação)

---

## 🔴 Crítico - Bloqueia Funcionamento

### 1. ✅ NEO4J_URI Configurada

**Status:** ✅ **RESOLVIDO**

**Configuração Atual:**
- ✅ URI: `neo4j+s://71de7683.databases.neo4j.io`
- ✅ Username: `neo4j`
- ✅ Password: Configurado
- ✅ Database: `neo4j`
- ✅ Instance ID: `71de7683`
- ✅ Instance Name: `My instance`

**Status da Conexão:**
- ✅ Configurado no `.env`
- ✅ Teste de conexão: Verificar abaixo

**Documentação:**
- [[../docs/NEO4J_AURA_SETUP|Guia Completo de Configuração Neo4j Aura]]
- [[../CONFIGURAR_AURA_DB|Configuração Rápida Aura DB]]
- [[COMO-CONFIGURAR-NEO4J-URI|Como Configurar NEO4J_URI]]

**Scripts Úteis:**
- `scripts/test_neo4j_connection.py` - Testar conexão
- `scripts/setup_aura_db.py` - Configuração interativa

**Prioridade:** ✅ **CONCLUÍDO**

---

## 🟡 Importante - Funcionalidades Específicas

### 2. ✅ Google API Key (Gemini)

**Status:** ✅ **CONFIGURADO**

**Configuração:**
- ✅ `GOOGLE_API_KEY` configurado
- ✅ Pronto para usar Google Gemini LLM e Embeddings

**Prioridade:** ✅ **CONCLUÍDO**

---

### 3. ✅ Neon (PostgreSQL Serverless)

**Status:** ✅ **CONFIGURADO**

**Configuração:**
- ✅ `NEON_PROJECT_ID` configurado
- ✅ MCP do Neon configurado

**Prioridade:** ✅ **CONCLUÍDO**

---

### 4. ✅ MongoDB Atlas

**Status:** ✅ **CONFIGURADO**

**Configuração:**
- ✅ `MONGODB_URI` configurado
- ✅ `MONGODB_DATABASE` configurado
- ✅ `MONGODB_ATLAS=true` configurado

**Prioridade:** ✅ **CONCLUÍDO**

---

### 5. ⚠️ Supabase

**Status:** ⚠️ **MCP CONFIGURADO** (verificar variáveis de ambiente)

**Nota:** Você mencionou que "subiu o MCP" do Supabase. Verifique se precisa configurar:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

**Onde Configurar:**
- Arquivo: `.env`

**Prioridade:** 🟡 **VERIFICAR**

---

### 6. OpenAI API Key

**Status:** ❌ Não configurado

**Quando é Necessário:**
- Se `LLM=gpt-4` ou `LLM=gpt-3.5`
- Se `EMBEDDING_MODEL=openai`

**Impacto:**
- ❌ Modelos OpenAI não funcionam
- ❌ Embeddings OpenAI não funcionam

**Onde Configurar:**
- Arquivo: `.env`
- Linha: `OPENAI_API_KEY=sk-...`

**Como Obter:**
1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova chave
3. Copie (ela só aparece uma vez!)

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#openai-api-key|Detalhes OpenAI API Key]]

**Prioridade:** 🟡 Média (só se usar OpenAI)

---

### 3. Google API Key

**Status:** ⚠️ Vazio (configurado mas sem valor)

**Quando é Necessário:**
- Se `EMBEDDING_MODEL=google-genai-embedding-001`

**Impacto:**
- ❌ Embeddings Google não funcionam

**Onde Configurar:**
- Arquivo: `.env`
- Linha: `GOOGLE_API_KEY=sua_chave_aqui`

**Como Obter:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Crie uma chave de API
3. Copie

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#google-api-key|Detalhes Google API Key]]

**Prioridade:** 🟡 Média (só se usar Google)

---

### 4. AWS Credentials (Bedrock)

**Status:** ❌ Não configurado

**Quando é Necessário:**
- Se `LLM=claudev2` ou outros modelos AWS Bedrock
- Se `EMBEDDING_MODEL=aws`

**Variáveis Faltantes:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION` (opcional, padrão: us-east-1)

**Impacto:**
- ❌ Modelos AWS Bedrock não funcionam

**Onde Configurar:**
- Arquivo: `.env`
- Linhas:
  ```bash
  AWS_ACCESS_KEY_ID=sua_access_key_id
  AWS_SECRET_ACCESS_KEY=sua_secret_access_key
  AWS_DEFAULT_REGION=us-east-1
  ```

**Como Obter:**
1. Acesse: https://aws.amazon.com/
2. Vá em IAM → Users → Security credentials
3. Crie Access Keys

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#aws-credentials-bedrock|Detalhes AWS Credentials]]

**Prioridade:** 🟡 Média (só se usar AWS)

---

### 5. Supabase

**Status:** ❌ Não configurado

**Quando é Necessário:**
- Se usar DB Manager com Supabase
- Para armazenar dados no Supabase

**Variáveis Faltantes:**
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_ROLE_KEY` (opcional)

**Impacto:**
- ❌ DB Manager não consegue usar Supabase

**Onde Configurar:**
- Arquivo: `.env`
- Linhas:
  ```bash
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Opcional
  ```

**Como Obter:**
1. Acesse: https://supabase.com/
2. Crie um projeto
3. Vá em Settings → API
4. Copie as chaves

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#supabase|Detalhes Supabase]]
- [[../docs/DB_MANAGER_README|DB Manager README]]

**Prioridade:** 🟡 Média (só se usar Supabase)

---

### 6. Neon Database

**Status:** ❌ Não configurado

**Quando é Necessário:**
- Se usar DB Manager com Neon
- Para PostgreSQL serverless

**Variáveis Faltantes:**
- `NEON_DATABASE_URL`
- `NEON_PROJECT_ID` (opcional)

**Impacto:**
- ❌ DB Manager não consegue usar Neon

**Onde Configurar:**
- Arquivo: `.env`
- Linhas:
  ```bash
  NEON_DATABASE_URL=postgresql://usuario:senha@ep-xxxxx.us-east-2.aws.neon.tech/dbname
  NEON_PROJECT_ID=xxxxx  # Opcional
  ```

**Como Obter:**
1. Acesse: https://neon.tech/
2. Crie um projeto
3. Vá em Connection Details
4. Copie a Connection String

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#neon-database|Detalhes Neon]]
- [[../docs/DB_MANAGER_README|DB Manager README]]

**Prioridade:** 🟡 Média (só se usar Neon)

---

### 7. MongoDB

**Status:** ❌ Não configurado

**Quando é Necessário:**
- Se usar DB Manager com MongoDB
- Para armazenar dados NoSQL

**Variáveis Faltantes:**
- `MONGODB_URI`
- `MONGODB_DATABASE` (padrão: default)
- `MONGODB_ATLAS` (true/false)

**Impacto:**
- ❌ DB Manager não consegue usar MongoDB

**Onde Configurar:**
- Arquivo: `.env`
- Linhas:
  ```bash
  MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/database
  MONGODB_DATABASE=default
  MONGODB_ATLAS=true  # se usar Atlas
  ```

**Como Obter:**
1. **MongoDB Atlas:**
   - Acesse: https://www.mongodb.com/cloud/atlas
   - Crie cluster gratuito
   - Vá em Connect → Connect your application
   - Copie a Connection String

2. **MongoDB Local:**
   - Use: `mongodb://localhost:27017/database`

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#mongodb|Detalhes MongoDB]]
- [[../docs/DB_MANAGER_README|DB Manager README]]

**Prioridade:** 🟡 Média (só se usar MongoDB)

---

## 🟢 Opcional - Melhorias

### 8. LangChain Tracing (Smith)

**Status:** ❌ Não configurado

**Quando é Necessário:**
- Para rastreamento e debugging de chains LangChain
- Para visualizar execuções no LangSmith

**Variáveis Faltantes:**
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_PROJECT`
- `LANGCHAIN_API_KEY`

**Impacto:**
- ⚠️ Sem rastreamento de chains (não crítico)

**Onde Configurar:**
- Arquivo: `.env`
- Linhas:
  ```bash
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_PROJECT=meu-projeto
  LANGCHAIN_API_KEY=ls_xxxxx...
  ```

**Como Obter:**
1. Acesse: https://smith.langchain.com/
2. Crie uma conta
3. Crie um projeto
4. Vá em Settings → API Keys

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#langchain-tracing-smith|Detalhes LangChain Tracing]]

**Prioridade:** 🟢 Baixa (opcional)

---

### 9. Obsidian Vault Path

**Status:** ❌ Não configurado

**Quando é Necessário:**
- Se usar integração com Obsidian
- Para sincronizar notas do projeto com Obsidian

**Variável Faltante:**
- `OBSIDIAN_VAULT_PATH`

**Impacto:**
- ❌ Integração com Obsidian não funciona

**Onde Configurar:**
- Arquivo: `.env`
- Linha: `OBSIDIAN_VAULT_PATH=C:/Users/Gianmarino L/Documents/Obsidian/IA-Test`

**Como Obter:**
- Caminho para a pasta do seu vault Obsidian
- Exemplo Windows: `C:/Users/SeuUsuario/Documents/Obsidian/MeuVault`

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#obsidian-vault-path|Detalhes Obsidian Vault Path]]

**Prioridade:** 🟢 Baixa (opcional)

---

### 10. Ollama Base URL

**Status:** ⚠️ Configurado com padrão

**Quando é Necessário:**
- Se usar modelos Ollama (LLM ou embeddings)
- Padrão funciona se Ollama estiver rodando

**Variável:**
- `OLLAMA_BASE_URL=http://host.docker.internal:11434` (Docker)
- ou `OLLAMA_BASE_URL=http://localhost:11434` (local)

**Impacto:**
- ⚠️ Modelos Ollama não funcionam se URL estiver errada

**Onde Ajustar:**
- Arquivo: `.env`
- Linha: `OLLAMA_BASE_URL=http://localhost:11434`

**Documentação:**
- [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES#ollama-base-url|Detalhes Ollama]]

**Prioridade:** 🟢 Baixa (geralmente funciona com padrão)

---

## 📊 Status Geral

### Resumo de Configurações

| Categoria | Total | Configuradas | Faltando | Percentual |
|-----------|-------|--------------|----------|------------|
| 🔴 Crítico | 1 | 0 | 1 | 0% |
| 🟡 Importante | 6 | 0 | 6 | 0% |
| 🟢 Opcional | 3 | 1 | 2 | 33% |
| **TOTAL** | **10** | **1** | **9** | **10%** |

### Checklist Rápido

- [ ] 🔴 NEO4J_URI configurada
- [ ] 🟡 OPENAI_API_KEY (se usar OpenAI)
- [ ] 🟡 GOOGLE_API_KEY (se usar Google)
- [ ] 🟡 AWS_ACCESS_KEY_ID (se usar AWS)
- [ ] 🟡 SUPABASE_URL + KEY (se usar Supabase)
- [ ] 🟡 NEON_DATABASE_URL (se usar Neon)
- [ ] 🟡 MONGODB_URI (se usar MongoDB)
- [ ] 🟢 LANGCHAIN_API_KEY (opcional)
- [ ] 🟢 OBSIDIAN_VAULT_PATH (opcional)
- [ ] 🟢 OLLAMA_BASE_URL (ajustar se necessário)

---

## 🛠️ Scripts de Verificação

### Verificar Todas as Configurações

```bash
python scripts/check_missing_keys.py
```

Este script mostra:
- ✅ O que está configurado
- ❌ O que está faltando
- 📊 Percentual de conclusão
- 💡 Recomendações

### Testar Conexão Neo4j

```bash
python scripts/test_neo4j_connection.py
```

Verifica se a conexão com Neo4j Aura está funcionando.

### Configurar Neo4j Aura Interativamente

```bash
python scripts/setup_aura_db.py
```

Script interativo para configurar Neo4j Aura DB.

### Gerar Relatório JSON

```bash
python scripts/generate_errors_report.py
```

Gera relatório completo em JSON: `Obsidian_guardar aqui/errors_report.json`

---

## 📚 Documentação Relacionada

### Documentos Principais

1. [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES|Lista Completa de Chaves e Configurações]]
   - Explicação detalhada de cada configuração
   - Como obter cada chave
   - Onde preencher

2. [[../docs/NEO4J_AURA_SETUP|Configuração do Neo4j Aura DB]]
   - Guia completo de configuração
   - Como conectar no Neo4j Desktop
   - Troubleshooting

3. [[../docs/ONDE_DADOS_SAO_SALVOS|Onde os Dados do Projeto São Salvos]]
   - Explicação de onde cada dado está
   - Como sincronizar para Neo4j
   - Estrutura de dados

4. [[../docs/IMPORTAR_DADOS_NEO4J_AURA|Como Importar Dados para Neo4j Aura]]
   - Via interface web
   - Via código do projeto
   - Comparação de métodos

### Documentos de Agentes

- [[Agentes/Orchestrator|Orchestrator]] - Coordenador central
- [[Agentes/System-Health|System Health Agent]] - Diagnóstico
- [[Agentes/DB-Manager|DB Manager]] - Gerenciamento de bancos
- [[Agentes/MCP-Manager|MCP Manager]] - Gerenciamento MCP

### Documentos de Setup

- [[PROJETO-IA-TEST|Mapeamento Completo do Projeto]]
- [[OTIMIZACAO_AGENTES|Otimização e Consolidação de Agentes]]
- [[VIDEOS_MCP_AGENTES|Vídeos sobre MCP e Agentes]]

---

## 🎯 Plano de Ação Recomendado

### Fase 1: Crítico (Fazer Agora)

1. ✅ **Configurar NEO4J_URI**
   - Acessar console Neo4j Aura
   - Copiar Connection URI
   - Editar `.env`
   - Testar: `python scripts/test_neo4j_connection.py`

### Fase 2: Importante (Se Usar)

2. ⏳ **Configurar APIs conforme necessário:**
   - OpenAI (se usar GPT)
   - Google (se usar embeddings Google)
   - AWS (se usar Bedrock)

3. ⏳ **Configurar Bancos de Dados (se usar):**
   - Supabase (se usar)
   - Neon (se usar)
   - MongoDB (se usar)

### Fase 3: Opcional (Melhorias)

4. ⏳ **Configurar Opcionais:**
   - LangChain Tracing (para debugging)
   - Obsidian Vault Path (para integração)
   - Ajustar Ollama URL (se necessário)

---

## 🔍 Como Verificar Status

### Via Dashboard

1. Execute: `streamlit run src/apps/agent_dashboard.py`
2. Vá na aba **"🔍 Diagnóstico"**
3. Clique em **"🔄 Executar Diagnóstico Completo"**
4. Veja todos os problemas encontrados

### Via Código

```python
from src.agents.system_health_agent import get_system_health_agent

health = get_system_health_agent()
report = health.run_full_health_check()

# Ver problemas
for issue in report.diagnostic_issues:
    print(f"{issue.severity.value}: {issue.title}")
    print(f"  {issue.description}")
```

### Via Script

```bash
python scripts/check_missing_keys.py
```

---

## 📝 Notas Importantes

### ⚠️ Segurança

- **NUNCA** commite o arquivo `.env` no Git
- Use variáveis de ambiente em produção
- Rotacione senhas periodicamente

### 🔄 Atualizações

Este documento deve ser atualizado sempre que:
- Novas configurações forem adicionadas
- Problemas forem resolvidos
- Novos erros forem detectados

### 📊 Última Verificação

Execute periodicamente:
```bash
python scripts/check_missing_keys.py
```

---

## 🆘 Precisa de Ajuda?

1. **Verifique a documentação:**
   - [[../docs/CHAVES_E_CONFIGURACOES_FALTANTES|Lista Completa]]
   - [[../docs/NEO4J_AURA_SETUP|Setup Neo4j Aura]]

2. **Execute diagnósticos:**
   - `python scripts/check_missing_keys.py`
   - Dashboard → Diagnóstico

3. **Consulte logs:**
   - Verifique mensagens de erro
   - Execute testes de conexão

---

## 🏷️ Tags

#erros #configurações #troubleshooting #setup #neo4j #apis #bancos-de-dados

---

**Última atualização:** 2025-01-27  
**Próxima revisão:** Após resolver itens críticos
