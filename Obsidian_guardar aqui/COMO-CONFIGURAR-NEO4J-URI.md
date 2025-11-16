# 🔴 Como Configurar NEO4J_URI - Passo a Passo

> **Guia Rápido para Resolver o Erro Crítico**  
> Status: ⚠️ **BLOQUEANTE** - Resolver Primeiro

---

## 🎯 Objetivo

Configurar a `NEO4J_URI` no arquivo `.env` para conectar o projeto ao seu Neo4j Aura DB.

---

## 📍 Passo 1: Obter a Connection URI

### Na Interface do Neo4j Aura:

1. **Você está na página "Instances"** ✅
   - Vejo que você tem uma instância rodando: "My instance" (ID: 71de7683)

2. **Clique no botão "Connect"** (com seta para baixo)
   - Está no card da instância "My instance"
   - Isso abre um modal com as informações de conexão

3. **No modal que abrir:**
   - Procure por **"Connection URI"** ou **"Connection String"**
   - Formato esperado: `neo4j+s://xxxxx-xxxxx.databases.neo4j.io`
   - **Copie essa URI completa**

4. **Você também verá:**
   - Username: `neo4j` (já configurado ✅)
   - Password: `zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM` (já configurado ✅)

---

## 📝 Passo 2: Configurar no Projeto

### Opção A: Editar Manualmente

1. **Abra o arquivo `.env`** na raiz do projeto:
   ```
   C:\Users\Gianmarino L\Documents\IA\IA-test\.env
   ```

2. **Encontre a linha:**
   ```bash
   NEO4J_URI=neo4j+s://SUBSTITUA_PELA_URI_DO_AURA_DB.databases.neo4j.io
   ```

3. **Substitua pelo valor copiado:**
   ```bash
   NEO4J_URI=neo4j+s://xxxxx-xxxxx.databases.neo4j.io
   ```
   (Onde `xxxxx-xxxxx` é a parte única da sua instância)

4. **Salve o arquivo**

### Opção B: Usar Script Interativo

Execute:
```bash
python scripts/setup_aura_db.py
```

O script vai:
- Pedir a URI
- Pedir o username (já tem: `neo4j`)
- Pedir a password (já tem)
- Atualizar o `.env` automaticamente

---

## ✅ Passo 3: Testar a Conexão

Execute:
```bash
python scripts/test_neo4j_connection.py
```

**Resultado esperado:**
```
✅ Conexão com Neo4j estabelecida com sucesso!
✅ Database: neo4j
✅ Versão: 5.x
```

Se der erro, verifique:
- A URI está correta?
- A senha está correta?
- A instância está rodando? (deve estar, você viu que está "RUNNING")

---

## 🔍 Onde Encontrar a URI (Alternativas)

### Se não encontrar no botão "Connect":

1. **Na página da instância:**
   - Clique no nome "My instance" para abrir os detalhes
   - Procure por "Connection Details" ou "Connection Info"

2. **No menu lateral:**
   - Vá em **"Tools" → "Query"**
   - Às vezes a URI aparece lá

3. **No console Neo4j:**
   - Acesse: https://console.neo4j.io/
   - Clique na sua instância
   - Procure por "Connection URI"

---

## 📋 Checklist

- [ ] Abri o botão "Connect" na instância
- [ ] Copiei a Connection URI completa
- [ ] Editei o arquivo `.env`
- [ ] Substituí o placeholder pela URI real
- [ ] Salvei o arquivo
- [ ] Executei `python scripts/test_neo4j_connection.py`
- [ ] Conexão testada com sucesso ✅

---

## 🆘 Problemas Comuns

### Erro: "Connection refused"
- **Causa:** URI incorreta ou instância parada
- **Solução:** Verifique se a instância está "RUNNING" e se a URI está correta

### Erro: "Authentication failed"
- **Causa:** Senha incorreta
- **Solução:** Verifique a senha no `.env` (deve ser: `zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM`)

### Erro: "Invalid URI format"
- **Causa:** URI mal formatada
- **Solução:** Certifique-se de que começa com `neo4j+s://` e termina com `.databases.neo4j.io`

---

## 📚 Documentação Relacionada

- [[00-ERROS-E-CONFIGURACOES-PENDENTES|Erros e Configurações Pendentes]]
- [[../docs/NEO4J_AURA_SETUP|Setup Completo Neo4j Aura]]
- [[../docs/IMPORTAR_DADOS_NEO4J_AURA|Como Importar Dados]]

---

## 🎯 Próximos Passos

Depois de configurar a URI:

1. ✅ Testar conexão
2. ⏳ Sincronizar dados do projeto para Neo4j:
   ```bash
   python scripts/sync_to_neo4j.py
   ```
3. ⏳ Visualizar no Neo4j Desktop (se quiser)

---

**Última atualização:** 2025-01-27


