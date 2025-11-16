# 📥 Como Importar Dados para Neo4j Aura

Existem **duas formas** de importar dados para o Neo4j Aura:

1. **Via Interface Web do Neo4j Aura** (mais fácil para dados externos)
2. **Via Código do Projeto** (melhor para dados do próprio projeto)

---

## 🌐 Opção 1: Importar via Interface Web do Neo4j Aura

### Quando usar:
- ✅ Você tem dados em bancos relacionais (PostgreSQL, MySQL, etc.)
- ✅ Você tem arquivos CSV/JSON
- ✅ Você quer importar dados de fontes externas
- ✅ Você não quer escrever código

### Como fazer:

1. **Acesse o Console do Neo4j Aura:**
   - Vá para: https://console.neo4j.io/
   - Faça login
   - Selecione seu projeto e instância

2. **Navegue até Import:**
   - No menu lateral, clique em **"Data services"**
   - Clique em **"Import"** (ícone de nuvem com seta para baixo)

3. **Conecte uma Data Source:**
   - Clique no botão **"New data source"**
   - Escolha o tipo:
     - **Relational Database** (PostgreSQL, MySQL, SQL Server, etc.)
     - **CSV Files** (upload de arquivos)
     - **JSON Files**
     - **Outros formatos**

4. **Configure a Importação:**
   - Conecte ao banco de dados ou faça upload dos arquivos
   - Mapeie os dados para o modelo de grafo
   - Configure relacionamentos entre nós
   - Execute a importação

5. **Monitore o Progresso:**
   - Acompanhe na aba **"Import jobs"**
   - Veja logs e erros se houver

### Vantagens:
- ✅ Interface visual e intuitiva
- ✅ Não precisa escrever código
- ✅ Suporta muitos formatos
- ✅ Mapeamento visual de dados

### Desvantagens:
- ❌ Limitado a dados externos
- ❌ Não integra diretamente com o projeto

---

## 💻 Opção 2: Importar via Código do Projeto (Recomendado)

### Quando usar:
- ✅ Você quer importar dados do próprio projeto
- ✅ Você quer sincronizar MCPs, notas do Obsidian, etc.
- ✅ Você quer automatizar importações
- ✅ Você quer usar GraphRAG

### Como fazer:

#### 2.1. Sincronizar MCPs para Neo4j

```python
from src.agents.orchestrator import get_orchestrator

orchestrator = get_orchestrator()

# Sincroniza todos os MCPs
result = orchestrator.sync_mcp_to_neo4j()
print(f"Sincronizados: {result['synced_count']}/{result['total']}")
```

#### 2.2. Sincronizar Obsidian para Neo4j

```python
# Sincroniza notas do Obsidian
result = orchestrator.sync_mcp_to_obsidian()
print(f"Notas criadas: {result['created_count']}")
```

#### 2.3. Importar Vault do Obsidian

```python
from src.agents.mcp_neo4j_integration import get_neo4j_manager

manager = get_neo4j_manager()

# Importa todo o vault do Obsidian
vault_path = "C:/Users/Gianmarino L/Documents/Obsidian/IA-Test"
result = manager.import_obsidian_vault(vault_path)
print(f"Importados: {result['nodes_created']} nós, {result['relationships_created']} relacionamentos")
```

#### 2.4. Criar Nós Manualmente

```python
from src.agents.mcp_neo4j_integration import get_neo4j_manager

manager = get_neo4j_manager()

# Criar um nó MCP
mcp_info = {
    "name": "meu_mcp",
    "description": "Descrição do MCP",
    "tools": ["tool1", "tool2"]
}
node = manager.create_mcp_node("meu_mcp", mcp_info)
print(f"Nó criado: {node}")
```

#### 2.5. Usar o Dashboard para Importar

1. Execute o dashboard:
   ```bash
   streamlit run src/apps/agent_dashboard.py
   ```

2. Vá na aba **"🤖 Agentes"**
3. Selecione **"Neo4j GraphRAG"**
4. Use os botões de sincronização

### Vantagens:
- ✅ Integração direta com o projeto
- ✅ Automatização possível
- ✅ Sincronização de MCPs e Obsidian
- ✅ Usa GraphRAG

### Desvantagens:
- ❌ Requer conhecimento de código
- ❌ Mais complexo para dados externos

---

## 🎯 Recomendação: Qual Usar?

### Use Interface Web se:
- Você tem dados em bancos relacionais externos
- Você tem arquivos CSV/JSON para importar
- Você quer uma solução rápida sem código

### Use Código do Projeto se:
- Você quer sincronizar MCPs do projeto
- Você quer importar notas do Obsidian
- Você quer automatizar importações
- Você quer usar GraphRAG

---

## 📋 Passo a Passo Completo (Interface Web)

### Importar de Banco Relacional:

1. **No Neo4j Aura Console:**
   - Vá em **Data services** → **Import**
   - Clique em **"New data source"**
   - Selecione **"Relational Database"**

2. **Configure Conexão:**
   - Escolha o tipo (PostgreSQL, MySQL, etc.)
   - Preencha:
     - Host
     - Port
     - Database
     - Username
     - Password
   - Teste a conexão

3. **Mapeie para Grafo:**
   - Selecione tabelas para importar
   - Defina:
     - **Nodes**: Quais tabelas viram nós
     - **Relationships**: Como conectar os nós
   - Configure propriedades

4. **Execute:**
   - Revise o mapeamento
   - Clique em **"Start Import"**
   - Monitore na aba **"Import jobs"**

### Importar de CSV:

1. **No Neo4j Aura Console:**
   - Vá em **Data services** → **Import**
   - Clique em **"New data source"**
   - Selecione **"CSV Files"**

2. **Upload Arquivos:**
   - Faça upload dos arquivos CSV
   - Configure encoding e delimitadores

3. **Mapeie para Grafo:**
   - Defina quais colunas viram nós
   - Configure relacionamentos
   - Mapeie propriedades

4. **Execute:**
   - Revise e execute a importação

---

## 🔧 Scripts Úteis do Projeto

### Script de Sincronização Completa

Crie um arquivo `scripts/sync_to_neo4j.py`:

```python
"""
Script para sincronizar todos os dados do projeto para Neo4j Aura.
"""

from src.agents.orchestrator import get_orchestrator

def sync_all():
    """Sincroniza tudo para Neo4j."""
    orchestrator = get_orchestrator()
    
    print("🔄 Sincronizando MCPs...")
    mcp_result = orchestrator.sync_mcp_to_neo4j()
    print(f"   ✅ {mcp_result['synced_count']} MCPs sincronizados")
    
    print("🔄 Sincronizando Obsidian...")
    obsidian_result = orchestrator.sync_mcp_to_obsidian()
    print(f"   ✅ {obsidian_result['created_count']} notas criadas")
    
    print("✅ Sincronização completa!")

if __name__ == "__main__":
    sync_all()
```

Execute:
```bash
python scripts/sync_to_neo4j.py
```

---

## 🧪 Verificar Dados Importados

### Via Neo4j Browser (Desktop):

1. Conecte no Neo4j Desktop (veja `docs/NEO4J_AURA_SETUP.md`)
2. Abra o Browser
3. Execute queries:

```cypher
// Ver todos os nós
MATCH (n) RETURN n LIMIT 25

// Contar nós por tipo
MATCH (n)
RETURN labels(n) as tipo, count(n) as quantidade

// Ver relacionamentos
MATCH ()-[r]->()
RETURN type(r) as tipo, count(r) as quantidade
```

### Via Código:

```python
from src.agents.mcp_neo4j_integration import get_neo4j_manager

manager = get_neo4j_manager()

# Contar nós
result = manager.graph.query("MATCH (n) RETURN count(n) as total")
print(f"Total de nós: {result[0]['total']}")
```

---

## 📚 Recursos Adicionais

- [Neo4j Aura Import Documentation](https://neo4j.com/docs/aura/import/)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/)

---

## ❓ FAQ

### Preciso importar dados para usar o projeto?

**Não necessariamente.** O projeto funciona sem dados importados, mas:
- GraphRAG será mais útil com dados
- Sincronização de MCPs/Obsidian adiciona valor
- Dados externos podem ser úteis para análise

### Posso usar ambas as formas?

**Sim!** Você pode:
- Importar dados externos via interface web
- Sincronizar dados do projeto via código
- Ambos ficam no mesmo banco Neo4j Aura

### Os dados importados via interface aparecem no projeto?

**Sim!** Uma vez importados, os dados estão no Neo4j Aura e podem ser acessados pelo projeto normalmente.

---

**Última atualização:** 2025-01-27


