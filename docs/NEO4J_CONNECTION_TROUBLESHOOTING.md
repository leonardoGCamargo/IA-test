# 🔧 Troubleshooting - Conexão Neo4j Aura

## ⚠️ Erro: "Unable to retrieve routing information"

Este erro geralmente indica um problema de conectividade ou configuração SSL.

---

## ✅ Configuração Aplicada

```bash
NEO4J_URI=neo4j+s://71de7683.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM
NEO4J_DATABASE=neo4j
AURA_INSTANCEID=71de7683
AURA_INSTANCENAME=My instance
```

---

## 🔍 Possíveis Causas e Soluções

### 1. Verificar se a Instância está Rodando

**No Console Neo4j Aura:**
- Acesse: https://console.neo4j.io/
- Verifique se a instância "My instance" está com status **"RUNNING"**
- Se estiver parada, inicie-a

### 2. Verificar a URI no Console

**A URI pode estar diferente no console:**

1. No console Neo4j Aura, clique em "My instance"
2. Clique no botão **"Connect"**
3. Verifique a **Connection URI** exata
4. Compare com a configurada no `.env`

**Possíveis diferenças:**
- Pode ter um prefixo diferente (ex: `neo4j+ssc://`)
- Pode ter um formato ligeiramente diferente

### 3. Tentar URI com `neo4j+ssc://`

Se o problema for SSL, tente usar `neo4j+ssc://` (self-signed certificate):

```bash
NEO4J_URI=neo4j+ssc://71de7683.databases.neo4j.io
```

### 4. Verificar Firewall/Proxy

- Verifique se há firewall bloqueando a conexão
- Se estiver em rede corporativa, pode precisar configurar proxy
- Teste de outro local/rede

### 5. Verificar Credenciais

- Confirme que o username é exatamente `neo4j`
- Confirme que a senha está correta (sem espaços extras)
- No console, você pode resetar a senha se necessário

---

## 🧪 Testes Adicionais

### Teste 1: Verificar URI no Console

1. Acesse: https://console.neo4j.io/
2. Clique em "My instance"
3. Clique em "Connect"
4. Copie a URI exata mostrada
5. Compare com a do `.env`

### Teste 2: Testar com Neo4j Browser

1. No console, clique em "Connect"
2. Use o **Neo4j Browser** (se disponível)
3. Se funcionar no browser, o problema pode ser no código

### Teste 3: Verificar Logs da Instância

1. No console, vá em "Operations" ou "Logs"
2. Verifique se há erros na instância
3. Verifique se há tentativas de conexão bloqueadas

---

## 🔄 Próximos Passos

1. **Verificar URI no console** - Compare com a configurada
2. **Testar com neo4j+ssc://** - Se o problema for SSL
3. **Verificar status da instância** - Deve estar RUNNING
4. **Verificar credenciais** - Confirme username e password

---

## 📞 Suporte

Se o problema persistir:
- Verifique a documentação oficial: https://neo4j.com/docs/
- Consulte os logs da instância no console
- Verifique se há atualizações ou manutenção programada

---

**Última atualização:** 2025-01-27


