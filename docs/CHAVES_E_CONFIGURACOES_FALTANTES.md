# 🔑 Lista Completa de Chaves e Configurações Faltantes

Este documento lista todas as chaves de API, senhas, URLs e configurações que podem estar faltando no projeto, organizadas por categoria e prioridade.

## 📋 Índice

1. [🔴 Crítico - Essenciais para Funcionamento](#crítico)
2. [🟡 Importante - Funcionalidades Específicas](#importante)
3. [🟢 Opcional - Melhorias e Recursos Extras](#opcional)
4. [📝 Onde Preencher](#onde-preencher)

---

## 🔴 Crítico - Essenciais para Funcionamento

### 1. Neo4j Aura DB ⚠️ **FALTANDO URI**

**Status:** ✅ Senha configurada | ❌ URI faltando

**Variáveis:**
```bash
NEO4J_URI=neo4j+s://SUBSTITUA_PELA_URI_DO_AURA_DB.databases.neo4j.io  # ❌ FALTANDO
NEO4J_USERNAME=neo4j  # ✅ Configurado
NEO4J_PASSWORD=zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM  # ✅ Configurado
```

**Onde obter:**
- Acesse: https://console.neo4j.io/
- Clique na sua instância Aura DB
- Copie a Connection URI

**Onde preencher:**
- Arquivo: `.env` (raiz do projeto)
- Linha: `NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io`

**Impacto:** Sem isso, o projeto não consegue conectar ao banco de dados.

---

## 🟡 Importante - Funcionalidades Específicas

### 2. OpenAI API Key

**Status:** ❌ Não configurado

**Variável:**
```bash
OPENAI_API_KEY=sk-...  # ❌ FALTANDO
```

**Quando é necessário:**
- Se `LLM=gpt-4` ou `LLM=gpt-3.5`
- Se `EMBEDDING_MODEL=openai`

**Onde obter:**
1. Acesse: https://platform.openai.com/api-keys
2. Faça login
3. Clique em "Create new secret key"
4. Copie a chave (ela só aparece uma vez!)

**Onde preencher:**
- Arquivo: `.env`
- Linha: `OPENAI_API_KEY=sk-...`

**Impacto:** Funcionalidades que usam OpenAI não funcionarão.

---

### 3. Google API Key

**Status:** ⚠️ Vazio (configurado mas sem valor)

**Variável:**
```bash
GOOGLE_API_KEY=  # ⚠️ VAZIO
```

**Quando é necessário:**
- Se `EMBEDDING_MODEL=google-genai-embedding-001`

**Onde obter:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave

**Onde preencher:**
- Arquivo: `.env`
- Linha: `GOOGLE_API_KEY=sua_chave_aqui`

**Impacto:** Embeddings do Google não funcionarão.

---

### 4. AWS Credentials (Bedrock)

**Status:** ❌ Não configurado

**Variáveis:**
```bash
AWS_ACCESS_KEY_ID=  # ❌ FALTANDO
AWS_SECRET_ACCESS_KEY=  # ❌ FALTANDO
AWS_DEFAULT_REGION=us-east-1  # ⚠️ Padrão, pode precisar ajustar
```

**Quando é necessário:**
- Se `LLM=claudev2` ou outros modelos AWS Bedrock
- Se `EMBEDDING_MODEL=aws`

**Onde obter:**
1. Acesse: https://aws.amazon.com/
2. Faça login no AWS Console
3. Vá para IAM → Users → Security credentials
4. Crie Access Keys
5. Anote Access Key ID e Secret Access Key

**Onde preencher:**
- Arquivo: `.env`
- Linhas:
  ```bash
  AWS_ACCESS_KEY_ID=sua_access_key_id
  AWS_SECRET_ACCESS_KEY=sua_secret_access_key
  AWS_DEFAULT_REGION=us-east-1  # ou sua região
  ```

**Impacto:** Modelos AWS Bedrock não funcionarão.

---

### 5. Supabase

**Status:** ❌ Não configurado

**Variáveis:**
```bash
SUPABASE_URL=https://seu-projeto.supabase.co  # ❌ FALTANDO
SUPABASE_KEY=sua-anon-key  # ❌ FALTANDO
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key  # ❌ FALTANDO (opcional)
```

**Quando é necessário:**
- Se usar o DB Manager com Supabase
- Para armazenar dados no Supabase

**Onde obter:**
1. Acesse: https://supabase.com/
2. Crie um projeto (gratuito disponível)
3. Vá em Settings → API
4. Copie:
   - Project URL → `SUPABASE_URL`
   - anon public key → `SUPABASE_KEY`
   - service_role key → `SUPABASE_SERVICE_ROLE_KEY` (opcional, mais permissões)

**Onde preencher:**
- Arquivo: `.env`
- Linhas:
  ```bash
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Opcional
  ```

**Impacto:** DB Manager não conseguirá usar Supabase.

---

### 6. Neon Database

**Status:** ❌ Não configurado

**Variáveis:**
```bash
NEON_DATABASE_URL=postgresql://usuario:senha@host/database  # ❌ FALTANDO
NEON_PROJECT_ID=seu-project-id  # ❌ FALTANDO (opcional)
```

**Quando é necessário:**
- Se usar o DB Manager com Neon
- Para PostgreSQL serverless

**Onde obter:**
1. Acesse: https://neon.tech/
2. Crie uma conta (gratuita)
3. Crie um projeto
4. Vá em Connection Details
5. Copie a Connection String → `NEON_DATABASE_URL`
6. Project ID está na URL → `NEON_PROJECT_ID`

**Onde preencher:**
- Arquivo: `.env`
- Linhas:
  ```bash
  NEON_DATABASE_URL=postgresql://usuario:senha@ep-xxxxx.us-east-2.aws.neon.tech/dbname
  NEON_PROJECT_ID=xxxxx  # Opcional
  ```

**Impacto:** DB Manager não conseguirá usar Neon.

---

### 7. MongoDB

**Status:** ❌ Não configurado

**Variáveis:**
```bash
MONGODB_URI=mongodb://usuario:senha@host:porta/database  # ❌ FALTANDO
MONGODB_DATABASE=default  # ⚠️ Padrão
MONGODB_ATLAS=false  # true se usar MongoDB Atlas
```

**Quando é necessário:**
- Se usar o DB Manager com MongoDB
- Para armazenar dados NoSQL

**Onde obter:**
1. **MongoDB Atlas (recomendado):**
   - Acesse: https://www.mongodb.com/cloud/atlas
   - Crie cluster gratuito
   - Vá em Connect → Connect your application
   - Copie a Connection String → `MONGODB_URI`
   - Substitua `<password>` pela senha do usuário
   - Configure `MONGODB_ATLAS=true`

2. **MongoDB Local:**
   - Instale MongoDB localmente
   - Use: `mongodb://localhost:27017/database`

**Onde preencher:**
- Arquivo: `.env`
- Linhas:
  ```bash
  MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/database
  MONGODB_DATABASE=default
  MONGODB_ATLAS=true  # se usar Atlas
  ```

**Impacto:** DB Manager não conseguirá usar MongoDB.

---

## 🟢 Opcional - Melhorias e Recursos Extras

### 8. LangChain Tracing (Smith)

**Status:** ❌ Não configurado

**Variáveis:**
```bash
LANGCHAIN_TRACING_V2=false  # ⚠️ Desabilitado
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com  # ✅ Padrão
LANGCHAIN_PROJECT=  # ❌ FALTANDO
LANGCHAIN_API_KEY=  # ❌ FALTANDO
```

**Quando é necessário:**
- Para rastreamento e debugging de chains LangChain
- Para visualizar execuções no LangSmith

**Onde obter:**
1. Acesse: https://smith.langchain.com/
2. Crie uma conta
3. Crie um projeto
4. Vá em Settings → API Keys
5. Copie a API Key → `LANGCHAIN_API_KEY`
6. Nome do projeto → `LANGCHAIN_PROJECT`

**Onde preencher:**
- Arquivo: `.env`
- Linhas:
  ```bash
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_PROJECT=meu-projeto
  LANGCHAIN_API_KEY=ls_xxxxx...
  ```

**Impacto:** Sem rastreamento de chains (não crítico).

---

### 9. Obsidian Vault Path

**Status:** ❌ Não configurado

**Variável:**
```bash
OBSIDIAN_VAULT_PATH=  # ❌ FALTANDO
```

**Quando é necessário:**
- Se usar integração com Obsidian
- Para sincronizar notas do projeto com Obsidian

**Onde obter:**
- Caminho para a pasta do seu vault Obsidian
- Exemplo Windows: `C:/Users/SeuUsuario/Documents/Obsidian/MeuVault`
- Exemplo Linux/Mac: `/home/usuario/Documents/Obsidian/MeuVault`

**Onde preencher:**
- Arquivo: `.env`
- Linha: `OBSIDIAN_VAULT_PATH=C:/Users/Gianmarino L/Documents/Obsidian/IA-Test`

**Impacto:** Integração com Obsidian não funcionará.

---

### 10. Ollama Base URL

**Status:** ⚠️ Configurado com padrão

**Variável:**
```bash
OLLAMA_BASE_URL=http://host.docker.internal:11434  # ⚠️ Padrão Docker
# ou
OLLAMA_BASE_URL=http://localhost:11434  # Para uso local
```

**Quando é necessário:**
- Se usar modelos Ollama (LLM ou embeddings)
- Padrão funciona se Ollama estiver rodando

**Onde ajustar:**
- Arquivo: `.env`
- Linha: `OLLAMA_BASE_URL=http://localhost:11434` (local) ou `http://host.docker.internal:11434` (Docker)

**Impacto:** Modelos Ollama não funcionarão se URL estiver errada.

---

## 📝 Onde Preencher

### Arquivo Principal: `.env`

Todas as configurações devem ser adicionadas no arquivo `.env` na **raiz do projeto**.

**Localização:** `C:\Users\Gianmarino L\Documents\IA\IA-test\.env`

### Template de Referência

Use o arquivo `config/env.example` como referência, mas **não edite ele diretamente**. Copie as variáveis necessárias para o `.env`.

### Formato do Arquivo `.env`

```bash
# Comentários começam com #
# Cada variável em uma linha
VARIAVEL=valor

# Sem espaços ao redor do =
# Strings não precisam de aspas (a menos que tenham espaços)
```

### Exemplo Completo

```bash
# Neo4j Aura DB
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM

# LLM e Embeddings
LLM=llama2
EMBEDDING_MODEL=sentence_transformer
OLLAMA_BASE_URL=http://localhost:11434

# APIs (adicione conforme necessário)
# OPENAI_API_KEY=sk-...
# GOOGLE_API_KEY=...
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...

# Bancos de Dados (adicione conforme necessário)
# SUPABASE_URL=https://...
# SUPABASE_KEY=...
# NEON_DATABASE_URL=postgresql://...
# MONGODB_URI=mongodb://...

# Opcional
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=ls_...
# OBSIDIAN_VAULT_PATH=C:/Users/...
```

---

## 🔍 Verificar Configurações

### Script de Diagnóstico

Execute o System Health Agent para verificar o que está faltando:

```python
from src.agents.system_health_agent import get_system_health_agent

health = get_system_health_agent()
report = health.run_full_health_check()

# Ver problemas
for issue in report.diagnostic_issues:
    print(f"{issue.severity.value}: {issue.title}")
    print(f"  {issue.description}")
```

### Via Dashboard

1. Execute o dashboard: `streamlit run src/apps/agent_dashboard.py`
2. Vá na aba "🔍 Diagnóstico"
3. Clique em "🔄 Executar Diagnóstico Completo"
4. Veja os problemas encontrados

---

## 📊 Resumo por Prioridade

### 🔴 Crítico (Precisa agora)
- [ ] **NEO4J_URI** - URI do Aura DB

### 🟡 Importante (Se usar funcionalidades específicas)
- [ ] **OPENAI_API_KEY** - Se usar GPT-4/3.5
- [ ] **GOOGLE_API_KEY** - Se usar embeddings Google
- [ ] **AWS_ACCESS_KEY_ID** + **AWS_SECRET_ACCESS_KEY** - Se usar Bedrock
- [ ] **SUPABASE_URL** + **SUPABASE_KEY** - Se usar Supabase
- [ ] **NEON_DATABASE_URL** - Se usar Neon
- [ ] **MONGODB_URI** - Se usar MongoDB

### 🟢 Opcional (Melhorias)
- [ ] **LANGCHAIN_API_KEY** - Para rastreamento
- [ ] **OBSIDIAN_VAULT_PATH** - Para integração Obsidian
- [ ] **OLLAMA_BASE_URL** - Ajustar se necessário

---

## 🆘 Precisa de Ajuda?

1. Execute o diagnóstico: `python scripts/test_neo4j_connection.py`
2. Veja o dashboard: `streamlit run src/apps/agent_dashboard.py`
3. Consulte a documentação em `docs/`

---

**Última atualização:** 2025-01-27


