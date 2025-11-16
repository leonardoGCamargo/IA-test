# Database Manager - Agente Gerenciador de Bancos de Dados

## Visão Geral

O Database Manager é um agente unificado que permite gerenciar múltiplos tipos de bancos de dados dentro do sistema, incluindo Supabase, Neon e MongoDB, respeitando os limites de cada plataforma.

## Bancos de Dados Suportados

### 1. Supabase
- **Tipo**: PostgreSQL com recursos adicionais (Auth, Storage, Realtime)
- **Uso**: Ideal para aplicações que precisam de funcionalidades adicionais além de um banco relacional
- **Limites**: Dependem do plano do Supabase (Free, Pro, Team, Enterprise)

### 2. Neon
- **Tipo**: PostgreSQL serverless
- **Uso**: Ideal para aplicações que precisam de escalabilidade automática
- **Limites**: Dependem do plano do Neon (Free, Pro, Scale)

### 3. MongoDB
- **Tipo**: NoSQL
- **Uso**: Ideal para aplicações que precisam de flexibilidade de schema
- **Limites**: Dependem do plano do MongoDB (Atlas Free, M0, M2, etc.)

### 4. Neo4j
- **Tipo**: Graph database
- **Uso**: Mantido para compatibilidade com o sistema existente
- **Limites**: Dependem da instalação local ou cloud

## Instalação

### Dependências

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

As dependências incluem:
- `supabase>=2.0.0` - Para Supabase
- `psycopg2-binary>=2.9.0` - Para Neon (PostgreSQL)
- `pymongo>=4.5.0` - Para MongoDB
- `pgvector>=0.2.0` - Para vector stores PostgreSQL

## Configuração

### Variáveis de Ambiente

Adicione as seguintes variáveis de ambiente ao arquivo `.env`:

```bash
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=seu-anon-key
SUPABASE_SERVICE_ROLE_KEY=seu-service-role-key

# Neon
NEON_DATABASE_URL=postgresql://usuario:senha@host/database
NEON_PROJECT_ID=seu-project-id

# MongoDB
MONGODB_URI=mongodb://usuario:senha@host:porta/database
MONGODB_DATABASE=default
MONGODB_ATLAS=false  # true se usar MongoDB Atlas
```

### Configuração Programática

Você também pode configurar bancos de dados programaticamente:

```python
from src.agents.db_manager import DatabaseManager, DatabaseConfig, DatabaseType

db_manager = DatabaseManager()

# Adicionar Supabase
supabase_config = DatabaseConfig(
    db_type=DatabaseType.SUPABASE,
    name="meu_supabase",
    uri="https://seu-projeto.supabase.co",
    api_key="seu-anon-key",
    metadata={"service_role_key": "seu-service-role-key"}
)
db_manager.add_database(supabase_config)

# Adicionar Neon
neon_config = DatabaseConfig(
    db_type=DatabaseType.NEON,
    name="meu_neon",
    connection_string="postgresql://usuario:senha@host/database",
    metadata={"project_id": "seu-project-id"}
)
db_manager.add_database(neon_config)

# Adicionar MongoDB
mongodb_config = DatabaseConfig(
    db_type=DatabaseType.MONGODB,
    name="meu_mongodb",
    uri="mongodb://usuario:senha@host:porta/database",
    database="default",
    metadata={"atlas": False}
)
db_manager.add_database(mongodb_config)
```

## Uso

### Via Orchestrator

O Database Manager está integrado ao Orchestrator:

```python
from src.agents.orchestrator import Orchestrator, AgentType

orchestrator = Orchestrator()

# Listar bancos de dados
task = orchestrator.create_task(
    AgentType.DB_MANAGER,
    "Listar bancos de dados",
    {"action": "list_databases"}
)
result = orchestrator.execute_task(task)
print(result)

# Conectar a um banco
task = orchestrator.create_task(
    AgentType.DB_MANAGER,
    "Conectar ao banco",
    {"action": "connect", "name": "meu_supabase"}
)
result = orchestrator.execute_task(task)
print(result)

# Executar query (Neon/PostgreSQL)
task = orchestrator.create_task(
    AgentType.DB_MANAGER,
    "Executar query",
    {
        "action": "execute_query",
        "name": "meu_neon",
        "query": "SELECT * FROM usuarios LIMIT 10"
    }
)
result = orchestrator.execute_task(task)
print(result)
```

### Diretamente

```python
from src.agents.db_manager import get_db_manager

db_manager = get_db_manager()

# Listar bancos de dados
databases = db_manager.list_databases()
print(databases)

# Conectar a um banco
db_manager.connect("meu_supabase")

# Executar query (Neon/PostgreSQL)
result = db_manager.execute_query(
    "meu_neon",
    "SELECT * FROM usuarios LIMIT 10"
)
print(result.data)

# Executar RPC (Supabase)
result = db_manager.execute_rpc(
    "meu_supabase",
    "minha_funcao",
    {"parametro1": "valor1"}
)
print(result.data)

# Executar operação MongoDB
result = db_manager.execute_mongodb_operation(
    "meu_mongodb",
    "usuarios",
    "find",
    filter_dict={"ativo": True}
)
print(result.data)
```

## Operações Suportadas

### Supabase
- **execute_rpc()**: Executa funções RPC no Supabase
- **execute_query()**: Limitações - use RPC ou REST API para queries SQL diretas

### Neon (PostgreSQL)
- **execute_query()**: Executa queries SQL (SELECT, INSERT, UPDATE, DELETE, etc.)
- **list_tables()**: Lista tabelas do banco
- **get_status()**: Obtém status da conexão

### MongoDB
- **execute_mongodb_operation()**: Executa operações MongoDB
  - `find`: Buscar documentos
  - `find_one`: Buscar um documento
  - `insert_one`: Inserir um documento
  - `update_one`: Atualizar um documento
  - `delete_one`: Deletar um documento
- **list_tables()**: Lista coleções do banco
- **get_status()**: Obtém status da conexão

## Limites e Considerações

### Supabase
- **Free Plan**: 
  - 500 MB de banco de dados
  - 2 GB de bandwidth
  - 50.000 linhas de limite
- **Recomendação**: Use para desenvolvimento e pequenas aplicações

### Neon
- **Free Plan**:
  - 0.5 GB de armazenamento
  - Project pausa após 7 dias de inatividade
- **Recomendação**: Use para desenvolvimento e aplicações pequenas/médias

### MongoDB
- **Atlas Free (M0)**:
  - 512 MB de armazenamento
  - Compartilhado com outros usuários
- **Recomendação**: Use para desenvolvimento e testes

## Exemplos de Uso

### Exemplo 1: Consultar dados do Neon

```python
from src.agents.db_manager import get_db_manager

db_manager = get_db_manager()

# Conectar ao Neon
db_manager.connect("meu_neon")

# Executar query
result = db_manager.execute_query(
    "meu_neon",
    "SELECT id, nome, email FROM usuarios WHERE ativo = %s",
    parameters={"ativo": True}
)

if result.success:
    for row in result.data:
        print(f"ID: {row['id']}, Nome: {row['nome']}, Email: {row['email']}")
else:
    print(f"Erro: {result.error}")
```

### Exemplo 2: Inserir dados no MongoDB

```python
from src.agents.db_manager import get_db_manager

db_manager = get_db_manager()

# Conectar ao MongoDB
db_manager.connect("meu_mongodb")

# Inserir documento
result = db_manager.execute_mongodb_operation(
    "meu_mongodb",
    "usuarios",
    "insert_one",
    document={
        "nome": "João Silva",
        "email": "joao@example.com",
        "ativo": True
    }
)

if result.success:
    print(f"Documento inserido: {result.data[0]['inserted_id']}")
else:
    print(f"Erro: {result.error}")
```

### Exemplo 3: Executar RPC no Supabase

```python
from src.agents.db_manager import get_db_manager

db_manager = get_db_manager()

# Conectar ao Supabase
db_manager.connect("meu_supabase")

# Executar RPC
result = db_manager.execute_rpc(
    "meu_supabase",
    "buscar_usuarios_ativos",
    parameters={"limite": 10}
)

if result.success:
    for usuario in result.data:
        print(usuario)
else:
    print(f"Erro: {result.error}")
```

## Integração com Orchestrator

O Database Manager está totalmente integrado ao Orchestrator, permitindo que outras partes do sistema usem diferentes bancos de dados de forma transparente.

### Status do Sistema

O status do Database Manager é incluído no status geral do sistema:

```python
from src.agents.orchestrator import get_orchestrator

orchestrator = get_orchestrator()
status = orchestrator.get_system_status()

print(status["db_manager"])
# {
#     "available": True,
#     "databases_count": 3,
#     "databases": [...]
# }
```

## Troubleshooting

### Erro: "Biblioteca não instalada"
**Solução**: Instale as dependências necessárias:
```bash
pip install supabase psycopg2-binary pymongo
```

### Erro: "Falha ao conectar"
**Solução**: Verifique as variáveis de ambiente e credenciais

### Erro: "Tipo de banco não suportado"
**Solução**: Verifique se o tipo de banco está correto (supabase, neon, mongodb)

## Referências

- [Supabase Documentation](https://supabase.com/docs)
- [Neon Documentation](https://neon.tech/docs)
- [MongoDB Documentation](https://docs.mongodb.com)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)

## Contribuindo

Para contribuir com melhorias no Database Manager, consulte a documentação de desenvolvimento do projeto.

