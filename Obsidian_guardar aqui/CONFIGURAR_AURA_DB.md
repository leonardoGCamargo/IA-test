# ⚡ Configuração Rápida - Neo4j Aura DB

## ✅ Senha Configurada

A senha do Neo4j Aura DB já foi configurada no arquivo `.env`:
```
NEO4J_PASSWORD=zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM
```

## 🔗 Próximo Passo: Adicionar a URI

Você precisa adicionar a **Connection URI** do seu Aura DB no arquivo `.env`.

### Como obter a URI:

1. Acesse: https://console.neo4j.io/
2. Faça login na sua conta
3. Clique na sua instância do Aura DB
4. Copie a **Connection URI** (algo como: `neo4j+s://xxxxx.databases.neo4j.io`)

### Editar o arquivo `.env`:

Abra o arquivo `.env` na raiz do projeto e substitua esta linha:

```bash
NEO4J_URI=neo4j+s://SUBSTITUA_PELA_URI_DO_AURA_DB.databases.neo4j.io
```

Por:

```bash
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
```

(Onde `xxxxx.databases.neo4j.io` é a URI real do seu Aura DB)

## 🧪 Testar Conexão

Após adicionar a URI, teste a conexão:

```bash
python scripts/test_neo4j_connection.py
```

## 🖥️ Conectar no Neo4j Desktop

1. Abra o **Neo4j Desktop**
2. Clique em **"Add"** → **"Remote Graph"**
3. Preencha:
   - **Name**: `IA-Test Aura`
   - **Connection URI**: Cole a mesma URI do `.env`
   - **Username**: `neo4j`
   - **Password**: `zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM`
4. Clique em **"Connect"**
5. Clique em **"Open"** para visualizar no Browser

## 📝 Resumo da Configuração

- ✅ **Password**: Configurado
- ⏳ **URI**: Precisa ser adicionada
- ✅ **Username**: `neo4j` (padrão)

---

**Dica**: Se você não tiver a URI, você pode encontrá-la no console do Neo4j Aura na seção "Connection Details" da sua instância.

