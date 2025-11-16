# 📝 Como Sincronizar Documentação com Obsidian

## 🚀 Uso Rápido

### Opção 1: Passando o caminho como argumento
```bash
python sync_obsidian_docs.py "C:\Users\SeuUsuario\Documents\Obsidian\MeuVault"
```

### Opção 2: Configurando no .env
Adicione no arquivo `.env` (ou `e15fdb03f6467054904bd1a6eee67b8b6839bbbc4d2e4ec3419781663c81fd57.env`):

```bash
OBSIDIAN_VAULT_PATH=C:\Users\SeuUsuario\Documents\Obsidian\MeuVault
```

Depois execute:
```bash
python sync_obsidian_docs.py
```

### Opção 3: Script detecta automaticamente
O script tentará encontrar o vault automaticamente em:
- `C:\Users\Usuario\Documents\Obsidian\*`
- `C:\Users\Usuario\Obsidian\*`
- `C:\Users\Usuario\AppData\Roaming\Obsidian\*`

## 📋 O que o script faz

1. **Detecta ou pede o caminho do vault Obsidian**
2. **Lê todos os arquivos .md de documentação**
3. **Cria/atualiza as notas no Obsidian**
4. **Organiza em pastas** (Agentes/, etc.)

## 📁 Estrutura no Obsidian

Após a sincronização, você terá:

```
Vault/
├── 00-MAPA-DE-AGENTES.md
├── 01-Guia-Obsidian.md
├── 02-Guia-Cursor.md
├── 03-Manual-Sistema-Agentes.md
├── 04-Como-Criar-Agentes.md
├── RESUMO-MAPA-AGENTES.md
└── Agentes/
    ├── Orchestrator.md
    ├── Master-Agent.md
    ├── Helper-System.md
    ├── MCP-Manager.md
    ├── Docker-Integration.md
    ├── Neo4j-GraphRAG.md
    ├── Obsidian-Integration.md
    └── Kestra-Agent.md
```

## 🔄 Atualização Automática

Você pode executar o script sempre que quiser atualizar as notas:

```bash
python sync_obsidian_docs.py
```

O script detectará mudanças e atualizará os arquivos automaticamente.

## 🐛 Problemas Comuns

### Vault não encontrado
- Verifique o caminho do vault no Obsidian (Settings → Files & Links → Vault location)
- Ou configure manualmente via `.env`

### Permissão negada
- Verifique se tem permissão de escrita no vault
- Execute como administrador se necessário

### Arquivos não atualizados no Obsidian
- O Obsidian detecta mudanças automaticamente
- Se não atualizar, pressione `Ctrl+R` no Obsidian para recarregar

## 💡 Dica

Configure o caminho no `.env` para não precisar informar sempre:

```bash
OBSIDIAN_VAULT_PATH=C:\Users\Gianmarino L\Documents\Obsidian\MeuVault
```

