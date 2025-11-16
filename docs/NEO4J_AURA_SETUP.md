# 🔗 Configuração do Neo4j Aura DB

Este guia explica como conectar o projeto ao **Neo4j Aura DB** e visualizar os dados no **Neo4j Desktop**.

## 📋 Pré-requisitos

1. Conta no Neo4j Aura (gratuita disponível)
2. Instância Aura DB criada
3. Neo4j Desktop instalado (opcional, para visualização)

## 🚀 Passo 1: Criar Instância no Neo4j Aura

1. Acesse: https://console.neo4j.io/
2. Faça login ou crie uma conta
3. Clique em **"Create Database"**
4. Escolha o plano (Free tier disponível)
5. Selecione a região
6. Configure:
   - **Database Name**: `ia-test` (ou outro nome)
   - **Password**: Anote a senha gerada (você só verá uma vez!)
7. Aguarde a criação (pode levar alguns minutos)

## 🔑 Passo 2: Obter Credenciais

Após criar a instância:

1. Na página do console, clique na sua instância
2. Você verá:
   - **Connection URI**: Algo como `neo4j+s://xxxxx.databases.neo4j.io`
   - **Username**: Geralmente `neo4j`
   - **Password**: A senha que você configurou

**⚠️ IMPORTANTE**: Anote essas informações! A senha só é mostrada uma vez.

## ⚙️ Passo 3: Configurar o Projeto

### 3.1. Atualizar arquivo `.env`

Crie ou edite o arquivo `.env` na raiz do projeto:

```bash
# Neo4j Aura DB
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=sua_senha_aqui
```

**Nota**: 
- Para Aura DB, use `neo4j+s://` (com SSL) ou `neo4j+ssc://` (self-signed certificate)
- Substitua `xxxxx.databases.neo4j.io` pela URI real do seu Aura DB

### 3.2. Verificar Conexão

Teste a conexão:

```python
from src.agents.mcp_neo4j_integration import get_neo4j_manager

manager = get_neo4j_manager()
# Se não houver erro, a conexão está funcionando!
```

Ou use o script de teste:

```bash
python scripts/test_neo4j_connection.py
```

## 🖥️ Passo 4: Conectar no Neo4j Desktop

### 4.1. Instalar Neo4j Desktop

1. Baixe: https://neo4j.com/download/
2. Instale e abra o Neo4j Desktop

### 4.2. Adicionar Conexão Aura

1. No Neo4j Desktop, clique em **"Add"** → **"Remote Graph"**
2. Preencha:
   - **Name**: `IA-Test Aura`
   - **Connection URI**: Cole a URI do Aura DB
   - **Username**: `neo4j`
   - **Password**: Cole a senha
3. Clique em **"Connect"**

### 4.3. Visualizar Dados

1. Após conectar, clique em **"Open"** no grafo
2. Isso abrirá o Neo4j Browser
3. Execute queries como:
   ```cypher
   MATCH (n) RETURN n LIMIT 25
   ```

## 🔧 Configurações Adicionais

### Para Docker

Se estiver usando Docker, atualize o `docker-compose.yml`:

```yaml
environment:
  NEO4J_URI: ${NEO4J_URI:-neo4j+s://xxxxx.databases.neo4j.io}
  NEO4J_USERNAME: ${NEO4J_USERNAME:-neo4j}
  NEO4J_PASSWORD: ${NEO4J_PASSWORD:-sua_senha}
```

**Nota**: Não precisa do container `neo4j` local quando usar Aura DB.

### Para Desenvolvimento Local

Se quiser usar Aura DB em desenvolvimento local:

1. Configure as variáveis de ambiente no `.env`
2. O código detectará automaticamente a URI do Aura
3. Não inicie o container Neo4j local

## 🧪 Testar Conexão

Crie um script de teste (`scripts/test_neo4j_connection.py`):

```python
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        print("✅ Conexão com Aura DB bem-sucedida!")
        print(f"   URI: {uri}")
        print(f"   Username: {username}")
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
finally:
    driver.close()
```

Execute:

```bash
python scripts/test_neo4j_connection.py
```

## 📊 Sincronizar Dados

Após conectar, você pode sincronizar dados do projeto:

```python
from src.agents.orchestrator import get_orchestrator

orchestrator = get_orchestrator()

# Sincronizar MCPs para Neo4j
result = orchestrator.sync_mcp_to_neo4j()

# Sincronizar Obsidian para Neo4j
result = orchestrator.sync_mcp_to_obsidian()
```

## 🔒 Segurança

- **Nunca commite** o arquivo `.env` no Git
- Use variáveis de ambiente em produção
- Rotacione senhas periodicamente
- Use IP whitelist no Aura DB (se disponível)

## 🆘 Troubleshooting

### Erro: "Unable to connect"

- Verifique se a URI está correta
- Confirme que a senha está correta
- Verifique se o Aura DB está ativo no console

### Erro: "Certificate verification failed"

- Use `neo4j+ssc://` ao invés de `neo4j+s://` (self-signed)
- Ou configure certificados SSL adequadamente

### Erro: "Connection timeout"

- Verifique firewall/proxy
- Confirme que o Aura DB está acessível
- Verifique se não há bloqueio de IP

## 📚 Recursos

- [Neo4j Aura Documentation](https://neo4j.com/docs/aura/)
- [Neo4j Desktop Guide](https://neo4j.com/docs/desktop-manual/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)

---

**Última atualização:** 2025-01-27

